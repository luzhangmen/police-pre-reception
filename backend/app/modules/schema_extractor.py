from app.core.state import Scenario


def extract_slots(text: str, scenario: Scenario) -> dict:
    """Extract fields for the selected scenario."""
    return {
        "raw_text": text,
        "scenario": scenario,
    }

