# Project Structure Architect

Maintained by [aipieksel](https://github.com/aipieksel). Upstream credits and licenses remain with their respective authors.

Project Structure Architect is a Codex skill for making an existing repository easier to navigate and maintain. It inspects the real application, build configuration, data paths, tests, and documentation before proposing or performing a folder reorganization. Its target structure separates application behavior, UI, entry points, database artifacts, configuration, and durable project documents.

The skill works within the current repository. It does not change the product's stack or behavior to make folders look tidy. A successful run accounts for imports, build and deployment paths, active services, documentation links, and verification before calling the reorganization complete.

Its target separates `app/business`, `app/view`, and `app/entry`, with `db/` for data artifacts, `config/` for relocatable configuration, and `documents/` for durable project knowledge. These are targets to assess against the actual stack, not folders to impose blindly.

## Architecture and completion

Preserve the monorepo while organizing each application's responsibilities. Read the [mandatory conformance contract](references/conformance-and-completion.md) and [monorepo example](examples/monorepo-dashboard-workflow.md). Production logic under scripts/shared must be classified, exceptions need exact technical evidence, root shims need named consumers, and active services require sequencing rather than automatic exemptions. Final reports reconcile every target row and cannot claim completion with required moves, activation or verification pending.

These are instructions and review criteria, not an automated guarantee of agent compliance. Inventory and architecture-guard scripts remain heuristic tools.

## Typical requests

Invoking `$project-structure-architect` without a mode, or with `preview=ask`,
always opens with all three choices: **A. Review the plan first**, **B. Audit and
apply the reorganization**, and **C. Audit, show the plan, then apply the
reorganization automatically without approval**. The agent waits for a choice
before inspecting the repository. An explicit `preview=yes|no|show` selects
A/B/C directly. See [the opening-response contract](SKILL.md#start-here-always-present-the-three-options).

- “Analyze this repo and show me the current structure and your recommended final structure.”
- “Reorganize this project using the Project Structure Architect skill.”
- “Clean up my project root and move configs into sensible folders without breaking the toolchain.”
- “Separate business logic from the view and migrate the repo.”
- “Audit the repo structure only; do not change files.”

## Included files

- `SKILL.md` — complete operating instructions.
- `scripts/project_inventory.py` — dependency-free repository inventory helper.
- `scripts/document_path_audit.py` — finds legacy docs/task roots and every affected skill/path consumer; can safely rewrite unambiguous path prefixes.
- `scripts/architecture_guard.py` — heuristic post-migration boundary checker.
- `references/` — architectural, classification, migration, tool-adapter, verification, and output guidance.
- `templates/` — reusable report templates.
- `examples/` — worked single-application and monorepo examples; retain the actual project stack and workspace boundaries.

## Inventory helper

```bash
python scripts/project_inventory.py /path/to/project --format md
python scripts/project_inventory.py /path/to/project --format json --output inventory.json
```

The inventory helper never reads secret values from `.env` files. It is a deterministic baseline only; the skill must still inspect source semantics before final classification.

Audit documentation/task paths and installed skills with:

```bash
python scripts/document_path_audit.py /path/to/project --format md
```

The canonical root normalization is `documentation/** -> documents/documentation/**` and `docs/tasks/** -> documents/tasks/**`. Generic `docs/**` is classified by content rather than blindly renamed.

After a migration, you can also run:

```bash
python scripts/architecture_guard.py /path/to/project
```

Treat the guard as an extra check, not a substitute for compiler/linter/test validation.

## Skill-aware document migration

The skill treats installed skills, agent instructions, task helpers, package scripts, CI, generators, and source literals as filesystem dependencies. If a project moves documentation/task directories, the final report must list every affected skill and whether it was updated. The included `examples/skills-document-path-audit.md` shows this against the supplied sample skill corpus.

## Boundaries

When a target project uses agent skills or task tooling, their file paths are part of the migration inventory. The architect accounts for those consumers without redesigning their workflows. Browser-visible outcomes require the target project's browser verification policy; a file inventory alone cannot prove a rendered result.

## Installation and rights

Copy this entire folder into your assistant's supported skill directory, preserving `SKILL.md`, scripts, references, examples and templates. Python 3.10+ is required for the Python helpers. Host autocomplete and tool availability depend on the installed assistant. Keep generated project/task records and private conversations outside the shared skill package. This package is licensed under [MIT](LICENSE).
