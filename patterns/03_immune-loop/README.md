# Pattern 03: Immune Loop

**Self-healing agent infrastructure: detect violations → plan repairs → act.**

## The Problem

Agents deployed with `nohup python agent.py &` are silent failures waiting to happen.
When something breaks, you find out 3 days later when a stakeholder asks why the output stopped.

## The Architecture

```
[Timer fires daily]
       ↓
violation_detector.py    ← scans for known failure conditions
       ↓ violations.json
repair_planner.py        ← calls Claude API to generate concrete repair steps
       ↓ repair_plan_YYYY-MM-DD.md
[Human or next agent reads the plan and acts]
```

The loop is not fully autonomous (the repair *execution* is intentional human territory),
but the **detection and planning** happens without human intervention.

## Setup

```bash
pip install anthropic

# Install systemd units
cp immune-detector.service ~/.config/systemd/user/
cp immune-detector.timer   ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now immune-detector.timer
```

Ensure `~/.config/physical-agent/env` contains `ANTHROPIC_API_KEY` (and optionally `ANTHROPIC_MODEL`).

## Manual run

Run from **`patterns/03_immune-loop/`** — both scripts write output to the **current working directory** (`violations.json`, `repair_plan_YYYY-MM-DD.md`). Running from elsewhere scatters those files.

```bash
cd patterns/03_immune-loop
python violation_detector.py   # → ./violations.json (this directory)
python repair_planner.py       # → ./repair_plan_YYYY-MM-DD.md (this directory)
```

The systemd units set `WorkingDirectory` to this directory, so scheduled runs stay consistent.

## Extending

Add your own rules to `RULES` in `violation_detector.py`. Each rule is a tuple:
`(name: str, description: str, check_fn: Callable[[Path], bool])`

Return `True` to flag a violation, `False` for healthy.

## Model selection

`repair_planner.py` uses `ANTHROPIC_MODEL` (default: `claude-haiku-4-5`).
