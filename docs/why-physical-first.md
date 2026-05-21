# Why Physical-First?

Most agent failures are invisible. The agent "ran." The function returned. The log said "success."
But nothing useful exists on disk — and you won't find out until someone asks why the output stopped.

**Physical-first** is a simple discipline: an agent action is not complete until physical evidence
(a file, a record, a log entry) exists on disk. No file = not done, regardless of what the process returned.

## The Core Rule

Write evidence to disk → THEN declare completion.

Never the other way around.

## Why This Matters

| Without physical-first | With physical-first |
|------------------------|---------------------|
| "It ran successfully" (no proof) | Evidence file exists or it didn't run |
| Silent failure discovered days later | Failure detected on the next check |
| Debugging requires log archaeology | Evidence file is the ground truth |
| Retries produce duplicates silently | Idempotent: skip if evidence exists for today |

## The Three Patterns in This Repo

Each pattern in this repository is built on the physical-first principle:

- **[01: systemd Runtime](../patterns/01_systemd-runtime/)** — output file = proof of run
- **[02: Physical-First](../patterns/02_physical-first/)** — evidence JSON written before "done" is printed
- **[03: Immune Loop](../patterns/03_immune-loop/)** — violation and repair plan both written to disk

## Connection to AOS-spec

Physical-first is one of the operational disciplines formalized in
[AOS-spec](https://github.com/aos-standard/AOS-spec) — a lightweight standard for defining
what an agent operation's scope and output boundaries should look like.

In AOS terms: every `permitted` action must produce an observable artifact.
An action with no artifact is indistinguishable from an action that never ran.
