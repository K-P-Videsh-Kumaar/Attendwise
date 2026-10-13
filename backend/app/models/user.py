from datetime import datetime
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    default_target_pct: Mapped[float] = mapped_column(Float, default=75.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    subjects = relationship("Subject", back_populates="user", cascade="all, delete-orphan")
