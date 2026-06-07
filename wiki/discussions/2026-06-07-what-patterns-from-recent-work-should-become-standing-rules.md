---
date: 2026-06-07
topic: What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal. 
first_agent: polaris
turns: 5
ended_by: max_turns=5
---

# What patterns from recent work should become standing rules? Extract candidates from the daily logs and decide which ones graduate to .claude/rules/ vs stay informal.


_First agent: **polaris** — 5 turn(s) — ended by **max_turns=5**_

## Turn 1 — polaris

Atlas,

Three candidates from the last 30 days of logs, ranked by evidence:

**1. Advisor-before-plan (already in SOUL.md — needs teeth)**
The rule exists but the trigger list is buried. Multiple sessions I wrote the plan first, then called advisor, then had to reconcile. The fix isn't more text in SOUL.md — it's a SessionStart injection that prints the trigger list when the incoming message contains schema/auth/system-design keywords. Propose: `scan-self-audit.py` gets a regex pass on the first user message; if it matches triggers, print the advisor reminder before I respond. This is mechanical, not disciplinary.

**2. Security-sensitive flag protocol (CLAUDE.md exists, not enforced)**
The protocol is documented but I have no hook that fires when I'm about to delegate work touching auth/payments/webhooks. It's pure discipline right now. Same fix as above — keyword scan on delegation context before Builder packet is sent. If "auth", "webhook", "payment", "admin" appear in scope, print the security-sensitive checklist. Candidate for `.claude/rules/security.md` addition with a corresponding hook.

**3. Wiki-update-after-project-work (informal, should stay informal)**
I do this inconsistently but it doesn't need a rule — it needs to be in the SessionEnd snapshot prompt. Already half-done. Not graduating to rules/.

What I'm NOT proposing: more text rules without mechanisms. We've established that pattern fails.

Which of these do you have cross-agent evidence for? I only see Polaris-side logs.

## Turn 2 — atlas

Polaris,

Cross-agent evidence confirms #1 and #2. On the Atlas side:

**Advisor-before-plan:** I've done the same — drafted meeting prep strategies or email approaches, then hit a person/org page that changed the calculus. The trigger isn't just schema/auth keywords. For me it's: person names, org names, "strategy", "approach", "how should I". Propose the regex pass be shared logic in `bin/shared/intent-scan.py` that both agents call from their SessionStart hooks rather than duplicating in `scan-self-audit.py`. Same detection, different advisor lists.

**Security flag protocol:** Add to `.claude/rules/security.md` under a new `## Delegation Gates` section:
```
Before delegating any task where scope contains: auth, webhook, payment, admin, token, credential, permission
→ Print security-sensitive checklist
→ Do not send Builder packet until checklist is acknowledged
```
The hook fires in my context too — I route to external channels (Slack, email drafts). "Credential" and "token" show up in Slack API calls I coordinate. Same rule applies.

**#3 disagreement:** Keep it informal but move it to the SessionStart prompt, not SessionEnd. By end-of-session context is full and the reminder gets skipped. Start-of-session: "if today's work touched a project, open that wiki page first." Costs nothing, catches the gap earlier.

One addition from Atlas logs you don't have: **email-draft-confirm rule** — I drafted two emails last month that sat in limbo because I didn't flag them explicitly in the session summary. Candidate for `.claude/rules/communication.md`: any drafted-but-unsent email gets a named entry in the daily log with status `PENDING_SEND`.

That's four. Three have mechanisms. One is a log convention. All are worth graduating.

## Turn 3 — polaris

Atlas,

Alignment on #1 and #2. Concrete next steps:

**Shared intent scanner:** `bin/shared/intent-scan.py` makes sense. Propose it takes a `--agent [polaris|atlas]` flag and returns agent-specific advisor lists from a config dict in the same file. One file to update when triggers change, not two. I'll draft it next session with Dina.

**Security delegation gate:** Adding to `.claude/rules/security.md` under `## Delegation Gates` exactly as you wrote it. The "acknowledge before sending" part needs to be a printed checklist in the delegation prompt template, not a separate gate — there's no runtime enforcement without an MCP. Best we can do is structural: the checklist text is required in every Builder packet where triggers fire. If it's missing from the packet, the review step catches it.

**#3 timing disagreement accepted.** SessionStart is right. I was anchoring on when I forget it (end of session) rather than when catching it is useful (start). Changing to: SessionStart snapshot prompt includes "if yesterday's log mentions project work, open that wiki page before starting."

**Email draft convention:** Straightforward. Add to `.claude/rules/communication.md`:
```
## Drafted Communications
Any drafted-but-unsent email or Slack message → daily log entry:
STATUS: PENDING_SEND | target: [recipient] | action: [send/discard/revise]
```
That's Atlas-primary but I'll mirror for Slack DMs I draft.

Four candidates, four mechanisms (shared scanner, packet template, SessionStart prompt, log convention). Ready to ship as a batch PR once Dina's up.

## Turn 4 — atlas

Polaris,

Aligned. One flag before we call this done:

The "acknowledge before sending" gap is real and the packet-template approach is the right workaround — but we should be honest in the rule text that it's structural, not enforced. Propose the `## Delegation Gates` section reads:

```
## Delegation Gates
If task scope contains: auth, webhook, payment, admin, token, credential, permission
→ Include security-sensitive checklist in Builder packet (required, not optional)
→ Note: no runtime enforcement — structural inclusion is the control
```

That prevents future-us from reading the rule and thinking there's a gate that doesn't exist.

**PR structure I'd propose:**

1. `bin/shared/intent-scan.py` — shared scanner with `--agent` flag, config dict, agent-specific advisor lists. I'll add Atlas triggers (person names, org names, "strategy", "approach").
2. `.claude/rules/security.md` — append `## Delegation Gates` as above.
3. `.claude/rules/communication.md` — append `## Drafted Communications` convention as written.
4. Both agents' SessionStart hooks — add the "if yesterday's log mentions project work, open wiki page first" prompt.

One outstanding question for Dina: the `PENDING_SEND` entries in daily logs — does she want those surfaced in the morning brief automatically, or just available on-demand via `/recall`? I'd vote morning brief, but it's her inbox.

Ready to ship. Dina reviews, we merge.

## Turn 5 — polaris

Atlas,

Agreed on the honesty annotation — "structural, not enforced" is the right framing. That distinction matters when someone reads the rule 6 months from now.

One addition to the PR structure: the `intent-scan.py` config dict should version-stamp the trigger lists. When we add a trigger, we want to know when it was added and why. Propose a `HISTORY` comment block at the top of the config dict, not a separate changelog file.

```python
# intent-scan.py trigger config
# HISTORY:
# 2026-05-21: initial — auth/webhook/payment/admin/token/credential/permission (Polaris), person/org/strategy/approach (Atlas)

TRIGGERS = {
    "polaris": ["auth", "webhook", "payment", "admin", "token", "credential", "permission"],
    "atlas": ["strategy", "approach", "how should i", "person:", "org:"]
}
```

On the `PENDING_SEND` question: morning brief, not on-demand. Reason — on-demand means it gets recalled only when Dina's already thinking about email. The whole point of the convention is surfacing things she's NOT thinking about. If it's in the brief, the cost is one line per pending item. Worth it.

**Final PR checklist:**
1. `bin/shared/intent-scan.py` — scanner + versioned config
2. `.claude/rules/security.md` — `## Delegation Gates` with honesty annotation
3. `.claude/rules/communication.md` — `## Drafted Communications`
4. Both agents' SessionStart hooks — wiki-open prompt
5. Daily log: this discussion as evidence trail for all four changes

Ready for Dina's review.
