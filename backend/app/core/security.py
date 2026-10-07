from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
import hmac
from fastapi import HTTPException, status
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored value.

    bcrypt hashes are checked with bcrypt. Rows written before hashing was
    enforced on registration hold the raw password, so they are compared in
    constant time; ``needs_rehash`` lets the caller upgrade them on login.
    """
    if not plain_password or not hashed_password:
        return False
    if hashed_password.startswith(_BCRYPT_PREFIXES):
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8")[:72], hashed_password.encode("utf-8"))
        except ValueError:
            return False
    return hmac.compare_digest(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def needs_rehash(hashed_password: str) -> bool:
    """True when the stored value is not a bcrypt hash (legacy plaintext row)."""
    return not (hashed_password or "").startswith(_BCRYPT_PREFIXES)


def get_password_hash(password: str) -> str:
    """Hash a password for storage (bcrypt, per-password salt)."""
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify a token and return the payload.

    Args:
        token: JWT token to verify

    Returns:
        Token payload

    Raises:
        HTTPException: If token is invalid
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
