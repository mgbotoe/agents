---
name: heartbeat
description: Proactive check-in with pre-gathered context. Run automatically via Task Scheduler every 30 minutes.
---

Proactive heartbeat — gather context first, then reason.
Adapted from unclaw (github.com/shahshrey/unclaw).

1. **Gather context** (deterministic, no reasoning yet):
   ```powershell
   powershell -ExecutionPolicy Bypass -File .claude/scripts/gather-context.ps1
   ```

2. **Check #atlas-cos inbox since last seen.** Read `.claude/runtime/atlas-last-seen.ts` (single-line Unix timestamp). **If the file doesn't exist, create it with current UTC Unix seconds** (`powershell -Command "[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()" > .claude/runtime/atlas-last-seen.ts`) and skip the rest of this step this run — there's no backlog to process on first bootstrap. Otherwise, call `mcp__polaris-slack__slack_read` on channel `C0ASHFXMHM5` and look for messages with `ts > atlas-last-seen.ts`. Process any Atlas-authored messages directed to Polaris (replies to my pings, cross-posted acks, etc.). After reading, write the newest message `ts` back to `.claude/runtime/atlas-last-seen.ts` so subsequent heartbeats skip what's already processed. Mirrors Atlas's `polaris-last-seen.ts` pattern — symmetric polling closes the real-time gap in the Polaris→Atlas direction where the watcher can't spawn me on my own bot's posts.

3. **Read the output** and assess:
   - Is memory stale (>48 hours)? -> **critical**, update immediately
   - Are there new wiki inbox items from Atlas? -> review them
   - Is the slack-watcher alive? If NOT RUNNING -> **critical**, notify Dina
   - Are there pending/follow-up items with passed or imminent deadlines?
   - Are there uncommitted changes that have been sitting for a long time?
   - Is disk space running low?
   - Are any scheduled tasks NOT FOUND?
   - Any patterns in today's log that suggest an unfinished thread?
   - Any recent runtime errors?

4. **Act** based on what you find:
   - If memory is stale -> update `identity/memory.md` with current state from daily logs
   - If wiki inbox has items -> read and review them (mark as reviewed when done)
   - If slack-watcher is dead -> notify Dina via `slack_dm_owner` (can't restart it yourself)
   - If there are urgent pending items -> send a notification and summarize what needs attention
   - If scheduled tasks are missing -> log warning, notify Dina
   - If nothing needs attention -> do nothing (don't generate output for the sake of it)

5. **Only notify if something is actionable.** Silent heartbeats are good. Don't be noisy.

## Rules
- **Never send unsolicited Slack messages unless something is genuinely actionable.** "Everything is fine" is not a message.
- **Never modify code or make commits.** Heartbeat monitors and flags — it doesn't fix code.
- **Never run for more than 2 minutes.** If an action is complex, log it as a TODO and exit.
- **The gather-context script is the single source of truth.** Don't run additional checks beyond what the script provides. If you need more checks, update the script.
- **Memory staleness is the #1 priority.** If memory is stale, update it before anything else.
- If the slack-watcher is flaky, check `.claude/runtime/scheduled-tasks.log` before escalating.
