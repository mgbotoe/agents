# Workstation Map — Windows → Mac Port

**Purpose:** inventory every place Claude Code config lives, decide what ports to the Mac vs stays Windows-only vs gets cleaned up. Built 2026-06-18 from a cross-workspace sweep + `~/.claude` audit. This is a **discussion doc** — port decisions in the last section are proposals, not final.

**Open this first on the Mac.** The runbook at the bottom is the execution checklist.

---

## How config travels (3 mechanisms)

| Mechanism | What uses it | Mac action |
|---|---|---|
| **Git repo** | Everything in a tracked repo (skills, agents, commands, CLAUDE.md, py scripts) | `git clone` — travels for free |
| **Marketplace source** | Plugins (declared in `settings.json` → `extraKnownMarketplaces`) | auto-installs from github on first launch |
| **Per-machine regenerate** | secrets, MCP tokens, hook absolute paths | `setup-mac.sh` rebuilds from `.example` + env |

Legend for decisions below: ✅ **TRAVELS** (clone) · 🔧 **REGENERATE** (per-machine) · 🪟 **WINDOWS-ONLY** (port to shell or leave) · 🧹 **CLEANUP** (stale/dead)

---

## 1. User-global — `~/.claude` → `mgbotoe/my.claude` (✅ pushed today)

| Item | Count | Decision |
|---|---|---|
| Subagents (`agents/`) | 12 | ✅ TRAVELS |
| Skills (`skills/`) | 3 — agent-browser, ast-grep, gemini-image-gen | ✅ TRAVELS |
| Slash commands (`commands/`) | 6 — council, familiarize, scan-code-size, seo-public-page, start/stop-watcher | ✅ TRAVELS |
| Hooks (`hooks/`) | 2 — context-mode-cache-heal.mjs, pre-commit-format.mjs | 🔧 REGENERATE (paths are machine-abs; declared in `settings.local.json`) |
| `CLAUDE.md`, `settings.json` | — | ✅ TRAVELS |
| `settings.local.json` | — | 🔧 REGENERATE (gitignored, per-machine hooks live here) |
| Plugins / marketplaces | 6 marketplaces, 18 plugins | ✅ auto — re-install from `extraKnownMarketplaces` |

## 2. Custom skills marketplace → `mgbotoe/claude-skills` (✅ created today, private)

17 skills: product-owner-workflow, qa-testing, debugger, devops-deployment, ai-ml-implementation, ui-ux-audit, ui-ux-designer, design-system-migration, technical-writing, database-admin, rag-knowledge-engineering, rag-knowledge-maintenance, api-documenter, ai-guardrails-audit, smoke-testing, seo-public-page, council. → ✅ auto-installs (declared as `custom-skills` github source).

## 3. Polaris — `C:\Workspace\agents\dev-agent` → `mgbotoe/agents`

