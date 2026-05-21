# Pattern 02: Physical-First

**Rule:** An agent action is not complete until physical evidence (a file) exists on disk.

## The Problem

```
agent.run()      # "success"
# But where's the output?
# Was it logged? Stored? Processed?
# You have no idea.
```

Most agentic systems report success based on return values or logs.
Both are ephemeral. A crash, restart, or log rotation erases them.

## The Solution

Write evidence to disk **before** declaring completion.
If the file doesn't exist — the run didn't happen, regardless of what the logs say.

```bash
export ANTHROPIC_API_KEY=sk-...
python agent_with_evidence.py "Your task here"
# → evidence/evidence_2026-05-22.json
```

## Verification

```python
from agent_with_evidence import verify_evidence
assert verify_evidence(), "Today's run has no physical evidence"
```

This single assertion catches silent failures that would otherwise go unnoticed for days.

## Model selection

Uses `ANTHROPIC_MODEL` (default: `claude-haiku-4-5`).
