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
