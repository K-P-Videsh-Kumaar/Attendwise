from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    target_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    baseline_attended_count: Mapped[int] = mapped_column(Integer, default=0)
    baseline_absent_count: Mapped[int] = mapped_column(Integer, default=0)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="subjects")
    attendance_records = relationship("AttendanceRecord", back_populates="subject", cascade="all, delete-orphan")
