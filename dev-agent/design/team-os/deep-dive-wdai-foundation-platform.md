# Deep Dive: `wdai-foundation-platform`

**The main WDAI product.** Next.js monorepo, Clerk + Stripe + Supabase + Luma + Vercel. What the team-OS plugs into, but does not replace.

---

## Structure at a glance

```
wdai-foundation-platform/
├── .claude/                       ← Per-repo Claude Code config
│   ├── settings.local.json
│   ├── skills/
│   │   ├── accessibility-audit/   ← (you shipped this)
│   │   ├── commit-workflow/
│   │   ├── council/
│   │   ├── defrag/                ← (you shipped this)
│   │   ├── pr-merge-workflow/
│   │   ├── review-codex/
│   │   └── seo-public-page/
│   ├── commands/
│   │   ├── commit.md
│   │   ├── council.md
│   │   ├── implement.md
│   │   ├── local-dev.md
│   │   ├── review-codex.md
│   │   └── test-db.md
│   ├── council/                   ← Multi-perspective planning config
│   └── defrag/                    ← Refactoring config
├── .github/
│   ├── CODEOWNERS                 ← Yes — branch protection via codeowners
│   └── workflows/
│       ├── ci.yml
│       ├── course-content-agent.yml      ← Paradigm 4 — MONTHLY 1st 9am UTC
│       └── website-content-agent.yml     ← Paradigm 4 — MONTHLY 15th 9am UTC
├── apps/                          ← Monorepo apps tier
├── packages/                      ← Monorepo packages tier
│   ├── course-update-agent/       ← Analyzes course content, creates PR with updates
│   └── website-agent/             ← Updates CMS content files
├── web/                           ← Main Next.js app (everything happens here)
│   ├── app/
│   │   ├── (app)/                 ← Authenticated routes
│   │   ├── api/                   ← API routes
│   │   └── components/            ← Business-specific React components
│   ├── components/                ← Generic reusable UI components
│   ├── lib/                       ← Shared TS helpers, cache strategies
│   ├── prisma/                    ← Schema, migrations
│   ├── scripts/                   ← Ops scripts (manage-test-accounts, etc.)
│   ├── docs/
│   │   └── testing.md
│   └── __tests__/
├── docs/                          ← Repo-level docs
│   └── adr/                       ← EMPTY (no ADRs yet, despite the discipline rule)
├── _poc/                          ← Old proof-of-concept work
├── CLAUDE.md                      ← 36KB — heavy governance doc
├── README.md                      ← 18KB — entry point
├── PR_DESCRIPTION.md              ← Working draft for current PR
└── tsconfig.tsbuildinfo
```

---

## Stack (confirmed from CLAUDE.md + package.json)

- **Framework:** Next.js 16 with App Router
- **Cache:** Experimental `'use cache'` directive + `cacheLife` + `cacheTag` (PPR/`cacheComponents` deferred per Linear `WDA-285`)
- **DB:** Supabase (Postgres) via Prisma
- **Auth:** Clerk
- **Payments:** Stripe
- **Events:** Luma API
- **Media:** Vimeo, Vercel Blob storage
- **Testing:** vitest (unit + integration configs), Playwright MCP
- **Linting:** Biome
- **Project mgmt:** **Linear** (WDA-* ticket prefix referenced inline in CLAUDE.md)

---

## TWO production code-modifying agents in this repo

Both are paradigm-4 (cloud cron via GitHub Actions). Both autonomously open PRs for human review.

### 1. `course-content-agent.yml` + `packages/course-update-agent/`
- **Schedule**: 1st of each month, 9am UTC
- **What it does**:
  - Reads course content from DB
  - Outputs `content-snapshot.json` from a built JS file
  - Analyzes course content (via Anthropic API, secrets.ANTHROPIC_API_KEY)
  - Creates a PR with proposed updates
- **Concurrency control**: `cancel-in-progress: false`, prevents overlapping runs
- **Manual trigger**: `workflow_dispatch` with `dry_run: boolean` input
- **Secrets**: `AGENT_DATABASE_URL` (separate from main DATABASE_URL — likely read-only)

### 2. `website-content-agent.yml` + `packages/website-agent/`
- **Schedule**: 15th of each month, 9am UTC (offset from course-agent to avoid collisions)
- **What it does**: Updates CMS content files
- **Same pattern**: workflow_dispatch with dry_run, concurrency group, Anthropic SDK

**Significance for the team-OS:** Production code is already being modified by autonomous agents on a schedule, with PR-as-the-approval-gate model. This is the most mature paradigm-4 implementation in WDAI. The team-OS federation can use the same pattern at the organizational level — bots that propose PRs to the wdai-team-os repo, humans review and merge.

---

## CLAUDE.md (36KB — heavy governance)

Major sections it defines:
- **Component Placement Rules** — `/web/components/` (generic, reusable, "could be npm packages") vs. `/web/app/components/` (business-specific, WDAI-domain). Explicit decision test.
- **Common Commands** — all from `web/` directory: `npm run dev`, `db:push`, `db:seed`, `db:local:reset`, `commit`.
- **Local Dev Test Accounts** — `leader@test.com` / `TestLeader123!` (Annual), `member@test.com` / `TestMember123!` (Monthly). Stripe test card `4242 4242 4242 4242`.
- **Database Migration Safety** — explicit **Expand-Contract pattern** (3 PRs for destructive changes), risk matrix, "code can be reverted, migrations cannot" golden rule.
- **Performance Patterns** — full caching strategy table (TTLs from 5min to 1hr), `cacheTag` invalidation, cache function inventory.
- **Testing Patterns** — vitest mock idioms, integration test config (separate `vitest.integration.config.ts`).
- **Adding Features Checklist**.

