# Pattern 01: systemd Runtime

Run a Claude API agent as a reliable daily job — no custom orchestration, no magic frameworks.

## Why systemd?

systemd is the battle-tested init system already running on your Linux machine.
It handles retries, logging, scheduling, and failure detection out of the box.
Using it for LLM agents means you inherit decades of operational maturity for free.

## Setup

```bash
# 1. Install dependency
pip install anthropic

# 2. Set your API key (and optionally override the model)
mkdir -p ~/.config/physical-agent
cat > ~/.config/physical-agent/env <<'EOF'
ANTHROPIC_API_KEY=sk-...
ANTHROPIC_MODEL=claude-haiku-4-5
EOF
chmod 600 ~/.config/physical-agent/env

# 3. Install and start the timer
cp physical-agent.service ~/.config/systemd/user/
cp physical-agent.timer   ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now physical-agent.timer

# 4. Check status
systemctl --user status physical-agent.timer
journalctl --user -u physical-agent.service -f
```

## What it produces

Each run writes `output/agent_run_YYYY-MM-DD.md`. If the file already exists, the run is skipped.
This is the **physical-first** principle: no output file = not complete.

## Model selection

`agent.py` uses `ANTHROPIC_MODEL` (default: `claude-haiku-4-5`). Set it in your env file or export it before running manually.
