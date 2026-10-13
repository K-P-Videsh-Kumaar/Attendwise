from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.v1.dependencies import current_user
from app.api.v1.endpoints.planner import subject_metrics
from app.db.session import get_db
from app.models.subject import Subject
from app.models.user import User
from app.services.risk_service import risk_status

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(user: User = Depends(current_user), db: Session = Depends(get_db)):
    subjects = db.scalars(select(Subject).where(Subject.user_id == user.id, Subject.archived.is_(False)).order_by(Subject.name)).all()
    summaries = []
    for subject in subjects:
        current = subject_metrics(subject, db); target = subject.target_pct if subject.target_pct is not None else user.default_target_pct
        risk, explanation = risk_status(current.percentage, target)
        summaries.append({"subject_id": subject.id, "name": subject.name, "target_pct": target, "attended": current.attended, "total": current.total, "percentage": current.percentage, "risk": risk, "risk_explanation": explanation})
    return {"subjects": summaries, "subject_count": len(summaries), "below_target_count": sum(s["risk"] == "below_target" for s in summaries), "note": "Attendance is student-entered and may not match official college records."}
