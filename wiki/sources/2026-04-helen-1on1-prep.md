---
name: Helen 1:1 Prep — April 2026
source_type: meeting-prep
date: 2026-04-13
tags: [wdai, helen, 1on1, product-strategy, prep]
---

# Helen 1:1 — Agenda

## Pre-read for Madina
- [[projects/wdai-product-spectrum-registry|Product Spectrum Registry]] (Google Sheet)
- [[sources/2026-03-30-madina-helen-1on1|Last 1:1 transcript (Mar 30)]]
- [[projects/wdai-product-signal-detector|Signal Detector spec]]

---

## 1. Present the Registry as the Framework (5 min)

You owed Helen a one-slide prioritization framework. You built something better — a living registry with spectrum placement, scoring, ownership, and decisions.

**Walk Helen through:**
- The spectrum model (🟢 Standalone → 🟡 Middle Ground → 🔴 Deeply Integrated)
- The scoring system (how you ranked 1-8)
- The "Decision Needed" column — this is where you need her input

**Ask:** Does this format work as our recurring anchor, or does she still want a slide version?

---

## 2. Top 5 Decisions — Need Helen's Input (15 min)

Sorted by score. Don't try to cover all 17 — these are the ones that need a call.

### Customer Support Email Bot (8/8)
- Helen's rebuilding the automation from scratch
- **Decision:** Set a deadline for the rebuild? Assign a documented runbook?
- **Your POV:** Yes to both. This is core infrastructure with no backup.

### PostHog Analytics (7/8)
- Rebekah has deep codebase understanding, actively implementing
- **Decision:** Is Rebekah formally the technical lead for portal instrumentation?
- **Your POV:** Yes — she's already doing the work. Formalize it.

### Meet → Vimeo Pipeline (7/8)
- Helen is sole maintainer. No backup.
- **Decision:** Document as owned infrastructure + assign backup maintainer?
- **Your POV:** This is a bus factor risk. Need at least one other person who can touch it.

### BadgeBot (7/8)
- April 23 Show Don't Tell is 10 days away
- **Decision:** Should this be integrated into the portal before the demo? Who owns the technical handoff?
- **Your POV:** Come in with a recommendation — integrate or demo as standalone?

### Weekly Member Dashboard (7/8)
- Pattern posting weekly, Helen monitoring daily
- **Decision:** Should this become the official leadership dashboard?
- **Your POV:** Yes — it's already being used that way informally. Make it official.

---

## 3. Bus Factor / Ownership Cleanup (5 min)

Helen's name is on 7+ items in the registry. That's not sustainable.

**Frame it as:** "Here's what I'm seeing in the registry — you're the sole owner or maintainer on these. Which ones do you actually want to keep, and which should we find someone else for?"

Items where Helen is sole owner with no backup:
- Customer Support Email Bot
- Meet → Vimeo Pipeline
- Leaders Training Site
- Mailchimp-cc
- Slack Auto-Invite
- Google Meet Event Tool

**Ask:** Can we use the Leaders Training graduates as a bench for some of these?

---

## 4. Product Signal Detector — Pitch (5 min)

You've been manually scanning Slack to populate the registry. That doesn't scale.

**Pitch:** "I want to build a bot that watches Slack for build signals — someone sharing a URL, a demo, a repo, a 'what if we built X' — and classifies it by relevance and maturity before surfacing it to me."

**Open questions for Helen:**
1. Should signals go to a public Slack channel (like `#product-radar`) or stay private to you?
2. Does Helen want access to the signal feed, or should everything flow through you first?
3. Should community members know their builds are being tracked? (transparency vs. surveillance optics)

---

## 5. Action Items Checkpoint (2 min)

### From Mar 30 (overdue):
- [x] Build prioritization framework → done (registry sheet)
- [ ] Meet with Brigitte to map website/portal structure before pulling in others

### New items from this call:
- [ ] (capture during meeting)

---

## Tone Notes

Helen values strategic thinking. She wants to see *your* point of view, not a menu of options. Come in with recommendations on every decision item and defend them. That's the strategy practice she's giving you.

Don't try to be comprehensive — be decisive. Better to make 3 strong calls than present 17 items with no opinion.
