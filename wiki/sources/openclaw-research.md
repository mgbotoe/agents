---
name: OpenClaw Research
source_type: research
date: 2026-04-12
tags: [agent, framework, research]
---

# OpenClaw Research

## What Is OpenClaw

OpenClaw (formerly Clawdbot/Moltbot) is the dominant open-source personal AI agent framework in 2026. MIT-licensed, 163K+ GitHub stars, 200+ contributors, 5,700+ community skills.

- **Repo:** https://github.com/openclaw/openclaw
- **Docs:** https://docs.openclaw.ai
- **Website:** https://openclaw.ai

It runs as a persistent daemon on your machine, connects to 20+ messaging platforms (Telegram, Discord, WhatsApp, Slack, Signal, iMessage, WeChat, etc.), and takes autonomous action on your behalf: shell commands, browser automation, email, calendar, file operations.

## Architecture

Five-component design with clean separation of concerns:

### 1. Gateway
Always-on process that routes messages from channels (Telegram, Discord, WhatsApp, Slack, etc.) through a single config file. Handles protocol normalization so the brain never thinks about transport.

### 2. Brain (Agent Loop)
ReAct reasoning loop: call LLM, execute requested tools, feed results back, repeat until done. Supports Claude 4, GPT-4o, Gemini 2.0, DeepSeek V3. Structured tool definitions let the AI decide when to act.

### 3. Memory
Multi-tiered, file-based (Markdown):
- **T0 — SOUL (Identity):** Immutable personality/boundaries. Human-authorized changes only.
- **T1 — Core Memory (Evergreen):** MEMORY.md and memory files. Always loaded.
- **T2 — Episodic:** Daily logs, session history.
- **T3 — Semantic/Vector:** Chunked (~400 tokens, 80-token overlap), embedded, stored in SQLite with optional sqlite-vec acceleration. Hybrid retrieval: `finalScore = vectorWeight * vectorScore + textWeight * textScore` (BM25 keyword + vector similarity). Temporal decay with 23-day half-life.

### 4. Skills
Human-authored Markdown files loaded from workspace, personal, shared, or plugin scopes. ClawHub marketplace hosts 5,700+ community skills. Portable format.

### 5. Heartbeat (Scheduler)
Periodic agent turns in isolated sessions. The agent wakes up, runs scheduled tasks, goes back to sleep. Uses `isolatedSession: true` to avoid sending full conversation history (~100K down to ~2-5K tokens per run). This is OpenClaw's most distinctive feature — the agent is proactive without being prompted.

## Permission & Security Model

- **Three-tier permission gates** for sandboxed agents: agent-level tool allow/deny, sandbox-level tool filter, Docker network access.
- **Tool policy precedence** (later overrides earlier): Tool Profile > Provider Profile > Global Policy > Provider Policy > Agent Policy > Group Policy > Sandbox Policy.
- **Docker sandboxing:** Agents can be isolated in containers. Network disabled by default. Sandbox tool policy is separate from agent tool policy.
- **Sender filtering:** DM senders and group members treated as untrusted by default.
- **Known weakness:** 469 open security issues as of April 2026. SECURITY.md explicitly lists prompt injection as out of scope. Sender filtering is channel-level, not group-level.

## Ecosystem

