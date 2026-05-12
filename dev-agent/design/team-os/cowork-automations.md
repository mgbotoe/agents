# Cowork Automations Audit

**Headline:** ZERO Cowork-scheduled-task automations exist in any WDAI production repo today.

This is a **major architectural tension** with the team-OS design doc, which proposes Cowork as the federation runtime while no current WDAI production code uses Cowork-scheduled tasks.

---

## What I searched

| Surface | Method | Cowork hits |
|---------|--------|-------------|
| `wdai-marketing` repo | grep | 1 file (README.md, twice — but only as "CC or Cowork session" for ad-hoc interactive use, not automation) |
| `wdai-foundation-platform` | grep | 0 |
| `mailchimp-cc` | grep | 0 |
| `wdai-admin` | sub-agent confirmed | 0 |
| `wdai-lumabot` | sub-agent confirmed | 0 |
| `chief-of-staff` (Atlas) | grep | 0 |
| `dev-agent` (Polaris) | grep | only in our own design/team-os files |
| `wiki/` | grep | 1 file (`2026-04-01-wdai-core-team-sync.md` — Atlas-routed meeting transcript) |

---

## Why no WDAI production code uses Cowork today

The team has, in practice, chosen *other* paradigms for every actual automation:

| Real automation | Paradigm chosen | Why |
|-----------------|-----------------|-----|
| `wdai-marketing` daily Luma sync | Paradigm 4 (GitHub Actions, daily 6am UTC — currently paused) | Lives in repo, deterministic, free, no laptop dependency |
| `course-update-agent` (monthly) | Paradigm 4 (GitHub Actions, 1st of month) | Same |
| `website-content-agent` (monthly) | Paradigm 4 (GitHub Actions, 15th of month) | Same |
| `wdai-admin` AdminBot | Paradigm 2 (Fastify service, always-on) | Slack event listener needs always-on |
| `wdai-admin` weekly-stats | Paradigm 4 (GitHub Actions Fri 17:00 UTC → curl POST endpoint) | Cron without laptop dependency |
| `wdai-lumabot` | Paradigm 2 (Railway, always-on, node-cron) | Slash commands need always-on |
| `wdai-marketing-content-calendar` Slack bot | Paradigm 4 (GitHub Action posting via webhook) | Reads repo state, posts on cron |
| `WDAI Newswire` welcome bot | Paradigm 4 (event-driven, infra-hosted) | Channel-join event triggers |
| Helen's morning briefing | Paradigm 3 (Gumloop daily flow) | Existed before Cowork |
| Helen's Syl + Pattern + Wit agents | Paradigm 1 (OpenClaw on Mac mini, NOT Cowork) | OpenClaw was Helen's earlier choice |
| Madina's Atlas + Polaris | Paradigm 1 (OpenClaw on Windows) | Same |
| Madina's `promote.yml` + `discuss.yml` | Paradigm 4 (GitHub Actions cron, after migrating off local Task Scheduler) | **Madina explicitly moved AWAY from local-laptop scheduling toward cloud cron** |
| Atlas scheduled scripts (morning-brief.ps1, midday-check.ps1, friday-wrap.ps1, decay.cmd) | Windows Task Scheduler (paradigm-1-equivalent) | Predates the cloud-cron migration |

**Pattern recognition:**
- Anything that needs to be reliable has moved to paradigm 2 (always-on) or paradigm 4 (cloud cron)
- Anything Cowork-style remains paradigm 1 (Mac mini OpenClaw — close cousin to Cowork, but vendor-lock different)
- Madina's migration from Windows Task Scheduler to GitHub Actions cron is the explicit direction-of-travel
- Helen herself is using Cowork as a *tool to edit OpenClaw configs* (per topic-openclaw, May 9) — not as a runtime

---

## The Cowork limitation that drives this

Cowork scheduled tasks have a documented constraint:

- **Desktop-bound.** Jobs only fire while Claude Desktop is running and the computer is awake. A closed laptop at 7 AM means the morning brief waits until you open it.
- **Permission "Always allow" can regress.** After a Claude Desktop update or occasionally on its own, scheduled runs re-prompt for folder/tool approval and silently stall.

