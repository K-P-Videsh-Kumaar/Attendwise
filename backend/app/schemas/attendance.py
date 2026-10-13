from datetime import date, datetime
from pydantic import BaseModel, Field
from app.models.attendance import AttendanceStatus
from .common import ORMModel


class AttendanceIn(BaseModel):
    subject_id: int
    class_date: date
    status: AttendanceStatus
    session_label: str | None = Field(default=None, max_length=100)
    note: str | None = Field(default=None, max_length=1000)


class AttendancePatch(BaseModel):
    class_date: date | None = None
    status: AttendanceStatus | None = None
    session_label: str | None = Field(default=None, max_length=100)
    note: str | None = Field(default=None, max_length=1000)


class AttendanceOut(ORMModel):
    id: int
    subject_id: int
    class_date: date
    status: AttendanceStatus
    session_label: str | None
    note: str | None
    created_at: datetime
    updated_at: datetime
