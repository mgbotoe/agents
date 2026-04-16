---
name: AI Tools Training — Interactive Session Planning
source_type: transcript
meeting_type: demo/workshop
date: 2026-04-08
tags: [danaher, lbs, ai-training, copilot, san-diego]
participants: [Madina Gbotoe]
---

# AI Tools Training — Interactive Session Planning

Post-session debrief at LBS San Diego during the [[projects/github-copilot-adoption|GitHub Copilot]] training week (Apr 7-10). Focused on improving training format and building an interactive polling tool for Day 2.

## Training Feedback

- Format too lecture-heavy for mixed audience — participants wanted hands-on interaction throughout
- Visual/kinesthetic learners need "doing" not watching; examples felt too complex to follow along
- Day 2 plan: more interactive examples + dedicated afternoon for 1-on-1 problem solving (test generation, documentation, agent creation)
- Ideal format: 2-3 week embedded sprint per team, not a 2-day firehose
- Madina glad to participate despite developer focus; got VS Code access for better follow-along

## Interactive Polling Tool

- Building custom quiz/polling system for audience engagement during training
- Separate questions from main slides — participants access quiz independently
- Real-time synchronization forces follow-along; shows participant count + vote tracking
- Implementation options considered: VM hosting, DNS alias to laptop, Vercel (chosen as fallback — pure anonymous, nothing proprietary)
- Previous experience: built similar tool in 30 min with Lovable, but replicating internally proved harder

## AI Usage Observations

- Used AI for test case generation with limited working code — fed requirements only, got surprisingly aligned output
- AI most valuable for making mundane work less tedious and organizing thoughts
- Chris reviewed AI-generated test cases to ensure completeness

## Key Sources

- [[sources/2026-04-10-eai-workshop-debrief|EAI Workshop Debrief (Apr 10)]]
- [[sources/2026-04-10-lbs-ai-tools-pulse|LBS AI Tools Pulse (Apr 10)]]
