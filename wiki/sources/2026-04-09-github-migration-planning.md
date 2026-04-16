---
name: GitHub Migration Planning — LBS Team Discussion
source_type: transcript
date: 2026-04-09
meeting_type: team-sync
participants: [Madina Gbotoe, LBS team (Keith, Anish, Ty, others)]
tags: [danaher, lbs, github, bitbucket, perforce, migration, devops]
granola_id: 4f0a83d4-2ebe-4fed-ab62-01ca1c5915a4
---

# GitHub Migration Planning — LBS Team Discussion

Informal discussion among LBS team members about the state of their source control and the possibility of migrating to GitHub. Captured during the San Diego on-site week.

## Current State — Three Places for Code
1. **Perforce** — legacy; never fully migrated out of it
2. **BitBucket** — scanner team moved here without asking; now validated through QA/quality process
3. **GitLab** — backup only; has ~5-year-old version of SAM stuff; can be shut down

## Migration Challenges

### Validation Blocker
- QA validated BitBucket as part of Git validation — the usage procedure heavily references BitBucket
- Moving to GitHub would require re-validation (or leverage Melbourne's existing GitHub validation)
- This is a quality/regulatory concern, not a technical one

### Enterprise Coordination Gap
- "Enterprise just needs to pick a lane" — frustration with lack of clear direction
- Different opcos have different tech stacks, products, and customers → hard to standardize
- KPI measurement is contentious: whatever KPI you pick penalizes something else
- No coordination outside opco boundaries, and limited within

### Copilot Metrics Discussion
- Enterprise tracks Copilot usage but metrics can be "gamed" — running scans after merge makes individual commits look clean
- Hard to compare one org to another meaningfully
- Team wants to correlate AI spending with P4G (productivity) improvements but can't make the connection yet

### Sustaining Activities Proposal
- Proposal: dedicate 30% of time (one day/week) to sustaining — vulnerability review, customer issues, tech debt
- First month of "sustaining day" could be spent building agents to automate the burn-down
- Need to be transparent about cost so leadership understands the investment

## Staffing Notes
- Discussion about product manager hiring and travel requirements
- "Must be on-site" mandate means more PMs needed for coverage
- Ukraine contractors mentioned as alternative to hiring junior staff
- Tension between "go to gemba" philosophy and distributed team reality

## Cross-References
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
- [[sources/2026-04-10-eai-workshop-debrief|EAI Workshop Debrief]]
- [[organizations/danaher|Danaher]]
