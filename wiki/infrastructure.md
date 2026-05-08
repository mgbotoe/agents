# Agent Infrastructure

Shared services and onboarding checklist for spinning up new agents in the `C:\Workspace\agents\` monorepo.

## Active Agents

| Agent | Role | Directory | Slack Channel |
|-------|------|-----------|---------------|
| Atlas | Chief of Staff | `chief-of-staff/` | #atlas-cos (C0ASHFXMHM5) |
| Polaris | Tech Lead | `dev-agent/` | #polaris-tl (C0ASYTE8PB4) |

## Shared Services

### Slack Watcher (`C:\Workspace\agents\slack-watcher\`)
Persistent Socket Mode listener. Watches all agent channels, routes messages to the right agent, spawns Claude sessions automatically.

- **Start:** `node watcher.mjs` (or `watcher.cmd`)
- **Add a new agent:** Add an entry to `config.json` — channel ID, agent name, label, and cwd. No code changes.
- **Log:** `watcher.log`
- **Session history:** `sessions/<channelId>.json` (20 messages, 30 min TTL)
- **Bot:** atlas bot in DaFudge workspace (shared across all agents)

### Wiki (`C:\Workspace\agents\wiki\`)
Shared knowledge base. All agents can read and write.
- Atlas owns: people, organizations, decisions, meeting sources, career context
- Polaris owns: technical architecture, ADRs, stack details
- Read `index.md` first, then navigate to relevant pages
- Always update `index.md` and `log.md` after changes

### Inter-Agent Communication
- **Wiki log** (`wiki/log.md`) — permanent record. Use `**AgentName:**` prefix for directed messages.
- **Slack** — notification layer. Post to the other agent's channel when routing work.
- **Granola MCP** — available to all agents via claude.ai account. Pull meeting transcripts by ID.

#### When to Slack (ping the other agent)
Both agents follow the same discipline: Slack is for things that need a response within ~1h. Everything else goes in the wiki log.

**Atlas → Polaris (4 triggers):**
1. Technical decision Atlas can't make (e.g., reviewing a fix in Polaris's code pre-push)
2. Blocking on Polaris's work that's gone stale
3. WDAI meeting transcript routing (automatic, `routing: technical` in frontmatter)
4. Handoff of infra/engineering asks from Dina's meetings

**Polaris → Atlas (tiered by urgency):**

*Same-hour (urgent):*
1. Security / credential incident in code or config
2. About to break shared infra (watcher, scheduler, shared scripts) — preempt her next spawn
3. Dina's explicit "coordinate with Atlas on X" request

*Next Atlas spawn (worst case 6:45 AM MorningBrief — NOT real-time; see limitation below):*
4. Technical transcript review complete — post assessment after reading a routed Granola transcript
5. Operational-impact work shipped (audits, P0s, infra changes, CODEOWNERS, rule edits) — Atlas folds into briefs
6. Non-technical findings surfaced in my lane — person, org, or decision facts I learn from code/PRs/commits
7. Atlas-reported issue resolved — close-loop so she stops re-surfacing it
8. New technical wiki page added — so her briefs can reference

*Do NOT ping:*
- Code details (she doesn't read code)
- Sub-agent raw output — summarize first
- Anything already in wiki/ she can look up
- "Thanks" or status mirrors — silence is fine

*Escalate past Atlas direct to Dina (via `slack_dm_owner`):*
- Security boundary calls
- Money or external commitments
- Cross-`.claude/rules/` conflicts
- Production incidents

**Limitation:** Polaris → Atlas via `#atlas-cos` is **not real-time**. Watcher self-filters polaris-bot posts to prevent loops. Atlas picks up my messages via SessionStart `slack_read` on her next spawn (scheduled tasks at 6:45 AM / 11 AM / 3:15 PM / 10 PM, or whenever Dina sends in-channel). For genuinely urgent traffic, DM Dina directly — don't rely on `#atlas-cos` routing for time-critical signals.

**What stays OFF Slack (goes in wiki log):**
- FYI updates, status summaries, WIP notes
- Anything that doesn't need a response in <1h

**What escalates to Dina directly:**
- Security/safety boundary call
- Money or external commitments
- Anything crossing `.claude/rules/`

**Discipline:** No "thanks for the fix!" acks. No status mirrors. Silence is fine — most of the time agents shouldn't be talking.

#### How messages reach each agent
- **Atlas** auto-watches #atlas-cos on session start + hourly heartbeat reads #polaris-tl since last-seen ts (stored in `chief-of-staff/.claude/runtime/polaris-last-seen.ts`)
- **Polaris** polls wiki/sources/ for `routing: technical` items on session start; also receives watcher-spawned sessions when messages land in #polaris-tl

### Nightly Agent Discussion (`bin/discuss.py` + `.github/workflows/discuss.yml`)

Multi-turn overnight conversation between Atlas and Polaris on a rotating topic (or manual override). No claude.exe, no MCP tools — pure Anthropic API calls. Each agent gets full identity context (CLAUDE.md + SOUL.md + memory) loaded as system prompt per turn.

- **Schedule:** daily at 10:00 UTC (03:00 PT)
- **Topics:** rotated by ISO week from `bin/topics.yml`. Edit freely.
- **Turns:** capped at 5. Either agent can return `NO_RESPONSE` to end the thread cleanly.
- **Output:** transcript at `wiki/discussions/YYYY-MM-DD-<slug>.md`, committed automatically.
- **Manual trigger:** `gh workflow run discuss.yml --repo mgbotoe/agents -f topic="..." -f first_agent=polaris`
- **What agents CAN do:** read repo files (memory, daily logs, code), reference history, propose specific changes
- **What agents CANNOT do:** any MCP tool (no slack_send, no gh, no Granola). They propose; Dina applies.
- **Cost:** ~$0.30/night ceiling at 5 turns, ~10c/turn with Sonnet 4.6.

## New Agent Checklist

When spinning up a new agent:

1. **Create directory** under `C:\Workspace\agents\<agent-name>\`
2. **Create Slack channel** in DaFudge workspace (e.g. #agent-name)
3. **Invite atlas bot** to the new channel
4. **Add to slack-watcher** — add channel entry to `C:\Workspace\agents\slack-watcher\config.json`:
   ```json
   "CHANNEL_ID": {
     "name": "agent-name",
     "label": "Agent Label",
     "cwd": "C:\\Workspace\\agents\\agent-name",
     "description": "What this agent does"
   }
   ```
5. **Restart watcher** — `Ctrl+C` then `node watcher.mjs` (or restart the Windows service)
6. **Create CLAUDE.md** with identity, rules, and wiki access instructions
7. **Create identity files** — `identity/SOUL.md`, `identity/memory.md`
8. **Add to wiki** — update this page's Active Agents table and `index.md`
9. **Add inter-agent protocol** — document which channels the new agent reads/writes in its CLAUDE.md
10. **Test** — post a message in the new channel and verify the watcher routes it correctly

## Workspace Layout

```
C:\Workspace\agents\
  chief-of-staff/    # Atlas — CoS
  dev-agent/         # Polaris — Tech Lead
  slack-watcher/     # Shared Socket Mode listener
  wiki/              # Shared knowledge base
```
