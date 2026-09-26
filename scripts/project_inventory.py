#!/usr/bin/env python3
"""Deterministic first-pass repository inventory for Project Structure Architect.

No third-party dependencies. It inventories paths, languages, manifests, likely tools,
root clutter, rough semantic roles, and import-like references. It intentionally does
not read secret/env file contents and does not modify the repository.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORES = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "env",
    "dist", "build", "out", ".next", ".nuxt", ".svelte-kit", ".astro", ".vite",
    ".turbo", ".cache", ".parcel-cache", "coverage", "target", "bin", "obj",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea",
    ".DS_Store", ".wrangler", ".alchemy", ".vercel", ".netlify"
}

SECRET_BASENAMES = {
    ".env", ".env.local", ".env.development", ".env.production", ".env.test",
    ".dev.vars", "credentials.json", "service-account.json"
}

LANG_BY_SUFFIX = {
    ".ts": "TypeScript", ".tsx": "TypeScript/TSX", ".mts": "TypeScript", ".cts": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript/JSX", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".py": "Python", ".go": "Go", ".rs": "Rust", ".php": "PHP", ".rb": "Ruby",
    ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin", ".cs": "C#", ".fs": "F#",
    ".swift": "Swift", ".c": "C", ".h": "C/C++ Header", ".cpp": "C++", ".cc": "C++",
    ".vue": "Vue SFC", ".svelte": "Svelte", ".astro": "Astro",
    ".css": "CSS", ".scss": "SCSS", ".sass": "Sass", ".less": "Less",
    ".html": "HTML", ".md": "Markdown", ".mdx": "MDX", ".sql": "SQL",
    ".json": "JSON", ".jsonc": "JSONC", ".yaml": "YAML", ".yml": "YAML",
    ".toml": "TOML", ".xml": "XML", ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell",
    ".ps1": "PowerShell", ".dockerfile": "Dockerfile"
}

MANIFEST_NAMES = {
    "package.json", "pnpm-workspace.yaml", "yarn.lock", "pnpm-lock.yaml", "package-lock.json",
    "bun.lock", "bun.lockb", "pyproject.toml", "requirements.txt", "poetry.lock", "uv.lock",
    "go.mod", "go.sum", "Cargo.toml", "Cargo.lock", "composer.json", "composer.lock",
    "Gemfile", "Gemfile.lock", "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle",
    "settings.gradle.kts", "Package.swift", "Podfile"
}

ROOT_ALLOWED_PATTERNS = [
    re.compile(r"^README(?:\..+)?$", re.I), re.compile(r"^LICENSE(?:\..+)?$", re.I),
    re.compile(r"^CHANGELOG(?:\..+)?$", re.I), re.compile(r"^CONTRIBUTING(?:\..+)?$", re.I),
    re.compile(r"^package\.json$"), re.compile(r"^(pnpm-lock\.yaml|yarn\.lock|package-lock\.json|bun\.lockb?|npm-shrinkwrap\.json)$"),
    re.compile(r"^(pyproject\.toml|poetry\.lock|uv\.lock|requirements(?:\..+)?\.txt)$"),
    re.compile(r"^(go\.mod|go\.sum|Cargo\.toml|Cargo\.lock|composer\.json|composer\.lock|Gemfile|Gemfile\.lock)$"),
    re.compile(r"^\.git(?:ignore|attributes|modules)$"), re.compile(r"^\.editorconfig$"),
]

TOOL_FILE_PATTERNS = {
    "Vite": [r"^vite\.config\.", r"/vite\.config\."],
    "Vitest": [r"^vitest\.config\.", r"/vitest\.config\."],
    "Playwright": [r"^playwright\.config\.", r"/playwright\.config\."],
    "Drizzle": [r"drizzle.*\.config\.", r"/drizzle/", r"/_journal\.json$"],
    "Prisma": [r"schema\.prisma$", r"/prisma/"],
    "Wrangler/Cloudflare": [r"^wrangler\.(toml|json|jsonc)$", r"/wrangler\.(toml|json|jsonc)$"],
    "Docker": [r"(^|/)Dockerfile", r"docker-compose", r"compose\.ya?ml$"],
    "GitHub Actions": [r"^\.github/workflows/"],
    "Tailwind": [r"tailwind\.config\.", r"@tailwind", r"@import\s+[\"']tailwindcss"],
    "TypeScript": [r"tsconfig.*\.json$"],
    "ESLint": [r"eslint\.config\.", r"\.eslintrc"],
    "Prettier": [r"prettier\.config\.", r"\.prettierrc"],
    "Alembic": [r"alembic\.ini$", r"/alembic/"],
    "Django": [r"manage\.py$", r"settings\.py$"],
}

PACKAGE_TOOL_DEPS = {
    "React": ["react", "react-dom"],
    "TanStack Start": ["@tanstack/react-start", "@tanstack/start"],
    "TanStack Router": ["@tanstack/react-router"],
    "TanStack Query": ["@tanstack/react-query"],
    "Vite": ["vite"],
    "Vitest": ["vitest"],
    "Playwright": ["@playwright/test", "playwright"],
    "Drizzle": ["drizzle-orm", "drizzle-kit"],
    "Prisma": ["prisma", "@prisma/client"],
    "Tailwind": ["tailwindcss"],
    "DaisyUI": ["daisyui"],
    "Wrangler/Cloudflare": ["wrangler", "@cloudflare/workers-types"],
    "Next.js": ["next"], "Nuxt": ["nuxt"], "SvelteKit": ["@sveltejs/kit"],
    "Astro": ["astro"], "Express": ["express"], "Fastify": ["fastify"],
    "Zod": ["zod"],
}

IMPORT_PATTERNS = [
    re.compile(r"\bfrom\s+[\"']([^\"']+)[\"']"),
    re.compile(r"\brequire\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"\bimport\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"^\s*import\s+([A-Za-z_][\w\.]*)", re.M),
]

TEXT_SUFFIXES = set(LANG_BY_SUFFIX) | {".txt", ".ini", ".conf"}

LEGACY_DOCUMENT_ROOTS = {
    "docs", "doc", "documentation", "tasks", "task", "plans", "planning",
    "specs", "specifications", "reports", "research", "decisions", "architecture",
    "notes", "audit", "audits"
}

@dataclass
class FileInfo:
    path: str
    size: int
    language: str
    role: str
    generated_likely: bool
    root_level: bool
    imports: list[str]


def is_ignored(rel: Path, extra_ignores: set[str]) -> bool:
    return any(part in DEFAULT_IGNORES or part in extra_ignores for part in rel.parts)


def is_secret_file(path: Path) -> bool:
    name = path.name
    return name in SECRET_BASENAMES or name.startswith(".env.") or name.endswith((".pem", ".key", ".p12", ".pfx"))


def language_for(path: Path) -> str:
    if path.name.lower() == "dockerfile" or path.name.lower().startswith("dockerfile."):
        return "Dockerfile"
    return LANG_BY_SUFFIX.get(path.suffix.lower(), "Other")


def likely_generated(rel: str) -> bool:
    s = rel.lower()
    markers = ["generated", "__generated__", ".gen.", "/gen/", "/dist/", "/build/", "routeTree.gen", ".d.ts"]
    return any(m.lower() in s for m in markers)


def classify_role(rel: str, lang: str, text: str = "") -> str:
    p = "/" + rel.lower().replace("\\", "/") + "/"
    name = Path(rel).name.lower()
    # Runtime folders are candidates requiring producer/consumer review, not source code.
    if rel.startswith("backups/"):
        return "recovery-backup"
    if rel.startswith("tmp/"):
        return "temporary-output-review-retention"
    if rel.startswith(".local/"):
        return "local-service-state"
    if rel.startswith("data/"):
        return "product-data-review-contents"
    if rel.startswith("documents/") or "/docs/" in p or lang in {"Markdown"}:
        return "documents"
    if rel.startswith("tests/") or "/test/" in p or "/tests/" in p or re.search(r"\.(test|spec)\.[^.]+$", name):
        return "tests"
    if rel.startswith("scripts/") or "/scripts/" in p:
        return "scripts"
    if rel.startswith("public/") or "/public/" in p:
        return "public"
    if re.search(r"(^|/)(migrations?|seeds?|snapshots?)(/|$)", rel.lower()) or lang == "SQL":
        return "db-artifact"
    if any(k in p for k in ["/components/", "/pages/", "/layouts/", "/views/", "/templates/", "/hooks/", "/styles/", "/charts/"]):
        return "view"
    if lang in {"TypeScript/TSX", "JavaScript/JSX", "Vue SFC", "Svelte", "Astro"}:
        if re.search(r"\b(react|react-dom|vue|svelte|solid-js)\b", text) or re.search(r"<\w+[\s>]", text):
            if "route" in p or "/routes/" in p:
                return "view-route"
            return "view"
    if any(k in p for k in ["/routes/", "/router/", "/controllers/"]):
        return "entry-or-view-route"
    if any(k in p for k in ["/domain/", "/entities/", "/value-objects/", "/policies/"]):
        return "business-domain"
    if any(k in p for k in ["/services/", "/use-cases/", "/usecases/"]):
        return "business-service"
    if any(k in p for k in ["/workflows/", "/pipelines/"]):
        return "business-workflow"
    if any(k in p for k in ["/repositories/", "/repository/"]):
        return "business-repository"
    if any(k in p for k in ["/providers/", "/integrations/", "/adapters/"]):
        return "business-provider-or-adapter"
    if any(k in p for k in ["/database/", "/db/", "/schema/"]) or re.search(r"\b(drizzle-orm|prisma|sqlalchemy|diesel|entityframework|knex|kysely)\b", text, re.I):
        return "business-database"
    if any(k in p for k in ["/auth/", "/authorization/", "/authentication/"]):
        return "business-auth"
    if any(k in p for k in ["/validation/", "/validators/"]):
        return "business-validation"
    if any(k in p for k in ["/jobs/", "/workers/", "/cron/"]):
        return "business-job-or-entry"
    if re.search(r"(config|\.config\.|tsconfig|wrangler|eslint|prettier)", name):
        return "config"
    if name in MANIFEST_NAMES:
        return "root-manifest-or-lock"
    return "unclassified"


def safe_read_text(path: Path, max_bytes: int = 250_000) -> str:
    if is_secret_file(path) or path.stat().st_size > max_bytes:
        return ""
    if path.suffix.lower() not in TEXT_SUFFIXES and language_for(path) == "Other":
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def parse_imports(text: str, limit: int = 40) -> list[str]:
    found: list[str] = []
    seen = set()
    for pat in IMPORT_PATTERNS:
        for m in pat.finditer(text):
            val = m.group(1)
            if val not in seen:
                seen.add(val)
                found.append(val)
                if len(found) >= limit:
                    return found
    return found


def detect_package_tools(root: Path) -> tuple[list[str], dict]:
    pkg = root / "package.json"
    if not pkg.exists():
        return [], {}
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return [], {}
    deps = {}
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        deps.update(data.get(key, {}) or {})
    tools = []
    for tool, names in PACKAGE_TOOL_DEPS.items():
        if any(name in deps for name in names):
            tools.append(tool)
    return sorted(set(tools)), data


def scan(root: Path, scan_depth: int, extra_ignores: set[str]) -> dict:
    files: list[FileInfo] = []
    languages = Counter()
    roles = Counter()
    manifests = []
    root_items = []
    root_clutter = []
    skill_files = []
    detected_tools = set()
    package_tools, package_json = detect_package_tools(root)
    detected_tools.update(package_tools)

    for cur, dirs, names in os.walk(root):
        curp = Path(cur)
        rel_dir = curp.relative_to(root)
        dirs[:] = [d for d in dirs if not is_ignored(rel_dir / d, extra_ignores)]
        if scan_depth >= 0 and len(rel_dir.parts) >= scan_depth:
            dirs[:] = []
        for name in names:
            path = curp / name
            relp = path.relative_to(root)
            if is_ignored(relp, extra_ignores):
                continue
            rel = relp.as_posix()
            root_level = len(relp.parts) == 1
            if root_level:
                root_items.append(rel)
            if name in MANIFEST_NAMES or name.endswith((".csproj", ".sln", ".fsproj")):
                manifests.append(rel)
            if name.lower() == "skill.md":
                skill_files.append(rel)
            lang = language_for(path)
            try:
                size = path.stat().st_size
            except OSError:
                continue
            text = safe_read_text(path)
            role = classify_role(rel, lang, text)
            imports = parse_imports(text)
            info = FileInfo(rel, size, lang, role, likely_generated(rel), root_level, imports)
            files.append(info)
            languages[lang] += 1
            roles[role] += 1
            normalized = rel.replace("\\", "/")
            for tool, patterns in TOOL_FILE_PATTERNS.items():
                if any(re.search(p, normalized, re.I) or (text and re.search(p, text, re.I)) for p in patterns):
                    detected_tools.add(tool)

    for item in root_items:
        name = Path(item).name
        if any(p.search(name) for p in ROOT_ALLOWED_PATTERNS):
            continue
        if name in SECRET_BASENAMES or name.startswith(".env"):
            continue
        root_clutter.append(item)

    legacy_document_roots = []
    canonical_document_root = (root / "documents").exists()
    try:
        for entry in root.iterdir():
            if entry.name.lower() in LEGACY_DOCUMENT_ROOTS:
                legacy_document_roots.append(entry.name + ("/" if entry.is_dir() else ""))
    except OSError:
        pass

    return {
        "root": str(root),
        "file_count": len(files),
        "languages": dict(languages.most_common()),
        "roles": dict(roles.most_common()),
        "manifests": sorted(manifests),
        "detected_tools": sorted(detected_tools),
        "package_scripts": (package_json.get("scripts", {}) if package_json else {}),
        "root_items": sorted(root_items),
        "root_clutter_candidates": sorted(root_clutter),
        "canonical_documents_root_present": canonical_document_root,
        "legacy_document_roots": sorted(legacy_document_roots),
        "skill_files": sorted(skill_files),
        "files": [asdict(f) for f in files],
    }


def build_tree(root: Path, max_depth: int, extra_ignores: set[str]) -> list[str]:
    lines = [root.name + "/"]

    def walk(dirp: Path, prefix: str, depth: int) -> None:
        if max_depth >= 0 and depth >= max_depth:
            return
        try:
            entries = [e for e in dirp.iterdir() if not is_ignored(e.relative_to(root), extra_ignores)]
        except OSError:
            return
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
        for idx, entry in enumerate(entries):
            last = idx == len(entries) - 1
            connector = "└── " if last else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(prefix + connector + entry.name + suffix)
            if entry.is_dir():
                walk(entry, prefix + ("    " if last else "│   "), depth + 1)

    walk(root, "", 0)
    return lines


def to_markdown(data: dict, tree: list[str]) -> str:
    out = []
    out.append("# Project Inventory\n")
    out.append(f"**Root:** `{data['root']}`  ")
    out.append(f"**Files inventoried:** {data['file_count']}\n")
    out.append("## Current structure\n")
    out.append("```text")
    out.extend(tree)
    out.append("```\n")

    out.append("## Detected tools / frameworks\n")
    if data["detected_tools"]:
        out.extend(f"- {x}" for x in data["detected_tools"])
    else:
        out.append("- None confidently detected by deterministic scan")
    out.append("")

    out.append("## Languages / file types\n")
    out.append("| Language/type | Files |")
    out.append("|---|---:|")
    for k, v in data["languages"].items():
        out.append(f"| {k} | {v} |")
    out.append("")

    out.append("## Heuristic roles\n")
    out.append("| Role | Files |")
    out.append("|---|---:|")
    for k, v in data["roles"].items():
        out.append(f"| {k} | {v} |")
    out.append("")

    out.append("## Manifests / lockfiles\n")
    out.extend(f"- `{x}`" for x in data["manifests"] or ["(none detected)"])
    out.append("")

    out.append("## Root clutter candidates\n")
    if data["root_clutter_candidates"]:
        out.extend(f"- `{x}`" for x in data["root_clutter_candidates"])
    else:
        out.append("- None detected by baseline rules")
    out.append("")

    out.append("## Document-root normalization candidates\n")
    out.append(f"- Canonical `documents/` present: {'yes' if data.get('canonical_documents_root_present') else 'no'}")
    if data.get("legacy_document_roots"):
        out.extend(f"- Legacy/competing root: `{x}`" for x in data["legacy_document_roots"])
    else:
        out.append("- No legacy top-level document/task roots detected")
    out.append("")

    out.append("## Installed skill files\n")
    if data.get("skill_files"):
        out.extend(f"- `{x}`" for x in data["skill_files"])
        out.append("- Run `scripts/document_path_audit.py` to identify document/task path literals inside these skills.")
    else:
        out.append("- None detected")
    out.append("")

    if data.get("package_scripts"):
        out.append("## Package scripts\n")
        out.append("| Script | Command |")
        out.append("|---|---|")
        for k, v in sorted(data["package_scripts"].items()):
            out.append(f"| `{k}` | `{str(v).replace('|', '\\|')}` |")
        out.append("")

    out.append("## File classifications\n")
    out.append("| Path | Language | Role | Generated? | Imports (sample) |")
    out.append("|---|---|---|---|---|")
    for f in data["files"]:
        imports = ", ".join(f["imports"][:6]).replace("|", "\\|")
        out.append(f"| `{f['path']}` | {f['language']} | {f['role']} | {'yes' if f['generated_likely'] else 'no'} | {imports} |")
    out.append("")
    out.append("> Heuristic classifications are an inventory aid, not the final architectural decision. Inspect source semantics, callers, manifests, and framework constraints before moving files.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory a repository without modifying it.")
    ap.add_argument("project", nargs="?", default=".", help="Project root (default: current directory)")
    ap.add_argument("--format", choices=["json", "md"], default="md")
    ap.add_argument("--output", "-o", help="Write output to a file instead of stdout")
    ap.add_argument("--max-depth", type=int, default=5, help="Displayed tree depth; -1 for unlimited")
    ap.add_argument("--scan-depth", type=int, default=-1, help="Inventory scan depth; -1 for unlimited (default)")
    ap.add_argument("--ignore", action="append", default=[], help="Additional directory basename to ignore; repeatable")
    args = ap.parse_args()

    root = Path(args.project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    extra = set(args.ignore)
    data = scan(root, args.scan_depth, extra)
    tree = build_tree(root, args.max_depth, extra)
    rendered = json.dumps({**data, "tree": tree}, indent=2) if args.format == "json" else to_markdown(data, tree)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
