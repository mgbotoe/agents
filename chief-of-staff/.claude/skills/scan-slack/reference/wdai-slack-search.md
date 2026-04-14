---
name: wdai-slack-search
description: Efficient WDAI Slack search for Build Radar. Use for all scans. Lists
  all accessible channels, filters by prefix to ensure blanket coverage, then reads
  each channel for qualifying content. Prevents missed channels and ensures consistency
  every run.
---

## Why This Approach
Slack Search scope (search:read) is unavailable in Gumloop.
Instead: list ALL channels first, filter by prefix, then
read each one. This ensures blanket coverage every run
including any new channels created since last run.

## Step 1 — List All Accessible Channels
Call the Slack list_channels tool to get every channel
the bot has access to. Do this at the start of every run.

## Step 2 — Filter by Prefix
From the full channel list, keep ONLY channels that start
with any of these prefixes:

#gig-              → always include (auto-qualifies)
#team-             → always include
#programs-         → always include
#aifoundations     → always include
#topic-            → always include
#infra-            → always include
#ops-              → always include
#share-            → always include
#wdai-             → always include
#general           → always include
#random            → always include

Also always include these specific channels regardless
of prefix:
- #general
- #random
- #wdai-leaders-training

Skip everything else unless it is a known WDAI channel
not covered by these prefixes.

## Step 3 — Read Each Filtered Channel
For each channel in the filtered list:
- Read messages from the last 4 days (regular run)
- Read messages from date range (backfill run)
- Check original message timestamp — discard anything
  older than the search window even if the thread has
  recent replies. Always check message timestamp not
  thread timestamp.

## Step 4 — Apply Qualification Rules
Apply wdai-qualification-rules to every message found.

For each qualifying result capture:
- Full Slack handle (@handle) — NEVER first name only
- Channel name
- Direct permalink URL to the original message

Only read a specific thread deeper if you need more
context AFTER finding a qualifying signal there.

## Coverage Note (include in every output)
After scanning report:
- Total channels accessible via list
- Channels scanned by prefix filter
- Any channels the bot could not access (not_in_channel)
- New channels discovered this run vs last run
- Canvas scanning: limited — manual flags only

## New Channel Alert
If a new channel matching any watched prefix appears
that was not in the previous run's coverage list
— flag it in the Slack digest:
📌 New channel detected: #[channel-name] — now being monitored
