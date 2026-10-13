from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from .config import get_settings

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(value: str) -> str:
    return password_hash.hash(value)


def verify_password(value: str, hashed: str) -> bool:
    return password_hash.verify(value, hashed)


def create_access_token(user_id: int) -> str:
    settings = get_settings()
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(credentials: HTTPAuthorizationCredentials | None) -> int:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required")
    try:
        payload = jwt.decode(credentials.credentials, get_settings().jwt_secret, algorithms=[get_settings().jwt_algorithm])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired access token")
