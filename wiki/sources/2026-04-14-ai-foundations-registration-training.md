---
name: AI Foundations Registration Flow & Training Strategy Review
source_type: transcript
date: 2026-04-14
meeting_type: team-sync
participants: [Madina Gbotoe, Josh (EAI), Martin Kang]
tags: [danaher, wdai, ai-foundations, github-copilot, lbs, training]
granola_id: 212c8663-6b50-4508-8934-f5e22f82ff8d
---

# AI Foundations Registration Flow & Training Strategy Review

Two-topic meeting: (1) EAI team debrief on LBS on-site training in San Diego, and (2) WDAI AI Foundations registration flow redesign.

## Part 1: LBS On-Site Training Debrief (Danaher / EAI)

### Training Outcomes
- ~13 developers + 4-5 SQA roles + 1 PM attended in San Diego
- LBS has separate leadership across San Diego, Thai, Melbourne, Shanghai — each with their own R&D structure
- Melbourne team is advanced — already has VPs with full permission/budget to experiment with AI
- Shanghai also knowledgeable; they plan to set up their own discussion group starting next week

### Key Feedback from Developers
- **"You're not meeting us where we are"** — direct feedback from developers
- Many developers don't use GitHub and find GitHub Copilot limiting
- Some developers are secretly using other AI tools (Claude Code, Cursor, etc.) because GitHub Copilot doesn't meet their needs
- Developers want more tools validated and brought in-house, not a one-size-fits-all approach
- First day was too much lecture, not enough hands-on
- Trainer kept saying "that's my secret sauce" when asked about agent swarming — frustrating

### Strategic Implications
- **Power user identification:** Martin suggested sending a broad email about a Claude Code pilot — people who volunteer are the power users
- Cursor pilot precedent: found power users because they self-selected into it
- Training vendor relationship: not delivering expected value; options are (1) work tightly with vendor, (2) bring training in-house, (3) try new vendor, (4) give opcos budget to self-source training
- Martin leaning toward AI kaizen model: week-long events with real projects + on-site trainer, not lecture format
- Virtual classrooms with Microsoft launching in ~1 week — could handle intro-level content

### Decisions
- Will explore Claude Code pilot as power-user discovery mechanism
- Need to reassess training vendor approach before rolling out to more opcos
- 510(k) clinical trial work done with Copilot worth capturing as a win, even if small

## Part 2: WDAI AI Foundations Registration Flow

### Current Problem
- Registration happens through a Google Form that's disconnected from the member portal
- No automated flow connecting sign-up to cohort placement to email sequences
- Manual work by Lauren to manage cohort membership

### Proposed Flow
- Registration form integrated into the member portal (members-only access = security built in)
- Form collects: name, email, cohort preference (live vs self-paced)
- MailChimp tags drive automated email sequences based on cohort enrollment
- Cutoff for joining a live cohort: ~3 days after start (after that, wait for next cohort or self-pace)
- When cohort fills or starts, form automatically switches to waitlist mode

### Registration UX Decisions
- Sales page in member portal with cohort info + registration form
- Self-paced content always available via portal link
- Live cohort has specific dates displayed on the page
- Form dates/tags updated manually between cohorts (minimal lift)

### Facilitator Training Program
- 4-week alpha training for facilitators to lead AI Foundations open calls
- Targeting people who've completed curriculum + raised their hand for mentoring
- Time commitment matches mentoring commitment (~1-2 hrs/week) — acts as a filter
- Lauren has short list of candidates
- Separate from general volunteer onboarding (which is step zero, not yet built)

### Metrics & Data
- Helen wants registration flow changes reflected in metrics tracking
- Historically WDAI hasn't looked at data much — shifting to data-informed
- Need to track sign-ups, cohort completion, re-registration rates

### Action Items
- [ ] Build sales page in member portal branch (deadline: Saturday morning)
- [ ] Drop-dead deadline for all testing: Wednesday Apr 22
- [ ] Iron out cohort cutoff rules (3-day window proposal)
- [ ] Update MailChimp tags/automation for new flow

## Cross-References
- [[projects/ai-foundations|AI Foundations]]
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
- [[people/martin-kang|Martin Kang]]
- [[organizations/wdai|Women Defining AI]]
- [[organizations/danaher|Danaher]]
