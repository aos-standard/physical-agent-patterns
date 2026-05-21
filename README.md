# physical-agent-patterns

> **Patterns for building AI agent infrastructure that actually survives in production.**

Most agent tutorials show you how to *start*. This repository shows you how to *keep running*.

---

## The Problem

You've built an agent. It works great. Then:

- It runs silently with no output on day 3.
- You don't know if it ran, failed, or produced garbage.
- When it breaks, you find out from a stakeholder, not a log.

This happens because most agent setups are **ephemeral by design** — they return values, print logs, then disappear. Nothing survives a restart.

---

## Three Patterns

| Pattern | Problem Solved | Key Idea |
|---------|---------------|----------|
| [01: systemd Runtime](patterns/01_systemd-runtime/) | "How do I run an agent reliably every day?" | Use the OS init system, not a custom scheduler |
| [02: Physical-First](patterns/02_physical-first/) | "How do I know the agent actually did something?" | An action is not complete until a file exists on disk |
| [03: Immune Loop](patterns/03_immune-loop/) | "How do I know when my agent is broken?" | Automated violation detection + AI-generated repair plans |

---

## Quick Start

```bash
git clone https://github.com/aos-standard/physical-agent-patterns
cd physical-agent-patterns
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
export ANTHROPIC_MODEL=claude-haiku-4-5   # optional; override for Sonnet/Opus

# Try pattern 02: run with physical evidence
python patterns/02_physical-first/agent_with_evidence.py "What are the top 3 AI agent trends?"
# → evidence/evidence_YYYY-MM-DD.json  (this is your proof it ran)

# Try pattern 03: detect violations (must run from pattern directory)
cd patterns/03_immune-loop
python violation_detector.py   # → ./violations.json
python repair_planner.py       # → ./repair_plan_YYYY-MM-DD.md
cd ../..
```

---

## Why These Patterns?

These patterns emerged from running a personal AI agent infrastructure (**63 tools, 21 systemd timers**) for **6+ months**. The lessons are distilled here in minimal, dependency-free form.

The underlying philosophy is formalized in **[AOS-spec](https://github.com/aos-standard/AOS-spec)** — a lightweight standard for defining what an agent operation's physical scope and boundaries should look like.

---

## Requirements

- Python 3.11+
- `anthropic` SDK (`pip install anthropic`)
- Linux with systemd (for patterns 01 and 03)
- An Anthropic API key

---

## License

MIT
