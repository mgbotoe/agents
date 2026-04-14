---
name: Karpathy LLM Wiki — Community Feedback
source_type: research
date: 2026-04-12
tags: [wiki, architecture, improvements]
---

# Karpathy LLM Wiki — Community Feedback

Synthesized from 120+ gist comments, the LLM Wiki v2 extension by rohitg00, and community blog posts/implementations. Focus: actionable insights for Atlas's wiki implementation.

## Architecture Improvements

### Memory Lifecycle (from LLM Wiki v2)
The original treats all wiki content as equally valid forever. In practice, knowledge has a lifecycle:
- **Confidence scoring**: every fact carries a score — how many sources support it, recency of confirmation, whether anything contradicts it. Confidence decays with time, strengthens with reinforcement.
- **Supersession**: new info doesn't just annotate old claims — it explicitly supersedes them. Linked, timestamped, old version preserved but marked stale.
- **Forgetting curve**: facts not accessed or reinforced in months get deprioritized (not deleted). Ebbinghaus-style decay. Architecture decisions decay slowly; transient bugs decay fast.
- **Consolidation tiers**: working memory (recent, unprocessed) -> episodic (session summaries) -> semantic (cross-session facts) -> procedural (workflows/patterns). LLM promotes info up tiers as evidence accumulates.

### Knowledge Graph Layer
Flat pages with wikilinks leave structure on the table:
- **Entity extraction on ingest**: extract typed entities (people, projects, libraries, concepts, decisions) with attributes and relationships.
- **Typed relationships**: "uses," "depends-on," "contradicts," "caused," "supersedes" carry different semantic weight. Better than generic "relates to" links.
- **Graph traversal for queries**: walk outward from entity nodes through typed edges. Catches connections keyword search misses.

### Source Provenance (@Jwcjwc12)
The moment source files change, compiled knowledge might be wrong and doesn't know it. Fix: every proposition records which source files produced it and their content hashes at compilation time. On query, check if files on disk still match. Match = valid. Mismatch = stale. Prevents silently serving outdated knowledge.

## Search & Scale

### Hybrid Search (from LLM Wiki v2, @Paul-Kyle)
`index.md` works up to ~100-200 pages. Beyond that:
- **BM25** (keyword matching with stemming)
- **Vector search** (semantic similarity via embeddings)
- **Knowledge graph traversal** (entity-aware relationship walking)
- Fuse with **Reciprocal Rank Fusion (RRF)**. agentmemory reports 95.2% on LongMemEval-S with this approach.
- Keep `index.md` as human-readable catalog but don't rely on it as primary search past ~100 pages.

### TLDR Optimization (@YokoPunk)
Add a TLDR at the top of every wiki article. LLMs do an index scan, read TLDR first, then decide whether to read the full article. Saves significant tokens.

## Operational Patterns

### Compiler as Pipeline, Not Prompt (@xoai, sage-wiki)
Five focused passes per ingestion: diff -> summarize -> extract concepts -> write articles -> images. Each incremental. One new paper touches ~10-15 wiki pages but skips everything else. Same mental model as `make`.

### Classify Before Extract (@hejiajiudeeyu)
Don't treat every document the same. Classify by type first (report vs. letter vs. transcript vs. declaration), then run type-specific extraction. A 50-page report needs different handling than a 2-page letter. Saves tokens, produces better results.

### Reflect Step (@bendetro)
The loop should be `ingest -> compile -> reflect -> query -> lint`, not just `ingest -> compile -> query -> lint`. The reflect step synthesizes not just what changed, but why — enabling the wiki to critique its own evolution and restructure when framing was wrong.

### Drift Detection (@trox)
When using multiple tools (Obsidian as wiki, Zotero as references, cloud as files), they drift apart. Build drift detection that audits structural alignment across layers and proposes corrections without executing them.

## Multi-Agent Coordination

### Shared Memory Architecture (@Arrmlet, @gayawellness)
- Agents claim which docs to ingest via shared coordination layer, avoiding duplicate work.
- Separate **provenance layer** (called "Anamnesis" by one team running 13 Claude instances) tracks how knowledge was compiled, why decisions were made, what superseded what. The wiki is the codebase; provenance is the git log.

### Vault Separation (from community consensus)
Your vault (personal, curated, verified) and the agent's working vault (speculative writes, messy drafts) need to be physically separate directories. Prevents agent drafts from contaminating verified knowledge.

## Known Failure Modes

1. **Error accumulation**: LLM writes something slightly wrong during synthesis, saves it as context, future answers build on the wrong thing. Unlike RAG where raw source stays intact, the wiki is a derived artifact that can drift from reality.
2. **Information loss through compression**: summarization discards edge cases, exact wording, subtle differences.
3. **Partial context**: LLM only sees a subset of documents during updates, leading to incomplete synthesis.
4. **Traceability loss**: answers come from a mix of generated pages, summaries, and linked ideas — hard to answer "where did this come from?"
5. **Page sprawl**: duplicate pages, messy links, overlapping concepts accumulate without aggressive lint cycles.
6. **Meta-query ranking weakness**: queries like "what happened recently" still rank structural pages (index) above actual recent content.

## Tool & Integration Ideas

| Tool/Approach | What it does | Source |
|---|---|---|
| `.brain/` folder pattern | index.md + architecture.md + decisions.md + changelog.md at project root as persistent agent memory | @samflipppy |
| Obsidian Bases plugin | First-party replacement for Dataview, better for structured queries | @ppeirce |
| Obsidian Seed | Discovery wizard that builds personalized vault structure through conversation | @dkushnikov |
| TagSpaces | File manager for non-markdown raw sources (PDFs, screenshots, emails) with inline preview and tagging | @uggrock |
| Palinode | Git-versioned markdown with `git blame` on every fact, 18 MCP tools, hybrid BM25+vector search via SQLite-vec | @Paul-Kyle |
| Graph database backend | Route wiki output into graph DB built on ontology for cleaner compounding over time | @blex2011 |
| SQLite over filesystem | After 6-12 months on filesystem, local SQLite was better abstraction for agents, especially at scale with multiple agents | @bradwmorris |
| Append-and-review note | Karpathy's separate pattern (from bearblog) — continuously append to a single note, periodically review. Complements wiki. | @expectfun |
| Content hash provenance | Every proposition records source file content hashes; query-time validation catches stale claims | @Jwcjwc12 |
| Cron heartbeat architecture | Monitor inbox folders, route to domains, update foundations vs. current data, collect state.md files into morning brief | @umbex |

## Key Takeaway for Atlas

The community consensus is clear: the core pattern (raw -> wiki -> schema, with ingest/query/lint operations) is sound. What kills implementations is:
1. No confidence scoring or staleness tracking
2. No source provenance (content hashes)
3. Manual-only maintenance (needs event-driven hooks)
4. Flat search that breaks past ~100 pages
5. No separation between agent working space and verified knowledge

Atlas already has the tiered memory architecture (hot/cold/raw/archive). The highest-value additions would be: content hash provenance on compiled facts, confidence decay on claims, hybrid search (BM25 + semantic), and the classify-before-extract ingestion pipeline.
