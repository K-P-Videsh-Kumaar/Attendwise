from datetime import datetime
from pydantic import BaseModel, Field
from .common import ORMModel


class SubjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    code: str | None = Field(default=None, max_length=50)
    target_pct: float | None = Field(default=None, ge=1, le=100)
    baseline_attended_count: int = Field(default=0, ge=0)
    baseline_absent_count: int = Field(default=0, ge=0)


class SubjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    code: str | None = Field(default=None, max_length=50)
    target_pct: float | None = Field(default=None, ge=1, le=100)
    baseline_attended_count: int | None = Field(default=None, ge=0)
    baseline_absent_count: int | None = Field(default=None, ge=0)
    archived: bool | None = None


class SubjectOut(ORMModel):
    id: int
    name: str
    code: str | None
    target_pct: float | None
    baseline_attended_count: int
    baseline_absent_count: int
    archived: bool
    created_at: datetime
