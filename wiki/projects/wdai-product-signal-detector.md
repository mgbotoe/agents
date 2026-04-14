---
name: WDAI Product Signal Detector
org: wdai
type: tool
status: spec-draft
tags: [wdai, slack, product-management, automation, cpo-tooling]
participants: [Madina Gbotoe]
---

# WDAI Product Signal Detector

## What This Is

A Slack watcher that continuously scans WDAI channels for signals that someone is building a product, tool, or automation. It classifies what it finds by **relevance** (personal vs. WDAI) and **maturity** (ideation → in progress → deployed), then surfaces the right things to Madina at the right time.

This is the automated version of how the [[projects/wdai-product-spectrum-registry|Product Spectrum Registry]] was initially populated — manual Slack scanning. The goal is to make the CPO function scalable without Madina reading every channel.

## Origin

Helen and Madina's March 30 1:1 ([[sources/2026-03-30-madina-helen-1on1|transcript]]) defined the CPO-like role: own the framework for categorizing projects on the spectrum (standalone → deeply integrated), prioritize them, and staff them. The registry sheet was the first deliverable. This bot is the pipeline that feeds it.

## Signal Detection Criteria

### What triggers detection

A message is a **build signal** if it contains any of:

| Signal Type | Examples |
|------------|---------|
| **Deployed URL** | Lovable, Vercel, Render, Netlify, GitHub Pages, Replit links |
| **Repo link** | GitHub/GitLab repo shared in channel |
| **Build language** | "I built", "I made", "check this out", "here's what I created", "shipping this", "just deployed" |
| **Demo request** | "can I demo", "want to show", "Show Don't Tell submission" |
| **Automation mention** | "Gumloop workflow", "Zapier", "n8n", "Claude agent", "automation I set up" |
| **Tool pitch** | "this could help with", "what if we used this for", "should we integrate" |
| **Helen/Madina tag** | A leader explicitly asks Helen or Madina to look at something |
| **Gig channel activity** | New messages in `#gig-*` channels (these are project workgroups by definition) |

### What is NOT a signal

- General discussion, questions, articles shared
- Course reflections or lesson completions
- Event RSVPs or scheduling
- Bot-generated messages (Wit, Pattern, Newswire, etc.)

## Relevance Filter: WDAI vs. Personal

### WDAI-relevant (track it)

- Built *for* WDAI or its members
- Uses WDAI infrastructure (portal, Slack workspace, GitHub org, mailchimp-cc)
- Solves an org problem (ops, engagement, content delivery, member experience)
- Someone explicitly pitches it for integration or asks where it should live
- A leader tags it for review
- Built in a `#gig-*` channel (these are org workgroups)

### Personal (don't track in registry)

- Built for personal/family use (meal planner, daycare tracker, personal finance, etc.)
- No mention of WDAI, members, or the org
- Shared as "look what I learned" — celebrating skill growth, not pitching a product
- Lives entirely outside WDAI systems with no integration intent

### Gray zone → track quietly

- Someone builds a personal tool, then says "hey this could work for members too"
- A personal project uses WDAI-taught skills and the builder suggests adapting it
- **Rule:** If it starts personal but gains WDAI context in a later message, reclassify it

## Maturity Classification

### Ideation 💭

**Signals:** "what if we", "wouldn't it be cool if", "has anyone thought about", "I was thinking we could", brainstorming threads, feature requests

**Bot behavior:**
- Log it silently (who, what channel, date, summary)
- Do NOT surface to Madina yet
- Track repeat mentions — if the same idea appears **3+ times** across different people or channels, escalate to "emerging"
- Track time — if someone revisits their own idea after 2+ weeks, they're still thinking about it → escalate

### Emerging 🌱

**Signals:** Repeat ideation (3+ mentions OR revisited after 2 weeks), someone claims they'll build it ("I'm going to", "I'll take this on"), early wireframes or mockups shared

**Bot behavior:**
- Surface to Madina as a low-priority awareness item
- Include: who, what, channel, mention count, first seen date

### In Progress 🔨

**Signals:** WIP screenshots, "working on", shared code snippets, progress updates, "almost done", Lovable/Replit project links (not deployed yet)

**Bot behavior:**
- Surface to Madina as a medium-priority item
- Suggest initial spectrum placement based on context
- Include: who, what, channel, how long they've been building, any integration mentions

### Deployed 🚀

