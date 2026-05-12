# Pass 1 · Drive context (deltas surfaced 2026-05-12)

> **Status:** Drive read 2026-05-12 · Confidence: **high for primary-source quotes** (Helen's 3Y vision · Madina's planning quote · Brigitte's Drive SOP · contributor onboarding doc) — all sourced from named Google Docs with view URLs.

**What this file is:** context surfaced by reading WDAI's Google Drive that strengthens or corrects claims elsewhere in Pass 1. Pass 1 was built primarily from Slack + repo audits; Drive is the parallel knowledge layer that Pass 3 must also account for.

**What this file is NOT:** the team's project tracker. Q2 Priorities, partnerships, fundraising, grant applications, content-calendar logistics — out of scope. Pass 1 documents current state, not in-flight work.

---

## 1. The 3-year North Star (formalized 2026)

WDAI's strategic frame, from `WDAI_Living_Strategy_Doc.docx` + board pre-read (Feb 17 board meeting):

**By end of 2029:**
- **10,000 cumulative learners** (from ~1,500 today — a ~6.7× scale)
- **7 regional hubs** (from 3 today)
- **Open-source playbook** published for field-wide adoption
- **Sustainable funding model** beyond any single grant

**Four strategic priorities (the decision filter):**
1. **Scale learner reach** — partner channels, digital-first
2. **Build the Learner-to-Leader Flywheel** — learner → builder → mentor → instructor
3. **Operational infrastructure** — "systems that compound, not just grow"
4. **Funding & sustainability**

**Why this matters for Pass 3:** the team-OS isn't an engineering luxury — it's strategic priority #3, named verbatim ("systems that compound") in the 3Y vision. Every Pass 3 federation decision should be testable against "does this compound, or just grow?"

---

## 2. Madina's 2026-planning quote — the team-OS thesis, verbatim

From `WDAI Core Team Meeting: Running Agenda` (2026 Planning Notes section):

> **Madina:** Migrate critical assets from Helen's personal accounts into shared, tiered access (Helen space → middle ground → open access)
>
> **Madina:** Put guardrails on permissions now while the team is small enough to do it cleanly
>
> **Madina:** Continue stabilizing the website/portal and automation work already underway

This is the **Q7 federation thesis pre-stated** months before Pass 1 was written. The "tiered access" model (Helen-space → middle-ground → open-access) is Madina's proposal; Pass 3 must decide whether to adopt that tiering as the contract or design something different.

---

## 3. Helen's stated 2026 transition vs current behavior (the Q1 paradox)

**Helen wrote (Feb 6 Personal Operating Manual):**
> "What I will need to do more of in 2026 and beyond is lean on all of you more, and shift my focus away from tinkering and more towards nonprofit leadership and stewardship which in 2026 will be nearly entirely focused on finding sources of funding for the org."

**Helen's observable behavior (May 2026):**
- Overhauling AI Intermediate curriculum from ground up (5/5 meeting: "Helen is generating the content")
- Personally reviewing `mailchimp-cc` PRs as recent as May 11
- Sitting with title placement decisions in real-time
- Operating Newswire / AdminBot / Course Reflections via code she authored
- Still primary recipient of all support emails
- Still primary on-call human responder

**The gap is the design constraint.** Pass 3 cannot build the team-OS around stated-intent Helen. It must build for current Helen — who still tinkers — and create the conditions that make stated-intent Helen possible. Removing operational load is a precondition for the role transition, not a consequence of stating intent.

This pattern matches Madina's tiered-access proposal (#2 above): you can't shift Helen out of "Helen space" if there's no "middle ground" or "open access" to shift work into.

---

## 4. Cohort registration migration off Luma — mid-flight

Verified via 5/12 + 5/5 + 4/28 + 4/14 Core Team meeting notes + Q2 Priorities sheet:

**State as of 2026-05-12:**
- `/courses` page: **Mailchimp forms successfully replaced Luma** for cohort registration. AI Basics May 4 cohort used the new flow. Q2 sheet status: "on track."
- `/events` page: **Brigitte PR open** to replace Luma here too. Not yet shipped.
- Brigitte built/tested members-can-stop-cohort-emails-without-unsubscribing functionality.
- Direct quote (5/5): *"Mailchimp forms have successfully replaced Luma for the majority of registrants."*

**Pass 1 impact — diagrams to mentally adjust until updated:**
- `02-process-flows.md` "Member signup" sequence: Stripe → Platform path is current; Luma reads are stale for cohort registration (still current for events)
- `02-process-flows.md` "Cohort kickoff" `/new-basics` skill: still accurate for the skill itself; the upstream registration is now Mailchimp-driven
- `01-system-context.md` L1: Luma is still a valid external (events) but is shrinking in surface area
- `03-operational-architecture.md` external risk register: Luma's blast-radius is contracting

**Open dependency:** Brigitte explicitly stated she'd need "Mailchimp API access and someone to help me with the database coordination" to do cohort-end-date tagging programmatically. That's the next-step ask, not yet resolved.

---

## 5. AI Intermediate launches 2026-06-08 with curriculum overhaul

From 5/5 + 4/28 meeting notes:

- **Date:** June 8, 2026 kickoff
- **Curriculum change:** moving FROM "customGPTs" TO "3 weeks of understanding what AI agents are and building your own chief of staff in various platforms: Claude or OpenAI projects, Claude Cowork, Gumloop or ChatGPT workspace agents"
- **Learning goals (Helen verbatim):**
  1. Understand what makes an agent different + the differences between agent tools (Cowork vs ChatGPT agents vs OpenClaw etc.)
  2. Have built at least one of their own + feel empowered by the simplicity
- **Helen's content timeline:**
  - Structure + narrative by May 8 (script, slides, recorded demos)
  - Final videos by May 14
  - QA + page reviews May 15-18
- **External commitments derived from this content:** Helen presenting live "60-min workshop format" of this on 5/27 + 5/28 to Glue Club + Off The Record communities.

**Pass 1 impact:**
- `course-update-agent` (in `wdai-foundation-platform`) currently knows the OLD AI Intermediate structure. The 1st-of-month autonomous PR may attempt to update lessons against the legacy structure unless its content snapshot reflects the overhaul. → cross-check on June 1 run.
- `WDAI_Content_Calendar` sheet (Drive) still lists June 8 as "Build a customGPT (Part 2)" — content calendar lags curriculum overhaul. Sandhya owns this; correction expected.

---

## 6. Newsletter cadence — monthly Issues

From `WDAI_Content_Calendar` (Drive):

- **Issue 1:** April 4 — welcome + April programming overview
- **Cadence:** monthly Issues, owned by marketing pillar (Sandhya / Sheena drafts).
- **Sections (consistent template):** From the Editor · Event/Spotlight · Resources & Reads · Community Q&A
- **Distribution:** Mailchimp campaigns.

**Pass 1 impact (lightweight):** the newsletter is one of the ~5 member-facing entry points already in 02's member-surface map, but the explicit monthly Issue cadence wasn't captured. Adds nuance to what "Mailchimp emails" means as a touch point — it's not just transactional cohort emails, it's also a curated monthly community digest.

---

## 7. The `#get-help` Q&A capture bot

Verified via `Get-Help WDAI Knowledge Base` (Helen-owned, modified May 8):

- **Section title in doc:** "Pending Review — New Q&A Candidates"
- **Source line:** *"These Q&A pairs were auto-captured from #get-help by the support bot. They are NOT part of the official KB yet."*
- **4 weekly batches visible:** 2026-04-22, 2026-04-24, 2026-05-01, 2026-05-08
- **Format:** each Q&A includes original asker, answerer, Slack permalink, asked-date
- **Behavior:** "The bot ignores everything in this section when answering questions." → implies the bot ALSO answers questions in the channel, not just captures.

**Not in `bot-registry.md`.** Paradigm unconfirmed — Gumloop is the most likely host given Helen's pattern of single-Slack-identity-many-flows, but the actual flow definition is not audited.

**Pass 1 impact:**
- Add to bot-registry as a new entry (paradigm TBD)
- Add to `01-system-context.md` finding #27 (already done in this commit)
- Treat as evidence that Helen has BEEN BUILDING federation primitives quietly — the support bot does exactly what Pass 3's "agents propose, humans approve" needs at the knowledge-layer level (auto-capture + tiered review-before-promotion).

---

## 8. The tiered-access Drive architecture already exists (Brigitte SOP, Mar 12)

This is the most material finding for Q7. Madina's verbatim "Helen space → middle ground → open access" proposal **is already implemented at the Drive layer.** From `Intro to our shared Drives` (Brigitte-authored SOP in `SOPs/` folder, dated 2026-03-12):

**Existing structure:**

| Tier | Drive | Who has access | What lives there |
|------|-------|----------------|------------------|
| **Helen / leadership** | `Women Defining AI Org` shared drive | Core team only | Board Materials · Grant Applications · Core team folder · Helen's in-flight work |
| **Open access / volunteers** | `Volunteer Resources` shared drive | All `@womendefiningai.org` volunteers (auto-granted on email provisioning) | Guidance · resources · marketing materials · templates · per-pillar folders (Marketing, AI Foundations, etc.) |

**GWorkspace user groups (Brigitte set up):**
- `coreteam@womendefiningai.org` — email + share target for core team
- `volunteers@womendefiningai.org` — email + share target for all volunteers

**Cross-drive pattern:** shortcuts (not copies) from volunteer drive into leadership drive resources, with **explicit per-folder/document permission grants**. The Logo + Brand Assets folder is the documented example — lives in leadership drive, shortcut in volunteer drive, Viewer permission at folder level.

**SOP convention:** "It's signed and dated — please do that for any SOPs you create. We don't need to be rigid, but we do need to know who to ask when we have questions." → light-weight decision-author tracking at the SOP level.

**Why this matters for Pass 3:**
- Madina's tiered-access thesis is NOT a greenfield design ask — it's an extension of an existing Drive primitive across the GitHub + Slack + agent layers
- The "middle ground" Madina mentions corresponds to **the Core team folder inside the leadership drive** (core-team-only, but distinct from Helen-only working stuff)
- A federated team-OS could plausibly use the **GWorkspace user-group ID** as the identity primitive — every contributor already has a `@wdai.org` email tied to a group; the same identity can scope GitHub access, Slack channel membership, and agent provisioning
- Pass 1's prior framing ("no shared tiered access exists") was wrong at the Drive layer; correct at the GitHub layer (CODEOWNERS only in platform); correct at the Slack layer (channels are member-led, not tiered)

---

## 9. The `/commit` skill is the platform-side Q4 volunteer onboarding primitive

From `New volunteer / Github and systems onboarding` (Apr 2026, v0.1 draft — `Volunteer Onboarding` folder):

**The codified contributor flow** for `wdai-foundation-platform`:

1. **One-time setup:** Node.js LTS · Git · Claude Code (terminal) · IDE choice (VSCode / Cursor / Antigravity)
2. **Repo clone + `npm install`** in `/web/` subfolder (the doc explicitly flags the nested-folder gotcha)
3. **`.env.local` from 1Password** — shared via 1Password by Helen or Madina, manual-paste (the doc flags a quirk: 1Password mangles section-header formatting, contributor must re-add `#` to comment lines)
4. **Vercel team access** — "View Only" member, email must match GitHub email
5. **Test accounts** — `member@test.com` / `leader@test.com` (passwords in-doc; test-tier creds, not prod)
6. **Make changes** → run `/commit` slash skill
7. **PR review** — Helen or Madina reviews, Vercel preview link auto-attached, iterate on same branch/PR

**The `/commit` skill itself** lives in `.claude/skills/commit-workflow` in the repo (already audited in Pass 1). It automates:
- Lint
- Typecheck
- Stage changes
- Generate commit message
- Push to GitHub
- Open PR
- Auto-loop on test failures until passing

**This is the parallel Q4 primitive to `mailchimp-cc`'s tiered model:**

| Repo | Q4 onboarding primitive | Risk tier |
|------|-------------------------|-----------|
| `mailchimp-cc` | Runbooks → `.claude/skills/` → source code (per `CONTRIBUTING.md`) | Tiered by file path |
| `wdai-foundation-platform` | `/commit` skill abstracts ALL git operations; volunteers never run individual git commands; checkout flow is explicitly out-of-bounds | Tiered by capability (skill-level only) |

**Pass 1 corrections:**
- `01-system-context.md` Q4 framing should add platform's `/commit` skill alongside mailchimp-cc — there are TWO working references for Pass 3, not one
- The "platform contributor doc" (v0.1, April 2026) is itself a **federation primitive being built right now** — Helen and Madina are codifying the volunteer-onboarding contract while Pass 1 is being written
- **1Password is verified** as the password-manager-of-record (downgrade to "tool unverified" in earlier audit was over-cautious — correcting in this commit). 1Password is used manually-pasted, NOT via CLI/secret-injection integration

**What this surfaces about Helen's behavior:** Helen authored `wdai-foundation-platform/CLAUDE.md` (36KB), the `/commit` skill, AND this v0.1 onboarding doc. The volunteer-Github-onboarding pipeline is HER deliberate Q4 design — Pass 3 inherits a working reference, not a greenfield ask.

---

## 11. The Drive layer Pass 1 underweighted

Pass 1 was built from Slack + repos. Drive carries a parallel knowledge layer that should be treated as a first-class container in Pass 3's federation design:

**Categories observed:**
- **Strategy:** `WDAI_Living_Strategy_Doc` + `Living Strategy & Decisions Document — Q2 2026`
- **Meeting cadence:** `WDAI Core Team Meeting: Running Agenda` (live, weekly) + `Weekly Claude Code/Github with Helen` notes (Gemini auto-captured) + Biweekly Programs Sync
- **Personas:** `WDAI Core Team: Personal Operating Manuals` (the source `05-people-and-process.md` now cites)
- **Knowledge:** `Get-Help WDAI Knowledge Base` (the doc that hosts the support-bot pipeline)
- **Marketing:** `WDAI_Content_Calendar` + `April 2026 Advanced Cohort Promo Plan` + `AI_Basics_Promotion_Plan_May4_Cohort`
- **Madina's CPO work:** `CPO — Product & Infrastructure` folder with `Product Radar Registry`, `Product Spectrum`, `Build Signals — Historical` — separate parallel knowledge architecture
- **Programs:** `Biweekly Programs Sync` (Lauren-owned) · `WDAI Certified Learning Facilitator` (Lauren-owned, 162KB) · `AI Foundations Mentor Guide` (Lauren-owned)

**Q6 implication:** Granola transcripts AND Gemini auto-notes AND Otter recordings (4/1 meeting transcript link) AND live-doc agendas ALL coexist as meeting-context surfaces. Multiple synthesizers, no shared output sink, no dedup contract.

---

## What Pass 1 should NOT inherit from this delta

- Q2 Priorities sheet contents — that's a project tracker, not state-of-the-system documentation
- WIN Grant detail — fundraising context, not federation scope
- Board composition (Elena, Ailian, Nichole) — board exists; not relevant to Pass 1's operational system framing
- Partnership conversations (Girls Inc., Lean In, WellFed) — strategic but out of operational scope
- Volunteer tier proposal (T1/T2/T3) — proposed by Sandhya, not yet adopted
- WDAI UK chapter mechanics — member-led infra, out of team-OS scope per existing finding #24

Pass 3 may pull any of these in if its design needs them. Pass 1 does not.
