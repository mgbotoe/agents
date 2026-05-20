#!/usr/bin/env python3
"""inventory-repo: deep-read a repo before claiming what it contains.

For when shallow scan (ls + package.json regex) isn't enough — i.e. before
producing a diagram, table, summary, or "current state" answer about a repo.

Reads:
- Every workflow YAML in .github/workflows/  (extracts on:, first job step)
- package.json deps fully (categorized: framework / auth / db / monitoring / etc)
- top of README.md (first 80 lines)
- CLAUDE.md if present (first 80 lines)
- packages/*/package.json + READMEs if monorepo
- deploy markers: vercel.json, railway.json, fly.toml, Dockerfile
- DB markers: prisma/schema.prisma, supabase/, postgres mentions in .env.example

Usage:
    python .claude/scripts/inventory-repo.py <repo-path>

Outputs structured markdown to stdout. No cache — read-only.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

DEV_AGENT_ROOT = Path(__file__).resolve().parent.parent.parent
INVOCATION_STATE = DEV_AGENT_ROOT / ".claude" / "state" / "inventory-invocations.json"

# Optional yaml; fall back to regex if not installed
try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# Categorize deps by purpose so the dep section is readable
DEP_CATEGORIES = [
    ("Framework", re.compile(r"^(next|react|react-dom|vue|svelte|fastify|express|hono|nestjs|@nestjs|astro)$")),
    ("Auth", re.compile(r"^(@clerk|@auth|next-auth|@supabase/auth|firebase-auth|lucia)")),
    ("Database / ORM", re.compile(r"^(prisma|@prisma|drizzle|kysely|@supabase|mongoose|sequelize|pg|mysql|sqlite|knex)")),
    ("Payments", re.compile(r"^(stripe|@stripe|paddle|paypal)")),
    ("Email / Messaging", re.compile(r"^(@mailchimp|mailchimp|resend|sendgrid|postmark|@slack|nodemailer)")),
    ("LLM / AI", re.compile(r"^(@anthropic|openai|@anthropic-ai|@openai|langchain|@google-ai|ollama)")),
    ("Monitoring", re.compile(r"^(@sentry|posthog-js|@posthog|@datadog|@vercel/analytics|mixpanel|amplitude)")),
    ("Storage", re.compile(r"^(@vercel/blob|@aws-sdk/client-s3|aws-sdk|@google-cloud/storage)")),
    ("Integration APIs", re.compile(r"^(airtable|googleapis|google-spreadsheet|@octokit|@linear|notion|@pinecone)")),
    ("Testing", re.compile(r"^(vitest|jest|playwright|cypress|@testing-library|mocha|chai)")),
    ("Build / tooling", re.compile(r"^(turbo|@turbo|biome|@biomejs|prettier|eslint|typescript|tsx|tsup|esbuild|webpack|vite|swc)")),
]


def categorize_dep(name: str) -> str:
    for label, pattern in DEP_CATEGORIES:
        if pattern.match(name):
            return label
    return "Other"


def read_workflow_yaml(path: Path) -> dict:
    """Return {triggers: [...], first_step: 'name or run cmd', job_count: N, raw_lines: N}."""
    text = path.read_text(encoding="utf-8", errors="replace")
    result = {
        "name": path.name,
        "triggers": [],
        "first_step_name": None,
        "first_step_run": None,
        "job_count": 0,
        "raw_lines": len(text.splitlines()),
    }
    if HAS_YAML:
        try:
            data = yaml.safe_load(text)
            if isinstance(data, dict):
                on = data.get("on") or data.get(True)  # PyYAML may parse 'on' as bool True
                if isinstance(on, str):
                    result["triggers"].append(on)
                elif isinstance(on, list):
                    result["triggers"].extend(str(t) for t in on)
                elif isinstance(on, dict):
                    for k, v in on.items():
                        if isinstance(v, dict) and "cron" in v.get("schedule", [{}])[0]:
                            crons = [s.get("cron") for s in v.get("schedule", []) if isinstance(s, dict)]
                            result["triggers"].append(f"{k} ({', '.join(c for c in crons if c)})")
                        elif k == "schedule" and isinstance(v, list):
                            crons = [s.get("cron") for s in v if isinstance(s, dict) and "cron" in s]
                            result["triggers"].append(f"schedule ({', '.join(c for c in crons if c)})")
                        else:
                            result["triggers"].append(str(k))
                jobs = data.get("jobs") or {}
                result["job_count"] = len(jobs) if isinstance(jobs, dict) else 0
                if isinstance(jobs, dict):
                    for _, job in jobs.items():
                        if not isinstance(job, dict):
                            continue
                        steps = job.get("steps") or []
                        if steps and isinstance(steps[0], dict):
                            first = steps[0]
                            result["first_step_name"] = first.get("name") or first.get("uses")
                            run = first.get("run")
                            if run:
                                result["first_step_run"] = run.splitlines()[0] if run else None
                            break
        except Exception as exc:
            result["parse_error"] = str(exc)
    else:
        # Regex fallback
        on_match = re.search(r"^on:\s*(.+)$", text, re.MULTILINE)
        if on_match:
            result["triggers"].append(on_match.group(1).strip())
        cron_matches = re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", text)
        result["triggers"].extend(f"cron: {c}" for c in cron_matches)
        step_name = re.search(r"^\s+-\s+name:\s*(.+)$", text, re.MULTILINE)
        if step_name:
            result["first_step_name"] = step_name.group(1).strip()
    return result


def read_package_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": str(e)}
    deps_all: dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        section = data.get(key) or {}
        if isinstance(section, dict):
            for n, v in section.items():
                if n not in deps_all:
                    deps_all[n] = v
    categorized: dict[str, list[tuple[str, str]]] = {}
    for name, version in sorted(deps_all.items()):
        cat = categorize_dep(name)
        categorized.setdefault(cat, []).append((name, version))
    return {
        "name": data.get("name"),
        "version": data.get("version"),
        "description": data.get("description"),
        "scripts": list((data.get("scripts") or {}).keys())[:15],
        "deps_categorized": categorized,
        "total_deps": len(deps_all),
        "main": data.get("main") or data.get("module"),
    }


def detect_deploy_target(repo: Path) -> list[str]:
    markers = []
    if (repo / "vercel.json").exists():
        markers.append("Vercel (vercel.json)")
    if (repo / "railway.json").exists() or (repo / "railway.toml").exists():
        markers.append("Railway (railway.json/toml)")
    if (repo / "fly.toml").exists():
        markers.append("Fly.io (fly.toml)")
    if (repo / "Dockerfile").exists():
        markers.append("Docker (Dockerfile)")
    if (repo / "serverless.yml").exists() or (repo / "serverless.yaml").exists():
        markers.append("Serverless (serverless.yml)")
    if (repo / "netlify.toml").exists() or (repo / "_netlify").exists():
        markers.append("Netlify (netlify.toml)")
    if (repo / "wrangler.toml").exists() or (repo / "wrangler.jsonc").exists():
        markers.append("Cloudflare Workers (wrangler)")
    # Heroku indicators
    if (repo / "Procfile").exists():
        markers.append("Heroku-style (Procfile)")
    return markers


def detect_database(repo: Path) -> list[str]:
    markers = []
    schema = list(repo.glob("**/prisma/schema.prisma"))
    if schema:
        markers.append(f"Prisma ({len(schema)} schema file(s))")
    if (repo / "supabase").exists():
        markers.append("Supabase (supabase/ directory)")
    if (repo / "migrations").exists() and not schema:
        markers.append("SQL migrations (migrations/)")
    # .env.example for DB hints
    for env_path in (repo / ".env.example", repo / "web" / ".env.example"):
        if env_path.exists():
            try:
                content = env_path.read_text(encoding="utf-8", errors="replace")
                if "DATABASE_URL" in content or "POSTGRES" in content.upper():
                    markers.append(f"Postgres URL in {env_path.relative_to(repo)}")
                if "REDIS" in content.upper():
                    markers.append(f"Redis URL in {env_path.relative_to(repo)}")
            except Exception:
                pass
            break  # only need one env example
    return markers


def head(path: Path, lines: int = 80) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    out = text.splitlines()[:lines]
    return "\n".join(out)


def find_monorepo_packages(repo: Path) -> list[dict]:
    """If repo is a monorepo (has packages/ or apps/), enumerate sub-packages."""
    results = []
    for parent_name in ("packages", "apps"):
        parent = repo / parent_name
        if not parent.is_dir():
            continue
        for sub in sorted(parent.iterdir()):
            if not sub.is_dir():
                continue
            pj = sub / "package.json"
            readme = sub / "README.md"
            entry = {
                "kind": parent_name,
                "name": sub.name,
                "path": f"{parent_name}/{sub.name}",
                "has_package_json": pj.exists(),
                "has_readme": readme.exists(),
            }
            if pj.exists():
                try:
                    data = json.loads(pj.read_text(encoding="utf-8"))
                    entry["pkg_name"] = data.get("name")
                    entry["pkg_description"] = data.get("description")
                except Exception:
                    pass
            if readme.exists():
                entry["readme_head"] = head(readme, lines=10)
            results.append(entry)
    return results


def render_report(repo: Path) -> str:
    lines = []
    lines.append(f"# inventory-repo: {repo.name}")
    lines.append("")
    lines.append(f"**Path:** `{repo}`")
    lines.append("")

    # Deploy + DB
    deploy = detect_deploy_target(repo)
    db = detect_database(repo)
    lines.append("## Deployment + storage")
    lines.append("")
    lines.append(f"- **Deploy target(s):** {', '.join(deploy) if deploy else 'unknown / not detected'}")
    lines.append(f"- **Database:** {', '.join(db) if db else 'none detected'}")
    lines.append("")

    # Top-level package.json
    pj_path = repo / "package.json"
    if pj_path.exists():
        info = read_package_json(pj_path)
        lines.append("## package.json (root)")
        lines.append("")
        lines.append(f"- **Name:** `{info.get('name')}`")
        lines.append(f"- **Version:** {info.get('version')}")
        if info.get("description"):
            lines.append(f"- **Description:** {info['description']}")
        lines.append(f"- **Total deps:** {info.get('total_deps')}")
        if info.get("scripts"):
            lines.append(f"- **Scripts:** {', '.join(info['scripts'])}")
        lines.append("")
        lines.append("### Dependencies by category")
        deps = info.get("deps_categorized") or {}
        # Show non-Other categories first
        ordered = [c for c, _ in DEP_CATEGORIES if c in deps]
        if "Other" in deps:
            ordered.append("Other")
        for cat in ordered:
            entries = deps.get(cat) or []
            if not entries:
                continue
            lines.append(f"- **{cat}:** " + ", ".join(f"`{n}`" for n, _ in entries))
        lines.append("")

    # Monorepo sub-packages
    sub_packages = find_monorepo_packages(repo)
    if sub_packages:
        lines.append(f"## Monorepo packages ({len(sub_packages)})")
        lines.append("")
        for p in sub_packages:
            lines.append(f"### `{p['path']}`")
            if p.get("pkg_name") and p["pkg_name"] != p["name"]:
                lines.append(f"- npm name: `{p['pkg_name']}`")
            if p.get("pkg_description"):
                lines.append(f"- description: {p['pkg_description']}")
            if p.get("readme_head"):
                rh = p["readme_head"].strip()
                if rh:
                    lines.append(f"- README excerpt:")
                    lines.append("  ```")
                    for ln in rh.splitlines()[:6]:
                        lines.append(f"  {ln}")
                    lines.append("  ```")
            lines.append("")

    # Workflows
    wf_dir = repo / ".github" / "workflows"
    if wf_dir.is_dir():
        workflows = sorted([w for w in wf_dir.iterdir() if w.suffix in (".yml", ".yaml")])
        lines.append(f"## GitHub workflows ({len(workflows)})")
        lines.append("")
        for w in workflows:
            info = read_workflow_yaml(w)
            triggers = ", ".join(info["triggers"]) if info["triggers"] else "unknown"
            first = info.get("first_step_name") or info.get("first_step_run") or "(no first step detected)"
            lines.append(f"### `{info['name']}`")
            lines.append(f"- **Triggers:** {triggers}")
            lines.append(f"- **Jobs:** {info['job_count']}")
            lines.append(f"- **First step:** {first}")
            if info.get("parse_error"):
                lines.append(f"- ⚠ parse error: {info['parse_error']}")
            lines.append("")
    else:
        lines.append("## GitHub workflows")
        lines.append("")
        lines.append("None (no `.github/workflows/` directory).")
        lines.append("")

    # CLAUDE.md
    claude_md = repo / "CLAUDE.md"
    if claude_md.exists():
        lines.append("## CLAUDE.md (excerpt, first 80 lines)")
        lines.append("")
        lines.append("```markdown")
        lines.append(head(claude_md, 80))
        lines.append("```")
        lines.append("")

    # README
    readme = repo / "README.md"
    if readme.exists():
        lines.append("## README.md (excerpt, first 80 lines)")
        lines.append("")
        lines.append("```markdown")
        lines.append(head(readme, 80))
        lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Generated by `inventory-repo.py`. Use this output before producing diagrams, tables, or 'current state' summaries about this repo._")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: inventory-repo.py <repo-path>", file=sys.stderr)
        return 1
    try:
        repo = Path(argv[1]).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        print(f"Could not resolve repo path: {exc}", file=sys.stderr)
        return 1
    if not repo.is_dir():
        print(f"Not a directory: {repo}", file=sys.stderr)
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(render_report(repo))
    # Track invocation so post-response-audit Stop hook can verify discipline
    try:
        INVOCATION_STATE.parent.mkdir(parents=True, exist_ok=True)
        invocations: dict = {}
        if INVOCATION_STATE.exists():
            try:
                invocations = json.loads(INVOCATION_STATE.read_text(encoding="utf-8"))
            except Exception:
                invocations = {}
        invocations[str(repo)] = time.time()
        INVOCATION_STATE.write_text(json.dumps(invocations, indent=2), encoding="utf-8")
    except Exception:
        pass  # state tracking best-effort; don't fail the report
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
