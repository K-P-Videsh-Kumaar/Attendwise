from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.v1.dependencies import current_user
from app.api.v1.endpoints.subjects import owned_subject
from app.db.session import get_db
from app.models.attendance import AttendanceRecord
from app.models.subject import Subject
from app.models.user import User
from app.schemas.planner import SimulateIn
from app.services.attendance_service import metrics
from app.services.planner_service import recovery, simulate

router = APIRouter(prefix="/planner", tags=["planner"])


def subject_metrics(subject: Subject, db: Session):
    statuses = list(db.scalars(select(AttendanceRecord.status).where(AttendanceRecord.subject_id == subject.id)))
    return metrics(subject.baseline_attended_count, subject.baseline_absent_count, statuses)


@router.post("/simulate")
def simulate_attendance(payload: SimulateIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    result = []
    for scenario in payload.scenarios:
        subject = owned_subject(scenario.subject_id, user, db)
        before = subject_metrics(subject, db); after = simulate(before, scenario.attended, scenario.missed)
        result.append({"subject_id": subject.id, "subject_name": subject.name, "current_percentage": before.percentage, "projected_percentage": after.percentage, "current_attended": before.attended, "current_total": before.total, "projected_attended": after.attended, "projected_total": after.total})
    return {"read_only": True, "projections": result}


@router.get("/recovery/{subject_id}")
def get_recovery(subject_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    subject = owned_subject(subject_id, user, db)
    target = subject.target_pct if subject.target_pct is not None else user.default_target_pct
    return {"subject_id": subject.id, "target_pct": target, "current_percentage": subject_metrics(subject, db).percentage, **recovery(subject_metrics(subject, db), target)}
