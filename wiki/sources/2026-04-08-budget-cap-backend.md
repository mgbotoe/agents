---
name: Budget Cap & Backend Update — LBS
source_type: transcript
meeting_type: team-sync
date: 2026-04-08
tags: [danaher, lbs, budget, infrastructure, gpu, github-migration, san-diego]
participants: [Madina Gbotoe]
---

# Budget Cap & Backend Update — LBS

Informal team sync at LBS San Diego covering infrastructure budget, AI development projects, GitHub migration, and company policies.

## Infrastructure Budget

- $600K allocated for infrastructure upgrades in 2026
- Currently $150K short of desired hardware purchases
- Need 25 GPUs for server rack, 10 new motherboards
- GPU licensing: $5K/year per GPU (Nvidia virtualization requires Enterprise licensing)
- Team exploring Nvidia SaaS as alternative to hardware ownership
- SSD issues: moving from Seagate rebrands to Samsung 990s for reliability
- Manufacturing floor has RTX 4090s/5090s potentially available for reallocation
- RAM prices doubled in Q1, affecting upgrade plans

## AI & Development Projects

- **SAM backend rebuilt** with versioned API support — SOAP (V1) and JSON RESTful (V2)
  - Hundreds of unit tests comparing old vs new backend
  - Chris (architect) to review after additional testing
- **Local LLM deployment options:**
  - Raspberry Pi with AI hat for simple use cases
  - Mac Studio clustering (5 units = 2.5TB RAM total) for larger workloads
- **GitHub migration:** team wants to move from BitBucket to GitHub Enterprise for static code analysis, AI tools, better integrations

## Company Policies

- Badge scanning/office presence monitoring increasing — management tracking in-office vs remote
- Team frustrated with inconsistent enforcement across departments
- Team worked 24/7 on-call for 6 months during recent product launch — tension between delivery expectations and office presence requirements

## Compliance & Documentation

- TPS reports transferred from Jean — combines FDA guidance with Danaher licensing requirements
- 6-month documentation cycle for releases
- FDA submission feedback expected — IQC footprint may be too small
- Server room fire suppression only sprinklers (inadequate for servers) — exploring off-site data center

## Facilities

- Manufacturing floor expansion needed for CS5
- Considering acquiring neighboring building; food bank building ($17M) previously declined

## Key Sources

- [[sources/2026-04-08-ai-code-review-strategy|AI Code Review Strategy (Apr 8)]]
- [[sources/2026-04-08-robot-arm-recap|Robot Arm Recap (Apr 8)]]
- [[sources/2026-04-09-github-migration-planning|GitHub Migration Planning (Apr 9)]]
