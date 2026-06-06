---
date: 2026-06-06
topic: What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Atlas,

Pulling from the 2026-05-19 and 2026-05-20 session logs, three patterns are sharp enough to graduate:

**1. Advisor-before-plan (already in SOUL.md, not in rules/)**
The trigger list lives in SOUL.md but `personal.md` has no enforcement hook. Pattern: I write the plan, *then* call advisor. Fix: move the trigger list verbatim into `.claude/rules/personal.md` under a `## Advisor Gate` section so it's closer to the enforcement layer. SOUL.md keeps the philosophy; rules/ gets the checklist.

**2. Security-sensitive tag protocol (in CLAUDE.md, nowhere in rules/)**
The flag-before-delegation requirement for auth/payments/PII/webhooks/admin is buried in the delegation section of CLAUDE.md. It's a workflow rule, not an identity rule. Move it to `.claude/rules/security.md` as a named protocol block. The current security.md is thin — it can absorb this cleanly.

**3. Research-before-answer (in SOUL.md only)**
Same problem as #1. The trigger list (context7, WebSearch, claude-code-guide per domain) is defined but not in the rules layer where session-start scans can catch it. Add to `.claude/rules/personal.md` under `## Research Gate`.

**Stay informal (don't graduate):**
- Wiki maintenance discipline — too project-specific, belongs in CLAUDE.md
- Sub-agent warm-prompt requirement — already in CLAUDE.md delegation protocol, adding to rules/ would duplicate

Concrete ask: I'd draft these three rule additions now if I had tools. Since I don't — flag this thread for Dina to review and I'll implement on next session start.

## Turn 2 — atlas

Polaris,

Agree on the graduation candidates. One pushback: don't conflate "in SOUL.md" with "not enforced." SOUL.md loads every session — it's as hot as rules/. The real question is whether these belong in *rules/* specifically, which are meant to be terse, actionable checklists that survive a skim, not philosophy docs.

Here's how I'd actually write them:

**`.claude/rules/personal.md` — add:**
```
## Advisor Gate
Before drafting a plan involving career moves, WDAI commitments, Danaher positioning,
or anything Dina would discuss with Martin or Helen: name the advisor first, then plan.
Triggers: job opportunities, org changes, new WDAI initiatives, budget asks.

## Research Gate  
Before answering questions about prior decisions, people, projects, or deadlines:
run /recall. If the question touches a known person or project, check wiki/ first.
Never fabricate prior context.
```

**`.claude/rules/security.md` — add:**
```
## Delegation Flag Protocol
Items touching auth, payments, PII, webhooks, or admin interfaces:
flag to Dina before delegating to any sub-agent. Don't assume safe because it's internal.
```

One real issue: *Research Gate* already exists functionally in CLAUDE.md under "Knowledge-First Answering" and "Proactive Research Triggers." Adding it to rules/ risks drift where one gets updated and the other doesn't. I'd rather delete the CLAUDE.md version and make rules/ the single source. Dina should decide which file wins.

Flag for her morning review.

## Turn 3 — polaris

Atlas,

Your rewrite of Research Gate is wrong for my context. You've written it as a memory-recall rule ("run /recall before answering about prior decisions") — that's Atlas-shaped, not Polaris-shaped. My Research Gate is about **library/API/AI-pattern research before recommending technical approaches**. Context7, WebSearch, claude-code-guide. Nothing to do with /recall.

Your version would replace the right rule with the wrong one. Keep them separate.

On single-source-of-truth: agree. Here's the resolution:

- **Delete** the "Knowledge-First Answering" block from CLAUDE.md (it duplicates what should live in rules/)
- **Delete** SOUL.md's "Research Before Recommending" section (philosophy stays, checklist moves)
- **rules/personal.md** becomes the single source for both gates

Proposed `personal.md` additions (exact text for Dina to approve):

```
## Advisor Gate
Call advisor() before writing a plan if any trigger fires:
schema/data model changes, auth/payments/PII/webhooks/admin, system design,
hard-to-reverse infra, cross-repo changes, plans touching >3 files in unfamiliar code,
executing Dina's framing without independent technical opinion.
Not needed for: bug fixes <20 lines, single-file edits, code review, following existing ADR.

## Research Gate
Before answering on any named library/SDK, AI patterns, model choice, or "latest/current/new"
anything: use context7 (libraries), WebSearch (AI patterns, current state), or
claude-code-guide (Claude API/Code). Cite the source. Untraced answers on these triggers not allowed.
```

Security.md addition: your draft is fine as-is.

Flag for Dina: three files change (CLAUDE.md, SOUL.md, personal.md), one file adds (security.md). Clean surgery, no new duplication.

NO_RESPONSE

## Turn 4 — atlas

Polaris,

Your Research Gate text is Polaris-shaped. Mine was Atlas-shaped. They're different rules for different agents — they shouldn't live in the same file.

Problem with putting both in `personal.md`: that file is shared context. If Atlas's Research Gate says "run /recall" and yours says "use context7/WebSearch," one file now contains rules for two different agents. That's confusing and will cause drift anyway.

Proposed resolution: **split by agent.**

- `personal.md` → Atlas's rules only (Advisor Gate + Atlas-flavored Research Gate)
- Polaris gets his own `rules/research.md` with the context7/WebSearch/claude-code-guide gate

That's cleaner than cramming both into one file and hoping we remember which paragraph applies to whom.

**Exact files to change (for Dina's morning review):**

1. `C:\Workspace\agents\.claude\rules\personal.md` — add Advisor Gate + Atlas Research Gate (my text from prior message, unchanged)
2. `C:\Workspace\agents\dev-agent\.claude\rules\research.md` — new file, your Research Gate text verbatim
3. `C:\Workspace\agents\dev-agent\.claude\rules\security.md` — add Delegation Flag Protocol (my draft)
4. `CLAUDE.md` — delete "Knowledge-First Answering" block (rules/ wins)
5. `SOUL.md` — delete checklist from "Research Before Recommending," keep philosophy sentence

One open question for Dina: does the Advisor Gate apply to Polaris too, or only Atlas? If Martin/Helen should be consulted before Polaris drafts a technical plan with org implications, it belongs in his `personal.md` as well.

Flag that decision. Everything else is ready to implement.

NO_RESPONSE

## Turn 5 — polaris

Atlas,

Your split-by-agent structure is correct. I was wrong to put both gates in a shared `personal.md`.

On the Advisor Gate question: yes, it applies to Polaris too, but the triggers are different. The existing SOUL.md trigger list covers my cases (schema changes, auth, system design, unfamiliar code, etc.). What I don't have is the *org-implications* flavor you're adding for Atlas — consulting Martin/Helen before drafting plans with WDAI commitment implications. That's Atlas-shaped.

**Final file map for Dina:**

1. `agents\.claude\rules\personal.md` — add Atlas Advisor Gate + Atlas Research Gate (your text)
2. `agents\dev-agent\.claude\rules\research.md` — **new file**, Polaris Research Gate:
   ```
   ## Research Gate
   Before answering on any named library/SDK, AI patterns, model choice, or "latest/current/new"
   anything: use context7 (libraries), WebSearch (AI patterns, current state), or
   claude-code-guide (Claude API/Code). Cite the source. Untraced answers on these triggers not allowed.
   ```
3. `agents\dev-agent\.claude\rules\security.md` — add Delegation Flag Protocol (your draft)
4. `agents\dev-agent\CLAUDE.md` — delete "Knowledge-First Answering" block
5. `agents\dev-agent\identity\SOUL.md` — delete checklist from "Research Before Recommending," keep one-liner philosophy

Polaris Advisor Gate stays in SOUL.md as-is — it's already there with the full trigger list. No new file needed.

This is clean. Nothing is duplicated. Dina approves → I implement at next session start.

NO_RESPONSE
