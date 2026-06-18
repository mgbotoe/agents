---
date: 2026-05-12
type: meeting-extract
source: WDAI Core Team Sync (Granola)
granola_id: 86f237bd-7cb7-4932-8094-eb8c0564a155
routing: technical
participants: Helen, Lauren, Sheena, Brigitte, Rita, Madina, Sandhya (absent)
status: live-transcript-partial
---

# WDAI Core Team Sync — 2026-05-12 — Improvements & Requests

Extracted from the live meeting transcript. Items are **agreed by the group** unless flagged.

## P0 — This week (AI Intermediate launch blockers)

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 1 | **Move AI Intermediate live sessions 10am PT → 9am PT** | Lauren | 10am is a friction point on Thursdays |
| 2 | **Skim Intermediate portal lesson pages** — verify links, suggest missing resources via core team channel | All | Helen's brain switches to AI Advanced next week |
| 3 | **Push Luma → Mailchimp PR live this week** (Madina's PR on the events block) | Helen reviews, Madina merges | Consolidate events into Mailchimp; questions already in PR thread |
| 4 | **Update process doc: course swap = new DB reference number** | Madina | RSVPs are keyed on DB reference number, not slug. Swapping intermediate breaks RSVP state unless re-mapped. Document so it doesn't bite next cohort |
| 5 | **Manual calendar-link injection in MailChimp registration email** → generate via repo instead | Madina | Helen to DM Mailchimp API key |
| 6 | **End-of-week target:** registration state correctly displays on site before Sheena's marketing push | All | Hard date — Sheena gates marketing on this |

## P1 — Before AI Intermediate marketing send

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 7 | **Auto-advance notification email** — when Basics grad is auto-rolled into Intermediate, send "congrats, you've been auto-registered, here's how to opt out" | Sheena (placement TBD) + Madina/Rita (build) | Currently silent → users don't know they're enrolled. Likely fits at the *end* of Helen's basics email sequence |
| 8 | **Pre-event FAQ** — common orientation questions in an email + portal page before live sessions | Sheena drafts | Pulled from past kickoff Q&A; ahead of housekeeping confusion |
| 9 | **Sheena signs up for AI Intermediate** to audit onboarding email flow as a user | Sheena | |

## P2 — Future cohorts (explicit "not now, but on the list")

| # | Item | Notes |
|---|------|-------|
| 10 | **Replace time-based onboarding emails with an onboarding period inside the course** | Root cause of orientation pain — users who register Sun before Mon start miss the Thu/Fri info emails entirely |
| 11 | **Onboarding video** | Helen + Rita acknowledged this last week |
| 12 | **Registration-day-aware email flows** — bundle all onboarding info into one email if user registers <2 days out | Sheena's suggestion |
| 13 | **Cancel-RSVP from the website** | Currently can't; have to do it manually |
| 14 | **"My courses / My RSVPs" consolidated view in member portal** | For people using employer education credits — exportable list of courses taken w/ dates |
| 15 | **WDAI certificate export from saved Reflections** | "Completed X, here are my reflections" — Helen says this is *the* reason she wants Reflections saved. Small post-leadership-training project |
| 16 | **Course content gets a permanent home** outside Helen's local machine | Currently on GitHub but no formal repo; team-OS should write into it |
| 17 | **AI Basics drop-off / community erosion** | Sheena flagged ongoing concern from member conversations. **Tabled** for dedicated session — not this cohort |

## Open / Unresolved

- **Course content repo decision** (#16) — "let's figure it out" was the answer. Needs a follow-up.
- **AI Basics drop concerns** (#17) — group agreed it's real but not solving now.
- **Marketing email "thanks for attending" automation** — group decided **not to build**. Acceptable to lose this when leaving Luma; AI Foundations module surveys cover it.

## Technical items mapped to WDAI code (what already exists)

Verified against `wdai-foundation-platform` @ master.

### #3 — Luma → Mailchimp event swap
**Status: in-flight, already coded.** PR #598 (`content-update/events-cohort-remove-luma`, Brigitte). 18 files. Touches `app/(app)/events/`, `app/(app)/courses/`, `app/api/cohort/register/route.ts`, `lib/rsvp-actions.ts`, `lib/server-data.ts`, new `MailchimpForm.tsx`. I reviewed this 2026-05-09 with 2 must-fix + 2 should-fix findings (memory.md). **Action:** address review findings, merge.

### #4 — RSVP / course reference mapping
**Status: real risk, no code change needed *yet* — but needs a process-doc + likely a one-shot migration helper.**

Current model (`prisma/schema.prisma:589`):
```
CohortRsvp { userId, courseId (Resource.id UUID), cohortDate (Date), ... }
@@unique([userId, courseId, cohortDate])
```

`courseId` is the `Resource` row UUID. `cohortDate` is resolved from human string in `content/product/courses.ts:48` (`'June 8, 2026'` for Intermediate) via `resolveCohortDateForCourse` at `lib/server-data.ts:560`.

Two failure modes when Helen "swaps" Intermediate to the new content:
- **If she creates a new `Resource` row** → new UUID → existing RSVPs orphan. Site shows `userHasRsvp: false` for everyone.
- **If she only changes `cohortDate` in `courses.ts`** ('June 8, 2026' → new date) → RSVPs in DB still keyed on old date → site shows `userHasRsvp: false`.

**Action:** (a) document the swap procedure in a process doc, (b) provide a `scripts/swap-cohort.ts` that takes `(oldCourseId, newCourseId, oldDate, newDate)` and migrates RSVP rows in one transaction. Small — single file, ~50 lines + test.

### #5 — Auto-generate calendar link via repo
**Status: net-new.** Grep'd `web/lib` and `web/app/api` — zero `.ics` / calendar generator code. Currently Madina manually pastes calendar links into Mailchimp templates per cohort.

**Action:** new endpoint `/api/cohort/[courseId]/calendar.ics` that emits an `.ics` file from `courseMarketing[].cohortDate` + `cohortWeeklyCalls`. Mailchimp registration email links to it. ~1 file, ~80 lines.

### #6 — Registration state visible on site
**Status: already built, needs verification post-#598.** `getCourses` at `lib/server-data.ts:577` already returns `userHasRsvp` boolean. `CohortEventCard` already consumes it. The meeting's discussion ("can users visually see they're signed up?") was Sheena not knowing this exists.

**Action:** QA pass after #598 merges to confirm `userHasRsvp` flows correctly through the new Mailchimp path. Not a build task.

### Summary for P0 launch-blockers

| # | Real scope | Effort |
|---|------------|--------|
| 3 | Already coded (#598) — finish review cycle, merge | hours |
| 4 | Process doc + small migration helper script | half-session |
| 5 | New `.ics` route — genuinely net-new | single session |
| 6 | Already built — needs QA verification only | hours |

So **only #5 is real new code**. #3 is in flight, #4 is a script + docs, #6 is verification.

## How to prompt me for this kind of pull next time

> "Pull the latest [meeting name] transcript from Granola and give me a PO-style breakdown: P0 this-week, P1 before-launch, P2 future, plus open/unresolved. Cite owners where the group named one."

That's enough — I'll auto-tier by language cues ("this week" / "before marketing" / "future" / "not today problem"), name owners only where explicit, and flag anything left hanging.
