"""Create or refresh the pre-acceptance Word template."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.modules.document_generator import TEMPLATE_PATH, create_blank_template  # noqa: F401


def create_template(target: Path | None = None) -> Path:
    path = target or TEMPLATE_PATH
    return create_blank_template(path)


if __name__ == "__main__":
    out = create_template()
    print(f"Template written to: {out}")