| Item | Detail | Decision |
|---|---|---|
| `CLAUDE.md`, `identity/`, `.claude/rules/` | — | ✅ TRAVELS |
| Skills (`.claude/skills/`) | 16 | ✅ TRAVELS |
| Subagents (`.claude/agents/`) | 5 — builder, designer, qa, devops, security | ✅ TRAVELS |
| Scripts (`.claude/scripts/`) | 19 Python | ✅ TRAVELS (already `parents[N]` path-derived, OS-agnostic) |
| `gather-context.ps1` | superseded by `gather-context.py` | 🧹 CLEANUP — delete leftover |
| `.mcp.json` | polaris-slack + wdai-slack; **inline tokens + `C:\` paths** | 🔧 REGENERATE (`setup-mac.sh` builds from `.mcp.json.example` + `secrets.env`) |
| `bin/setup-mac.sh` | Mac bootstrap | ✅ already exists |
| `bin/scheduled/run-task.cmd` | Task Scheduler runner | 🪟 keep until self-improve cloud migration lands, then 🧹 |
| `bin/scheduled/{register-tasks.bat, setup-tasks.cmd, decay.cmd}` | Task Scheduler registration | 🧹 CLEANUP — scheduler is empty; cloud cron replaced these |
| `.claude/drafts/*.ps1` | one-off draft | 🧹 CLEANUP |

**Status: ~90% Mac-ready.** Remaining = regenerate `.mcp.json` + delete dead Windows scripts.

## 4. Atlas — `C:\Workspace\agents\chief-of-staff` → (its own repo)

| Item | Detail | Decision |
|---|---|---|
| `CLAUDE.md`, skills (14), agents (2) | — | ✅ TRAVELS |
| Scripts (`.claude/scripts/`) | 5 Python + 4 shell (`.sh`) | ✅ TRAVELS (already portable) |
| `.mcp.json` | atlas-gdrive/gmail/gcal/discord/slack, `C:\` abs paths | 🔧 REGENERATE |
| Hooks in `settings.json` + `settings.local.json` | machine-abs paths | 🔧 REGENERATE (same split as Polaris) |
| `bin/scheduled/` | **10 `.ps1` + 3 `.cmd` + 1 `.vbs`** (morning-brief, midday-check, meeting-prep, evening-wrapup, friday-wrap, weekly-review, …) | 🪟 **biggest port lift** — see open question |

**Status: NOT ported.** Atlas is the Windows-coupled agent. No scheduled tasks currently registered → the `.ps1` scripts are **orphaned or cloud-migrated** (needs confirming). Atlas needs its own porting pass — out of scope for this session, flagged.

## 5. Project repos — travel with their own git repos (✅ all TRAVELS)

Most carry only `CLAUDE.md` (portable). Those with `.claude/skills/`:

| Repo | Skills | Notes |
|---|---|---|
| WDAI/wdai-foundation-platform | 11 | + `.claude/hooks/`, council/, defrag/, patterns/ |
| WDAI/wdai-team-os | 5 | minimal |
| WDAI/mailchimp-cc, WDAI/wdai-admin | 1 each | minimal |
| Personal Projects (7 repos) | 0 | CLAUDE.md only — fully portable |

No Windows-only artifacts detected in any project repo. **Nothing to do — each ports when its repo is cloned.**

---

## Cleanup candidates (the "opportunity to clean" list)

1. 🧹 **dev-agent `CLAUDE.md` "Scheduling" section is stale** — describes Windows Task Scheduler tasks (Promote, Distill, SelfImprove, IndexLogs, Decay) that **no longer exist** (sweep found 0 registered tasks; automation is GitHub Actions cloud cron). Rewrite to reflect cloud cron + `/loop`.
2. 🧹 **dev-agent dead Task Scheduler scripts** — `register-tasks.bat`, `setup-tasks.cmd`, `decay.cmd` (cloud cron replaced them).
3. 🧹 **`gather-context.ps1`** — superseded by `gather-context.py`; delete.
4. 🧹 **Stray `nul` artifact** — polluting both `agents` and `my.claude` working trees.
5. 🧹 **`.mcp.json` inline tokens** — switch to `${ENV}` substitution (the `.example` already does this) so secrets aren't sitting in plaintext config.
6. ❓ **Atlas orphaned `.ps1` scheduled scripts** — 10 scripts with no registered tasks. Either dead (cloud-migrated) or run by an unknown mechanism. Confirm before porting Atlas.

---

## Mac onboarding runbook (DRAFT — derived from above)

```bash
# 1. Clone the config repos
git clone https://github.com/mgbotoe/my.claude  ~/.claude
git clone https://github.com/mgbotoe/agents      ~/Workspace/agents
#    agents is a MONOREPO — this one clone brings Polaris (dev-agent),
#    Atlas (chief-of-staff), wiki, and slack-watcher together.
# (Optional) edit the custom skills marketplace locally:
git clone https://github.com/mgbotoe/claude-skills  ~/Workspace/claude-skills

# 2. Bootstrap Polaris (secrets, MCP config, python shim, slack MCP deps)
cd ~/Workspace/agents/dev-agent && ./bin/setup-mac.sh
#    then edit config/secrets.env with the Slack tokens

# 3. Launch Claude Code in ~/Workspace/agents/dev-agent
#    - marketplaces auto-add from settings.json extraKnownMarketplaces
#    - plugins auto-enable from enabledPlugins
#    - custom-skills auto-installs from mgbotoe/claude-skills

# 4. Verify
#    - hooks fire (SessionStart workspace-scan runs) → if not, hooks-merge
#      assumption was wrong, move them from settings.local.json back
#    - `node` resolves (setup-mac.sh creates ~/.local/bin/python → python3 shim)
#    - MCP servers connect (polaris-slack / wdai-slack)
```

**Known gaps to resolve before this is final:** see open questions.

---

## Open questions for Dina

1. **Atlas port** — separate effort? Atlas has the real Windows coupling (10 `.ps1` + `.vbs`). Do we (a) port Atlas's `.ps1` → `.sh` now, (b) defer Atlas entirely (Polaris-on-Mac first), or (c) confirm those scripts are already dead (cloud-migrated) and just delete?
2. ~~`chief-of-staff` repo relationship~~ — **RESOLVED**: it's a subdir of the `agents` monorepo, travels with `git clone mgbotoe/agents`. (Also resolved: `claude-skills` was nested inside the monorepo by mistake → moved out to `C:\Workspace\claude-skills`.)
3. **Cleanup scope** — knock out cleanup items 1-5 now (low-risk, mostly deletes + a CLAUDE.md rewrite), or keep this session scoped to the cross-machine sharing we already shipped?
