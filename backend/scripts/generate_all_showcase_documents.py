"""Generate all presentation showcase Word documents (four scenarios)."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.showcase_states import SHOWCASE_CASES
from app.modules.document_generator import GENERATED_DIR, generate_pre_acceptance_document


def main() -> None:
    out = GENERATED_DIR / "showcase"
    out.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {out}\n")
    for key, state in SHOWCASE_CASES.items():
        path, name = generate_pre_acceptance_document(state, output_dir=out)
        print(f"[{key}] {name}")
        print(f"       -> {path}\n")
    print("Done. Open the .docx files in Word for答辩演示.")


if __name__ == "__main__":
    main()
