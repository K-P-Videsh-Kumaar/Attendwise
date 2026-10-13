from dataclasses import dataclass
from app.models.attendance import AttendanceStatus


@dataclass(frozen=True)
class AttendanceMetrics:
    attended: int
    total: int
    percentage: float | None


def metrics(baseline_attended: int, baseline_absent: int, statuses: list[AttendanceStatus]) -> AttendanceMetrics:
    attended = baseline_attended + sum(s == AttendanceStatus.attended for s in statuses)
    total = baseline_attended + baseline_absent + sum(s in (AttendanceStatus.attended, AttendanceStatus.absent) for s in statuses)
    return AttendanceMetrics(attended, total, round(attended / total * 100, 2) if total else None)
