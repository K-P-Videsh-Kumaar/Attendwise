from app.models.attendance import AttendanceStatus
from app.services.attendance_service import metrics
from app.services.planner_service import recovery, simulate
from app.services.risk_service import risk_status


def test_cancelled_record_is_excluded():
    value = metrics(2, 1, [AttendanceStatus.attended, AttendanceStatus.absent, AttendanceStatus.cancelled])
    assert (value.attended, value.total, value.percentage) == (3, 5, 60.0)


def test_simulation_is_math_only_and_correct():
    current = metrics(3, 2, [])
    result = simulate(current, attended=2, missed=1)
    assert (current.attended, current.total) == (3, 5)
    assert (result.attended, result.total, result.percentage) == (5, 8, 62.5)


def test_recovery_and_100_percent_edge_case():
    current = metrics(3, 2, [])
    assert recovery(current, 75)["classes_needed"] == 3
    assert recovery(current, 100)["classes_needed"] is None


def test_risk_edges():
    assert risk_status(None, 75)[0] == "no_data"
    assert risk_status(74.9, 75)[0] == "below_target"
    assert risk_status(77, 75)[0] == "warning"
    assert risk_status(81, 75)[0] == "on_track"