| Project | What it does |
|---------|-------------|
| [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) | 162 production-ready agent templates with SOUL.md configs |
| [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | 5,400+ curated skills from the official registry |
| [openclaw-mission-control](https://github.com/abhi1693/openclaw-mission-control) | Multi-agent orchestration dashboard |
| [OpenPersona](https://github.com/acnlabs/OpenPersona) | Four-layer AI persona framework (Soul/Body/Faculty/Skill) |
| [SoulClaw](https://github.com/clawsouls/soulclaw) | Soul-driven agent framework with 4-tier memory and 80+ personas |
| [clawskills.sh](https://clawskills.sh/) | Curated skill discovery |
| [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) | Train agents by talking to them |

## Competitors / Alternatives

| Framework | Differentiator |
|-----------|---------------|
| **NanoClaw** | Lightweight (~5K LOC), container isolation, minimalist philosophy. Still requires API key. |
| **Hermes** | Self-improving skills, serverless deployment, safer defaults. |
| **Claw Code** | Clean-room Python/Rust rewrite of Claude Code architecture. 48K+ stars. Coding-focused. |
| **Vellum** | Ironclad security, persistent memory, native macOS desktop control. Credentials never touch the model. |
| **Claude Managed Agents** | Anthropic's first-party solution. Managed infrastructure, no self-hosting. |

---

## UnClaw — What Atlas Is Built On

Atlas is built on **UnClaw** (https://github.com/shahshrey/unclaw), a "zero-framework" approach that runs inside Claude Code itself.

### UnClaw's Core Thesis
> "The best AI agent framework is the one you delete."

Third-party harnesses (OpenClaw, NanoClaw) cannot use Claude Max/Pro subscriptions — they hit the API directly at $$$+/month. UnClaw runs inside Claude Code, using your existing subscription at zero additional cost.

### How UnClaw Works
- **Zero lines of runtime code.** Markdown files, shell scripts, and a Python indexer. Claude Code is the only process.
- **Config as architecture.** `SOUL.md` = personality. `CLAUDE.md` = operating system. `memory.md` = brain. `.claude/rules/` = guardrails. `.claude/skills/` = capabilities.
- **Three-layer memory:** hot (always loaded, <2500 tokens) / cold (searched on-demand) / raw (daily logs, SQLite FTS5 indexed).
- **Self-improvement:** Nightly review of skills, rules, and hooks.
- **Multi-agent via directory isolation:** Clone the repo per role. Each gets its own identity, skills, rules, memory, security, and Telegram bot.

### UnClaw vs OpenClaw

| Dimension | OpenClaw | UnClaw |
|-----------|----------|--------|
| Cost | API usage ($$$) | $0 — uses Max subscription |
| Runtime | Custom Node.js harness | Claude Code (no custom runtime) |
| Lines of code | ~500K | 0 (markdown + shell) |
| Dependencies | 70+ npm packages | None |
| Maintenance | High | Near zero |
| Memory | Built-in multi-tier | Hot/cold/raw with FTS5 |
| Messaging | 20+ channels | Telegram (more via MCP) |
| Self-improvement | No | Yes — nightly refinement |
| Multi-agent | Single runtime, shared config | Full directory isolation |
| When Claude Code updates | Wait for harness patch | Nothing breaks |

---

## Gap Analysis: What Atlas Is Missing vs OpenClaw

### Features OpenClaw Has That Atlas Lacks

1. **Multi-channel messaging gateway.** OpenClaw supports 20+ channels from a single config. Atlas only has Telegram (via MCP plugin) and Discord (via MCP). No WhatsApp, Slack, Signal, iMessage, or others.

2. **Vector/semantic memory search.** OpenClaw chunks memory into embeddings with hybrid BM25+vector retrieval and temporal decay (23-day half-life). Atlas uses SQLite FTS5 keyword search only — no semantic similarity, no decay weighting.

3. **Docker sandboxing.** OpenClaw can isolate agents in containers with granular network and tool policies. Atlas relies on Claude Code's built-in sandbox only.

4. **Granular permission tiers.** OpenClaw has a 7-layer tool policy stack (Tool > Provider > Global > Provider > Agent > Group > Sandbox). Atlas has a simpler ask/allow/never model.

5. **Community skill marketplace.** OpenClaw has 5,700+ skills on ClawHub. Atlas skills are hand-authored and limited to what's in `.claude/skills/`.

6. **Proactive heartbeat with isolated sessions.** OpenClaw's heartbeat uses `isolatedSession: true` to keep costs at ~2-5K tokens per run. Atlas uses Windows Task Scheduler with full Claude Code sessions — likely much more expensive per heartbeat.

7. **Browser automation.** OpenClaw has built-in browser tools for web interaction. Atlas has Playwright via MCP but no dedicated browsing skills.

8. **Multi-model support.** OpenClaw can route to Claude, GPT-4o, Gemini, DeepSeek depending on task. Atlas is Claude-only.

### Features Atlas Has That OpenClaw Lacks

1. **Zero cost on Max subscription.** OpenClaw requires API keys and per-token billing. Atlas runs on Claude Code with an existing subscription.

2. **Self-improvement loop.** Nightly automated review of skills, rules, and hooks. OpenClaw doesn't do this.

3. **Zero maintenance burden.** No runtime to patch, no dependencies to update. When Claude Code updates, Atlas benefits automatically.

4. **Clean directory isolation for multi-agent.** Simpler and arguably safer than OpenClaw's shared-runtime multi-agent.

5. **Native Claude Code integration.** Hooks, skills, subagents, MCP — all first-class. No adapter layer.

---

## Patterns Worth Adopting

### From OpenClaw

1. **Hybrid memory retrieval.** Add vector embeddings (via `voyage` or local model) alongside FTS5. The `finalScore = vectorWeight * vectorScore + textWeight * textScore` formula is proven. Store in pgvector or sqlite-vec.

2. **Temporal decay on memory.** 23-day half-life means old context naturally fades. Implement in the `/promote` and `/search-memory` skills as a relevance multiplier.

3. **Isolated heartbeat sessions.** Find a way to run heartbeats with minimal context loading. The current Windows Task Scheduler approach likely loads full context each time.

4. **Skill registry / sharing format.** Standardize skill files so they could be shared or imported from a community registry. Follow OpenClaw's portable skill format.

5. **Three-tier permission gates.** Add sandbox-level and group-level tool filtering on top of the existing ask/allow/never model.

6. **Browser automation skills.** Build dedicated web interaction skills on top of the existing Playwright MCP, not just raw browser commands.

7. **Multi-channel abstraction.** If more channels are needed beyond Telegram/Discord, build a thin routing layer rather than per-channel MCP configs.

### From the Broader Ecosystem

8. **OpenPersona's four-layer persona model** (Soul/Body/Faculty/Skill) — cleaner separation than current SOUL.md which mixes identity with operational rules.

9. **Hermes-style self-improving skills** — skills that track their own success rate and refine themselves based on outcomes, not just nightly review.

10. **Vellum's credential isolation** — credentials never touch the model context. Atlas already has secrets hygiene rules, but could enforce this architecturally.

---

## Key Sources

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [OpenClaw Architecture Explained (Substack)](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
- [OpenClaw Memory System Deep Dive (Substack)](https://gaodalie.substack.com/p/i-studied-openclaw-memory-system)
- [OpenClaw Design Patterns Series (Ken Huang)](https://kenhuangus.substack.com/p/openclaw-design-patterns-part-1-of)
- [OpenClaw Security Hardening (Nebius)](https://nebius.com/blog/posts/openclaw-security)
- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [UnClaw GitHub](https://github.com/shahshrey/unclaw)
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [OpenClaw HEARTBEAT/SOUL/Memory Config Guide (Blink)](https://blink.new/blog/openclaw-heartbeat-soul-memory-configuration-guide-2026)
- [NanoClaw vs OpenClaw (DataCamp)](https://www.datacamp.com/blog/nanoclaw-vs-openclaw)
- [Best Self-Hosted AI Agents 2026 (Lushbinary)](https://lushbinary.com/blog/best-self-hosted-ai-agents-hermes-openclaw-ironclaw-compared/)
- [FreeCodeCamp OpenClaw Guide](https://www.freecodecamp.org/news/how-to-build-and-secure-a-personal-ai-agent-with-openclaw/)
- [Towards Data Science OpenClaw Tutorial](https://towardsdatascience.com/use-openclaw-to-make-a-personal-ai-assistant/)
