# Document and Skill Path Migration

## Objective

Converge project knowledge on one top-level root while preventing installed skills, task systems, scripts, CI, and generators from recreating legacy paths later.

Canonical top-level namespace:

```text
documents/
├── documentation/
├── tasks/
├── research/
├── audits/
├── reports/
├── notes/
└── archive/
```

Only create categories the repository actually uses.

## Unambiguous mappings

These mappings are safe as a root normalization because they preserve the existing internal system:

| Current | Canonical | Rule |
|---|---|---|
| `documentation/**` | `documents/documentation/**` | preserve relative subtree |
| `docs/documentation/**` | `documents/documentation/**` | preserve relative subtree |
| `docs/tasks/**` | `documents/tasks/**` | preserve relative subtree |

Examples:

```text
documentation/0-index.md
  -> documents/documentation/0-index.md

documentation/application/auth.md
  -> documents/documentation/application/auth.md

docs/tasks/task-system.config.yaml
  -> documents/tasks/task-system.config.yaml

docs/tasks/planning/2026-09-06-example/
  -> documents/tasks/planning/2026-09-06-example/
```

## Roots that require content classification

Do not blindly prefix or rename these without inspecting their contents:

```text
docs/
doc/
tasks/
plans/
planning/
specs/
specifications/
reports/
research/
decisions/
architecture/
notes/
audits/
```

Recommended destinations by semantic role:

| Content | Destination |
|---|---|
| Current implementation/product docs | `documents/documentation/**` |
| Architecture docs | `documents/documentation/architecture/**` |
| Specifications/contracts | `documents/documentation/specifications/**` |
| ADRs/project decisions | `documents/documentation/decisions/**` |
| Documentation-system unresolved findings | `documents/documentation/agent-observations/**` when that system uses it |
| Task plans/config/helpers/lessons/evidence/logs | `documents/tasks/**` |
| Research | `documents/research/**` |
| Structural/quality audits | `documents/audits/**` |
| Generated/periodic reports | `documents/reports/**` |
| Durable notes | `documents/notes/**` |
| Historical/deprecated material | `documents/archive/**` |

## Preserve installed subsystem contracts

A root cleanup should not silently redesign a documentation or task-management subsystem.

If a documentation skill currently defines:

```text
documentation/
├── 0-index.md
├── project-overview.md
├── application/
├── agent-observations/
└── agents/
```

prefer:

```text
documents/documentation/
├── 0-index.md
├── project-overview.md
├── application/
├── agent-observations/
└── agents/
```

Likewise, if a task system currently expects `docs/tasks/planning/`, task configuration files, lesson files, helpers, and evidence folders, move the entire task-system namespace under `documents/tasks/` first and preserve its relative topology.

## Skills are dependencies

Treat installed skill instructions as executable path consumers. Search them just like source code.

Common skill locations include:

```text
.agents/skills/**/SKILL.md
.claude/skills/**
.codex/skills/**
skills/**
```

Also scan companion files such as:

```text
agents/*.yaml
*.json
*.toml
install*.md
update*.md
AGENTS.md
CLAUDE.md
```

A skill that says:

```text
Read docs/tasks/task-system.config.yaml
```

must be changed to:

```text
Read documents/tasks/task-system.config.yaml
```

A skill that says:

```text
Current implementation documentation MUST live under documentation/application/
```

must be changed to:

```text
Current implementation documentation MUST live under documents/documentation/application/
```

## Do not rewrite skill installation paths

A skill name may itself include `documentation`, `task`, `plan`, or similar words:

```text
.agents/skills/update-documentation/SKILL.md
.agents/skills/document-task/SKILL.md
```

Those are skill installation paths, not project-document paths. Preserve them unless the user separately asks to reorganize the skills installation itself.

Only rewrite path literals inside the skill that refer to the project's document/task locations.

## Other path consumers

Search all of the following before and after moves:

- package scripts;
- Makefiles/task runners;
- shell/Python/Node helper scripts;
- CI workflows;
- Dockerfiles and Compose;
- deployment scripts/config;
- code generators;
- test fixtures and snapshot paths;
- source string literals;
- Markdown links;
- installer/update scripts;
- agent instructions;
- skill files and skill companion configuration;
- symlinks.

## Required audit command

When the bundled helper is available:

```bash
python3 scripts/document_path_audit.py . --format md -o document-path-audit.md
```

The report must identify:

1. skills discovered;
2. skills requiring path updates;
3. exact old path literals;
4. canonical replacements;
5. ambiguous paths that require semantic classification;
6. physical legacy roots present in the repository.

## Apply-mode helper

Only unambiguous prefix rewrites may be automated:

```bash
python3 scripts/document_path_audit.py . \
  --apply-safe-rewrites \
  --format md \
  -o document-path-audit-after.md
```

Then manually resolve any `REVIEW` entries.

The helper does not move directories. The migration workflow must move the corresponding physical paths and update all additional references.

## Completion gate

Do not call the document migration complete until all of these are true:

- no unintended top-level `documentation/` remains;
- no intended task-system files remain under `docs/tasks/`;
- generic `docs/**` content has been classified or explicitly exempted;
- affected mutable skills point to `documents/**`;
- task helpers/generators write to `documents/tasks/**`;
- documentation helpers/generators write to `documents/documentation/**`;
- package scripts/CI/deployment/test commands contain no stale path references;
- relative Markdown links still resolve where practical;
- a fresh task/documentation workflow does not recreate a legacy root.

## Output requirement

Always list the affected skills in the final report:

| Skill | File | Old path(s) | New path(s) | Updated? | Verification |
|---|---|---|---|---|---|

If a skill cannot be changed because it is external, generated, read-only, or intentionally versioned elsewhere, state that explicitly and treat it as an exception rather than silently ignoring it.
