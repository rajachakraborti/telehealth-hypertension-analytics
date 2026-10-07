from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.models.user import User
from app.core.security import (
    create_access_token,
    verify_password,
    needs_rehash,
    get_password_hash,
    decode_access_token
)
from app.db.database import get_db
from app.core.rate_limiter import limiter

router = APIRouter()

# Swagger Auth setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "clinician"

class RoleUpdate(BaseModel):
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    # One generic error for unknown user, wrong password and disabled account,
    # so the response does not reveal which usernames exist.
    if not user or not user.is_active or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if needs_rehash(user.hashed_password):
        user.hashed_password = get_password_hash(form_data.password)
        db.commit()

    # CRITICAL FIX: Include the 'role' and 'username' inside the JWT payload so RoleChecker works!
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Self-registration always yields the least-privileged clinical role;
    # elevated roles must be granted by an administrator.
    if user_data.role != "clinician":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Self-registration is limited to the clinician role",
        )
    role = "clinician"
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=role,  
        is_active=True,
        is_superuser=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}
