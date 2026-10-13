from fastapi import APIRouter
from .endpoints import auth, subjects, attendance, planner, dashboard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(subjects.router)
api_router.include_router(attendance.router)
api_router.include_router(planner.router)
api_router.include_router(dashboard.router)
