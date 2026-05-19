---
name: survey-prior-art
description: Survey public prior art before committing to an implementation pattern. Runs structured external research (WebSearch, GitHub repos, blog posts, framework docs) then produces a four-section digest with EXPLICIT delta justification — what we'd do differently from prior art and why. Use BEFORE proposing any non-trivial architectural decision. Trigger words "/survey-prior-art", "survey prior art", "what does the community do", "how do other people do X", "is there prior art".
---

# Survey Prior Art — Structured External Research

Pull-based external research skill. Used BEFORE proposing any non-trivial implementation pattern. Forces grounding in public prior art and explicit articulation of what we'd improve.

## When to use

- Designing a new hook system / agent pattern / memory architecture / workflow
- Choosing between competing technical approaches
- About to commit to a convention that will be hard to reverse
- Any time you're about to assert "X is the right way to do Y" without external grounding
- BEFORE forming an opinion to bring to advisor()

## When NOT to use

- Quick bug fixes
- Following an established pattern already documented in our own code/docs
- Single-file edits in well-known repo
- When the answer is clearly "do what the framework says" and the framework guidance is fresh

## Process (mandatory four steps)

### Step 1 — Define the question precisely
Frame as "I'm choosing between X and Y for the purpose of Z, in the context of W." Vague queries produce vague surveys. If you can't frame it concretely, you're not ready to survey yet.

### Step 2 — Run external research (parallel)
Execute in this order:
1. **WebSearch** for the pattern + current year ("2026 agent hook patterns", "Claude Code memory systems", etc.)
2. **GitHub search** for repos doing similar — filter to last 6 months activity
3. **Blog / docs** of established frameworks doing it (Anthropic, OpenAI, framework maintainers)
4. **context7** if a specific library is involved
5. **claude-code-guide** agent if Claude Code internals are involved

Pull at least 3 independent references. One source is not a survey.

### Step 3 — Produce the four-section digest

Output MUST contain all four sections. Skipping any one means survey is incomplete:

```
## A. Observations — What 3+ implementations do
- [Source 1] (link/repo): pattern they use, key choices
- [Source 2] (link/repo): pattern they use, key choices
- [Source 3] (link/repo): pattern they use, key choices

## B. Criticism — Where they fall short
- [Source 1]: known issue / failure mode / what's underbuilt
- [Source 2]: known issue / failure mode
- [Source 3]: known issue / failure mode
- Common gaps across the field: what nobody handles well

## C. Our context — What's unique that they don't share
- Constraints specific to Dina's setup (Windows, multi-workspace, agent ecosystem, etc.)
- Existing infrastructure we'd integrate with
- Why we can't just adopt one of the above wholesale

## D. Proposed delta — What we'd do differently, and why it's better
- Specific change vs prior art
- WHY this is an improvement, not a side-grade or novelty-for-its-own-sake
- What would falsify the improvement claim (how would we know we're wrong)
- If no meaningful delta exists: SAY SO. "Matching prior art X is correct here because Y."
```

### Step 4 — Hand off to advisor()
After producing the digest, call `advisor()`. Advisor reviews:
- Are the criticisms (Section B) substantive or rationalization for our preferred choice?
- Is the delta (Section D) a real improvement or a side-grade dressed up?
- Did Section C honestly identify uniqueness, or invent "our context is special" to justify novelty?

Don't ship the proposal until advisor's read on Section D is reconciled.

## Honest caveat

**Sometimes matching prior art IS the right answer.** Section D can correctly conclude "no improvement opportunity; match X because Y converged on it for reasons that apply to us." The discipline isn't "always innovate." It's "honestly survey, honestly assess, honestly decide."

The anti-pattern this skill prevents:
1. Answering from training data without external check (information lag)
2. Inventing novelty to justify our approach (engineering ego)
3. Matching prior art without acknowledgement (silent regression to mean)

## Output format expected

Result should be brief enough to bring into the conversation as evidence:
- Section A: 3-5 bullets per source
- Section B: 2-3 bullets per source
- Section C: 3-5 bullets, concrete
- Section D: 1-3 deltas, each with WHY + falsification criterion

Total under ~400 lines. If longer, you're over-surveying — stop, ship, advisor.

## Related

- `.claude/rules/personal.md` — research-before-AI-answer rule (this skill extends it to ALL substantive decisions, not just AI/lib)
- SOUL.md "Proposing Behavioral Change — Structural Requirement" — must name mechanism
- `feedback_chestertons_fence.md` — prior art's odd choices usually have reasons; survey forces you to find them before discarding
- `scan-self-audit.py` — detects sessions where implementation shipped without delta justification
