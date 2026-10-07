from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.core.config import settings
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _init_db():
    """Create tables and seed a default test user on first run."""
    from app.db.database import engine, Base, SessionLocal, DATABASE_URL
    from app.models.user import User
    Base.metadata.create_all(bind=engine)
    logger.info("Database: %s", DATABASE_URL)
    db = SessionLocal()
    try:
        # Demo accounts. Passwords are bcrypt-hashed before storage and can be overridden
        # per account with SEED_<USERNAME>_PASSWORD; set these on any shared deployment.
        from app.core.security import get_password_hash
        demo_accounts = [
            ("admin", "admin@telehealth.com", "admin123", "administrator", True),
            ("clinician", "clinician@telehealth.com", "clinician123", "clinician", False),
            ("analyst", "analyst@telehealth.com", "analyst123", "data_analyst", False),
            ("testuser", "test@example.com", "testpass123", "clinician", False),
        ]
        seed_users = []
        for username, email, default_pw, role, is_super in demo_accounts:
            if db.query(User).filter(User.username == username).first():
                continue
            pw = os.getenv(f"SEED_{username.upper()}_PASSWORD")
            if not pw:
                logger.warning("Demo account '%s' uses its built-in password; set SEED_%s_PASSWORD", username, username.upper())
            seed_users.append(dict(username=username, email=email, role=role, is_superuser=is_super,
                                   hashed_password=get_password_hash(pw or default_pw)))
        for u in seed_users:
            if not db.query(User).filter(User.username == u["username"]).first():
                db.add(User(is_active=True, **u))
        db.commit()
        logger.info("Seeded default users")
    finally:
        db.close()

_init_db()

from app.core.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(title="Telehealth Hypertension Predictive Analytics System")

# Attach Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
# Comma-separated list of allowed browser origins; defaults to "*" for the demo.
# On a shared deployment set CORS_ORIGINS to the dashboard URL.
_CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve sample data files
_STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.isdir(_STATIC_DIR):
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

# Include the API router
app.include_router(api_router, prefix="/api")

from prometheus_fastapi_instrumentator import Instrumentator

@app.get("/")
async def root():
    return {"message": "Welcome to the Telehealth Hypertension Predictive Analytics System API"}

# Instrument the FastAPI app for Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/api/metrics")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)