**Signals:** Live URL shared, "it's live", "just deployed", demo video, "go try it"

**Bot behavior:**
- Flag to Madina immediately as high-priority
- Needs spectrum placement + decision: standalone resource, partner build, claim it, or build into portal
- Include: who, what, URL, channel, audience

## Repeat-Mention Escalation Logic

Ideas that keep coming up are real demand signals.

```
mention_count = 1       → log, do nothing
mention_count = 2       → still log, still nothing
mention_count >= 3      → escalate to "emerging"
  - UNLESS all mentions are from same person in same channel
    (that's one person thinking out loud, not org-wide demand)
  - IF mentions span 2+ channels or 2+ people → stronger signal
different_people >= 3   → auto-escalate regardless of count
time_since_first > 14d AND revisited → escalate
```

## Output

### Where signals go

1. **Primary:** Discord notification to Madina (via Atlas) with a structured summary
2. **Secondary:** Append to the Product Spectrum Registry Google Sheet (new row, status = "Detected", needs Madina review)
3. **Tertiary:** Weekly digest — roll up of all signals from the week, grouped by maturity

### Signal notification format

```
🔍 Product Signal Detected

Project: [name/description]
Builder: [who] in #[channel]
Maturity: [💭 Ideation | 🌱 Emerging | 🔨 In Progress | 🚀 Deployed]
Relevance: [WDAI ✅ | Gray zone ⚠️]
First seen: [date]
Mentions: [count]
URL: [if applicable]

Suggested spectrum: [🟢 Standalone | 🟡 Middle Ground | 🔴 Deeply Integrated]
Decision needed: [yes/no — what decision]
```

### Weekly digest format

```
📊 WDAI Product Signals — Week of [date]

🚀 Deployed (needs decision): [count]
  - [project] by [who] — [one-line]

🔨 In Progress (awareness): [count]
  - [project] by [who] — [one-line]

🌱 Newly Emerging: [count]
  - [idea] — [mention count] mentions across [channels]

💭 Ideation (logged, not actionable): [count]

📈 Trending: [ideas gaining momentum]
```

## Spectrum Auto-Classification Heuristics

The bot should suggest a spectrum placement, not decide it. Heuristics:

| Signal | Suggested Spectrum |
|--------|-------------------|
| Uses WDAI API, portal, or database | 🔴 Deeply Integrated |
| Built by core team member or leader | 🔴 Deeply Integrated (if it breaks, we own it) |
| Standalone URL, no WDAI system dependencies | 🟢 Standalone |
| Gumloop workflow connecting WDAI systems | 🟡 Middle Ground |
| Resource/tool that could be linked from portal | 🟡 Middle Ground |
| Community member's personal build pitched for WDAI | 🟢 Standalone (until decision to integrate) |

**Helen's Q4 Rule** (from transcript): If Helen or a core team member built it and it touches WDAI systems → it's 🔴 by default, because if it breaks, the core team owns it whether they meant to or not.

## Channels to Monitor

Priority channels (most signal):
- `#gig-*` (all gig channels — project workgroups)
- `#ops-website`
- `#share-demos`
- `#general` (occasional build announcements)

Secondary channels:
- `#leaders-*` (training cohort channels)
- `#ai-advanced` (technical members building things)

Ignore:
- `#intros` (onboarding, not builds)
- `#events` (scheduling, not builds)
- Bot-only channels

## Technical Notes for Dev Agent

- WDAI Slack workspace already has bot infrastructure (Wit, Pattern, Newswire)
- The registry lives at: https://docs.google.com/spreadsheets/d/1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw/edit
- Output to Madina goes through Discord (Atlas channel)
- Consider whether this runs as a new bot or as a capability added to an existing one (Wit or Pattern)
- Slack API: use conversations.history + events API for real-time
- LLM classification (Claude) for ambiguous signals — relevance + maturity judgment calls
- Google Sheets API for registry updates

## Open Questions (for Madina + Helen)

1. Should this bot have its own Slack identity or run silently under Wit/Pattern?
2. Should it post detected signals back into a dedicated Slack channel (e.g., `#product-radar`) for transparency, or keep it private to Madina?
3. How often should the weekly digest run — Sundays (for Helen prep) or Mondays (for the week)?
4. Should community members know their builds are being tracked? Transparency vs. surveillance optics.
5. Does Helen want access to the signal feed too, or should everything go through Madina first?
