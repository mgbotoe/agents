---
title: "Rebekah <> Helen / Madina — Analytics & Technical Roadmap"
date: 2026-04-15
attendees: [Madina Gbotoe, Helen Kupp, Rebekah Leslie-Hurd]
source: granola
granola_id: af29dfea-1b7d-4067-a144-e33585896595
routing: technical
---

# Rebekah <> Helen / Madina — Analytics & Technical Roadmap

**Apr 15, 2026 | 8:30–9:15 AM PT | Google Meet**

## Summary

Deep dive review of WDAI's analytics infrastructure (PostHog), community value gaps, and technical roadmap planning. Rebekah (new WDAI volunteer, ex-Slack analytics) completed a PostHog audit. Helen framed two strategic community gaps. Madina pushed for staging environment and proper SDLC before scaling contributor access.

## Key Decisions

- **End of April target:** PostHog analytics cleanup and dashboard familiarization
- **After analytics:** Set up dev/staging environment for team onboarding
- **After staging:** On-call engineering agent work (Q2/Q3)
- **Rebekah gets WDAI email + PostHog admin access** — activated during call
- **Rebekah gets GitHub write access** to platform repo
- **Bridget also gets GitHub write access** — needs PR approval gates first
- **Branch protection with PR approval gates is urgent** — currently missing on platform repo (only MailChimp repo has it)
- **Code owners file needed**

## Analytics Infrastructure

- Significant PostHog tracking already exists but not all utilized
- Duplicate events (e.g., resources clicked from dashboard vs resources page)
- Manual dashboard runs weekly on Mondays — covers MailChimp, portal signups, cancellations, Slack onboarding, course metrics
- Missing: Slack instrumentation, some Luma events data
- Proposal: pare down to core metrics first, then build up based on questions each pillar wants answered
- Need analytics skill/check in CI process — flag gaps in logging when new features are built

## Community Value Gaps (Helen)

1. **Discovery gap:** Members don't know about programs beyond AI Foundations (study groups, recordings in portal)
2. **Peer connection gap:** When members find peers with shared interests, magic happens (super moms channel, Cloud Code study groups) — often leads to volunteering. Hard to engineer but worth pursuing.

## Technical Roadmap Items

- Dev/staging environment — **Madina's top priority before scaling team access**
- Branch protection + PR approval gates on platform repo (urgent)
- Code owners file
- Analytics CI skill (flag missing instrumentation on PRs)
- On-call engineering agent (Helen's Q2/Q3 vision) — incident manager that reviews errors, logs patterns, flags drift weekly, eventually creates PRs
- PostHog error tracking cleanup to feed the agent

## Rebekah Context

- Ex-Slack analytics team — dealt with engineers shipping features without instrumentation
- Bandwidth is "bursty" — big chunks then quiet periods. Responds well to deadlines.
- Prefers analytics project over feature work (less time-dependent)
- Will partner with Madina on technical roadmap (Helen's explicit ask)
- Sinus surgery Monday Apr 20 — next sync in ~2 weeks

## Action Items

- [ ] Madina: Forward PostHog error emails to Rebekah
- [ ] Madina: Set up technical roadmap (analytics → staging → on-call agent)
- [ ] Helen: Add PR approval gates + code owners file to platform repo
- [ ] Rebekah: Send calendar availability for next check-in (~2 weeks)
- [ ] Rebekah: Explore PostHog dashboards once access is granted

## Polaris Note

This meeting is tagged `technical`. The technical roadmap (staging env, branch protection, CI analytics skill, on-call agent) is in Polaris's lane. Pull full transcript from Granola ID `af29dfea-1b7d-4067-a144-e33585896595` for deeper context.
