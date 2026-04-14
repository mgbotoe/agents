---
name: wdai-qualification-rules
description: Qualification rules for WDAI Build Radar. Use when deciding whether a
  Slack message or project qualifies for the WDAI registry. Contains channel naming
  conventions, hard qualification criteria, and connection strength scoring.
---

## Critical Distinction
Sharing something IN a WDAI Slack channel is NOT the same as
building something FOR WDAI. Most posts are personal — do NOT
qualify. Only track something explicitly connected to WDAI
operations, platform, or community.

## Connection Strength — Apply This First
Not all WDAI connections are equal. Score the connection:

STRONG (register it)
- Built explicitly for WDAI by core team
- Built for WDAI by a community member on request
- Builder explicitly says "this is for WDAI"

MEDIUM (register as standalone, resources page max)
- Built personally, then formally offered to WDAI members
- Shared at a WDAI session as a resource for members to use

WEAK (catch-all only, do not register)
- Built personally, shared at a WDAI session but not offered
- Personal repo shared after a program session
- Only WDAI connection is the channel or event it appeared in

## Personal Repos Shared at WDAI Sessions
If someone shares a personal GitHub repo during or after
a WDAI program session:
- Connection strength = MEDIUM at most
- Always classify as 🟢 Standalone — never 🔴 or 🟡
- Recommended action = "Feature on resources page" at most
- Only register if builder explicitly offers it to WDAI members
- If not explicitly offered → catch-all only, do not register

## Channel Conventions
#gig-* → ALWAYS qualify. Auto-qualifies. Skip standard filter.
#programs-* → Qualify tools/builds made for the program.
#team-* → High signal. Apply standard rules carefully.
#aifoundations-* → Qualify if explicitly made for the program.
#topic-* → Standard rules. Explicit WDAI connection required.
#share-* / #general / #random → Strictest. Skip unless explicit.

## Hard Qualification Rules
Qualifies ONLY if AT LEAST ONE is explicitly stated:

✅ Builder says it is FOR WDAI, the portal, or a WDAI program
✅ Builder asks if it should live in portal or be offered to members
✅ Core team member (Helen, Madina, Lauren, Brigitte, Sandhya,
   Rho, Karen, Hannah) explicitly flags it as WDAI
✅ Built AS PART OF a named WDAI program (Build TogetHER,
   AI Foundations) — not just shared at one
✅ Being formally offered to WDAI members as a resource
✅ Posted in a #gig-* channel (auto-qualifies)

❌ SKIP: Personal projects with no WDAI mention
❌ SKIP: Tools shared as inspiration or "look what I made"
❌ SKIP: Personal repos shared at sessions but not offered
❌ SKIP: Articles, links, content (not builds)
❌ SKIP: Only WDAI connection is the channel it was posted in

When in doubt → SKIP, not include.

## Catch-All (Nothing Gets Lost)
Log in Doc "Reviewed but not added" if ANY:
- Posted in #gig-* but WDAI tie unclear
- Personal repo shared at a WDAI session (not explicitly offered)
- Core team member shared or reacted to it
- Mentions portal, WDAI platform, or community in any way

Format:
👀 Reviewed but not added:
- @[handle] — [one sentence] · #[channel] · 🔗 [link]
  Reason: [one sentence]

## Date Filter — Critical
Only surface messages where the ORIGINAL post date is within
the current search window. Discard results where the original
message is older than the window even if the thread has
recent replies. Always check message timestamp not thread
timestamp.
