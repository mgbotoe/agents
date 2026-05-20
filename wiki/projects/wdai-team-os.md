# WDAI Team OS

**Living document.** The shared knowledge base + agent-maintainable repo for WDAI's collective brain — what Helen calls *"how can Women Defining AI run without people?"*

- **Repo:** [`mgbotoe/wdai-team-os`](https://github.com/WomenDefiningAI/wdai-team-os) at `C:\Workspace\Women Defining AI\wdai-team-os\`
- **Owner:** Madina (build) + Helen (strategic direction)
- **Stage:** Phase 0-1 active (architectural scaffolding done; content backfill in progress)
- **Bootstrapped:** 2026-05-19
- **Related:** [[projects/wdai-platform|WDAI Platform]], [[projects/wdai-tech-debt|WDAI Tech Debt]]

---

## What it is

A repository-based shared knowledge layer for the WDAI core team. Aim: WDAI survives complete team turnover — if everyone quits today, the next round of volunteers can pick up where things were left.

**Strategic value prop** (Helen, May 11 1:1):
> *"How can Women Defining AI run without people? What would need to be true if someone else came on board to pick things up?"*

**Three operational value props (Madina, May 20):**
1. **Catch-up function** — fill gaps for people not in a meeting (synthesis surfaces context)
2. **Design-time surfacing** — when designing solutions, automatically surface relevant cross-pillar context
3. **Turnover resilience** — at ANY moment in time, a turnover test would pass

## Current build state (as of 2026-05-20)

### Architecture (mostly done)

7 ADRs accepted / proposed in `decisions/`:
- 0001 Team OS separate repo (Accepted)
- 0002 Linear as ticket system (Accepted)
- 0003 Tool-agnostic per-person ingest (Accepted)
- 0004 Mission Control via OTel + Langfuse (Proposed — Phase 4+)
- 0005 Hivemind deferral with deliberate upgrade path (Accepted)
- 0006 Decision capture conventions across WDAI repos (Proposed — **load-bearing, awaiting Helen ack**)
- 0007 Tiered autonomy supersedes HITL-everywhere (Proposed — awaiting Helen ack)

### Content backfill (in progress)

`docs/roadmap.md` C-series tracks 48 turnover-resilience gaps. **22 closed (~46%) as of 2026-05-20.**

| Category | Closed | Remaining |
|---|---|---|
| Strategy / mission / voice | 3 | 3 (theory of change, product spectrum, partnership history) |
| Member-facing content | 4 | 1 (member personas + churn → Lauren) |
| Programs / curriculum / pricing | 3 | 4 (workshop runbook, retros, partnership history → Brigitte/Lauren) |
| Operations runbooks | 5 | 4 (Lumabot, wdai-admin, admin access map, financials → Helen) |
| Skills indices | 2 | 0 |
| Drafts (platform-side) | 5 ADR drafts | gated on Helen ack of 0006 |
| Step-0 session items | 0 | 3 (admin scopes, Slack consent, Drive enum) |
| Maintenance automation | 0 | 3 (C47-C49 future skill + webhooks + agent) |

### Active PRs (as of 2026-05-20)

| PR | Branch | Scope |
|---|---|---|
| #4 | `madina/adr-0007-tiered-autonomy` | ADR-0007 (awaiting Helen ack) |
| #5 | `madina/current-state-deep-read` | current-state.md Section 1/2/4 enrichment + PR template |
| #6 | `madina/platform-adr-backfill-drafts` | 5 platform-side ADR drafts (gated on Helen ack of 0006) |
| #7 | `madina/gap-roadmap-and-pillar-backfill` | 22 C-series closures + maintenance system + platform-sourced strategy + grants + runbooks |
| #8 | `docs/current-state-section-5-linear-refresh` | Section 5 refresh (test agent) + 4 doc-gap fixes |

## Key architectural principles

1. **Contract-first, runtime-agnostic.** The MVP commits to the CONTRACT (format, schema, location, skill defs, HITL discipline, OTel). The RUNTIME (Hermes / OpenClaw / Cowork / GH Actions / hybrid) is its own future ADR.

2. **ADRs document HUMAN cross-cutting decisions only.** Per-incident agent-handled routine work (CVE triage, on-call alerts, defrag fixes) stays in Linear/source-of-record.

3. **Dual canonical sources for org content:**
   - `wdai-foundation-platform/web/content/*.ts` = canonical for ORG CONTENT (website-rendered)
   - `wdai-marketing/vault/` = canonical for VOICE/TONE (outbound creation)
   - Team-OS mirrors both for turnover-resilience discoverability

4. **Pillar-fill vs pointer-runbook.** Some files are SUBSTANTIVE pillar fills (grants/2026-win-ai-challenge.md, strategy/wdai-mission-and-positioning.md). Others are POINTER-RUNBOOKS that cite canonical sources (operations/runbooks/critical-patterns-index.md, operations/runbooks/mailchimp-cc.md). Both work; pillar-fill where source needs synthesis, pointer-runbook where code/docs stay canonical.

5. **The file IS the runbook.** Per turnover principle: any volunteer reading the maintenance section of current-state.md should be able to update it. Validated via fresh-agent test 2026-05-20 (PR #8) — passed with 4 doc gaps now fixed.

## Single point of failure (FLAGGED)

Helen currently holds:
- Google Workspace admin (sole)
- Slack workspace admin
- Primary Mailchimp admin
- Mailchimp-cc CLI operator
- Linear org admin

**C4 admin access map = HIGHEST priority turnover gap** to dissolve SPOFs.

## Phased roadmap

| Phase | Status | Scope |
|---|---|---|
| **Phase 0** (Week 1) | Active | Backfill 5 platform-side ADRs + scaffolding (gated on Helen ack of ADR-0006) |
| **Phase 1** (Week 2) | Pending | Brigitte writes ADR-0003 (cohort-tag semantics — her own correction; tests non-developer ADR-filing) |
| **Phase 1b** | Pending | Madina runs `/weekly-synthesis` for Granola — tests synthesis-slice |
| **Phase 1c** | ✅ Done 2026-05-20 | Turnover-resilience test — fresh agent updated Section 5, gaps fixed |
| **Phase 2** (Week 3-4) | Pending | Distribute remaining C-series to pillar owners |
| **Phase 2 (skill)** | Pending | C47 `update-current-state` skill (semi-auto maintenance) |
| **Phase 3** (3-6 mo) | Deferred | C48 webhook receivers (Linear, Clerk, GitHub) |
| **Phase 4+** | Deferred | C49 full maintenance agent; runtime selection ADR |

## Cross-references

- **Plan file:** `~/.claude/plans/enchanted-conjuring-fairy.md` (5-iteration refined POC plan, approved 2026-05-20)
- **Design source:** Helen's design doc preserved at `wdai-team-os/docs/design-doc-v1.md` (input not authority)
- **Pass-1 specs:** referenced from log 2026-05-11 — Pass-1 split into subfolder
- **Granola pipeline:** [[infrastructure/granola|Granola infra]] — feeds team-OS via Atlas→Polaris transcript routing
- **Marketing repo voice:** [[organizations/wdai|WDAI org]] — content + vault canonical
- **WIN AI Challenge grant:** $5M ask, currently in review — captured in `grants/2026-win-ai-challenge.md`

## How turnover-resilience gets maintained

Per `current-state.md` Maintenance section:

1. **Per-section triggers** — explicit table (Section 1 → Clerk webhook; Section 2 → inventory-repo scan; etc.)
2. **Forcing functions** — PR template, repo-aware-hook, Polaris weekly Monday check, audit-turnover-resilience (future), update-current-state skill (future C47)
3. **Knowledge transfer** — explicit per-section backup owners + credentials location

## Open questions / waiting on

- Helen ack of ADR-0006 (decision capture conventions) — unlocks Phase 0
- Helen ack of ADR-0007 (tiered autonomy) — unlocks Phase 4+ runtime ADR
- Brigitte availability for Phase 1 pilot (writing ADR-0003)
- C4 admin access map (Helen + Madina session)
- Phase 4+ runtime selection — explicitly deferred until evidence warrants

## Recent activity

- **2026-05-19:** Bootstrapped repo, ADRs 0001-0005, design doc preserved
- **2026-05-20:** Massive session — 22 C-series closures, 5 PRs opened, fresh-agent turnover test passed, maintenance system + value-first hook shipped to Polaris discipline layer
