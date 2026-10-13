from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


engine = create_engine(get_settings().database_url, connect_args={"check_same_thread": False} if get_settings().database_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
