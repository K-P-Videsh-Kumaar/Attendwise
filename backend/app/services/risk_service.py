def risk_status(percentage: float | None, target: float, warning_margin: float = 5) -> tuple[str, str]:
    if percentage is None:
        return "no_data", "No counted classes have been recorded yet."
    if percentage < target:
        return "below_target", f"{target - percentage:.2f} percentage points below your {target:g}% target."
    if percentage < target + warning_margin:
        return "warning", f"Within {warning_margin:g} percentage points of your {target:g}% target."
    return "on_track", f"At least {warning_margin:g} percentage points above your {target:g}% target."
