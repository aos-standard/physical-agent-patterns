"""
Violation Detector: scan the workspace for known failure conditions.
Writes a JSON report that repair_planner.py consumes.
"""
import datetime
import json
import pathlib
from typing import Callable

ROOT = pathlib.Path(__file__).parent.parent.parent  # repo root


def _check_stale_evidence(root: pathlib.Path) -> bool:
    """True if no evidence file exists for today."""
    evidence_dir = root / "patterns" / "02_physical-first" / "evidence"
    if not evidence_dir.exists():
        return True
    today = datetime.date.today().isoformat()
    return not (evidence_dir / f"evidence_{today}.json").exists()


def _check_missing_output(root: pathlib.Path) -> bool:
    """True if no output from systemd pattern exists for today."""
    output_dir = root / "patterns" / "01_systemd-runtime" / "output"
    if not output_dir.exists():
        return True
    today = datetime.date.today().isoformat()
    return not (output_dir / f"agent_run_{today}.md").exists()


RULES: list[tuple[str, str, Callable[[pathlib.Path], bool]]] = [
    (
        "stale_physical_evidence",
        "No physical evidence file found for today in pattern 02.",
        _check_stale_evidence,
    ),
    (
        "missing_daily_output",
        "No daily output file found for today in pattern 01.",
        _check_missing_output,
    ),
]


def detect(root: pathlib.Path = ROOT) -> list[dict]:
    violations = []
    for name, description, check_fn in RULES:
        try:
            triggered = check_fn(root)
        except Exception as exc:
            triggered = True
            description = f"{description} [check error: {exc}]"
        if triggered:
            violations.append(
                {
                    "rule": name,
                    "description": description,
                    "detected_at": datetime.datetime.now().isoformat(),
                }
            )
    return violations


if __name__ == "__main__":
    violations = detect()
    report_path = pathlib.Path("violations.json")
    report_path.write_text(json.dumps(violations, ensure_ascii=False, indent=2))
    status = "VIOLATIONS DETECTED" if violations else "OK"
    print(f"[{status}] {len(violations)} violation(s) → {report_path}")
