#!/usr/bin/env python3
"""Lightweight architecture-boundary checker.

Checks common import strings for canonical Project Structure Architect boundaries.
It is intentionally conservative and is not a replacement for the language's compiler,
linter, or a full dependency graph. Exit code 1 means violations were found.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

IGNORES = {
    ".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "out",
    ".next", ".nuxt", ".svelte-kit", ".astro", ".vite", ".turbo", "coverage",
    "target", "bin", "obj", "__pycache__", ".pytest_cache", ".wrangler"
}

CODE_SUFFIXES = {
    ".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".go", ".rs", ".php", ".rb", ".java", ".kt", ".kts", ".cs", ".swift"
}

STRING_IMPORTS = [
    re.compile(r"\bfrom\s+[\"']([^\"']+)[\"']"),
    re.compile(r"\brequire\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"\bimport\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"^\s*import\s+([A-Za-z_][\w\./@~-]*)", re.M),
    re.compile(r"\buse\s+([A-Za-z_][\w:]*)", re.M),
]

DB_PACKAGE_MARKERS = (
    "drizzle-orm", "@prisma/client", "prisma", "kysely", "knex", "sequelize",
    "typeorm", "sqlalchemy", "django.db", "gorm", "diesel", "sqlx", "entityframework",
)

UI_PACKAGE_MARKERS = (
    "react", "react-dom", "vue", "svelte", "solid-js", "@angular/", "preact",
)

@dataclass
class Violation:
    file: str
    rule: str
    evidence: str


def imports(text: str) -> list[str]:
    out=[]
    seen=set()
    for pat in STRING_IMPORTS:
        for m in pat.finditer(text):
            x=m.group(1)
            if x not in seen:
                seen.add(x); out.append(x)
    return out


def under(rel: str, prefix: str) -> bool:
    rel = rel.strip("/").replace("\\", "/")
    prefix = prefix.strip("/").replace("\\", "/")
    return rel == prefix or rel.startswith(prefix + "/")


def looks_like_view_ref(imp: str, view_path: str) -> bool:
    needles = ["/view/", "@view/", "~/view/", "@/view/"]
    base = Path(view_path).name
    needles += [f"/{base}/"]
    return any(n in imp.replace("\\", "/") for n in needles)


def looks_like_database_ref(imp: str) -> bool:
    s=imp.lower().replace("\\", "/")
    return any(x in s for x in ("/database/", "@database/", "~/database/", "@/business/database/", "/business/database/")) or any(x in s for x in DB_PACKAGE_MARKERS)


def scan(root: Path, business_path: str, view_path: str) -> list[Violation]:
    violations=[]
    for cur, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORES and not (Path(cur) == root and d in {"data", "tmp", "backups", ".local"})]
        curp=Path(cur)
        for name in files:
            p=curp/name
            if p.suffix.lower() not in CODE_SUFFIXES:
                continue
            rel=p.relative_to(root).as_posix()
            try:
                text=p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            imps=imports(text)

            if under(rel, business_path):
                for imp in imps:
                    if looks_like_view_ref(imp, view_path):
                        violations.append(Violation(rel, "BUSINESS_IMPORTS_VIEW", imp))
                low=text.lower()
                if any(re.search(rf"(^|[\"'/@]){re.escape(pkg)}([/\"']|$)", low) for pkg in UI_PACKAGE_MARKERS):
                    # Package-level UI imports in business are suspicious; allow reporting for manual review.
                    for imp in imps:
                        if any(imp.lower()==pkg or imp.lower().startswith(pkg + "/") for pkg in UI_PACKAGE_MARKERS):
                            violations.append(Violation(rel, "BUSINESS_IMPORTS_UI_FRAMEWORK", imp))

            if under(rel, view_path):
                for imp in imps:
                    if looks_like_database_ref(imp):
                        violations.append(Violation(rel, "VIEW_IMPORTS_DATABASE_DIRECTLY", imp))

    return violations


def main() -> int:
    ap=argparse.ArgumentParser(description="Check canonical business/view dependency boundaries.")
    ap.add_argument("project", nargs="?", default=".")
    ap.add_argument("--business", default="app/business")
    ap.add_argument("--view", default="app/view")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args=ap.parse_args()
    root=Path(args.project).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr); return 2
    violations=scan(root,args.business,args.view)
    if args.format=="json":
        import json
        print(json.dumps([v.__dict__ for v in violations], indent=2))
    else:
        if not violations:
            print("PASS: no heuristic architecture-boundary violations detected")
        else:
            print(f"FAIL: {len(violations)} heuristic architecture-boundary violation(s)")
            for v in violations:
                print(f"- {v.rule}: {v.file} -> {v.evidence}")
    return 1 if violations else 0

if __name__ == "__main__":
    raise SystemExit(main())
