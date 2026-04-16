---
name: AI Integration for Code Reviews — LBS Strategy Session
source_type: transcript
meeting_type: strategy
date: 2026-04-08
tags: [danaher, lbs, ai, code-review, scanner, automation, testing, cybersecurity, indica]
participants: [Madina Gbotoe]
---

# AI Integration for Code Reviews — LBS Strategy Session

Deep strategy session with LBS software team in San Diego covering AI-assisted code review, automated testing infrastructure, software architecture, cybersecurity, and revenue model challenges.

## AI-Assisted Code Review

- Goal: use AI for code reviews by end of 2026
- Challenge: scanner operates at sub-micron precision — AI review still requires human understanding of accuracy requirements
- No single team member has complete workflow mapping of all device workloads
- Need to stop outsourcing AI analysis to partners — bring in-house for recurring revenue (charge 2X cost)

## Automated Testing Infrastructure

- **Robot arm project (Ozan):** proof-of-concept completed but gear burned out; titanium replacement considered
- Alternative: use existing scanner mechanisms (travel/gripper) on lazy Susan — cheaper actuators already in warehouse
- Proposed: 24/7 stage movement testing, automated rack loading/unloading for burn-in testing
- Goal: eliminate FSE overnight presence requirement
- Current gap: 6 months chasing ghost problem from duplicated daughter boards (Elite project)

## Software Architecture

- **ICE interface replacement:** only need scanner shutdown/restart functions; backwards compatibility concern for Studio UI
- **SSD deployment strategy:** pre-configured SSD swapping (5-min installs) vs current manual FSE process; $300/SSD cost concern
  - Alternative: Cronus field flashing capability now available
- **PXE install system (Sean):** phone-based VPN certificate connection, automated image pulling, 5GB base GDI vs 30GB full clone

## Cybersecurity & Update Process

- Need regular security patch releases with automated update detection
- Customer-configurable update rules by severity level
- No proper version control SOPs currently followed
- Need quarterly CR release process implementation

## Indica Partnership & Revenue

- 49% ownership stake acquired
- 250+ part numbers for different software packages/algorithms
- Forced sales/marketing to view software as revenue vehicle
- Physical scanner limitations approaching (light/glass constraints)
- AI/robotics making market entry easier for competitors
- All device revenue currently goes to hardware side — fighting organizational resistance to software monetization

## Team Management

- 23 team members with diverse experience
- Risk of overcommitment (repeat of last year)
- **Nikolai scope limitation:** minimal MVP (compression job, LBS SDK import only), 1-2 month timeline, solo work — let him pursue ambitious goals after core delivery

## Key Sources

- [[sources/2026-04-08-budget-cap-backend|Budget Cap & Backend Update (Apr 8)]]
- [[sources/2026-04-08-robot-arm-recap|Robot Arm Recap (Apr 8)]]
- [[projects/github-copilot-adoption|GitHub Copilot Adoption]]
