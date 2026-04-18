# Domain Rules — Development

## TypeScript / JavaScript
- Strict mode always. No `any` types. `noImplicitAny` and `strictNullChecks` enabled.
- Next.js App Router by default. Pages Router only with reason.
- Tailwind for styling. No CSS modules unless forced by a library.
- Biome for formatting/linting. Run before every commit.
- Import order: React/Next.js, third-party, internal aliases (`@/...`), relative, types.
- No `.ts`/`.tsx` extensions in imports.

## Python
- Type hints everywhere. FastAPI for backends.
- Ruff for formatting/linting.
- Virtual environments required. Never install globally.

## Database
- Supabase for auth + DB. PostgreSQL via Prisma or raw SQL based on complexity.
- Parameterized queries only. Never string-concatenate SQL.
- Migrations tracked in version control.

## AI/ML
- Claude API via `@anthropic-ai/sdk`. Default to latest Sonnet for cost-sensitive, Opus for quality-sensitive.
- RAG: chunk small, embed with voyage, store in pgvector. Test retrieval before shipping.
- Always add guardrails (input validation, output filtering, cost caps) before deploying AI features.

## Git & CI
- Conventional commits. Keep them short and meaningful.
- Never force push to main/master.
- Pre-commit: type-check → lint → test → build. All must pass.
- Handle CRLF correctly — check `.gitattributes` and formatter configs.

## Code Quality
- Files under 200 lines where possible. At 150, plan a split. At 300+, mandatory.
- Separate data/config from code. No inline content in components.
- Search for existing code before writing anything new. Extend, don't duplicate.
- Tests ship WITH code, not after.

## Multi-Workspace Awareness
- `C:\Workspace\Personal Projects\` — portfolio, tax engine, personal tools
- `C:\Workspace\Webdesign Business\` — client projects, business platform
- `C:\Workspace\Women Defining AI\` — WDAI platform (Next.js 16, Clerk, Prisma, Stripe)
- Changes in one workspace don't bleed into the other unless explicitly asked.

## External Repo CLAUDE.md — Mandatory Pre-Delegation Read
Before delegating any work to Builder/Designer/QA that touches a repo outside `C:\Workspace\agents\`, **Polaris reads that repo's CLAUDE.md end-to-end first**. Then the delegation prompt must:
1. Cite the specific CLAUDE.md sections that apply to the task (e.g. "Database Migration Safety > Updating Seed File", "Testing > Mocking Patterns").
2. Restate any project-specific constraints that could be missed (critical rules, convention lists, "NEVER do X" items).
3. Require the sub-agent to cite which sections they actually read in their report-back — they're all instrumented to include this field, and a missing citation means the task gets bounced back.

Rationale: Sub-agent definitions already tell them to read CLAUDE.md, but without Polaris pre-reading and citing, the sub-agent is discovering constraints blind — they can skim past sections that apply. Pre-reading shifts the burden to Polaris (who's already architecting the work) and gives the sub-agent a pre-filtered map. Two people reading the same CLAUDE.md independently is the audit trail.
