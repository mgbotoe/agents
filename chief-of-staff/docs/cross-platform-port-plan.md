# Cross-Platform Port Plan — Windows + macOS

**Status:** plan only, nothing executed
**Date:** 2026-06-17
**Pairs with:** `wiki/decisions/2026-06-17-cross-platform-agent-runtime.md` (the *why*; this is the *how*)
**Scope:** the whole monorepo (`mgbotoe/agents`) — Atlas (chief-of-staff), Polaris (dev-agent), research-analyst. Per the standing agent-consistency rule, infra fixes apply to all agents unless noted.

## Decisions locked (2026-06-17)
- **Mac = primary.** Daily driver, richer local layer, secrets, full workspace map.
- **Windows = secondary.** Pulls the same brain, can run any agent when in use, does **not** own a competing local scheduler.
- **Cloud owns cadence.** GitHub Actions runs scheduled cognition for both machines. Neither laptop needs to be awake.
- **Everything comes to the Mac** — incl. Personal Projects + Webdesign Business workspaces (not just agents/WDAI).
- **Paths are never hardcoded absolute.** Repo-relative, or read from a per-machine gitignored config. Enforced mechanically, not by discipline.

## Current reality (verified, not assumed)
- Repo root is the monorepo: `/Users/zhalianna/Documents/AI World/agents`. Mac is **0/0 in sync** with `origin/master`. All content (agents, wiki, memory, logs) is already here — git carried it.
- **Only 2 things run in cloud:** `promote.yml` (07:00 UTC), `discuss.yml` (10:00 UTC), on `ubuntu-latest`. OS-independent, unaffected by any of this.
- **~12 other tasks are Windows Task Scheduler only** (MorningBrief, MiddayCheck, EveningWrapup, FridayWrap, WeeklyReview, GranolaIngest, IndexLogs, SelfImprove, Decay, ScanSlack ×2, ScanHeartbeat ×2). They run **only while Windows is awake** and have **no Mac or cloud equivalent.**
- `CLAUDE.md` "Active Tasks" table claims these are scheduled, implying live automation that on a Mac-primary world won't fire. **Stale — overclaims.**

---

## Bucket 1 — Portability fixes (make either machine able to run any agent)

### 1.1 Close the `python` gap  [P0 — silent failure today]
Every hook in `.claude/settings.json` calls `python .claude/scripts/*.py`. This Mac has only `python3`. Hooks are `|| true`-guarded, so they **fail silently** — the safety scaffolding *looks* like it runs and doesn't.
- **Fix (recommended):** a tiny committed launcher (e.g. `bin/py`) that execs `python3` if present else `python`, and point hook commands at it. Keeps `settings.json` OS-neutral — no per-machine edits.
- Apply to: `chief-of-staff`, `dev-agent`, `research-analyst` settings.json.
- Verify: re-open a session, confirm `index-daily-logs` / `sync-check` actually ran (no silent skip).

### 1.2 Centralize the workspace map  [P0]
`workspace-scan.py` (dev-agent) hardcodes a 6-entry `C:\Workspace\...` topology that doesn't exist on Mac.
- Add `.claude/workspace.local.json` (gitignored, per-machine) listing this machine's workspace roots.
- Ship a committed `workspace.local.json.example`.
- `workspace-scan.py` + friends read it instead of a hardcoded list.
- Mac entry must include the incoming **Personal Projects** + **Webdesign Business** roots (see Bucket 4).

### 1.3 Repo-relative path resolution  [P0]
Scripts derive agent/repo root from their own location (`__file__` / `$0`), never `C:\Workspace\agents`.
- Operational files to fix: `dev-agent/.claude/scripts/{workspace-scan,log-commit}.py`.

### 1.4 De-hardcode behavioral config  [P1 — agents read these as truth]
Replace `C:\Workspace\agents\...` with repo-relative references (e.g. `wiki/`, `<repo>/wiki/`):
- **Atlas:** `CLAUDE.md`, `identity/{memory,user}.md`, `.claude/rules/domain.md`, `.claude/skills/{recall,draft-email}/SKILL.md`
- **Polaris:** `CLAUDE.md`, `identity/{memory,user}.md`, `.claude/rules/domain.md`, `.claude/agents/{builder,designer,devops,qa,security}.md`, `.claude/skills/recall/SKILL.md`
- **research-analyst:** `identity/memory.md`
- **Wiki:** `infrastructure.md`, `projects/{career-ops,gbotoe-business,google-oauth-production,madina-portfolio}.md`
- **Leave alone (historical, append-only):** all `daily-logs/*.md`, `dev-agent/design/team-os/*`, `memory/projects.md`, `wiki/discussions/*`. Rewriting them falsifies the record.

