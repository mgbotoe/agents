---
name: wdai-registry-updater
description: Updates the WDAI Product Spectrum Google Sheet registry. Use when adding
  new items, updating existing rows, archiving disqualified items, or restoring archived
  items to the active registry.
---

## Sheet Details
ID: 1Gz50sLZ_b6asCjU6D7-BqhFjlaK_A11oYWN6RTe8arw
Tab 1 = Active Registry
Tab 2 = Archived (never delete from here)
Tab 3 = Dashboard (update every run)

## Row Format (Tab 1 and Tab 2)
Product | Builder | Slack Handle | Spectrum | Value Tier | Score | Recommended Action | Status | Decision Needed | Notes (one sentence) | Source URL | Date Added | Last Seen | Run Count

Tab 2 also has: Archive Note | Archive Date

## Before Writing Anything
1. Search Tab 1 by product name → if found, UPDATE row in place
2. If not in Tab 1, check Tab 2 → if found, apply Resurrection Rule
3. Only if not found anywhere → add as new row

## Run Count
Increment by 1 each time this item appears in a scan.
This is the archive threshold counter.

## Archive Rule
Move Tab 1 → Tab 2 only if ALL are true:
- Run Count reaches 4 with no confirmed WDAI connection
- Builder never mentioned WDAI in same context
- Clearly personal with no community angle
- No core team member flagged it

Archive Note format: "Archived [date] — [reason in one sentence]"
NEVER delete rows. Always move to Tab 2.

## Resurrection Rule
If a Tab 2 item resurfaces with confirmed WDAI connection:
- Move row from Tab 2 back to Tab 1
- Status = "Restored — awaiting Madina confirmation"
- Add to Notes: "Restored [date]. Previously archived [date]."
- Do NOT create a new row — restore the existing one
- Flag in Slack digest as 🔄 Returning item

## Dashboard Tab 3 (update every run)
Row 1: Total active items
Row 2: Total archived
Row 3: Items needing decision
Row 4: Deeply Integrated count
Row 5: Middle Ground count
Row 6: Standalone count
Row 7: Unclear count
Row 8: Last run date
Row 9: Next run date
