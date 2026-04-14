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
- Changes in one workspace don't bleed into the other unless explicitly asked.
- Always read the project's CLAUDE.md first to understand local conventions.
