from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.v1.dependencies import current_user
from app.db.session import get_db
from app.models.subject import Subject
from app.models.user import User
from app.schemas.subject import SubjectIn, SubjectOut, SubjectPatch

router = APIRouter(prefix="/subjects", tags=["subjects"])


def owned_subject(subject_id: int, user: User, db: Session) -> Subject:
    subject = db.scalar(select(Subject).where(Subject.id == subject_id, Subject.user_id == user.id))
    if not subject: raise HTTPException(status.HTTP_404_NOT_FOUND, "Subject not found")
    return subject


@router.get("", response_model=list[SubjectOut])
def list_subjects(include_archived: bool = False, user: User = Depends(current_user), db: Session = Depends(get_db)):
    query = select(Subject).where(Subject.user_id == user.id)
    if not include_archived: query = query.where(Subject.archived.is_(False))
    return db.scalars(query.order_by(Subject.name)).all()


@router.post("", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(payload: SubjectIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    subject = Subject(user_id=user.id, **payload.model_dump())
    db.add(subject); db.commit(); db.refresh(subject); return subject


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return owned_subject(subject_id, user, db)


@router.patch("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: int, payload: SubjectPatch, user: User = Depends(current_user), db: Session = Depends(get_db)):
    subject = owned_subject(subject_id, user, db)
    for field, value in payload.model_dump(exclude_unset=True).items(): setattr(subject, field, value)
    db.commit(); db.refresh(subject); return subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_subject(subject_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    subject = owned_subject(subject_id, user, db); subject.archived = True; db.commit(); return Response(status_code=204)