### 1.5 Mechanical enforcement  [P1 — rules-without-mechanism rot here]
Add a scanner (PreToolUse hook + CI step) that **fails** when a new hardcoded `C:\` or `/Users/<name>/` absolute path enters tracked code. Without it the migration silently rots the first time either machine writes an absolute path into a shared file.

---

## Bucket 2 — Cloud-ify the Windows-only tasks (kill the machine dependency)

Each Slack-posting task is a clean candidate to move to GitHub Actions like `promote`/`discuss` already are. Once moved, "which machine is primary" stops mattering for automation.

| Task | Decision needed | Notes |
|------|-----------------|-------|
| MorningBrief, MiddayCheck, EveningWrapup, FridayWrap, WeeklyReview | **→ cloud** | Pure Slack output; ideal for Actions. Mind TZ (cron is UTC). |
| ScanSlack ×2, ScanHeartbeat ×2 | **→ cloud** | Slack in, Slack out. |
| GranolaIngest | **verify** | Needs Granola access from CI — may require auth not available in Actions. If so, keep local on primary (Mac launchd). |
| IndexLogs, Decay, SelfImprove | **verify** | Repo-maintenance; can run in Actions on a schedule, committing back like promote does. |

- For anything that genuinely can't run in cloud (auth-bound), build a **Mac launchd** job from the existing `templates/launchd/*.plist` — primary machine only.
- **Retire the Windows Task Scheduler `\Atlas\` jobs** as each is cloud-ified, so nothing double-fires.

### 2.1 Tier-2 runner definitions + injection hardening  [net-new 2026-06-18]
The 4 Slack-posting daily-drivers were ported `.ps1`→`.sh` (`bin/scheduled/{morning-brief,midday-check,evening-wrapup,meeting-prep}.sh`) — portable runners holding the prompt bodies with repo-relative (`$AGENTS_ROOT`) paths. **Reuse these prompts when cloud-ifying — don't rewrite them.** Per the table above these target **cloud**, not launchd.

**[CRITICAL — clear before ANY Tier-2 runner goes live, cloud or local]** these flows ingest external email/Granola/web content and currently invoke `claude -p --dangerously-skip-permissions` → prompt-injection → RCE + file-write fanout. Required hardening:
- Replace `--dangerously-skip-permissions` with a scoped `--allowedTools` allowlist — real server prefixes are `mcp__atlas-gcal__*` / `mcp__atlas-gmail__*` / `mcp__atlas-slack__*` (NOT generic `mcp__gcal__*`), plus `WebSearch`/`WebFetch` (AI-radar + Open-Meteo) and `Read`/`Write`; add `--disallowedTools Bash` where the job needs no shell (verify evening-wrapup/meeting-prep — they write wiki sources).
- Compute wiki write paths + a sanitised slug `[a-z0-9-]+` in the caller, not the LLM (pin base to `wiki/sources/`); data-fence external text.
- **Interim:** the `.sh` are **fail-closed** — `exit 2` unless `ATLAS_TIER2_HARDENED=1` — so they can't run unhardened.

---

## Bucket 3 — Reconcile the docs with reality

- Rewrite `CLAUDE.md` "Scheduling / Active Tasks" to state what *actually* runs where after Bucket 2 (cloud vs. Mac-launchd vs. retired). No more phantom Windows tasks.
- Same pass on Polaris + research-analyst CLAUDE.md scheduling sections.
- Note the Windows→Mac primary shift in `identity/memory.md` (hot memory) for all agents.

---

## Bucket 4 — Bring the rest of the workspace to the Mac

"Everything → Mac" means cloning the non-agent workspaces and registering them:
- Clone **Personal Projects** + **Webdesign Business** to a Mac location.
- Add their roots to `.claude/workspace.local.json` (1.2).
- Confirm secrets/`.env` for any project that needs them (git won't carry these — by design).

---

## Bucket 5 — Move inter-agent notifications onto WDAI Slack (decided 2026-06-18)

Today's discovery: Atlas↔Polaris pinging only works from Windows. The inter-agent channels (`#atlas-cos` C0ASHFXMHM5, `#polaris-tl` C0ASYTE8PB4) live in the **DaFudge** workspace, served by the local Slack bot / `slack-watcher` — which isn't running on the Mac. The only Slack connector wired here is **WDAI**, so a Mac-side `slack_send_message` to `#polaris-tl` returns `channel_not_found`.

**Decision (Dina, 2026-06-18):** don't port DaFudge — **move inter-agent comms to the WDAI Slack workspace.** WDAI is already wired on the Mac, so this also fixes the notification gap.

Work:
- Create the inter-agent channels in WDAI (e.g. `#atlas-cos`, `#polaris-tl`) and capture their new channel IDs.
- Update `CLAUDE.md` "Inter-Agent Communication" + "Key Facts" (channel IDs), `identity/memory.md`, and the same in dev-agent — replace DaFudge IDs with WDAI IDs.
- Update `slack-watcher` config (`config.json`) to listen on the WDAI workspace/channels; retire the DaFudge wiring.
- Confirm the bot token / app is installed in WDAI with the needed scopes (per-machine secret, not committed).
- Until this lands, the **wiki log is the handoff** (Slack is only the doorbell) — already how routing survived today.

Note: keeps the audit trail unchanged (wiki log is workspace-agnostic); only the notification layer moves.

---

## Suggested order
1. **1.1 python shim** — unblocks all hooks; everything else is observable once safety scaffolding actually runs.
2. **1.2 + 1.3 + 1.5** — path config + enforcement, so no new absolute paths leak while we work.
3. **1.4** — behavioral config sweep (mechanical once the pattern's set).
4. **Bucket 2** — cloud-ify, one task at a time, retire the Windows twin as each lands.
5. **Bucket 3** — docs reconcile (do alongside 2 so they never drift again).
6. **Bucket 4** — workspace clones, whenever convenient.
7. **Bucket 5** — WDAI Slack inter-agent move; can run anytime (independent of 1–4). Atlas owns the CLAUDE.md/memory channel-ID swap; `slack-watcher` config + WDAI app install is ops/Polaris.

## Owner split
- **Polaris** owns the technical execution (scripts, hooks, Actions workflows, enforcement scanner) — his lane.
- **Atlas** owns CLAUDE.md/identity/memory reconciliation + coordination + this plan.
- **advisor() gap:** `rules/personal.md` makes outside-read mandatory for cross-workspace infra; no advisor is wired on Mac. Either wire it or formally scope the rule before code lands — don't leave a hard rule silently unenforceable.

## Open question still on the table
- GranolaIngest: does Granola auth work from GitHub Actions? If no → it stays a Mac-local launchd job and the "fully cloud" goal has one exception. Decide during Bucket 2.
