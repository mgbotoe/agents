---
name: project_wdai_ce_adoption
description: WDAI foundation repo adopting full Compound Engineering plugin — what WDAI skills do BETTER and must be preserved/grafted after install
metadata:
  type: project
---

Decision (2026-06-13, Dina/CAIO): install the FULL Every `compound-engineering` plugin into the WDAI foundation repo (`mgbotoe/compound-engineering-adoption` branch off main). All 37 skills + 43 agents. CE is `ce-`prefixed so it coexists with — does not overwrite — WDAI's existing `.claude/skills/`.

**Why grafting matters:** content-level head-to-head (2026-06-13, 3 sub-agents read both sides) found CE wins on execution (ce-work parallel worktrees), codification (ce-compound), debugging (ce-debug), observation (ce-product-pulse), doc-review. But WDAI's skills BEAT or fill gaps CE has. Preserve these after install:

1. **pr-merge-workflow — CE has NO equivalent safety gate.** Typed `CONFIRM DESTRUCTIVE MERGE` for DROP/ALTER...DROP/TRUNCATE/DELETE migration SQL; expand-contract 24h gate; one-PR-at-a-time; post-merge prod verify. KEEP as merge path; OR port the destructive-migration typed-confirm into ce-commit-push-pr/ce-work.
2. **council — cross-model diversity (Claude+Codex+Gemini).** CE planning is Claude-only. Keep council as optional pre-ce-plan grounding, or feed its multi-model synthesis into ce-plan.
3. **review-codex — independent cross-model review.** ce-code-review is all in-Claude (same blind spots). Run review-codex as a final independent pass alongside ce-code-review.
4. **commit-workflow specifics → graft into ce-commit-push-pr:** prisma-change → `npm run db:test` (mirrors CI DB job); prod build w/ explicit localhost:5433 env; Playwright visual test on UI diffs; pre-push re-validation (catches GitHub-UI auto-merge drift); post-merge prod verify vs www.womendefiningai.org.
5. **Domain skills CE entirely lacks — keep as-is:** accessibility-audit (WCAG 2.2 AA, legal grounding, AT matrix, /accessibility statement page); seo-public-page (the load-bearing middleware `createRouteMatcher` redirect gotcha — Clerk gates all routes by default); local-dev (role-based leader/member test-cred matrix + Stripe webhook forwarder); test-db (CI-parity ephemeral Postgres seed).
6. **defrag — whole-repo fragmentation** w/ Chesterton's-fence verification (git blame, intentional-divergence check). Distinct from ce-simplify-code (recent-diff scope). Keep both.
7. **.claude/patterns/ catalog + banned-patterns checker** (`web/scripts/check-banned-patterns.mjs`, WDA-377) + jscpd/size-limit/server-only build gates. Graft: ce-compound's `docs/solutions/` should reference/feed the patterns catalog; ce-project-standards-reviewer must read `.claude/patterns/` + AGENTS.md.
8. **WDAI-stack review checklist** (RSC-default, no `useUser()`, db-first-membership, Stripe Subscription Schedules not `.update()`, webhook idempotency, `_count` not fetch-all). Graft into ce-code-review personas.

**AGENTS.md already exists** in the repo (18.5KB, PR #675 / ADR-002, single-source w/ CLAUDE.md `@import` shim). `/ce-setup` must EXTEND it, not clobber — CE ships its own AGENTS.md convention.

**Process:** grafting = cross-repo architectural change → advisor() before writing skill/config modifications. Install (`/plugin ...` + `/ce-setup`) is Dina's manual step. See [[feedback_chestertons_fence]], [[feedback_review_vs_fix]].