This file is the **operational contract for any agent or human touching the platform**. Heavy by design.

---

## Skills in `.claude/skills/`

7 skills. Two of these are **yours**:

- `accessibility-audit/` — you shipped (PR #600, Apr 14 from memory.md)
- `defrag/` — you shipped (PR #560)
- `council/` — multi-perspective planning
- `commit-workflow/` — your branch-check + commit hygiene
- `pr-merge-workflow/`
- `review-codex/` — your `/review-loop` skill
- `seo-public-page/`

Plus commands (`.claude/commands/`): `commit.md`, `council.md`, `implement.md`, `local-dev.md`, `review-codex.md`, `test-db.md`.

**Significance:** This is the only repo where you have substantial skill ownership. The team-OS spec can show "Madina contributes skills to pillar repos" as an existing pattern, not aspirational.

---

## Conspicuous gap: `docs/adr/` is empty

Your Polaris identity says: *"every significant decision gets an ADR."* The platform repo has the folder. **No ADRs in it.** All architectural decisions live inline in CLAUDE.md (the Expand-Contract pattern, the cache strategy, the component placement rules).

**This is a real federation tension.** The team-OS spec needs to decide:
- Do ADRs live per-repo (in each project's `docs/adr/`) and the team-OS aggregates references? Or
- Do all ADRs migrate to `wdai-team-os/decisions/` and the per-repo docs/adr/ folders become thin pointers?

Helen's design doc says decisions live in the team-os repo. But the platform already has its own decision discipline (just embedded in CLAUDE.md, not formalized as ADRs). Migration cost is real.

---

## CODEOWNERS enforcement

`.github/CODEOWNERS` exists (49 lines, per a recent diff in session-events). Branch protection via codeowners means PRs require named reviewer sign-off. This is what enforces your "tech lead reviews everything" pattern technically — not just socially.

**Team-OS spec implication:** CODEOWNERS is the working primitive for "agents propose; humans approve." Wherever paradigm-4 agents touch this repo, the named owners gate the PR.

---

## CI pipeline (`ci.yml`)

49 lines. Standard checks: typecheck → lint → test → build. Same sequence Polaris's identity mandates.

---

## Patterns observed (deferred to Pass 3 for design decisions)

1. **CODEOWNERS + branch protection** as the access enforcement primitive. Already in place. Reusable.
2. **Monthly paradigm-4 agents** as the canonical example of "agent proposes, human reviews PR" at production scale. Two examples shipping.
3. **Per-repo `.claude/skills/`** distribution pattern. Skills live where they're used. Don't centralize unless cross-repo.
4. **Linear as the canonical issue tracker** — already referenced inline in CLAUDE.md (WDA-285, WDA-* prefix). This validates your May 9 proposal.
5. **Expand-Contract migration pattern** — schema-level discipline applicable to any pillar repo that touches the DB.
6. **Two-layer caching with `cacheTag`** — applicable to the team-OS dashboard layer (Pass 3).
7. **`/web/scripts/`** as the home for one-off ops scripts. Equivalent to `bin/` in agent repos.

---

## Open questions surfaced by this repo

1. **ADR location.** Per-repo (per-pillar) or centralized in `wdai-team-os/decisions/`? Strong argument for both — keep ADRs near the code, but link them from a central index.
2. **Linear↔repo bridge.** Linear tickets reference repo PRs and vice versa. The team-OS spec needs to name this cross-tool boundary.
3. **CLAUDE.md vs. team-OS CLAUDE.md.** Each repo has its own CLAUDE.md (36KB here, 18KB README in marketing). Helen's design doc proposes a root team-os CLAUDE.md as the federation contract. **Need to decide hierarchy** — root team-OS CLAUDE.md as a *pointer index* to per-repo CLAUDE.mds, OR a fully separate "team-level" doc that doesn't duplicate.
4. **Test accounts and env management** — every pillar repo has its own `.env.local` story. Federation onboarding needs to teach new members how to set up local env across multiple repos.
5. **Agent PR signing.** Both course-agent and website-agent open PRs — what identity do they post under? If under Helen's GitHub account, that's a single-point-of-failure pattern the team-OS spec should improve (employee-style provisioning for the agents themselves).

---

## What's surprising

1. **No ADRs despite the rule** — biggest tension between the discipline you set and the reality.
2. **`apps/` and `packages/` directories** exist (proper Turborepo monorepo structure, `.turbo` cache dir present) but most code lives in `web/`. The monorepo split is real but light — `packages/` is essentially the agent-services tier.
3. **`_poc/` directory** — old proof-of-concept work archived in repo. Federation pattern: dead code stays archived, not deleted.
4. **`.playwright-mcp/`** — Playwright MCP integration already wired in. The team-OS spec can assume browser-testing capability exists.

---

## Open questions for cross-repo work

1. **Does the platform reference the marketing repo?** Probably not directly — they're peers in the WDAI org. The team-OS federation establishes cross-references.
2. **Are course-update-agent and website-agent ever going to integrate with wdai-marketing's calendar-sync?** Three monthly cron jobs hitting Anthropic; some prompts likely overlap.
3. **Course content lives in DB** (via course-update-agent's `collect-content.js`). Where does the marketing pillar's "what's launching" data live, and is it synced from the same DB or separately from Luma? Could be a redundancy or a single-source-of-truth opportunity.
