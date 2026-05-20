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

## Process (schema-shaped, four expected steps)

> **Honest framing:** this is a "schema-shaped expectation," not enforced validation. The skill describes the shape of a complete survey; the agent's discipline (or the user's catch) is what enforces it. "Mandatory" claims without enforcement are the rule-without-mechanism pattern.

### Step 1 — Define the question precisely
Frame as "I'm choosing between X and Y for the purpose of Z, in the context of W." Vague queries produce vague surveys. If you can't frame it concretely, you're not ready to survey yet.

### Step 2 — Run external research (parallel)
Execute in this order:
1. **WebSearch** for the pattern + current year ("2026 agent hook patterns", "Claude Code memory systems", etc.)
2. **GitHub search** for repos doing similar — filter to last 6 months activity
3. **READ the actual repos** — not just search snippets:
   - `gh api repos/<owner>/<repo>/contents/README.md` for READMEs
   - `gh api repos/<owner>/<repo>/contents/<path>` for source files
   - `mcp__plugin_context-mode_context-mode__ctx_fetch_and_index` for blog posts (fallback: `gh api` if Bun missing)
4. **context7** if a specific library is involved
5. **claude-code-guide** agent if Claude Code internals are involved

Pull at least 3 independent references. Snippets from search alone are NOT a survey — they're a survey outline. Mark depth honestly in Section A.

**Right-neighborhood check:** for coding-agent decisions, the prior art lives in:
- Cursor, Aider, Cline, Continue, OpenClaw/ClaudeClaw, Claude Code itself
- NOT academic frameworks (MARS, SAGE) unless the decision is specifically about reflection/RL
- NOT general LLM frameworks (LangChain, CrewAI) unless the decision is about multi-agent orchestration

### Step 3 — Produce the four-section digest

Output is **schema-shaped, not mandatory-enforced**. The skill describes what a complete survey looks like; you (the agent) must choose to populate it honestly. There is no validation logic — if you skip Section D, nothing stops you. That makes Section D especially load-bearing: write "matched, no delta" explicitly when that's true, don't leave it empty.

**Honest-survey self-check before declaring done:**
- Did I actually read sources (repos, posts, docs), or just summarize search-result snippets? If snippets only, mark Section A as "thin — snippet-level, no repo reads."
- Did I survey the *right* neighborhood? For coding-agent decisions, that's Cursor/Aider/Cline/Continue/Claude Code ecosystems — NOT academic LLM-research frameworks.
- Did I use `gh api repos/...` or `ctx_fetch_and_index` to read actual repo contents?

**Section schema:**

```
## A. Observations — What 3+ implementations do
- [Source 1] (link/repo): pattern they use, key choices  [HOW READ: snippet | README | source]
- [Source 2] (link/repo): pattern they use, key choices  [HOW READ: ...]
- [Source 3] (link/repo): pattern they use, key choices  [HOW READ: ...]

Survey depth: thin (snippets only) | medium (READMEs read) | deep (source read)

## B. Criticism — Where they fall short
- [Source 1]: known issue / failure mode / what's underbuilt
- [Source 2]: known issue / failure mode
- [Source 3]: known issue / failure mode
- Common gaps across the field: what nobody handles well
- IF Section A is "thin": flag that Section B claims are weakly supported

## C. Our context — What's unique that they don't share
Honest constraint: "we're us" is NOT unique. Genuine uniqueness anchors:
- Documented behavioral failure modes specific to this agent's memory
- Specific upstream/downstream systems we integrate with (advisor, scanners, etc.)
- Constraints validated by data, not asserted
NOT: "solo dev", "multi-workspace", "Windows" — millions share those.

## D. Proposed delta — What we'd do differently, and why it's better
PICK ONE first-class output:

  D1. SUBSTANTIVE DELTA — specific change vs prior art
      - WHY it's an improvement, not a side-grade
      - Falsification criterion: how would we know we're wrong
      - Resist the temptation to claim multiple deltas when the work is plumbing
      - Single honest delta beats four overclaimed ones

  D2. MATCHED PRIOR ART — no meaningful delta
      - Which source we're matching
      - Why this is the right call for our context
      - This is a first-class acceptable answer. Don't invent novelty to fill the section.

  D3. INTEGRATION TARGET — we wired existing components into a system targeted at our specific failure modes
      - Cite the failure modes (from memory files / scanner output)
      - Acknowledge components are standard; novelty is the integration target
      - Most honest answer when shipping plumbing on top of known patterns
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
