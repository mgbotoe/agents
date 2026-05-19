---
name: coherent-commit
description: Pull-based commit discipline. Reads git status, splits staged changes into coherent chunks by domain/intent, proposes commit messages per chunk. Use when about to commit and unsure if scope is muddied, or when working across multiple repos to ensure each lands as a focused commit. Trigger words: "/coherent-commit", "split commit", "commit cleanup", "is this commit clean", "muddied scope".
---

# Coherent Commit Workflow

Pull-based commit discipline. Use BEFORE you stage everything and ship a kitchen-sink commit.

## When to use

- About to run `git add -A` or `git add .` (red flag — usually muddies)
- Working session touched multiple unrelated concerns (e.g., a bug fix + a docs change + a config tweak)
- Cross-repo work in one session (each repo needs its own coherent commit)
- You're not sure if what's staged belongs together

## What this skill does

Runs you through a **stage-by-coherence** ritual:

1. **Survey the working tree**
   - Run `git status` in the current repo
   - Categorize every changed/untracked file by domain:
     - `feature` — new product code
     - `fix` — bug fix paths (usually existing files in same module)
     - `docs` — `*.md`, `docs/`, README, CLAUDE.md
     - `config` — `package.json`, `*.toml`, `*.yml`, `*.json` configs, `.env*`
     - `test` — `*_test.*`, `*.test.*`, `__tests__/`, `tests/`
     - `infra` — CI files (`.github/`), Dockerfile, scripts/, bin/
     - `data` — content files, fixtures, seed data
     - `chore` — formatting, renames, generated files

2. **Detect muddy patterns** in what's currently STAGED:
   - Files spanning >2 domains → split candidate
   - Mix of `feature` + `fix` from different concerns → split
   - One commit touching >8 files → suspect, audit if cohesive
   - Mix of test-only files with prod code in unrelated paths → split

3. **Propose chunked commits** if muddied:
   ```
   Commit 1: feat(<scope>): <subject>
     - src/foo.ts
     - src/foo.test.ts

   Commit 2: docs: <subject>
     - README.md
     - docs/usage.md

   Commit 3: chore(deps): <subject>
     - package.json
     - package-lock.json
   ```
   Each chunk gets:
   - Files that belong together
   - A conventional-commit message (feat/fix/docs/chore/test/refactor)
   - Clear scope tag

4. **Execute on Dina's go-ahead**:
   - Reset the index (`git reset HEAD`) without losing changes
   - Stage chunk 1 specifically by file
   - Commit chunk 1 with proposed message
   - Repeat for each chunk
   - Final `git status` to confirm clean

5. **Cross-repo handling**: if changes span repos (very common for Polaris), do steps 1-4 in each repo independently. Do NOT try to bundle changes from different repos.

## Heuristic anchors

- A coherent commit's message tells you what the commit does in <72 chars without ellipsis
- If you can't write that subject without "and" or commas, you've got two commits
- Tests ship WITH the feature/fix they test — don't split unless test was a separate intent (e.g., backfilling tests for old code)
- Generated files (lockfiles, build output) go with the change that caused them, not separately

## Override

If you've verified the scope IS coherent despite tripping the heuristic (e.g., a big feature genuinely spans 10 files), proceed and say so explicitly: "Scope is large but cohesive — single commit." That writes the override decision to the conversation so it's auditable.

## Anti-patterns to refuse

- "Just commit everything, we'll fix the history later" — no, history doesn't get fixed later
- `git commit -am "wip"` followed by another commit later — that's two commits muddied into pseudo-staging
- Mixing your own bug fix into someone else's feature branch commit — splits attribution

## Related rules

- Conventional commits required (`.claude/rules/domain.md`)
- Pre-commit validation: type-check, lint, test, build all must pass
- Master pushes need explicit word; branch pushes auto-OK
