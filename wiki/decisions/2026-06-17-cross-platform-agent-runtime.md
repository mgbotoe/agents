---
name: Cross-Platform Agent Runtime (Windows + macOS)
date: 2026-06-17
status: proposed
context: Polaris cloned to a Mac (`/Users/zhalianna/Documents/AI World/agents`) alongside the existing Windows home base. Dina wants Polaris to run on BOTH machines off one shared repo, not pick one.
decision: One shared repo is the brain; each machine gets a thin platform-specific execution layer. Paths become repo-relative + config-driven (never absolute OS paths). Scheduling stays cloud-first (GitHub Actions) so neither OS owns the cadence.
tags: [agents, infra, cross-platform, polaris, runtime, migration]
alternatives:
  - "Windows-only (Mac is just a read/edit working copy) — rejected: Dina wants Polaris operational on the Mac, not just a checkout."
  - "Fork per-OS (two diverging configs) — rejected: memory/wiki would diverge, the whole point of one brain dies."
  - "Prefix-swap C:\\Workspace → /Users/... — rejected: the Mac topology is genuinely different (no Personal Projects / Webdesign Business dirs), so it's a remap, not a sed."
rationale: The repo is already cloud-cron driven (promote.yml/discuss.yml run in GitHub Actions, platform-agnostic). The hooks are already Python (portable runtime). The only truly OS-locked pieces are a handful of paths and 4 Windows shell scripts. So "both" is the low-cost path IF paths stop being absolute and the python/python3 invocation gap is closed.
advisor_read: UNAVAILABLE — this is a cross-workspace infra decision (mandatory advisor() trigger per rules/personal.md), but no advisor tool/MCP is wired on this machine. Proceeding as DRAFT; outside read still owed before code lands.
revisit_date: 2026-09-17
---

# Cross-Platform Agent Runtime

## Decision
Polaris runs on **both** Windows and macOS from a single shared repo. Architecture:
- **Shared brain (git):** identity, memory, wiki, daily-logs, skills, rules, hook *logic*. Synced via GitHub. Already the design.
- **Cloud execution layer (GitHub Actions):** scheduled cognition (`promote`, `discuss`, and any other cron) runs in CI, not on either laptop. OS-agnostic. Already partly true.
- **Per-machine execution layer (thin, uncommitted-where-appropriate):** shell-script dispatch, secrets backend, and the workspace path map. Differs by OS; everything else is shared.

**Hard rule that makes it work:** *paths are always resolved relative to the repo root or read from a per-machine config file — never hardcoded absolute OS paths.* Enforced once, mechanically (see below), not per-file by discipline.

## Audit — what actually breaks on the Mac (2026-06-17)

### P0 — silent failures (look like they work, don't)
1. **`python` vs `python3`.** Every hook in `.claude/settings.json` invokes `python .claude/scripts/*.py`. This Mac has only `python3` (3.9.6); no `python` on PATH. All hooks are `|| true`-guarded, so they **fail silently** — `sync-check`, `workspace-scan`, `scan-self-audit`, `index-daily-logs`, the PreToolUse delegation/repo-aware guards, `auto-distill`/`session-end-sync` on exit. The safety scaffolding *appears* to run and does not.
2. **`advisor()` unwired.** `rules/personal.md` makes advisor-before-plan a hard rule for exactly this class of decision; no advisor tool/MCP exists here. The rule is currently unenforceable on Mac.

### P1 — hardcoded Windows paths (found in 23 files)
- **Operational (must fix):** `.claude/scripts/{workspace-scan,check-wiki-inbox,log-commit}.py`, `gather-context.ps1`. workspace-scan maps a 6-entry `C:\Workspace\...` topology that doesn't exist here.
- **Behavioral config (must fix):** `CLAUDE.md`, `identity/{memory,user}.md`, `.claude/agents/*.md` (builder/designer/qa/devops/security), `.claude/rules/domain.md`, `.claude/skills/{inventory-repo,recall,repo-aware}/SKILL.md`.
- **Historical (leave alone):** `daily-logs/*.md`, `design/team-os/*`, `memory/projects.md` — append-only records; rewriting them falsifies history.

### P1 — Windows-only shell scripts (4)
`.claude/scripts/gather-context.ps1`, `bin/scheduled/{decay,run-task,setup-tasks}.cmd`. These are the Windows Task Scheduler layer. On Mac, cloud cron already covers Promote/Discuss; confirm which of Distill/Decay/IndexLogs/SelfImprove are cloud vs. local-only before building launchd equivalents — likely few or none needed.

### Drift finding (separate from porting)
`CLAUDE.md` "Active Tasks" still lists 5 Windows Task Scheduler jobs, but memory (2026-05-07) says automation moved to GitHub Actions. CLAUDE.md and reality disagree about where scheduling lives. Reconcile as part of this work.

### What's already portable (the good news)
- Hooks are Python, not PowerShell — runtime ports once the `python3` invocation is fixed.
- Cloud cron (`promote.yml`, `discuss.yml`) is OS-agnostic and already running.
- Slack MCP is the only MCP wired; secrets backend is the only per-machine concern there.

## Implementation outline (NOT started — plan only)
1. **Close the python gap.** Either symlink/shim `python`→`python3` per-machine, or change hook invocations to `python3`, or add a tiny launcher that picks the right interpreter. Pick one mechanically; don't rely on PATH luck.
2. **Centralize the workspace map.** One config file (e.g. `.claude/workspace.local.json`, gitignored per-machine) lists this machine's workspace roots. `workspace-scan.py` and friends read it instead of a hardcoded list. Ship a committed `.example`.
3. **Repo-relative path resolution.** Scripts derive the agent root from their own location, not `C:\Workspace\agents`.
4. **Mechanical enforcement (required — rules-without-mechanism is a known failure mode here):** add a scanner that fails when a NEW hardcoded `C:\` or `/Users/<name>/` absolute path enters tracked code, run it as a PreToolUse/CI check. Without this the migration silently rots the first time either machine writes an absolute path into a shared file.
5. **OS-specific shell layer.** Keep `.cmd` for Windows; add bash siblings only for tasks that genuinely must run locally (TBD after cloud-vs-local reconciliation).
6. **Decide advisor() story.** Either wire it on Mac too, or formally scope it as Windows-only and weaken the hard rule — but don't leave a mandatory rule silently unenforceable.

## Open questions for Dina
- Is the Windows machine still primary, or is the Mac becoming primary? (Changes which gets the richer local layer.)
- Are Personal Projects / Webdesign Business workspaces coming to the Mac, or is the Mac WDAI+agents only? (Defines the workspace map.)
- OK to make `.claude/settings.json` hook commands use `python3` directly, or do you want a shim so the committed file stays OS-neutral?
