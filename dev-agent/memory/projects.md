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

**Three services are the dev-onboarding foundation** (per Helen's framing): Clerk + Stripe + DB. Everything else (Luma, Mailchimp API, Vimeo admin, Slack, PostHog) gated to contributors actively working on those integrations — default `.env.local` only needs the three.

**Known drift sources:**
- Mailchimp cohort RSVP form URL hardcoded in `content/product/courses.ts` → preview deploys post to live audience. Accepted operational risk. Fix is env-driven URL resolution; future PR.
- `SLACK_DRY_RUN=true` in staging Vercel env no-ops Slack sends (confirmed via `grep -n SLACK_DRY_RUN lib/slack.ts`).

**Windows dev gotchas:**
- Prisma `db:generate` fails with EPERM DLL lock when the `next dev` server is running. Stop server first.
- `npm run db:local:reset` uses a bash script that PowerShell can't invoke — run `bash ./scripts/db-local.sh reset` instead.
- Biome line-ending warnings (`LF will be replaced by CRLF`) are Windows-only noise; CI on Linux is clean.
- Repo-wide biome sees ~240 errors locally (mostly CRLF); CI's `biome check . --diagnostic-level=error` passes on Linux.

**Pipeline architecture (added 2026-04-17 via PR #564):**
- `web/scripts/staging-refresh/{preflight,dump,transform,restore}.sh` — prod → staging refresh
- `.github/workflows/staging-refresh.yml` — weekly cron Sundays 11:00 UTC + `workflow_dispatch`
- `web/app/api/staging-status/route.ts` — leader-gated observability endpoint
- `web/prisma/schema.prisma` `StagingMeta` model (single-row, CHECK id=1)
- V1 ships without PII anonymization. V2 triggers documented in `docs/plans/staging-refresh-pipeline.md`.

<!-- added 2026-04-19 -->
## WDAI tech debt audit — Phase 1

Audit results: `wiki/projects/wdai-tech-debt.md`. **9 Must Fix / 19 Nice / 4 Negligible.**

**P0s (flagged to Atlas via #atlas-cos):**
- `MainProtection` GitHub ruleset allows 0-approval merges → tighten to require ≥1 review before contributor access broadens.
- 8-PR backlog stalled in review (incl. #569 Stripe race fix) — needs unblock pass.

**Phase 2 deferred** (needs Builder + QA delegation in a fresh session): duplication, file-size scan, dep CVE triage, test coverage map, docs gaps, rate limiting, CSP, secrets rotation, PII in logs, backup/DR.

<!-- added 2026-04-19 -->
## Agent ecosystem roadmap

Location: `wiki/projects/agent-ecosystem.md`. Living doc parallel to `wdai-tech-debt.md` but for agent infrastructure. Both Atlas and Polaris write here.

**Scope rule:** agent infra → this roadmap; external repos → per-project doc; agent-internals → that agent's memory.

**Tier seed:**
- **P0** — symmetric inbox polling (shipped 2026-04-19, commit `9cc35fc`).
- **P1** — cross-post migration at N=3 channels; Atlas's 5 UX items.
- **P2** — watcher hardening, distill short-circuit guard (shipped 2026-04-25), log rotation, runtime state centralization.
- **P3** — shared agent-core extraction, sub-agent SDK.

<!-- added 2026-04-19 -->
## CineVault redesign

Location: `C:\Workspace\Personal Projects\media-theater\docs\redesign\roadmap.md` — source of truth. Check there before recomputing scope from session memory or git log.

**Open buckets:** spotlight B, button primitive, Trakt CTA, YIR conform, vote/convince, share review, error parity, audit infra, a11y.

<!-- added 2026-05-19 -->
## Self-awareness instrumentation layer

Shipped 2026-05-19 to agents repo (6 commits: `7eff38b`, `bc67b57`, `05e8452`, `e9c767a`, `0d982b3`, `3e3b4d6` + fix `cdef880`).

**Components:**
- **Delegation-scope warning hook** — fires when ≥4 external files touched in a session; soft-warns to assess scope creep.
- **Multi-repo daily-log commit logger** — tracks commits across repos in the daily log entry, not just agents repo.
- **Lite session-snapshot on SessionEnd + PreCompact** — writes external files touched + delegation soft-warn signals to snapshot.
- **Prior-art surveying** — prepend survey step for all substantive decisions; honest-framing fix applied per advisor critique (commit `cdef880`).

<!-- added 2026-05-20 -->
## WDAI team-OS

Location: `wdai-team-os` repo. Full architecture: `memory/project_team_os_one_brain.md`.

**Structure:** Federated KB (NOT a doc). Two layers: individual weekly synthesis (per core team member) → team-OS dedup → wdai-team-os repo.

**Current state (as of 2026-05-20):**
- 22 of ~48 C-series turnover-resilience rows filled (strategy/, members/, programs/, curriculum/, operations/runbooks/, grants/, operations/infrastructure/)
- ~25 C-series rows still tribal knowledge (Helen: 9, Brigitte: 4, Lauren: 3, Sandhya/Sheena: 3, Step-0 session: 3, deferred: 2)
- C4 admin access map = HIGHEST priority SPOF dissolution (Helen+Madina)
- C47 update-current-state skill = build to make system self-sustaining

**Open PRs:**
- PR #4 (ADR-0007 tiered autonomy) — awaiting Helen ack, has conflicts; rebase when she responds
- PR #11 (Section 5 Linear refresh + 4 doc-gap fixes) — clean, ready for review

**Merged:**
- PR #7 (22 C-series closures + maintenance system)
- PR #9 (Beacon Slack app install reference)
- PR #10 (ADR-0008 content synthesis at scale)

**Key architecture decisions:**
- ADR-0007: tiered autonomy supersedes HITL-everywhere (pending Helen ack)
- ADR-0008 (merged): 4-stage synthesis-at-scale escalation. Stage 1 = long-context (Anthropic 2026). Stage 3 candidate: OpenAI text-embedding-3-small OR Voyage voyage-3-large. Stage 4 candidate: graphrag-hybrid (Neo4j+Qdrant).
- Contract-first / runtime-agnostic principle for distributed systems
- ADR scope = HUMAN cross-cutting decisions; per-incident agent work stays in Linear
- Dual canonical sources: platform `content/*.ts` for org content; marketing vault for outbound voice
- Wiki-vs-extend-folders TABLED (until orphaned content categories actually need to land)

**Team OS Beacon:**
- WDAI Slack app for contributor interface (verification pings, ADR acks, runbook check-ins, decision capture)
- Installed in WDAI workspace. Round-trip DM tested. `wdai-slack` MCP wired (needs session restart).
- Tokens in Windows Credential Manager (`wdai-slack` service: `bot_token`, `app_token`, `dina_user_id`)
- Polaris-as-driver = POC only — production needs WDAI-tier always-on runtime (ADR pending)
- Tier B scopes deferred (channels:manage, groups:write, channels:join) — need separate Helen consent

**Dina's key patterns (team-OS sessions):**
- Value-first anchoring before mechanism — caught Polaris ~5 times defaulting to artifacts over outcomes
- Helen design doc = INPUT, never source of truth
- "Drop dead tomorrow" turnover-resilience IS the strategic value prop
- Build for ANY runtime; defer runtime choice to its own future decision
- One source of truth per concept — don't proliferate multiple roadmaps
- "What are you grounding your decision on?" — real evidence required, not vibe-matching

<!-- added 2026-06-13 -->
## WDAI Compound Engineering (Every plugin)

**Status:** PR #689 open (docs-only, 4 commits as of 2026-06-14).

**What shipped:**
- CE plugin installed at WDAI foundation-platform project scope (team-wide, `ce-setup` ran)
- `wdai-foundation-platform/.claude/compound-engineering.yml` — project config scaffold with `extraKnownMarketplaces`
- `docs/decisions/adr-003-compound-engineering.md` — adoption ADR
- CLAUDE.md coexistence routing table: CE skills vs WDAI native skills vs overlap paths

**Key finding:** CE's destructive-migration guard is **already covered** by existing `ci.yml` `Check for destructive migrations` step (skill-agnostic). Stopped Builder mid-flight to avoid duplication.

**Open items:**
1. Admin must mark `Check for destructive migrations` as a **required** CI check in branch protection settings — neither Dina nor mgbotoe has admin access currently.
2. Fast-follow: AGENTS.md `docs/solutions/` pointer once `ce-compound` runs produce first solution.
3. Cross-tool CE (Codex/Gemini) optional per-machine — not blocking.

**Coexistence routing (summary):**
- CE `pr-merge-workflow` = kept path (replaces ad-hoc merge flows)
- WDAI `defrag` skill = kept (CE has no equivalent)
- WDAI `accessibility-audit` skill = kept (CE has no equivalent)
- WDAI `distill-session` skill = kept (CE has no equivalent)
- Overlap areas (code review, ADR drafting) → CE skill as default, WDAI-specific context injected via AGENTS.md
