import enum
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class AttendanceStatus(str, enum.Enum):
    attended = "attended"
    absent = "absent"
    cancelled = "cancelled"


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (UniqueConstraint("subject_id", "class_date", "session_key", name="uq_subject_date_session"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), index=True)
    class_date: Mapped[date] = mapped_column(Date)
    status: Mapped[AttendanceStatus] = mapped_column(Enum(AttendanceStatus))
    session_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    session_key: Mapped[str] = mapped_column(String(100), default="")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    subject = relationship("Subject", back_populates="attendance_records")
