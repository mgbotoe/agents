# Wiki Schema

This file tells any agent how the wiki is structured and how to maintain it.

**Location:** `C:\Workspace\agents\wiki\`
**Shared across all agents.** This is Dina's knowledge base, not any single agent's.

## Directory Structure

```
wiki/
├── index.md          — catalog of all pages, organized by category
├── log.md            — append-only chronological record of activity
├── SCHEMA.md         — this file (conventions and workflows)
├── people/           — entity pages for individuals
├── organizations/    — companies, nonprofits, schools, boards
├── projects/         — active work streams, initiatives, applications
├── decisions/        — key decisions with context and rationale
├── sources/          — summaries of ingested documents, transcripts, articles
└── raw/              — immutable source documents (never modified by Atlas)
```

## Page Conventions

### Frontmatter
Every wiki page has YAML frontmatter with at minimum:
- `name` — display name
- `tags` — array of tags for filtering
- Additional fields vary by page type (see below)

### People pages
Required: `name`, `role`, `org`, `emails`, `tags`
Optional: `meeting_cadence`, `last_meeting`, `phone`

### Organization pages
Required: `name`, `type`, `dina_role`, `tags`
Optional: `email`, `website`, `priority`, `status`

### Project pages
Required: `name`, `org`, `type`, `status`, `tags`
Optional: `due_date`, `cadence`, `participants`

### Decision pages
Required: `name`, `date`, `context`, `decision`, `tags`
Optional: `alternatives`, `rationale`, `revisit_date`

**When to create a decision page:**
- Dina explicitly says "let's go with X" or "I decided to Y"
- A Granola transcript captures a decision with stakeholders
- An email thread reaches a conclusion
- During interactive sessions when Dina makes a call

**What to capture:**
- What was decided and by whom
- What the alternatives were
- Why this option was chosen (rationale)
- What would trigger revisiting this decision
- Link to the source (meeting transcript, email, conversation)

**Why this matters:** Decisions get re-litigated when people forget the context. This prevents that. When someone asks "why did we do X?", Atlas checks decisions/ first.

### Source pages
Required: `name`, `source_type` (email/doc/transcript/article), `date`, `tags`
Optional: `author`, `raw_path`

## Cross-references
Use Obsidian-style wikilinks: `[[folder/page-name|Display Name]]`
Every page should link to related entities. Orphan pages are a lint failure.

## Workflows

### Ingest

**Step 0: Classify the source type.** Different sources get different treatment:

| Type | Template Focus | Example |
|------|---------------|---------|
| `1:1` | Relationship context, career signals, action items, feedback given/received | Martin 1:1, Madina<>Helen |
| `team-sync` | Decisions made, status updates, blockers, who owns what | WDAI Core Team Sync, EAI Team Sync |
| `strategy` | Key numbers, frameworks, competitive landscape, executive decisions | Board presentation, pricing strategy |
| `demo/workshop` | What was shown, technical details, evaluation, next steps | Anish demo, Snowflake workshop |
| `voc` | Customer/user pain points, quotes, insights, opportunity sizing | VOC calls with Ty, Keith, Anish |
| `external` | Who they are, what they want, what we committed to | Recruiter calls, vendor meetings |
| `wdai-program` | Curriculum updates, participant feedback, operational improvements | AI Foundations sessions |
| `personal` | Context only — no project extraction | Doctor visits, personal planning |
| `document` | Key claims, data points, author's thesis | Resume, personal statement, articles |
| `email-thread` | Decision reached, action items, who's waiting on who | Important email chains |

**Step 1: Extract using the type-specific template above.**
- 1:1s → focus on what the other person said, signals about priorities/politics, action items
- Strategy meetings → focus on numbers, decisions, frameworks
- VOC → focus on pain points and quotes
- Don't use the same generic summary for every meeting type.

**Step 2: Reflect — before writing, check for contradictions.**
- Does this new info contradict anything already in the wiki?
- Has a decision been reversed? A project status changed? A person's role shifted?
- If yes, update the existing page AND note the change: "Previously X, now Y as of [date]"
- This prevents wiki drift where old pages say one thing and new pages say another.

**Step 3: Write and cross-reference.**
1. Create a source page in `sources/` with the classified frontmatter
2. Update relevant entity pages (people, projects, orgs)
3. Create decision pages if decisions were made
4. Update `index.md`
5. Append to `log.md`

### Query
When answering questions that produce reusable knowledge:
1. Check `index.md` for relevant pages
2. Read relevant pages for context
3. If the answer is substantial, file it as a new wiki page
4. Update cross-references

### Lint (runs during nightly self-improve)
Check for:
- Contradictions between pages
- Stale info (dates passed, statuses changed)
- Orphan pages (no inbound links)
- Missing pages (entities mentioned but no page exists)
- Missing cross-references
- Data gaps worth filling

### Presentations (Marp)
When Dina asks to turn wiki content into slides:
- Generate Marp-formatted markdown
- Use `---` for slide breaks
- Keep slides concise: title + 3-5 bullets max
- Save to `wiki/sources/` with `source_type: presentation`

## Access from Project Spaces

The wiki is opt-in for project workspaces. When a project needs access to Dina's knowledge base (people, orgs, decisions), add this line to that project's CLAUDE.md:

```
# Shared Knowledge Base
@C:\Workspace\agents\wiki\SCHEMA.md
```

Don't add it by default — only when the project involves people/orgs/decisions in the wiki.

## Rules
- Any agent can read and write to the wiki. It's Dina's knowledge, not any single agent's.
- Raw sources in `raw/` are immutable — never modify them.
- Always update `index.md` and `log.md` after changes.
- One entity = one page. Don't duplicate info across pages.
- Keep pages concise. Link instead of repeating.
- Flag contradictions explicitly — don't silently resolve them.
