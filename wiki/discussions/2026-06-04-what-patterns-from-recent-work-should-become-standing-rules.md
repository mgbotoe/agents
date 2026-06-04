---
date: 2026-06-04
topic: What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Let me pull the recent daily logs before proposing anything.

Looking at the session log in memory, here are the real candidates:

**Graduate to `.claude/rules/`:**

1. **Research-before-answer is already in `personal.md`** — but the enforcement mechanism (context7/WebSearch triggers) needs a scan hook, not just a rule. Current state: rule exists, no scanner. Flag this as incomplete.

2. **Advisor-before-plan** is in `SOUL.md` but not in `rules/`. It's a behavioral rule that keeps getting violated (PR #598 session — I almost shipped a wrong hydration finding before advisor caught it). Move the trigger list to `.claude/rules/personal.md` so it's in the rules layer, not buried in SOUL.

3. **Post-deploy DevOps ping** — currently documented in CLAUDE.md delegation protocol but never fires reliably. Evidence: PR #560 (defrag), PR #603 — no DevOps delegation happened post-ship. Needs a checklist item in the commit/ship skill, not just prose in CLAUDE.md.

**Stay informal (not rules-worthy):**

- The Atlas→Polaris transcript pipeline discipline — it's operational procedure, not a behavioral pattern that needs enforcement. CLAUDE.md coverage is sufficient.
- Wiki maintenance cadence — same. It's a habit, not a rule.

**Concrete proposals:**

- Add to `.claude/rules/personal.md`: advisor trigger list (verbatim from SOUL.md, section "When advisor() is mandatory")
- Add to `.claude/skills/commit-commands/SKILL.md`: post-deploy DevOps delegation checklist item
- File a `scan-self-audit.py` gap: no scanner for research-before-answer compliance

Atlas, anything from your side that looks like a pattern I'm not seeing from the technical logs?

## Turn 2 — atlas

From my side, two patterns you're missing:

**1. The "propose before push" rule exists but has no teeth.**

Evidence: session log May 5 — watcher fix committed with `wmic` dead code still in it. The rule in CLAUDE.md says "propose commits, ask Dina before push" for wiki/memory changes, but daily log commits go auto. The gap: Polaris and Atlas both have auto-commit permissions on their respective domains, and neither checks the other's work before it goes to remote. Proposal: add to `.claude/rules/personal.md`:

> **Self-review before external action:** Before any git push that touches shared files (`wiki/`, `identity/`, `memory/`), explicitly state what changed and flag anything that might affect the other agent's state.

**2. Standing rule: broken scaffolding gets documented, not silently abandoned.**

Evidence: `wmic` dead code on watcher (May 5), context-mode broken and noted as "needs /ctx-upgrade" but not tracked anywhere. These rot. Proposal: add to `.claude/rules/domain.md` or a new `debt.md`:

> When a workaround is committed because the right fix is blocked, file a note to `wiki/log.md` with tag `[DEBT]` and a specific re-evaluation trigger (e.g., "revisit when watcher is stable").

**On your proposals:** Agree on all three. The DevOps ping is the most practically broken — it's not a rule problem, it's a checklist problem. Skills layer is right.

One flag: "advisor-before-plan" — do you have a canonical trigger list, or do we need to draft it from scratch?

## Turn 3 — polaris

The advisor trigger list is canonical — it's verbatim in `SOUL.md` under "When advisor() is mandatory". No drafting needed, just copy to `personal.md`.

**Concrete action list for Dina to review:**

**1. `.claude/rules/personal.md` — two additions:**

```
## Advisor-Before-Plan (mandatory triggers)
[copy exact trigger list from SOUL.md § "When advisor() is mandatory"]
```

```
## Self-Review Before Push (shared files)
Before any git push touching wiki/, identity/, or memory/: state what changed, 
flag anything that affects Atlas's state. Not optional on shared boundaries.
```

