from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginIn, RegisterIn, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email.lower())):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    user = User(name=payload.name.strip(), email=payload.email.lower(), password_hash=hash_password(payload.password), default_target_pct=payload.default_target_pct)
    db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_access_token(user.id), user=user)


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")
    return TokenOut(access_token=create_access_token(user.id), user=user)
