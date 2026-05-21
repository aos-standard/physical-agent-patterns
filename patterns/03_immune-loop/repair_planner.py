"""
Repair Planner: read violations.json, call Claude API for a concrete repair plan,
write the plan as physical evidence.
"""
import datetime
import json
import os
import pathlib
import sys

import anthropic

DEFAULT_MODEL = "claude-haiku-4-5"


def plan_repairs(
    violations_path: pathlib.Path = pathlib.Path("violations.json"),
) -> pathlib.Path | None:
    if not violations_path.exists():
        print("[skip] No violations file. Run violation_detector.py first.")
        return None

    violations: list[dict] = json.loads(violations_path.read_text())

    if not violations:
        print("[ok] No violations detected. System is healthy.")
        return None

    violations_text = json.dumps(violations, indent=2)
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an autonomous agent infrastructure repair planner.\n\n"
                    "The following violations were detected in a physical-first agent system:\n\n"
                    f"```json\n{violations_text}\n```\n\n"
                    "For each violation, provide:\n"
                    "1. Root cause (1-2 sentences)\n"
                    "2. Repair steps (numbered, concrete, executable)\n"
                    "3. Prevention measure (1 sentence)\n\n"
                    "Be specific. Assume a Linux environment with systemd and Python 3.11."
                ),
            }
        ],
    )

    repair_text = message.content[0].text
    today = datetime.date.today().isoformat()
    plan_path = pathlib.Path(f"repair_plan_{today}.md")
    plan_path.write_text(
        f"# Repair Plan: {today}\n\n"
        f"## Detected Violations\n```json\n{violations_text}\n```\n\n"
        f"## Repair Instructions\n\n{repair_text}\n",
        encoding="utf-8",
    )

    print(f"[done] Repair plan written: {plan_path}")
    return plan_path


if __name__ == "__main__":
    path = (
        pathlib.Path(sys.argv[1])
        if len(sys.argv) > 1
        else pathlib.Path("violations.json")
    )
    plan_repairs(path)
