from pydantic import BaseModel, EmailStr, Field
from .common import ORMModel


class RegisterIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    default_target_pct: float = Field(default=75, ge=1, le=100)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(ORMModel):
    id: int
    name: str
    email: EmailStr
    default_target_pct: float


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
