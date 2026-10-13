from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import Base, engine
import app.models  # Registers mapped models before create_all.

settings = get_settings()
app = FastAPI(title="AttendWise API", version="1.0.0", description="Student-managed attendance planning API.")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
