"""
Physical-First Pattern: an agent that is only "done" when physical evidence exists on disk.

The key insight: most agent failures are silent. The agent "ran" but nothing useful
was produced. By requiring a physical evidence file before declaring completion,
you catch silent failures immediately.
"""
import datetime
import json
import os
import pathlib
import sys

import anthropic

EVIDENCE_DIR = pathlib.Path(__file__).parent / "evidence"
DEFAULT_MODEL = "claude-haiku-4-5"


def run_with_evidence(task: str) -> pathlib.Path:
    EVIDENCE_DIR.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    evidence_path = EVIDENCE_DIR / f"evidence_{today}.json"

    if evidence_path.exists():
        print(f"[skip] Evidence already exists for {today}.")
        return evidence_path

    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": task}],
    )

    result_text = message.content[0].text

    # Write evidence BEFORE printing "done"
    evidence = {
        "date": today,
        "task": task,
        "result": result_text,
        "model": message.model,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "stop_reason": message.stop_reason,
    }
    evidence_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Only here can we say "done" — evidence is physically on disk
    print(f"[done] Evidence written: {evidence_path}")
    return evidence_path


def verify_evidence(date: str | None = None) -> bool:
    """Return True if today's evidence file exists and is non-empty."""
    target = date or datetime.date.today().isoformat()
    path = EVIDENCE_DIR / f"evidence_{target}.json"
    return path.exists() and path.stat().st_size > 0


if __name__ == "__main__":
    task = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Summarize the state of AI agent frameworks in 3 points."
    )
    run_with_evidence(task)
