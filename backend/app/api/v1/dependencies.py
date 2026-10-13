from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import bearer_scheme, decode_access_token
from app.db.session import get_db
from app.models.user import User


def current_user(db: Session = Depends(get_db), credentials=Depends(bearer_scheme)) -> User:
    user = db.get(User, decode_access_token(credentials))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User no longer exists")
    return user
