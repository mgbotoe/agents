# Projects — Cold Memory

Detailed project context. Searched on-demand, not loaded every session.

<!-- added 2026-04-17 -->
## WDAI Foundation Platform — environment architecture

Location: `C:\Workspace\Women Defining AI\wdai-foundation-platform\`
Stack: Next.js 16 + Clerk + Stripe + Prisma + Supabase Postgres. Node 20, Biome, Vitest, Playwright.

**Three environments:**

| Env | DB | Auth | Stripe | Email/Mailchimp |
|---|---|---|---|---|
| **Local dev** | Docker Postgres on `localhost:5433` (seed: `bash ./scripts/db-local.sh reset` from `web/`) | Clerk test mode | Stripe test mode | Mailchimp API key absent server-side; form URL hardcoded to live audience (accepted risk) |
| **Staging** | Supabase project `qfcjtidvmzvppxbkxupk` (us-east-2) | Clerk test mode (separate app) | Stripe test mode | Same Mailchimp URL leak as local |
| **Production** | Separate Supabase project | Clerk live mode | Stripe live mode | Mailchimp live |

**Three services are the dev-onboarding foundation** (per Helen's framing): Clerk + Stripe + DB. Everything else gated to contributors actively working on those integrations.

**Known drift sources:**
- Mailchimp cohort RSVP form URL hardcoded in `content/product/courses.ts` → preview deploys post to live audience. Accepted risk.
- `SLACK_DRY_RUN=true` in staging Vercel env no-ops Slack sends.

**Windows dev gotchas:**
- Prisma `db:generate` fails with EPERM DLL lock when the `next dev` server is running. Stop server first.
- `npm run db:local:reset` uses a bash script that PowerShell can't invoke — run `bash ./scripts/db-local.sh reset` instead.
- Biome line-ending warnings (`LF will be replaced by CRLF`) are Windows-only noise; CI on Linux is clean.

**Pipeline architecture (added 2026-04-17 via PR #564):**
- `web/scripts/staging-refresh/{preflight,dump,transform,restore}.sh` — prod → staging refresh
- `.github/workflows/staging-refresh.yml` — weekly cron Sundays 11:00 UTC + `workflow_dispatch`
- `web/app/api/staging-status/route.ts` — leader-gated observability endpoint
- V1 ships without PII anonymization. V2 triggers documented in `docs/plans/staging-refresh-pipeline.md`.

**Notable merged PRs:**
- PR #686 (merged 2026-06-13): Luma co-hosts → Google Meet + Calendar sync (creation + hourly cron). +1186/-66, 10 files.

<!-- added 2026-04-19 -->
## WDAI tech debt audit — Phase 1

Audit results: `wiki/projects/wdai-tech-debt.md`. **9 Must Fix / 19 Nice / 4 Negligible.**

**P0s (flagged to Atlas via #atlas-cos):**
- `MainProtection` GitHub ruleset allows 0-approval merges → tighten to require ≥1 review before contributor access broadens.
- 8-PR backlog stalled in review (incl. #569 Stripe race fix) — needs unblock pass.

**Phase 2 deferred** (needs Builder + QA delegation in a fresh session): duplication, file-size scan, dep CVE triage, test coverage map, docs gaps, rate limiting, CSP, secrets rotation, PII in logs, backup/DR.

<!-- added 2026-04-19 -->
## Agent ecosystem roadmap

Location: `wiki/projects/agent-ecosystem.md`. Living doc for agent infrastructure. Both Atlas and Polaris write here.

**Scope rule:** agent infra → this roadmap; external repos → per-project doc; agent-internals → that agent's memory.

<!-- added 2026-04-19 -->
## CineVault redesign

Location: `C:\Workspace\Personal Projects\media-theater\docs\redesign\roadmap.md` — source of truth.

**Open buckets:** spotlight B, button primitive, Trakt CTA, YIR conform, vote/convince, share review, error parity, audit infra, a11y.

<!-- added 2026-05-19 -->
## Self-awareness instrumentation layer

Shipped 2026-05-19 to agents repo (6 commits: `7eff38b`, `bc67b57`, `05e8452`, `e9c767a`, `0d982b3`, `3e3b4d6` + fix `cdef880`).

**Components:**
- **Delegation-scope warning hook** — fires when ≥4 external files touched in a session.
- **Multi-repo daily-log commit logger** — tracks commits across repos in the daily log entry.
- **Lite session-snapshot on SessionEnd + PreCompact** — writes external files touched + delegation soft-warn signals.
- **Prior-art surveying** — prepend survey step for all substantive decisions; honest-framing fix (`cdef880`).

<!-- added 2026-05-20 -->
## WDAI team-OS

Location: `wdai-team-os` repo. Full architecture: `memory/project_team_os_one_brain.md`.

**Structure:** Federated KB (NOT a doc). Two layers: individual weekly synthesis (per core team member) → team-OS dedup → wdai-team-os repo.

**Current state (as of 2026-05-20):**
- 22 of ~48 C-series turnover-resilience rows filled
- ~25 C-series rows still tribal knowledge (Helen: 9, Brigitte: 4, Lauren: 3, Sandhya/Sheena: 3, Step-0 session: 3, deferred: 2)
- C4 admin access map = HIGHEST priority SPOF dissolution
- C47 update-current-state skill = build to make system self-sustaining

**Open PRs:**
- PR #4 (ADR-0007 tiered autonomy) — awaiting Helen ack, has conflicts
- PR #11 (Section 5 Linear refresh + 4 doc-gap fixes) — clean, ready for review

**Merged:** PR #7 (22 C-series closures), PR #9 (Beacon app), PR #10 (ADR-0008 content synthesis).

**Key architecture decisions:**
- ADR-0007: tiered autonomy supersedes HITL-everywhere (pending Helen ack)
- ADR-0008 (merged): 4-stage synthesis-at-scale escalation
- Contract-first / runtime-agnostic principle
- ADR scope = HUMAN cross-cutting decisions; per-incident agent work stays in Linear

**Team OS Beacon:**
- WDAI Slack app for contributor interface. Installed + round-trip DM tested. `wdai-slack` MCP wired (needs session restart).
- Tokens in Windows Credential Manager (`wdai-slack` service: `bot_token`, `app_token`, `dina_user_id`)
- Polaris-as-driver = POC only — production needs WDAI-tier always-on runtime (ADR pending)

<!-- added 2026-06-13; updated 2026-06-14 -->
## WDAI Compound Engineering (Every plugin)

**Status:** PR #689 open (docs-only, 6 commits as of 2026-06-14). Pending merge.

**What shipped:**
- CE plugin installed at WDAI foundation-platform project scope
- `wdai-foundation-platform/.claude/compound-engineering.yml` — project config scaffold
- `docs/decisions/adr-003-compound-engineering.md` — adoption ADR
- CLAUDE.md coexistence routing table: CE skills vs WDAI native skills vs overlap paths
- `pr-merge-workflow` clarified as the kept PR-merge path

**Key finding:** CE's destructive-migration guard already covered by existing `ci.yml` step.

**Open items:**
1. Admin must mark `Check for destructive migrations` as a required CI check — neither Dina nor mgbotoe has admin.
2. Fast-follow: AGENTS.md `docs/solutions/` pointer once `ce-compound` runs produce first solution.
3. Cross-tool CE (Codex/Gemini) optional per-machine — not blocking.

<!-- added 2026-06-18 -->
## Cross-platform (Mac + Windows) port

**Branch:** `chore/cross-platform-agnostic` — not yet merged to master as of 2026-06-18.

**Key changes:**
- Path derivation via `parents[N]` (no hardcoded `C:\`); `.mcp.json.example` + `config/secrets.env.example` templates
- `gather-context.ps1` → `gather-context.py`: cross-platform; fixed 0GB disk bug via `shutil.disk_usage`; safe `os.kill(pid,0)` / ctypes liveness probe
- `heartbeat` skill → `/loop` (local-state watchdog, no cloud home)
- `decay.yml` + `self-improve.yml` cloud crons. Self-improve is **PR-gated** (opens PR, never writes master; security.md/SOUL.md/CLAUDE.md off-limits to auto-edit)
- Deleted all Windows Task Scheduler `.cmd`/`.bat` + `.ps1`; `bin/scheduled/` gone
- Per-machine workspace map via `_workspace.py` + gitignored `workspace.local.json` (+ .example)
- `bin/scan-paths.py` + `port-guard.yml` CI path-leak guard
- `/advisor` skill as a **fork** (cross-platform, zero per-machine CLI deps) — NOT wired to council yet (flag for Dina)
- `context-injector` now also scans `wiki/decisions/` (was only `wiki/projects/` — root cause of cross-platform ADR not surfacing)

**Three-repo cross-machine config ADR (candidate, not yet formalized):**
- `mgbotoe/my.claude` (683→29 tracked files; gitignores vendored plugins/)
- `mgbotoe/claude-skills` (private marketplace, 17 skills extracted)
- `agents` repo
- Declarative `extraKnownMarketplaces` + per-machine hooks in `settings.local.json`
- Marketplace freshness via `sync-skills.py` SessionStart hook (self-healing git-pull; needed because Claude Code doesn't auto-pull github marketplaces per issue #44276)

**Open items after branch merge:**
- Verify `settings.local.json` hooks merge correctly next session (`[sync-skills] up to date`)
- Delete `custom-skills.bak-directory-source`
- Confirm `f0ff7e7` (orphaned 2026-05-12 WDAI core team sync source) pushed
- Atlas `.ps1` meeting-prep port → cloud (pipeline DEAD since 2026-05-12)
- CE-overlap consolidation
- Wire `/advisor` → council: discuss with Dina
- Repo setting needed: "Allow GitHub Actions to create and approve pull requests" for self-improve.yml

**Issues encountered:**
- Corrupt git index mid-session (`bad signature 0x00000000`) — recovered via backup-aside + `git reset`
- `os.kill(pid,0)` is a Windows footgun (would TerminateProcess) — diverged to ctypes `OpenProcess`
- `scan-paths.py` initially swallowed relative-path findings via broad except → fixed
- Drive-letter regex false-positived on `word:\n` escape sequences → standalone-drive lookbehind
- Daily-logs on a feature branch conflict with master's copy — left uncommitted; needs handling at merge

**Atlas meeting-prep pipeline DEAD since 2026-05-12:**
- Task Scheduler killed in 2026-05-07 cloud migration; `.ps1` never ported to cloud
- Missed WDAI Core Team Syncs May 19 / Jun 2 + Helen sessions
- Posted #atlas-cos 2026-06-18; orphaned May-12 source committed (`f0ff7e7`)
- Fix: port Atlas meeting-prep `.ps1` to cloud cron (open work)
