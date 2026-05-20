---
name: repo-aware
description: Scan a repo's actual file inventory and surface drift between documented claims (roadmap, ADRs, pending-review, design docs) and reality. MUST be invoked before editing claim-bearing documents in any external repo; the PreToolUse hook enforces this.
---

# repo-aware

Mechanical enforcement of the "verify plan against code" discipline (per `feedback_verify_plan_against_code.md`). Reading from memory or last-seen state when proposing roadmap/ADR/conventions changes is the failure mode this skill prevents.

## When to invoke

**Mandatory before any of these actions in an external repo:**

- Editing or creating a roadmap file
- Editing or creating an ADR
- Editing pending-review trackers
- Editing design docs
- Editing convention/playbook docs
- Editing `docs/repos.md` or similar outbound indexes
- Producing analysis or claims about "what's in this repo"

The PreToolUse hook at `.claude/scripts/repo-aware-hook.py` blocks Edit/Write on these paths if a fresh scan (< 30 min) isn't cached. There is no soft-bypass — run the scan first.

**Optional but useful:**

- Starting work in a repo you haven't touched recently
- When asked "are you aware of X" or "what's in the repo"
- Before proposing additions to any operational backlog

## How to invoke

```bash
python .claude/scripts/repo-aware.py "<absolute-repo-path>"
```

Examples:

```bash
python .claude/scripts/repo-aware.py "C:/Workspace/Women Defining AI/wdai-team-os"
python .claude/scripts/repo-aware.py "C:/Workspace/Women Defining AI/wdai-foundation-platform"
```

The script writes markdown to stdout and caches state at `.claude/state/repo-aware-cache.json`. Cache freshness window: 30 minutes per repo.

## What it returns

1. **Inventory by category** — file counts grouped (Skills / ADRs / Conventions / Roadmap / Design docs / GitHub config / Hooks / Team onboarding / Root config / Placeholders / Source code / Other)
2. **Detail listings** for substantive categories (each file path enumerated)
3. **Drift analysis** — three classes:
   - **Claimed but missing**: paths referenced in roadmap/ADRs/conventions that don't exist on disk
   - **Broken ADR references**: `ADR-NNNN` mentions where the actual ADR file is missing
   - **Substantive files never referenced**: markdown that exists but isn't linked from any claim-bearing doc (signals orphan content)
4. **Last commit info** for context on how recently anything changed

## Interpreting the report

- **Drift = 0** → safe to proceed with the planned edit
- **Claimed missing > 0** → something we said exists doesn't; reconcile before adding new claims
- **Broken ADRs > 0** → fix the broken reference OR write the missing ADR before claiming it
- **Unreferenced substantive > 0** → soft signal; might mean content exists that should be linked, or that the report is over-counting (the report skips onboarding files, but ad-hoc docs may still show)

## What this skill does NOT do

- Doesn't read file contents — only file paths and reference patterns. The agent still reads files when needed.
- Doesn't enforce on edits inside `dev-agent/` itself — self-modification is a separate concern
- Doesn't run during sub-agent invocations (hook respects `CLAUDE_AGENT_NAME` env var)
- Doesn't auto-fix drift — surfaces it for human / agent judgment

## OpenTelemetry emission (future)

When the OTel collector is wired up (per ADR-0004 in `wdai-team-os/decisions/0004-mission-control-otel-langfuse.md`), this skill emits:

```yaml
agent_id: repo-aware
agent_kind: claude_code_session
owner: madina
trigger: pre-edit | manual
artifacts_emitted: 0  # reports + cache; not user-visible artifacts
files_scanned: <n>
drift_counts: { claimed_missing: <n>, missing_adrs: <n>, unreferenced: <n> }
```

## Related

- `.claude/scripts/repo-aware.py` — the scanner
- `.claude/scripts/repo-aware-hook.py` — the PreToolUse enforcement
- `.claude/state/repo-aware-cache.json` — per-repo scan cache (30 min freshness)
- `memory/feedback_verify_plan_against_code.md` — the past learning this mechanism enforces
- `identity/SOUL.md` "Proposing Behavioral Change" — why rule-only failed and mechanism was needed
