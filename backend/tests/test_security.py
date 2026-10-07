"""Authentication and registration checks (audit findings: login accepted any password,
registration stored plaintext and let callers pick any role)."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.security import get_password_hash, needs_rehash, verify_password
from app.db.database import SessionLocal
from app.main import app
from app.models.user import User

client = TestClient(app)


@pytest.fixture
def new_user():
    """Register a unique clinician through the API; remove it afterwards."""
    name = f"audit_{uuid.uuid4().hex[:10]}"
    r = client.post("/api/auth/register", json={"username": name, "email": f"{name}@example.com", "password": "S3cret-pass"})
    assert r.status_code == 200, r.text
    yield name
    db = SessionLocal()
    db.query(User).filter(User.username == name).delete()
    db.commit()
    db.close()


def _login(user, password):
    return client.post("/api/auth/login", data={"username": user, "password": password})


def test_hash_roundtrip_and_salting():
    h1, h2 = get_password_hash("pw-123456"), get_password_hash("pw-123456")
    assert h1 != h2 and h1.startswith("$2")
    assert verify_password("pw-123456", h1)
    assert not verify_password("wrong", h1)
    assert not verify_password("", h1)


def test_legacy_plaintext_rows_still_verify_and_are_flagged():
    assert verify_password("old-secret", "old-secret")
    assert not verify_password("other", "old-secret")
    assert needs_rehash("old-secret") and not needs_rehash(get_password_hash("x"))


def test_login_with_correct_password(new_user):
    r = _login(new_user, "S3cret-pass")
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"


def test_login_rejects_wrong_password(new_user):
    assert _login(new_user, "not-the-password").status_code == 401


def test_login_rejects_unknown_user():
    assert _login("no_such_user_" + uuid.uuid4().hex[:6], "anything").status_code == 401


def test_registration_stores_bcrypt_hash_not_plaintext(new_user):
    db = SessionLocal()
    try:
        stored = db.query(User).filter(User.username == new_user).first().hashed_password
    finally:
        db.close()
    assert stored != "S3cret-pass" and stored.startswith("$2")


def test_self_registration_cannot_choose_elevated_role():
    name = f"audit_{uuid.uuid4().hex[:10]}"
    r = client.post("/api/auth/register", json={"username": name, "email": f"{name}@example.com",
                                                "password": "S3cret-pass", "role": "administrator"})
    assert r.status_code == 403


def test_legacy_plaintext_user_is_upgraded_on_login():
    name = f"audit_{uuid.uuid4().hex[:10]}"
    db = SessionLocal()
    db.add(User(username=name, email=f"{name}@example.com", hashed_password="legacy-pass", role="clinician", is_active=True))
    db.commit()
    try:
        assert _login(name, "wrong").status_code == 401
        assert _login(name, "legacy-pass").status_code == 200
        db.expire_all()
        assert db.query(User).filter(User.username == name).first().hashed_password.startswith("$2")
    finally:
        db.query(User).filter(User.username == name).delete()
        db.commit()
        db.close()
