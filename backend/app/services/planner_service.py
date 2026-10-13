from math import ceil, floor
from .attendance_service import AttendanceMetrics


def simulate(current: AttendanceMetrics, attended: int, missed: int) -> AttendanceMetrics:
    total = current.total + attended + missed
    new_attended = current.attended + attended
    return AttendanceMetrics(new_attended, total, round(new_attended / total * 100, 2) if total else None)


def recovery(current: AttendanceMetrics, target_pct: float) -> dict:
    r = target_pct / 100
    if current.total == 0:
        return {"classes_needed": 0, "safe_absences": 0, "message": "No counted classes yet; record a class to start planning."}
    if current.percentage is not None and current.percentage >= target_pct:
        return {"classes_needed": 0, "safe_absences": max(0, floor(current.attended / r - current.total)), "message": "You are meeting your target."}
    if r >= 1:
        return {"classes_needed": None, "safe_absences": 0, "message": "A 100% target cannot be recovered after an absence."}
    needed = max(0, ceil((r * current.total - current.attended) / (1 - r)))
    return {"classes_needed": needed, "safe_absences": 0, "message": f"Attend the next {needed} counted class(es) consecutively to reach your target."}
