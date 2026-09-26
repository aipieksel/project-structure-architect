# Project Inventory

**Root:** `/mnt/data/project-structure-architect`  
**Files inventoried:** 18

## Current structure

```text
project-structure-architect/
├── examples/
│   ├── self-inventory.md
│   ├── skills-document-path-audit.md
│   ├── supplied-skills-findings.md
│   └── tanstack-cloudflare-drizzle.md
├── references/
│   ├── canonical-architecture.md
│   ├── classification-rules.md
│   ├── document-and-skill-path-migration.md
│   ├── framework-and-tool-adapters.md
│   ├── migration-playbook.md
│   ├── output-contract.md
│   └── verification-matrix.md
├── scripts/
│   ├── architecture_guard.py
│   ├── document_path_audit.py
│   └── project_inventory.py
├── templates/
│   ├── PROJECT_STRUCTURE_AUDIT.md
│   └── REORGANIZATION_LEDGER.md
├── README.md
└── SKILL.md
```

## Detected tools / frameworks

- Alembic
- Docker
- Drizzle
- ESLint
- Playwright
- Prettier
- Prisma
- Tailwind
- Vite
- Vitest

## Languages / file types

| Language/type | Files |
|---|---:|
| Markdown | 15 |
| Python | 3 |

## Heuristic roles

| Role | Files |
|---|---:|
| documents | 15 |
| scripts | 3 |

## Manifests / lockfiles

- `(none detected)`

## Root clutter candidates

- `SKILL.md`

## Document-root normalization candidates

- Canonical `documents/` present: no
- No legacy top-level document/task roots detected

## Installed skill files

- `SKILL.md`
- Run `scripts/document_path_audit.py` to identify document/task path literals inside these skills.

## File classifications

| Path | Language | Role | Generated? | Imports (sample) |
|---|---|---|---|---|
| `README.md` | Markdown | documents | no |  |
| `SKILL.md` | Markdown | documents | no |  |
| `templates/PROJECT_STRUCTURE_AUDIT.md` | Markdown | documents | no |  |
| `templates/REORGANIZATION_LEDGER.md` | Markdown | documents | no |  |
| `examples/tanstack-cloudflare-drizzle.md` | Markdown | documents | no |  |
| `examples/supplied-skills-findings.md` | Markdown | documents | no |  |
| `examples/skills-document-path-audit.md` | Markdown | documents | no |  |
| `examples/self-inventory.md` | Markdown | documents | no |  |
| `scripts/project_inventory.py` | Python | scripts | no | argparse, json, os, re, sys |
| `scripts/document_path_audit.py` | Python | scripts | no | argparse, json, os, re, shutil, sys |
| `scripts/architecture_guard.py` | Python | scripts | no | argparse, os, re, sys, json |
| `references/framework-and-tool-adapters.md` | Markdown | documents | no |  |
| `references/classification-rules.md` | Markdown | documents | no |  |
| `references/document-and-skill-path-migration.md` | Markdown | documents | no |  |
| `references/migration-playbook.md` | Markdown | documents | no | ./config/build/vite.config |
| `references/verification-matrix.md` | Markdown | documents | no |  |
| `references/canonical-architecture.md` | Markdown | documents | no |  |
| `references/output-contract.md` | Markdown | documents | no |  |

> Heuristic classifications are an inventory aid, not the final architectural decision. Inspect source semantics, callers, manifests, and framework constraints before moving files.
