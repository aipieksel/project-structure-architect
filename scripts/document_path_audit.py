#!/usr/bin/env python3
"""Audit repository references to documentation/task paths and optionally rewrite safe mappings.

Designed for Project Structure Architect. The default mode is read-only. It scans skill
instructions and other textual path consumers, identifies legacy/competing document roots,
recommends canonical paths under documents/, and lists skills that must be updated.

Safe automatic mappings:
  docs/tasks/**        -> documents/tasks/**
  docs/documentation/** -> documents/documentation/**
  documentation/**     -> documents/documentation/**

Generic docs/**, tasks/**, specs/**, plans/**, reports/**, etc. are reported for semantic
classification rather than blindly rewritten.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path

IGNORES = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "env",
    "dist", "build", "out", ".next", ".nuxt", ".svelte-kit", ".astro", ".vite",
    ".turbo", ".cache", ".parcel-cache", "coverage", "target", "bin", "obj",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea",
    ".DS_Store", ".wrangler", ".alchemy", ".vercel", ".netlify", "__MACOSX",
}

TEXT_SUFFIXES = {
    ".md", ".mdx", ".txt", ".yaml", ".yml", ".json", ".jsonc", ".toml", ".ini",
    ".conf", ".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".sh", ".bash", ".zsh", ".ps1", ".go", ".rs", ".php", ".rb",
    ".java", ".kt", ".kts", ".cs", ".swift", ".xml", ".html", ".css", ".sql",
}

# Exact/structurally safe normalization rules. Order matters: more specific first.
SAFE_RULES = [
    (re.compile(r"(?<![A-Za-z0-9_.-])docs/documentation(?=(?:/|\\))", re.I), "documents/documentation", "SAFE_REWRITE"),
    (re.compile(r"(?<![A-Za-z0-9_.-])docs/tasks(?=(?:/|\\|`|'|\"|$))", re.I), "documents/tasks", "SAFE_REWRITE"),
    (re.compile(r"(?<![A-Za-z0-9_.-])documentation(?=(?:/|\\))", re.I), "documents/documentation", "SAFE_REWRITE"),
]

# Path-like references that are document-related but need semantic classification.
REVIEW_PREFIXES = {
    "docs": "documents/<classified-category>",
    "doc": "documents/<classified-category>",
    "tasks": "documents/tasks",
    "task": "documents/tasks",
    "plans": "documents/tasks/<appropriate-subtree>",
    "planning": "documents/tasks/<appropriate-subtree>",
    "specs": "documents/documentation/specifications",
    "specifications": "documents/documentation/specifications",
    "reports": "documents/reports",
    "report": "documents/reports",
    "research": "documents/research",
    "decisions": "documents/documentation/decisions",
    "adr": "documents/documentation/decisions",
    "adrs": "documents/documentation/decisions",
    "architecture": "documents/documentation/architecture",
    "notes": "documents/notes",
    "audit": "documents/audits",
    "audits": "documents/audits",
}

CANONICAL_PREFIXES = ("documents/", "documents\\")

PATH_TOKEN = re.compile(
    r"(?P<path>(?:\.?\.?/)?(?:docs?|documentation|documents|tasks?|plans?|planning|specs?|specifications|reports?|research|decisions|adrs?|architecture|notes|audits?)(?:[/\\][A-Za-z0-9_@.{}<>*+\-]+)+[/\\]?)",
    re.I,
)

SKILL_HINTS = ("/skills/", "\\skills\\")
SELF_SKILL_NAMES = {"project-structure-architect"}

DOC_POLICY_RE = re.compile(r"\b(documentation|docs?|documents|task(?:s|[- ]system)?|planning|evidence|lessons?|reports?|audits?|research|specifications?|architecture)\b", re.I)
STRUCTURAL_POLICY_RE = re.compile(r"\b(root|under|beneath|inside|live|create|write|move|route|own|owns|folder|directory|path|must|should|remain|contain|store)\b", re.I)
CROSS_NAMESPACE_RE = re.compile(r"\b(task(?:s|[- ]system)?|planning|evidence|logs?|lessons?|reports?|audits?|migrations?|backups?)\b", re.I)

@dataclass
class Occurrence:
    file: str
    line: int
    consumer_type: str
    skill: str | None
    current: str
    recommended: str
    status: str
    context: str


def ignored(rel: Path) -> bool:
    return any(part in IGNORES for part in rel.parts)


def is_text_file(path: Path) -> bool:
    return path.name in {"SKILL.md", "AGENTS.md", "CLAUDE.md", "README", "README.md"} or path.suffix.lower() in TEXT_SUFFIXES


def consumer_type(rel: str) -> str:
    s = "/" + rel.replace("\\", "/")
    low = s.lower()
    if low.endswith("/skill.md") or "/skills/" in low:
        return "skill"
    if low.endswith((".yaml", ".yml", ".json", ".jsonc", ".toml", ".ini", ".conf")):
        return "config/manifest"
    if "/scripts/" in low or low.endswith((".py", ".sh", ".bash", ".zsh", ".ps1")):
        return "script"
    if "/.github/workflows/" in low:
        return "ci"
    if low.endswith((".md", ".mdx", ".txt")):
        return "documentation/instructions"
    return "source"


def skill_name_for(rel: Path) -> str | None:
    parts = list(rel.parts)
    lower = [p.lower() for p in parts]
    if rel.name.lower() == "skill.md":
        return rel.parent.name
    if "skills" in lower:
        idx = len(lower) - 1 - lower[::-1].index("skills")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def normalize_slashes(s: str) -> str:
    return s.replace("\\", "/")


def classify_path(token: str) -> tuple[str, str]:
    norm = normalize_slashes(token)
    stripped = norm
    while stripped.startswith("./") or stripped.startswith("../"):
        stripped = stripped[2:] if stripped.startswith("./") else stripped[3:]
    low = stripped.lower()
    if low.startswith("documents/"):
        return norm, "CANONICAL"
    if low == "documents":
        return norm, "CANONICAL"

    # Safe mapping preserves any leading ./ or ../ and suffix.
    prefix = norm[: len(norm) - len(stripped)]
    for source, target in (
        ("docs/documentation", "documents/documentation"),
        ("docs/tasks", "documents/tasks"),
        ("documentation", "documents/documentation"),
    ):
        if low == source or low.startswith(source + "/"):
            suffix = stripped[len(source):]
            return prefix + target + suffix, "SAFE_REWRITE"

    first, _, rest = stripped.partition("/")
    target = REVIEW_PREFIXES.get(first.lower())
    if target:
        suffix = ("/" + rest) if rest else ""
        # Only preserve suffix where category semantics are direct enough.
        if first.lower() in {"tasks", "task"}:
            return prefix + "documents/tasks" + suffix, "REVIEW"
        if first.lower() in {"specs", "specifications"}:
            return prefix + "documents/documentation/specifications" + suffix, "REVIEW"
        if first.lower() in {"reports", "report"}:
            return prefix + "documents/reports" + suffix, "REVIEW"
        if first.lower() == "research":
            return prefix + "documents/research" + suffix, "REVIEW"
        if first.lower() in {"decisions", "adr", "adrs"}:
            return prefix + "documents/documentation/decisions" + suffix, "REVIEW"
        if first.lower() == "architecture":
            return prefix + "documents/documentation/architecture" + suffix, "REVIEW"
        if first.lower() in {"audit", "audits"}:
            return prefix + "documents/audits" + suffix, "REVIEW"
        return prefix + target, "REVIEW"
    return norm, "UNCLASSIFIED"


def scan(root: Path) -> dict:
    occurrences: list[Occurrence] = []
    scanned_files = 0
    path_consumers = Counter()
    skills_seen: set[str] = set()
    skills_to_update: dict[str, dict] = defaultdict(lambda: {"files": set(), "safe": 0, "review": 0, "occurrences": 0})
    policy_review_candidates: list[dict] = []

    for cur, dirs, names in os.walk(root):
        curp = Path(cur)
        rel_dir = curp.relative_to(root)
        dirs[:] = [d for d in dirs if not ignored(rel_dir / d)]
        for name in names:
            path = curp / name
            relp = path.relative_to(root)
            if ignored(relp) or not is_text_file(path):
                continue
            rel_parts = [x.lower() for x in relp.parts]
            if "skills" in rel_parts:
                idx = rel_parts.index("skills")
                if idx + 1 < len(rel_parts) and rel_parts[idx + 1] in SELF_SKILL_NAMES:
                    continue
            try:
                if path.stat().st_size > 1_500_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned_files += 1
            ctype = consumer_type(relp.as_posix())
            skill = skill_name_for(relp)
            if skill in SELF_SKILL_NAMES:
                # This skill intentionally contains legacy path examples and migration
                # rules; treating those examples as stale project-path consumers would
                # cause self-corruption during an apply pass.
                continue
            if skill:
                skills_seen.add(skill)
            lines = text.splitlines()
            for line_no, line in enumerate(lines, 1):
                seen_line: set[tuple[str, str]] = set()
                if skill and DOC_POLICY_RE.search(line) and STRUCTURAL_POLICY_RE.search(line):
                    # Semantic policy lines are not auto-rewritten. They are surfaced
                    # because a rule can still conflict with the new namespace even
                    # after every literal path is updated.
                    policy_review_candidates.append({
                        "skill": skill,
                        "file": relp.as_posix(),
                        "line": line_no,
                        "cross_namespace": bool(re.search(r"documentation|documents/documentation", line, re.I) and CROSS_NAMESPACE_RE.search(line)),
                        "context": line.strip()[:280],
                    })
                for match in PATH_TOKEN.finditer(line):
                    current = match.group("path")
                    norm_current = normalize_slashes(current)
                    root_name = norm_current.lstrip("./").split("/", 1)[0].lower()
                    before = line[max(0, match.start()-48):match.start()].lower().replace("\\", "/")
                    # Do not mistake a referenced skill path such as
                    # `.agents/skills/update-documentation/SKILL.md` for a documentation root.
                    if norm_current.lower().endswith("/skill.md") and ("/skills/" in before or before.endswith("skills/")):
                        continue
                    # Generic words such as "planning/review" or "architecture/source"
                    # are only path evidence when they are visibly path-like.
                    left = line[match.start()-1:match.start()] if match.start() else ""
                    right = line[match.end():match.end()+1]
                    quoted = left in {"`", "'", '"'} or right in {"`", "'", '"'}
                    visibly_pathlike = quoted or norm_current.startswith(("./", "../", "/")) or norm_current.endswith("/") or bool(re.search(r"\.[A-Za-z0-9]{1,8}(?:$|/)", norm_current))
                    if root_name not in {"docs", "doc", "documentation", "documents"} and not visibly_pathlike:
                        continue
                    if root_name == "documentation" and not visibly_pathlike:
                        # Avoid prose compounds like "documentation/lessons" unless
                        # punctuation/extension/trailing slash makes them real path literals.
                        continue
                    recommended, status = classify_path(current)
                    key = (current, status)
                    if key in seen_line:
                        continue
                    seen_line.add(key)
                    occurrence = Occurrence(
                        file=relp.as_posix(),
                        line=line_no,
                        consumer_type=ctype,
                        skill=skill,
                        current=current,
                        recommended=recommended,
                        status=status,
                        context=line.strip()[:240],
                    )
                    occurrences.append(occurrence)
                    path_consumers[ctype] += 1
                    if skill and status in {"SAFE_REWRITE", "REVIEW"}:
                        row = skills_to_update[skill]
                        row["files"].add(relp.as_posix())
                        row["occurrences"] += 1
                        row["safe" if status == "SAFE_REWRITE" else "review"] += 1

    # Physical root candidates and concrete move suggestions. Prefer exact nested
    # mappings for known legacy subsystems before flagging generic docs/ remainder.
    physical = []
    exact_physical = [
        ("documentation", "documents/documentation", "SAFE_REWRITE"),
        ("docs/documentation", "documents/documentation", "SAFE_REWRITE"),
        ("docs/tasks", "documents/tasks", "SAFE_REWRITE"),
    ]
    for current, recommended, status in exact_physical:
        p = root / current
        if p.exists():
            physical.append({
                "current": current + ("/" if p.is_dir() else ""),
                "recommended": recommended + ("/" if p.is_dir() else ""),
                "status": status,
                "type": "directory" if p.is_dir() else "file",
            })

    # Generic top-level roots still require semantic classification. Avoid a
    # duplicate docs/ row when it contains only the two exact known subtrees.
    generic_names = {"docs", "doc", "tasks", "task", "specs", "specifications", "plans", "planning", "reports", "research", "decisions", "architecture", "notes", "audit", "audits"}
    for name in sorted(generic_names):
        p = root / name
        if not p.exists():
            continue
        if name == "docs" and p.is_dir():
            try:
                leftovers = [x.name for x in p.iterdir() if x.name.lower() not in {"tasks", "documentation"}]
            except OSError:
                leftovers = ["<unknown>"]
            if not leftovers:
                continue
        recommended, status = classify_path(name + "/placeholder")
        recommended_root = recommended.rsplit("/placeholder", 1)[0]
        physical.append({
            "current": name + ("/" if p.is_dir() else ""),
            "recommended": recommended_root + ("/" if p.is_dir() else ""),
            "status": status,
            "type": "directory" if p.is_dir() else "file",
        })

    skill_rows = []
    for skill, row in sorted(skills_to_update.items()):
        skill_rows.append({
            "skill": skill,
            "files": sorted(row["files"]),
            "occurrences": row["occurrences"],
            "safe_rewrites": row["safe"],
            "review_required": row["review"],
        })

    return {
        "root": str(root),
        "scanned_text_files": scanned_files,
        "skills_seen": sorted(skills_seen),
        "skills_requiring_update": skill_rows,
        "physical_legacy_roots": physical,
        "consumer_counts": dict(path_consumers),
        "policy_review_candidates": policy_review_candidates,
        "occurrences": [asdict(x) for x in occurrences],
    }


def apply_safe_rewrites(root: Path, backup_suffix: str | None = None) -> list[dict]:
    changed = []
    for cur, dirs, names in os.walk(root):
        curp = Path(cur)
        rel_dir = curp.relative_to(root)
        dirs[:] = [d for d in dirs if not ignored(rel_dir / d)]
        for name in names:
            path = curp / name
            relp = path.relative_to(root)
            if ignored(relp) or not is_text_file(path):
                continue
            rel_parts = [x.lower() for x in relp.parts]
            if "skills" in rel_parts:
                idx = rel_parts.index("skills")
                if idx + 1 < len(rel_parts) and rel_parts[idx + 1] in SELF_SKILL_NAMES:
                    continue
            try:
                if path.stat().st_size > 1_500_000:
                    continue
                old = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            new = old
            replacements = 0
            for pattern, target, _ in SAFE_RULES:
                def repl(match: re.Match[str]) -> str:
                    nonlocal replacements
                    start = match.start()
                    before = new[max(0, start - 120):start].lower().replace("\\", "/")
                    # Canonical project paths are idempotent. The generic
                    # `documentation/**` rule must not match the second segment
                    # of `documents/documentation/**` on a later apply pass.
                    if before.endswith("documents/"):
                        return match.group(0)
                    # Relative links are interpreted from the consumer file's
                    # location, which may itself move during reorganization.
                    # Prefixing them mechanically can produce paths such as
                    # `../documents/documentation/...` that resolve nowhere.
                    if before.endswith(("./", "../")):
                        return match.group(0)
                    # A raw replacement inside a JavaScript-style regex literal
                    # can introduce an unescaped slash and make the source
                    # unparsable. Leave escaped-separator patterns for manual
                    # review instead of claiming they are safe to rewrite.
                    if new[match.end():match.end() + 2] == r"\/":
                        return match.group(0)
                    # Never rewrite skill installation paths themselves, e.g.
                    # `.agents/skills/documentation/SKILL.md`.
                    if re.search(r"(?:^|/)skills/[a-z0-9_.@+-]*$", before):
                        return match.group(0)
                    # Never rewrite a segment inside an external URL.
                    if re.search(r"https?://\S*$", before):
                        return match.group(0)
                    replacements += 1
                    return target
                new = pattern.sub(repl, new)
            if new != old:
                if backup_suffix:
                    shutil.copy2(path, path.with_name(path.name + backup_suffix))
                path.write_text(new, encoding="utf-8")
                changed.append({"file": relp.as_posix(), "replacements": replacements})
    return changed


def esc(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def to_markdown(data: dict, changes: list[dict] | None = None) -> str:
    out = ["# Document Path and Skill Reference Audit", ""]
    out.append(f"**Root:** `{data['root']}`  ")
    out.append(f"**Text files scanned:** {data['scanned_text_files']}  ")
    out.append(f"**Skills found:** {len(data['skills_seen'])}  ")
    out.append(f"**Skills requiring path updates:** {len(data['skills_requiring_update'])}")
    out.append("")
    out.append("## Canonical document namespaces")
    out.append("")
    out.append("```text")
    out.append("documents/")
    out.append("├── documentation/    # current/stable project documentation")
    out.append("├── tasks/            # task lifecycle, plans, evidence, task configuration, lessons")
    out.append("├── research/")
    out.append("├── audits/")
    out.append("├── reports/")
    out.append("├── notes/            # only when the project genuinely uses durable notes")
    out.append("└── archive/")
    out.append("```")
    out.append("")

    if data["physical_legacy_roots"]:
        out.append("## Physical legacy roots")
        out.append("")
        out.append("| Current | Recommended | Status |")
        out.append("|---|---|---|")
        for r in data["physical_legacy_roots"]:
            out.append(f"| `{esc(r['current'])}` | `{esc(r['recommended'])}` | {r['status']} |")
        out.append("")

    out.append("## Skills requiring updates")
    out.append("")
    if data["skills_requiring_update"]:
        out.append("| Skill | Files | References | Safe rewrites | Manual classification |")
        out.append("|---|---|---:|---:|---:|")
        for r in data["skills_requiring_update"]:
            out.append(f"| `{r['skill']}` | {', '.join('`'+x+'`' for x in r['files'])} | {r['occurrences']} | {r['safe_rewrites']} | {r['review_required']} |")
    else:
        out.append("No skill files contain non-canonical document path references.")
    out.append("")

    out.append("## Skill policy review candidates")
    out.append("")
    policy_rows = data.get("policy_review_candidates", [])
    cross_rows = [r for r in policy_rows if r.get("cross_namespace")]
    if cross_rows:
        out.append("These lines mention documentation ownership/placement together with task, evidence, log, report, migration, backup, or similar operational concepts. Review their semantics after path normalization; a literal rewrite alone may preserve the wrong ownership rule.")
        out.append("")
        out.append("| Skill | File | Line | Policy text |")
        out.append("|---|---|---:|---|")
        for r in cross_rows:
            out.append(f"| `{r['skill']}` | `{r['file']}` | {r['line']} | {esc(r['context'])} |")
    else:
        out.append("No obvious cross-namespace policy conflicts detected by the heuristic scan.")
    out.append("")

    out.append("## Non-canonical references")
    out.append("")
    rows = [r for r in data["occurrences"] if r["status"] in {"SAFE_REWRITE", "REVIEW"}]
    if rows:
        out.append("| File | Line | Consumer | Current | Recommended | Status |")
        out.append("|---|---:|---|---|---|---|")
        for r in rows:
            out.append(f"| `{r['file']}` | {r['line']} | {r['consumer_type']} | `{esc(r['current'])}` | `{esc(r['recommended'])}` | {r['status']} |")
    else:
        out.append("No non-canonical references detected.")
    out.append("")

    if changes is not None:
        out.append("## Applied safe rewrites")
        out.append("")
        if changes:
            for c in changes:
                out.append(f"- `{c['file']}` — {c['replacements']} replacement(s)")
        else:
            out.append("- None")
        out.append("")

    out.append("> SAFE_REWRITE means the path prefix has an unambiguous canonical equivalent. REVIEW means the reference is document-related but its contents must be classified before moving or rewriting it.")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit documentation/task path references, especially inside skills.")
    ap.add_argument("project", nargs="?", default=".", help="Repository root")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--output", "-o")
    ap.add_argument("--apply-safe-rewrites", action="store_true", help="Rewrite only unambiguous path prefixes in text consumers")
    ap.add_argument("--backup-suffix", help="Optional backup suffix, e.g. .bak, when applying rewrites")
    args = ap.parse_args()

    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    changes = apply_safe_rewrites(root, args.backup_suffix) if args.apply_safe_rewrites else None
    data = scan(root)
    rendered = json.dumps({**data, "applied_changes": changes}, indent=2) if args.format == "json" else to_markdown(data, changes)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
