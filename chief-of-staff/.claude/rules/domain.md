# Domain Rules — Chief of Staff

## Full-Stack Web Development
- TypeScript strict mode, always. No `any` types.
- Next.js App Router by default. Pages Router only if there's a reason.
- Supabase for auth + DB. PostgreSQL via Prisma or raw SQL — pick based on complexity.
- FastAPI for Python backends. Type hints everywhere.
- Tailwind for styling. No CSS modules unless forced by a library.

## AI/ML Integration
- Claude API via `@anthropic-ai/sdk`. Default to latest Sonnet for cost-sensitive, Opus for quality-sensitive.
- RAG: chunk small, embed with voyage, store in pgvector. Test retrieval before shipping.
- Always add guardrails (input validation, output filtering, cost caps) before deploying AI features.

## Web Design Business
- Client delivery: scope it, build it, ship it. No scope creep without a conversation.
- Keep client work isolated per project. Don't cross-pollinate configs or dependencies.
- Brand consistency matters — check the client's guidelines before touching their UI.

## Two-Workspace Awareness
- `C:\Workspace\Personal Projects\` — portfolio, tax engine, personal tools
- `C:\Workspace\Webdesign Business\` — client projects, business platform
- Changes in one workspace don't bleed into the other unless explicitly asked.

## General Standards
- Biome for formatting/linting in JS/TS projects. Ruff for Python.
- Conventional commits. Keep them short.
- If it touches money (invoicing, tax), triple-check the math and add tests.
