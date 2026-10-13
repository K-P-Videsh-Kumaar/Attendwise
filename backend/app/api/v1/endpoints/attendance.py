from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.api.v1.dependencies import current_user
from app.api.v1.endpoints.subjects import owned_subject
from app.db.session import get_db
from app.models.attendance import AttendanceRecord
from app.models.subject import Subject
from app.models.user import User
from app.schemas.attendance import AttendanceIn, AttendanceOut, AttendancePatch

router = APIRouter(prefix="/attendance", tags=["attendance"])


def owned_record(record_id: int, user: User, db: Session) -> AttendanceRecord:
    record = db.scalar(select(AttendanceRecord).join(Subject).where(AttendanceRecord.id == record_id, Subject.user_id == user.id))
    if not record: raise HTTPException(status.HTTP_404_NOT_FOUND, "Attendance record not found")
    return record


def set_session_key(record: AttendanceRecord): record.session_key = (record.session_label or "").strip().lower()


@router.get("", response_model=list[AttendanceOut])
def list_records(subject_id: int | None = None, user: User = Depends(current_user), db: Session = Depends(get_db)):
    query = select(AttendanceRecord).join(Subject).where(Subject.user_id == user.id)
    if subject_id is not None: query = query.where(AttendanceRecord.subject_id == subject_id)
    return db.scalars(query.order_by(AttendanceRecord.class_date.desc(), AttendanceRecord.id.desc())).all()


@router.post("", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_record(payload: AttendanceIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    owned_subject(payload.subject_id, user, db)
    record = AttendanceRecord(**payload.model_dump()); set_session_key(record); db.add(record)
    try: db.commit()
    except IntegrityError:
        db.rollback(); raise HTTPException(status.HTTP_409_CONFLICT, "A record already exists for this subject, date, and session")
    db.refresh(record); return record


@router.patch("/{record_id}", response_model=AttendanceOut)
def update_record(record_id: int, payload: AttendancePatch, user: User = Depends(current_user), db: Session = Depends(get_db)):
    record = owned_record(record_id, user, db)
    for field, value in payload.model_dump(exclude_unset=True).items(): setattr(record, field, value)
    set_session_key(record)
    try: db.commit()
    except IntegrityError:
        db.rollback(); raise HTTPException(status.HTTP_409_CONFLICT, "A record already exists for this subject, date, and session")
    db.refresh(record); return record


@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    db.delete(owned_record(record_id, user, db)); db.commit(); return Response(status_code=204)
