---
name: inventory-repo
description: Deep-read a repo's actual content (workflows YAML, full deps, READMEs, CLAUDE.md, monorepo packages, deploy + DB markers) BEFORE producing any diagram, table, or "current state" summary about it. Mandatory when answering survey/inventory/landscape questions across one or more repos. Heavier than `repo-aware` (which is meta-state focused).
---

# inventory-repo

Prevents the "shallow scan → confident output" failure mode flagged in `feedback_verify_plan_against_code.md`. `ls` + `grep package.json` + filename inference is not enough to produce a Mermaid diagram or `current-state` answer. This skill forces the deep read.

## When to invoke (mandatory)

Any time the user asks you to:

- Produce a diagram, table, or summary of "what's in" a repo or set of repos
- Map workflows / agents / integrations across repos
- Survey the current state / landscape
- Compare repos
- Inventory tooling
- Audit what exists

The `context-injector.py` UserPromptSubmit hook detects these patterns and injects a `[INVENTORY CHECK PENDING]` marker. If you see that marker, you MUST invoke this skill against every target repo before producing the answer.

## When NOT to invoke

- Editing a single file you've already opened and read
- Quick fix in a known codebase
- Answering "what files are in this repo" (use `repo-aware` instead — lighter, file-list focused)
- Producing per-file analysis (read the file directly)

## How to invoke

```bash
python .claude/scripts/inventory-repo.py "<absolute-repo-path>"
```

For multiple repos, run sequentially (cheap — local file reads only):

```bash
for repo in "wdai-foundation-platform" "wdai-admin" "wdai-marketing"; do
  python .claude/scripts/inventory-repo.py "C:/Workspace/Women Defining AI/$repo"
done
```

Output goes to stdout as structured markdown. No caching — the script always reads fresh.

## What it returns

For each repo, a structured markdown report containing:

1. **Deploy + storage detection** — Vercel/Railway/Fly/Docker/Heroku/Cloudflare; Prisma/Supabase/Postgres/Redis
2. **package.json (root)** — name, version, total deps count, scripts list, **dependencies categorized** into: Framework / Auth / Database / Payments / Email / LLM / Monitoring / Storage / Integration APIs / Testing / Build
3. **Monorepo sub-packages** — `packages/*` and `apps/*` with their names, descriptions, README excerpts
4. **GitHub workflows** — each `.github/workflows/*.yml` parsed for **triggers** (push / PR / schedule with cron / workflow_dispatch), job count, and first step name. NOT just filename inference.
5. **CLAUDE.md excerpt** — first 80 lines if present (tells you about Claude Code integration in that repo)
6. **README excerpt** — first 80 lines (tells you what the repo is for, in its own words)

## How to use the output

After running for each target repo, you have the source material to draw accurate diagrams. Specifically:

- Workflow trigger info → whether a workflow is `cron`, `PR`, `manual` (replaces "I'll guess based on filename")
- Dep categorization → what external systems each repo actually touches
- Monorepo packages → existing internal agents (e.g., `packages/course-update-agent`) that shouldn't be double-built
- Deploy target → where each repo runs (Vercel / Railway / CLI / etc)
- CLAUDE.md presence → which repos have Claude Code integration wired

**Cite the output.** When you draft the diagram or table, your claims should be backed by what this script reported. If you find yourself drawing a relationship that the report didn't show explicitly, flag it as "inferred — not directly observed."

## What this skill does NOT do

- Doesn't read every file — only the structural ones (workflows, package.json, README, CLAUDE.md, deploy/db markers)
- Doesn't run code or query external systems — purely local file reads
- Doesn't cache — runs fresh every time (cheap; ~1-2s per repo)
- Doesn't replace `repo-aware` (which scans claim-bearing docs for drift). They're complementary.

## Related

- `.claude/scripts/inventory-repo.py` — the deep-read script
- `.claude/scripts/context-injector.py` — UserPromptSubmit hook that detects survey/inventory prompts and reminds you to invoke this
- `.claude/skills/repo-aware/` — lighter sibling for file-inventory drift checks before doc edits
- `memory/feedback_verify_plan_against_code.md` — the past failure this mechanism addresses
- `identity/SOUL.md` "Proposing Behavioral Change" — mechanism-not-rule rationale
