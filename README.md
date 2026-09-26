# Project Structure Architect Skill

Maintained by [aipieksel](https://github.com/aipieksel). Upstream credits and licenses remain with their respective authors.

A reusable repository-analysis and reorganization skill for converging software projects toward a clean architecture centered on:

- `app/business` — what the product does;
- `app/view` — what users see and interact with;
- `app/entry` — framework/runtime entry points;
- `db` — migrations, seeds, snapshots, and database artifacts;
- `documents/documentation` — current/stable documentation and documentation-system state;
- `documents/tasks` — task planning, task-system configuration, evidence, helpers, and lessons;
- `documents/research`, `documents/audits`, `documents/reports`, etc. — other durable project knowledge;
- `config` — relocatable tool/build/test/deployment configuration;
- minimal root files.

The skill is intentionally stack-agnostic. It analyzes the actual languages, frameworks, package manifests, imports, ORM/runtime usage, generated code, build/deploy configuration, tests, and framework constraints before proposing moves.

## Strict architecture and completion

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

## Companion project suite

These standalone skills share the same project namespace without depending on one another:

- `$project-documentation-builder` creates or comprehensively restructures `documents/documentation/**` and writes build evidence under `documents/tasks/documentation/build/**`.
- `$project-documentation-updater` performs focused maintenance and writes update evidence under `documents/tasks/documentation/update/**`.
- `$project-development-planner` creates an implementation-ready plan under `documents/tasks/development/**` without changing application code.
- `$project-development-plan-criticizer` audits and revises that same plan record against project evidence.
- `$project-development-plan-executor` implements and verifies a ready plan using the same record.

The architect should preserve these internal contracts when it encounters them. It may normalize legacy parent roots into `documents/**`, but it must not silently redesign the companion systems during unrelated repository cleanup.

For browser-visible verification, follow the target project's policy. Ego Browser is recommended when it is installed and authorized. It is not required for repository analysis or checks that have no browser-visible claim.

## Installation and rights

Copy this entire folder into your assistant's supported skill directory, preserving `SKILL.md`, scripts, references, examples and templates. Python 3.10+ is required for the Python helpers. Host autocomplete and tool availability depend on the installed assistant. Keep generated project/task records and private conversations outside the shared skill package. This package is licensed under [MIT](LICENSE).
