from app.core.state import CaseState


def generate_police_summary(state: CaseState) -> str:
    """Generate a short police-side case summary."""
    return (
        f"Scenario: {state.scenario}. "
        f"Emotion: {state.emotion}. "
        f"Risk: {state.risk_level}. "
        f"Missing fields: {', '.join(state.missing_fields) or 'none'}."
    )