These are the operational reasons why nothing serious in WDAI runs on Cowork today. Helen has personally cited both in #topic-openclaw discussions.

---

## Open architectural question surfaced (deferred to Pass 3)

**The federation runtime question:**

| Option | Pros | Cons |
|--------|------|------|
| **A. Cowork-only** (Helen's doc) | Familiar UX, single client | Laptop-bound, permission-regress risk, won't run if Brigitte/Lauren/Sheena close their laptops, vendor-lock to Anthropic |
| **B. Mixed paradigms** (current reality) | Each automation picks the right runtime — Cowork for interactive, GitHub Actions for reliable cron, Railway for always-on | Federation contract is harder; multiple runtimes to maintain |
| **C. Cloud-cron-only** (Madina's direction-of-travel) | Reliable, no laptop dependency, free, code-defined, version-controlled | Requires GitHub literacy from every contributor; no "drop something in a Slack channel" inbox primitive |
| **D. Hybrid: Cowork for capture + cloud cron for synthesis** | Capture phase is interactive (Cowork fits), synthesis is unattended (cloud cron fits) | Two systems to teach; per-paradigm onboarding overhead |

**Madina's working answer (per existing setup):** Option D in practice — Atlas/Polaris have local OpenClaw tasks for interactive work, GitHub Actions for unattended automations (promote.yml, discuss.yml). The current WDAI direction supports D.

**Recommendation:** the team-OS spec should explicitly name the runtime per layer, not collapse to "Cowork everywhere." Capture can be Cowork OR cloud cron OR Gumloop, depending on the contributor's existing tooling. The contract is the **output format** (frontmatter, file naming, branch + PR convention), not the runtime.

---

## Bonus finding: `perplex_computer/` is NOT Cowork — it's Perplexity Computer

The `C:\Workspace\Women Defining AI\perplex_computer\` folder contains three text files that I initially assumed might be Cowork notes. They're not. They're **Perplexity Computer "Space" definitions** — a sixth paradigm:

| File | Size | What it is |
|------|------|------------|
| `setup-recovery.md.txt` | 2.6KB | Recovery procedure for an oncall agent setup |
| `space instruction.txt` | 5.5KB | "Devops Space — Instructions" for an oncall agent. Lists read-only API credentials: Stripe, Supabase, PostHog, Vercel, GitHub, Sentry |
| `wdai-oncall-skill-bundle.md.txt` | 44.7KB | The skill bundle code — a `wdai-oncall-engineer` skill for Perplexity Computer |

**Perplexity Computer** = a separate Anthropic-competitor platform that hosts agents in cloud "Spaces" with bounded credential access. Helen mentioned testing it Mar 20 to build "a data pipeline." This `perplex_computer/` folder is Helen's evaluation artifact, not a deployed agent.

**Paradigm 6 (Perplexity Computer Spaces) joins the list:**
1. OpenClaw desktop (Helen Mac mini, Madina Windows)
2. Production microservices (wdai-admin Fastify, wdai-lumabot Railway)
3. SaaS workflow agents (Gumloop)
4. Cloud cron / GitHub Actions
5. Slack Workflow Builder (Educational Content - Reminder)
6. **Perplexity Computer Spaces (oncall agent, evaluated not deployed)**

Plus member-built personal Slack apps (Akshita's Assistant, etc.) which technically span paradigms 2 and 3.

---

## Open questions

1. **Does Helen want the team-OS spec to require Cowork specifically, or is "Cowork-style local-runtime" acceptable?** The pattern (scheduled tasks, identity files, skills folder, manual run-now bootstrap) matters more than the specific Anthropic-product label.
2. **The 2026-04-01 core team sync transcript** in `wiki/sources/` has one Cowork mention. Worth pulling to understand the team's actual Cowork posture from that meeting.
3. **For paradigm-2 services (admin/lumabot), is there a federation hook?** Both are always-on; could they double as the "consolidator" agent layer Helen describes?
4. **`perplex_computer/wdai-oncall-skill-bundle`** — Helen's stalled Perplexity Computer eval. Port to wdai-team-os skill, or abandon?