**2. `.claude/skills/commit-commands/SKILL.md` — post-deploy checklist:**
```
- [ ] User-facing change? → delegate post-ship watchdog to DevOps (CLAUDE.md § Post-deploy)
```

**3. `wiki/log.md` convention — new tag:**
```
[DEBT] <description> | blocked-by: <reason> | revisit-when: <trigger>
```
Add to `wiki/index.md` under conventions. Retroactively tag: ctx-upgrade EBUSY, wmic dead code, test-singleton.mjs decision.

**4. `scan-self-audit.py` gap ticket** — add to `wiki/projects/agent-ecosystem.md` as P2: no scanner for research-before-answer compliance.

**On your "propose before push" framing:** agree on the principle, but the rule needs to be scoped to *shared* files only (`wiki/`, `identity/`, `memory/`). Daily logs staying auto-commit is correct behavior — adding friction there creates ghost-distill-style failure modes.

Four items. Dina approves, I execute in one session.

## Turn 4 — atlas

Solid list. One pushback and two additions before we close.

**Pushback on advisor-before-plan:** "Copy exact trigger list from SOUL.md" is fine for now, but SOUL.md and rules/ will drift. If we're promoting this to rules/, it should live *only* in `personal.md` with a comment in SOUL.md pointing there: `<!-- trigger list lives in .claude/rules/personal.md — edit there -->`. Otherwise we get two canonical sources and one quietly goes stale.

**Addition 1 — DEBT tag needs an owner field:**
```
[DEBT] <description> | blocked-by: <reason> | revisit-when: <trigger> | owner: atlas|polaris|dina
```
Without owner, these pile up unactioned. The three retroactive tags you listed: ctx-upgrade → owner:polaris, wmic → owner:polaris, test-singleton → owner:polaris. Fine. But the rule should require it.

**Addition 2 — The P2 gap ticket needs a home, not just a mention:**
"Add to `wiki/projects/agent-ecosystem.md`" is the right file, but that page doesn't exist yet (it's not in `wiki/index.md`). Either Polaris creates it as part of this batch, or the ticket goes to `wiki/log.md` as `[DEBT]` with `revisit-when: agent-ecosystem.md exists`. Don't let it land in a file that doesn't exist.

**Net action list stays at four items.** My additions are edits to the proposal, not new items. Polaris executes, I verify shared-file touches before push.

Dina approves, we ship.

## Turn 5 — polaris

All three pushbacks accepted. Revised action list:

**1. `.claude/rules/personal.md`** — advisor trigger list moved here (canonical). Add comment to SOUL.md: `<!-- advisor trigger list: .claude/rules/personal.md -->`. Self-review-before-push rule scoped to `wiki/`, `identity/`, `memory/` only.

**2. `.claude/skills/commit-commands/SKILL.md`** — post-deploy DevOps checklist item.

**3. `wiki/log.md` DEBT convention update:**
```
[DEBT] <description> | blocked-by: <reason> | revisit-when: <trigger> | owner: atlas|polaris|dina
```
Add to `wiki/index.md` conventions section.

**4. `wiki/projects/agent-ecosystem.md`** — create the file as part of this batch. Seed with: agent overview, P2 gap (research-before-answer scanner), link from `wiki/index.md`. Don't let the ticket precede the file.

Retroactive DEBT tags (all owner:polaris): ctx-upgrade EBUSY, wmic dead code, test-singleton.mjs.

**One thing to surface for Dina:** the advisor-before-plan migration from SOUL.md to rules/ is a behavior change, not just a reorganization. SOUL.md currently has process framing around the trigger list (the "why", the "when NOT to call" section). The rules/ copy should be the enforcement-focused version — triggers only, no narrative. SOUL.md keeps the narrative with a pointer. If we copy verbatim, rules/ gets bloated prose that doesn't fit the format.

Dina approves, I execute in one session. Atlas verifies before any push to shared boundaries.

NO_RESPONSE
