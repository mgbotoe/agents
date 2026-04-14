---
name: wdai-digest-format
description: 'Formats and posts the WDAI Build Radar digest to #infra-radar in Slack.
  Use at the end of every live run to send the formatted summary. Do NOT use for dry
  runs or backfill runs.'
---

## When to Post
POST: live runs (!radar run or Wednesday/Friday schedule)
DO NOT POST: dry runs, backfill runs, !radar summary

## Digest — When Items Found

🛠️ *WDAI Build Radar — [Day, Date]*

Here's what surfaced since the last run:

*[Project name]* · @[handle] · #[channel]
[One sentence on what it is]
📍 [spectrum] · 📊 [value tier] ([score])
💡 [recommended action]
🔗 [direct permalink to original message]
⚡ Madina to decide: [decision — omit if none]

[Repeat per confirmed item — max 6 total]

---
🔄 *Returning items:*
- *[Project]* · @[handle] · #[channel]
  Previously archived — resurfaced this run.
  📍 [spectrum] · 📊 [value tier]
  🔗 [link]
  ⚡ Madina to confirm: restore or keep archived?
[Omit entire section if no returning items]

---
❓ *Worth a closer look:*
- @[handle] — [one sentence] · #[channel] · 🔗 [link]
[Omit entire section if catch-all is empty]

---
📡 *Coverage this run:*
Channels scanned: [list]
🔒 Private: [list or "none"]
⚠️ No access: [list or "none — full coverage"]
Canvas scanning: limited — manual flags only

💬 Miss something? Drop it in #infra-radar.

## Digest — Nothing Found

🛠️ *WDAI Build Radar — [Day, Date]*
No new WDAI-associated builds surfaced since the last run.

📡 *Coverage this run:*
Channels scanned: [list]
🔒 Private: [list or "none"]
⚠️ No access: [list or "none"]
Canvas scanning: limited — manual flags only

💬 Building something for WDAI? Drop it in #infra-radar.

## Formatting Rules
- Bold project names with *asterisks*
- Full @handles always — never first name only
- Direct permalink for every item
- Plain Slack formatting only — no markdown headers
