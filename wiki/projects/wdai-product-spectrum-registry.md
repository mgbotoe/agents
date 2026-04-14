---
name: WDAI Product Spectrum Registry
org: wdai
type: tool
status: active
tags: [wdai, product-management, cpo-tooling, registry]
participants: [Madina Gbotoe, Helen Kupp]
---

# WDAI Product Spectrum Registry

Google Sheet tracking all products, tools, and automations being built across WDAI.

## Link
https://docs.google.com/spreadsheets/d/1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw/edit

## Origin
Helen asked Dina for a one-slide prioritization framework during their Mar 30 1:1 ([[sources/2026-03-30-madina-helen-1on1|transcript]]). Dina built this sheet instead — a living registry with spectrum placement, scoring, ownership, and decision tracking. Created Apr 6, 2026.

## Structure
| Column | Purpose |
|--------|---------|
| Product | Name of the project/tool/automation |
| Builder | Who's building it |
| Slack Handle | Builder's Slack handle |
| Spectrum | 🟢 Standalone / 🟡 Middle Ground / 🔴 Deeply Integrated |
| Value Tier | High / Medium / Low |
| Score | 1-8 (or 1-10 for standalone) |
| Recommended Action | Build it / Claim it / Partner / Roadmap Q3+ |
| Status | Active — [substatus] |
| Decision Needed | What Dina/Helen need to decide |
| Notes | Context, history, sightings |
| Source URL | Slack thread or URL where it was found |
| Date Added | When first detected |
| Last Seen | Most recent activity |
| Run Count | How many times it's been spotted |

## How It Gets Fed
- Manually by Dina scanning Slack (original method)
- Automated via [[projects/wdai-product-signal-detector|Product Signal Detector]] (/scan-slack skill)

## Access
- GDrive account: `nonprofitcd`
- File ID: `1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw`

## Related
- [[projects/wdai-product-signal-detector|Product Signal Detector]] — automated pipeline feeding this sheet
- [[sources/2026-03-30-madina-helen-1on1|Madina <> Helen 1:1 (Mar 30)]] — origin conversation
