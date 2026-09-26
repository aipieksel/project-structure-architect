---
name: project-structure-architect
description: Analyze and, when requested, reorganize an existing software repository in place toward a canonical app/business/view + db + config + documents architecture. Use for deep repository cleanup, thin-root restructuring, configuration relocation, and document/task namespace normalization without rebranding, relocating the repository, changing stacks, or redesigning product behavior.
---

# Project Structure Architect

## Start here: always present the three options

On each new invocation without an explicit mode selection, including a bare
`$project-structure-architect` invocation or `preview=ask`, present the complete
A/B/C menu below before inspecting or changing the repository. This is the
required opening response; the user must not have to ask for the options.
Do not infer a selection from a previous unrelated run.

Ask in normal chat text, not through an interactive prompt tool. Include this
entire block in the response that ends the turn, then wait for the user's choice:

```text
Do you want to review the proposed folder structure and move plan before I make changes?

A. Review the plan first
B. Audit and apply the reorganization
C. Audit, show the plan, then apply the reorganization automatically without approval
```

Before sending, check that the question and all three labeled options are
present. A yes/no question, a skill link, or an explanation of why a choice is
needed does not satisfy this contract. Do not add a preamble, recommendation,
or another question. If higher-priority instructions require a disclosure or
skill citation, append it separately after the complete menu; never replace or
omit the options to make room for that explanation.

Accept A/a, B/b, or C/c, including ordinary trailing punctuation, as the modes
below. If the reply does not clearly select a mode, repeat the complete menu.
An explicit `preview=yes|no|show` or an already-supplied A/B/C choice for this
run selects the mode directly; do not ask the user to select it again.

### Invocation modes

Accept an optional `preview=ask|yes|no|show` invocation argument.

- **A / `preview=yes`:** Perform the complete read-only audit, display and record
  the proposed tree, move map, exceptions, and verification plan, then pause
  for explicit approval before any repository mutation.
- **B / `preview=no`:** Perform and record the same complete audit internally,
  then continue through the recovery checkpoint, migration, verification, and
  local cleanup commit in one uninterrupted run without an approval pause.
- **C / `preview=show`:** Perform the complete read-only audit, display and record
  the proposed tree, move map, exceptions, and verification plan in chat, then
  continue automatically through the recovery checkpoint, migration,
  verification, and local cleanup commit. Showing the plan is informational;
  do not ask the user to review or approve it and do not pause after displaying
  it.

Explicit invocation with apply intent authorizes the local checkpoint and final
cleanup commits required by this workflow. Do not ask separately for commit
approval. This authorization never includes pushing, deploying, rewriting Git
history, changing production/provider state, spending money, or deleting
material that cannot be recovered.

If the user asks only for analysis, an audit, a tree, or recommendations, remain
read-only regardless of `preview`. If apply intent is present and `preview=no`,
do not convert uncertainty into permission to guess: preserve unresolved items
and continue with independent proven-safe work.

## Purpose

Use this skill when a project has become structurally messy, source code is scattered across technology-named folders, configuration files have accumulated at the repository root, business logic is mixed into UI code, database concerns are spread across unrelated paths, or the user wants to standardize multiple repositories around one architecture.

The skill has one architectural destination regardless of stack:

```text
project/
├── app/                 # actual application source
│   ├── business/        # what the product does
│   ├── view/            # what users see/interact with
│   └── entry/           # runtime/framework entry points
├── db/                  # source-controlled migrations, seeds and schema artifacts
├── data/                # durable product data, organized by domain and run/entity
├── tmp/                 # disposable/debug output, organized by purpose
├── backups/             # recovery copies with provenance and retention
├── documents/           # canonical root for documentation/tasks/research/audits/reports
├── config/              # relocatable tool/build/test/deploy configuration
├── tests/               # cross-cutting integration/e2e/fixtures
├── scripts/             # repository automation, maintenance, generators
├── public/              # static public assets when the stack uses them
├── package/build manifest(s) that genuinely belong at root
├── lockfile(s)
├── README.md
└── minimal required root anchors/shims only
```

The exact internal folders are adapted to the product and stack, but the top-level architectural intent does not change.

## Mandatory conformance gate

Read [references/conformance-and-completion.md](references/conformance-and-completion.md) before target design and before final handoff. It defines mandatory per-application architecture, evidenced exceptions, active-service sequencing, explicit configuration paths and requirement-level completion. This contract narrows any permissive exception or shim wording elsewhere in this skill. Unresolved or deferred required work must remain visible and cannot be reported complete.

## Core architectural rule

Dependency direction should converge toward:

```text
view
  ↓
business
  ↓
repositories / providers / database runtime
  ↓
external systems / persistence
```

Never create the opposite dependency merely to satisfy the folder layout.

- `view` may call stable business/application APIs.
- `business` must not depend on presentation/UI code.
- domain logic must not import React/Vue/Svelte/templates/controllers/views solely to get work done.
- UI components must not directly query the database.
- database code must not depend on UI code.
- external provider SDKs should be behind adapters when practical.
- framework glue belongs at an entry/boundary layer rather than inside core domain logic.

## Modes

### 1. Audit / plan mode

Use when the user asks to analyze, document, recommend, propose, map, or review structure.

Do not move files. Produce:

1. current repository structure;
2. detected stack and languages;
3. current architectural boundaries;
4. structural problems and root clutter;
5. canonical recommended final structure;
6. complete current-path → target-path move map;
7. config/root-file relocation matrix;
8. import/dependency impact analysis;
9. migration phases;
10. verification plan;
11. exceptions that must remain because of framework/tool constraints.

### 2. Apply / verify mode

Use only when the user asks to reorganize, refactor, migrate, implement, apply, fix, or execute the structure.

Perform the audit first, then migrate in dependency-safe phases. Update all affected references and run project-appropriate verification. Do not declare success if only filesystem moves were completed.

## Non-negotiable principles

1. **Preserve behavior.** Reorganization must not intentionally change product behavior, API behavior, database semantics, permissions, routes, copy, styling, or features unless separately requested.
2. **Inspect before classifying.** Never classify a file solely from its filename if its imports, exports, callers, manifest references, or framework conventions provide better evidence.
3. **Source-aware over folder-aware.** Existing folder names may be wrong. Determine what code actually does.
4. **Framework-aware without framework-shaped architecture.** Respect required conventions, but contain framework-specific glue at the edges.
5. **Minimize root clutter.** Keep only true root manifests, lockfiles, README, repository metadata, and required anchors/shims.
6. **Prefer explicit configuration paths.** If a tool supports `--config`, `-c`, a manifest field, or equivalent, relocate the config into `config/<tool>/` and update scripts/CI.
7. **Require evidence for root shims.** Use supported explicit paths for owned callers. Retain a tiny root forwarder only for a named consumer whose discovery requirement is verified and cannot be updated within scope; record the evidence and alternatives in the exception table.
8. **Separate database runtime code from database artifacts.** Runtime DB clients/schema/repositories belong under `app/business/...`; migrations/seeds/snapshots belong under root `db/`.
9. **No junk drawers.** Avoid new generic folders such as `misc`, `stuff`, `helpers`, `common`, or `lib` unless the repository already has an externally imposed meaning for them.
10. **Verify after every migration phase.** Use the repository's own scripts and toolchain.
11. **Do not hide uncertainty.** Mark inferred classifications and unresolved framework constraints explicitly.
12. **Do not expose secrets.** Never print `.env`, credentials, tokens, keys, private certificates, database URLs, or secret values while auditing.
13. **Preserve tests by default.** A test, fixture, screenshot, or snapshot is not
    disposable merely because it is numerous, old-looking, or stored beneath a
    temporary-sounding path. Move valid tests into the canonical test boundary;
    remove only generated outputs or tests proven obsolete by documentation,
    callers/configuration, and replacement coverage.
14. **Treat physical clutter separately from Git cleanliness.** Ignored caches,
    local data, temporary output, backups, and tool state still affect repository
    legibility and disk usage. Classify their owner, regeneration rule, active
    process use, and recoverability before cleaning them.
15. **Require material structural improvement.** An apply run requested for a
    messy structure cannot close after formatting, README edits, or trivial junk
    removal. Compare before/after root metrics and complete the approved safe
    structural moves, unless the initial repository already satisfies the
    recorded target. If required moves remain unresolved or deferred, preserve
    them and report partially_implemented or blocked, never complete.

## Canonical target architecture

Start from this shape and specialize it based on the actual product:

```text
project/
├── app/
│   ├── business/
│   │   ├── domain/
│   │   ├── services/
│   │   ├── workflows/
│   │   ├── repositories/
│   │   ├── providers/
│   │   ├── database/
│   │   │   ├── client/
│   │   │   ├── schema/
│   │   │   ├── queries/
│   │   │   └── adapters/
│   │   ├── auth/
│   │   ├── validation/
│   │   ├── jobs/
│   │   └── shared/       # only stable, genuinely cross-domain business primitives
│   │
│   ├── view/
│   │   ├── routes/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── forms/
│   │   │   ├── tables/
│   │   │   ├── navigation/
│   │   │   └── feedback/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── charts/
│   │   ├── styles/
│   │   └── assets/
│   │
│   └── entry/
│       ├── client/
│       ├── server/
│       ├── router/
│       ├── worker/
│       ├── cli/
│       └── runtime-specific entry points as needed
│
├── db/
│   ├── migrations/
│   │   └── <dialect-or-database>/
│   ├── seeds/
│   ├── snapshots/
│   ├── fixtures/         # only database-specific fixtures
│   └── README.md
│
├── config/
│   ├── build/
│   ├── database/
│   ├── deployment/
│   ├── testing/
│   ├── linting/
│   ├── formatting/
│   ├── styling/
│   └── typescript-or-language-tooling/
│
├── documents/
│   ├── documentation/        # current/stable project knowledge
│   │   ├── 0-index.md        # when the project uses a routed documentation index
│   │   ├── project-overview.md
│   │   ├── application/
│   │   ├── architecture/
│   │   ├── specifications/
│   │   ├── decisions/
│   │   └── agent-observations/
│   ├── tasks/                # task lifecycle system; preserve its internal topology
│   │   ├── planning/
│   │   ├── evidence/
│   │   ├── lessons/          # or existing lesson files at this root if already canonical internally
│   │   └── task-system helpers/config as required by the installed task system
│   ├── research/
│   ├── audits/
│   ├── reports/
│   ├── notes/                # only when durable notes are a real project concept
│   ├── migrations/           # documentation about migrations, not DB migration artifacts
│   └── archive/
│
├── tests/
│   ├── integration/
│   ├── e2e/
│   ├── contract/
│   └── fixtures/
│
├── data/<domain>/<runs-or-entities>/<id>/
├── tmp/<purpose>/
├── backups/<operation-or-owner>/<timestamp>/
├── scripts/
├── public/
├── README.md
├── primary package/build manifest(s)
├── package/dependency lockfile(s)
└── required root metadata only
```

This is a destination model, not a command to create empty folders. Only create folders that the real repository needs.

## Runtime data, temporary output and backups

Read [references/runtime-storage.md](references/runtime-storage.md) whenever the audit finds live data, mixed var/runtime folders, screenshots, logs, caches or recovery copies. Classify their contents and consumers before moving them. Renaming a mixed directory to data is not classification or completion. Keep durable product data under data/<domain>/<runs-or-entities>/<id> when applicable, troubleshooting/verification output under tmp by purpose, and recovery copies under backups. Repair both writers and readers, prove preservation, and state which files are authoritative versus indexed or recoverable views. Tool-managed dependencies such as npm workspace node_modules are not configuration and must not be moved into config merely to reduce root clutter.

## Database rule

Use the following distinction consistently:

### Application database code → `app/business/database/`

Examples:

- database client creation;
- connection factories;
- ORM schema source code;
- typed database models that are persistence-specific;
- query builders;
- transaction helpers;
- D1/PostgreSQL/MySQL/SQLite adapters;
- ORM runtime integration;
- repository implementations.

### Database artifacts → `db/`

Examples:

- generated migrations;
- hand-written migration SQL;
- snapshots;
- seeds;
- schema dumps;
- database-only fixtures;
- migration metadata/journals that must travel with migration output.

### Database tool configuration → `config/database/`

Examples:

```text
config/database/drizzle.config.ts
config/database/prisma/
config/database/alembic.ini
config/database/flyway/
```

When the tool supports a custom config path, update package scripts, CI, containers, deploy scripts, and documentation to call it explicitly.

## Root configuration relocation policy

For every root-level configuration file, determine one of these statuses:

- **ROOT_REQUIRED** — package/build manifest or ecosystem requirement makes relocation harmful or impossible.
- **ROOT_PREFERRED** — a named consumer demonstrably requires root discovery and cannot be updated within scope; record technical evidence and investigate alternatives before retaining a shim or file.
- **RELOCATABLE_EXPLICIT** — tool supports a config path flag or manifest pointer; move it and update invocations.
- **RELOCATABLE_SHIM** — real config can live under `config/`; leave only a tiny import/extends forwarding file at root.
- **GENERATED** — should not be hand-organized; relocate its output directory through tool settings if supported.
- **UNKNOWN** — investigate before moving.

Prefer structures such as:

```text
config/
├── build/
│   └── vite.config.ts
├── database/
│   └── drizzle.config.ts
├── deployment/
│   └── wrangler.jsonc
├── testing/
│   ├── vitest.config.ts
│   └── playwright.config.ts
├── linting/
├── formatting/
└── typescript/
    ├── base.json
    ├── app.json
    └── node.json
```

Possible root shims, only if needed:

```text
tsconfig.json                 # extends ./config/typescript/app.json
eslint.config.js              # imports ./config/linting/eslint.config.js
```

Never assume a config can move because another tool can. Inspect the exact versions and commands used by the current project.

## Canonical documents namespace

The project must converge on **one** durable project-knowledge root: `documents/`. Do not leave competing top-level `docs/`, `doc/`, `documentation/`, `tasks/`, `specs/`, `plans/`, or similar roots after a completed migration unless an external tool makes one unavoidable.

The default normalization is:

```text
documentation/**       -> documents/documentation/**
docs/tasks/**          -> documents/tasks/**
docs/documentation/**  -> documents/documentation/**
```

For these unambiguous roots, preserve the existing relative subtree during the first migration. Example:

```text
documentation/application/auth.md
  -> documents/documentation/application/auth.md

docs/tasks/task-system.config.yaml
  -> documents/tasks/task-system.config.yaml

docs/tasks/planning/2026-09-06-restructure/
  -> documents/tasks/planning/2026-09-06-restructure/
```

Do **not** blindly rewrite generic `docs/**`. Classify its contents first:

- current/stable implementation documentation -> `documents/documentation/**`;
- task plans, task-system config, execution logs, task evidence, lessons -> `documents/tasks/**`;
- research -> `documents/research/**`;
- audit output -> `documents/audits/**`;
- generated/periodic reports -> `documents/reports/**`;
- historical material -> `documents/archive/**`;
- durable project decisions/ADRs -> normally `documents/documentation/decisions/**`.

The migration must preserve specialized documentation systems. For example, if an installed documentation skill defines `0-index.md`, `application/`, `project-overview.md`, or `agent-observations/`, relocate that system beneath `documents/documentation/` rather than redesigning its internal contract during an unrelated repository cleanup. Likewise, preserve an installed task system's internal paths beneath `documents/tasks/` unless the user separately asks to redesign that task system.

### Skills and agent instructions are path consumers

Skills are executable operating instructions. A filesystem move is incomplete if installed skills still instruct agents to write to old locations.

During every audit, search at minimum:

- `.agents/skills/**/SKILL.md`;
- `.claude/skills/**`, `.codex/skills/**`, `skills/**`, and equivalent installed skill roots;
- skill companion YAML/JSON/TOML files;
- `AGENTS.md`, `CLAUDE.md`, agent instruction files, installer/update instructions;
- task-system helpers and generators;
- scripts, package commands, CI workflows, Docker/deployment config;
- Markdown links and source-code string literals that reference document paths.

Run `scripts/document_path_audit.py` when available. It must list every skill with non-canonical document-path references and the exact references that require updates. Also inspect the semantics of path-ownership rules: a skill can still be wrong after a literal path rewrite if it says task ledgers, QA evidence, reports, migrations, logs, or other operational records belong beneath the documentation namespace. Such rules must be reclassified against the canonical `documents/*` ownership model rather than preserved mechanically.

Example:

```bash
python3 scripts/document_path_audit.py . --format md -o document-path-audit.md
```

In apply mode, safe prefix rewrites may be automated:

```bash
python3 scripts/document_path_audit.py . --apply-safe-rewrites --format md -o document-path-audit-after.md
```

However, automatic rewriting is limited to unambiguous mappings such as `documentation/** -> documents/documentation/**` and `docs/tasks/** -> documents/tasks/**`. Generic `docs/**`, `tasks/**`, `plans/**`, `reports/**`, etc. require semantic classification.

Do not accidentally rewrite skill installation paths merely because a skill name contains words such as `documentation` or `task`. For example, `.agents/skills/project-documentation-updater/SKILL.md` remains a skill path; only path literals *inside* that skill that point to the project's documentation/task directories should change.

### Required skill-impact output

Every audit/plan that finds installed skills must include:

| Skill | Skill file | Current document path(s) | Canonical path(s) | Update required? | Notes |
|---|---|---|---|---|---|

In apply mode, update all affected skill path literals **and conflicting path-policy language** in the same migration, then re-run the audit until no obsolete unambiguous references remain. Re-read each modified skill after rewriting to verify its ownership rules still make sense. If a skill is intentionally external/read-only or cannot be modified, list it as an explicit exception.

## Required audit workflow

### Phase A — Establish repository facts

1. Locate the repository root.
2. Record Git status before changes.
3. Read root manifests and workspace manifests.
4. Inspect package manager/build files.
5. Inspect language-specific manifests.
6. Inspect Docker/Compose, CI, deployment, infrastructure, and hosting files.
7. Inspect ORM/database configuration and migration output.
8. Inspect test configuration.
9. Inspect source directories.
10. Inspect route/entry-point conventions.
11. Inspect path aliases and module resolution.
12. Inspect code generation and generated-file locations.
13. Detect monorepo/workspace structure before proposing a single-app move.
14. Detect competing document/task roots (`docs/`, `documentation/`, `tasks/`, etc.).
15. Discover installed skills and agent instruction files.
16. Scan skills/scripts/config/CI/source for hard-coded document-path references.
17. Build a document-root migration map and a skill-impact list.

Run `scripts/project_inventory.py` when available to create a deterministic baseline, but do not treat its heuristic classifications as authoritative without source inspection.

### Phase B — Build the current structure report

Produce:

- a current tree with ignored generated/vendor directories omitted;
- top-level folder/file purpose table;
- language/type counts;
- framework/runtime/tool inventory;
- source ownership map;
- database/storage map;
- configuration map;
- entry-point map;
- test map;
- generated-code map;
- import/dependency hotspots;
- root clutter list;
- legacy/competing document roots;
- installed skill inventory;
- skills/instructions containing document/task path literals;
- document-path consumer map;
- files whose purpose is ambiguous.

### Phase C — Source-code classification

Classify by semantic role using evidence in this order:

1. runtime role and externally required convention;
2. imports/exports and call graph;
3. framework registration and manifest references;
4. public types/interfaces/contracts;
5. filename/path naming;
6. language heuristics.

Assign each source item to one primary target role:

- `app/business/domain`
- `app/business/services`
- `app/business/workflows`
- `app/business/repositories`
- `app/business/providers`
- `app/business/database`
- `app/business/auth`
- `app/business/validation`
- `app/business/jobs`
- `app/business/shared`
- `app/view/routes`
- `app/view/pages`
- `app/view/layouts`
- `app/view/components`
- `app/view/features`
- `app/view/hooks`
- `app/view/charts`
- `app/view/styles`
- `app/view/assets`
- `app/entry`
- `db`
- `config`
- `documents/documentation`
- `documents/tasks`
- `documents/research`
- `documents/audits`
- `documents/reports`
- `documents/archive`
- `tests`
- `scripts`
- `public`
- `root-required`

Give every proposed move a confidence: `HIGH`, `MEDIUM`, or `LOW`.

### Phase D — Detect architectural violations

Flag at least:

- UI importing ORM/database clients directly;
- business/domain importing UI framework packages;
- circular dependencies crossing view/business boundaries;
- provider SDK calls scattered through UI/domain code;
- raw SQL in UI/controllers/components;
- auth/authorization enforced only in browser/view code;
- schema types coupled directly to component state where a domain contract should exist;
- duplicate DB clients;
- duplicate config files;
- migrations outside controlled DB artifact locations;
- root-level source modules;
- unrelated docs scattered through source;
- competing `docs/`, `documentation/`, `tasks/`, `plans/`, or other project-knowledge roots;
- installed skills still writing to obsolete documentation/task paths;
- scripts/CI/package commands/generators that recreate legacy roots;
- generic junk-drawer directories;
- generated output committed or mixed with source unexpectedly;
- test fixtures mixed into runtime source;
- deployment logic buried inside presentation code;
- business logic implemented inside route components/controllers/templates.

### Phase E — Generate the recommended final structure

The target tree must be derived from real existing responsibilities. Preserve all important capabilities and show where every current major subsystem will live.

Do not output only a generic skeleton. Include product-specific/domain-specific folders discovered in the repository.

### Phase F — Generate the move map

Produce a table with at least:

| Current path | Target path | Role | Confidence | References to update | Risk | Notes |
|---|---|---|---|---|---|---|

Every material source/config/docs/db path must appear once. Documentation moves must also identify every skill/instruction/script/config/CI consumer that contains the old path.

For a large repository, group repetitive moves with an explicit glob only when all matching files share the same role and migration behavior.

### Phase G — Generate root cleanup matrix

For each root file/config:

| File | Tool | Current role | Status | Proposed path | Invocation change | Keep root shim? |
|---|---|---|---|---|---|---|

Do not propose root cleanup without showing how scripts/CI/tooling will still discover the file.

### Phase H — Generate skill/document-path impact matrix

If any skills or agent instructions exist, output:

| Skill/instruction | File | Old path literal | New path literal | Auto-safe? | Additional dependency |
|---|---|---|---|---|---|

Also list non-skill consumers such as helper scripts, package scripts, CI, Docker, code generators, and documentation links. This matrix is mandatory even when the physical document move itself is trivial.

## Apply-mode migration workflow

### 0. Safety checkpoint

Before moving anything, read every applicable `AGENTS.md` and the project's
documentation entry point. Then:

- resolve the exact repository root, branch, `HEAD`, remotes, worktrees,
  submodules, nested repositories, tracked/untracked/ignored state, generated
  files, case-sensitive rename risks, and current validation commands;
- inspect the complete candidate checkpoint inventory for secrets, personal
  data, unresolved conflicts, embedded repositories, oversized binaries, and
  other unsafe material without printing secret values;
- create a private restrictive quarantine outside the repository for unsafe or
  non-Git-recoverable originals, with hashes, source paths, reasons, and restore
  instructions;
- if Git exists and the worktree contains reviewed safe changes, stage every
  safe non-ignored change, inspect the exact staged list and patch, and commit it
  locally as `chore: checkpoint before repository reorganization`; if the
  worktree is clean, record the current `HEAD` instead of making an empty commit;
- never omit an unsafe original silently: quarantine it, ignore it where
  appropriate, and account for it in the checkpoint manifest;
- for a non-Git project, create and verify a restorable private snapshot outside
  the project before mutation;
- run a feasible baseline validation so pre-existing failures are distinguishable
  from migration regressions.

Stop only when recovery cannot be proven or a higher-priority rule forbids the
local checkpoint even after explicit invocation. Never push automatically.

Create a reorganization ledger before mutation with one row per proposed move,
archive, quarantine, or removal:

```text
path -> class -> owner -> disposition -> evidence -> recovery -> verification
```

Allowed dispositions are `preserve`, `move`, `archive`, `quarantine`, `remove`,
and `unresolved`. Never mutate an `unresolved` row.

### 1. Create architectural destination folders

Create only needed destinations.

### 2. Normalize documents and task systems first

- create `documents/` and only the subtrees the repository actually needs;
- move `documentation/**` to `documents/documentation/**` while preserving its internal contract;
- move `docs/tasks/**` to `documents/tasks/**` while preserving task-system topology;
- classify any remaining generic `docs/**`, `plans/**`, `reports/**`, etc. by content before moving;
- update installed skills, agent instructions, helper scripts, package commands, CI, generators, links, and source literals that point at the old paths;
- do not rewrite `.agents/skills/<skill-name>/...` installation paths merely because a skill name contains `documentation` or `task`;
- run the document-path audit again and require zero obsolete safe-mapping references before continuing.

Move other passive reports/specs/research/audit material into the appropriate `documents/*` namespace and repair links.

### 3. Move database artifacts and DB tooling

- move migrations/seeds/snapshots into `db/`;
- move ORM config under `config/database/` when supported;
- update migration `out`, schema paths, scripts, CI, Docker, deploy automation;
- keep ORM runtime/schema code under `app/business/database/`.

### 4. Move business/infrastructure code

Move domain, services, workflows, repositories, providers, database runtime, auth, validation, and jobs. Repair imports after each coherent batch.

### 5. Move view code

Move routes/pages/layouts/components/features/hooks/styles/assets while preserving route semantics and framework requirements.

### 6. Move/contain entry points

Converge runtime bootstraps, router construction, worker/server/client entry points under `app/entry/` where the framework allows. If a framework requires a conventional source path, use a thin adapter or configure the framework rather than duplicating business logic.

### 7. Relocate configuration

Move each config according to the root relocation matrix. Update:

- package scripts;
- task runner files;
- CI workflows;
- Dockerfiles/Compose;
- deploy/platform commands;
- IDE/workspace settings if tracked;
- code generation;
- test commands;
- docs;
- installed skills and agent instructions that name config or document paths.

### 8. Repair module resolution

Update:

- relative imports;
- path aliases;
- TypeScript/project references;
- Python import packages;
- Go modules/packages;
- Java/Kotlin package paths when moves change namespace expectations;
- C# namespaces/project includes;
- PHP Composer PSR mappings;
- Ruby autoload paths;
- framework aliases;
- CSS asset paths;
- test imports/mocks;
- codegen paths.

Prefer stable aliases for cross-layer imports where the stack supports them.

### 9. Enforce boundaries

Where practical, add lint/import rules so the repository cannot immediately regress. Examples of policy, adapted to the stack:

```text
business -> must not import view
view -> may import public business contracts/services
components -> must not import database clients
business/domain -> must not import UI framework modules
```

### 10. Verify

Run the repository's real commands. At minimum when applicable:

- dependency install consistency / lockfile check;
- typecheck;
- lint;
- formatting check;
- unit tests;
- integration tests;
- build;
- framework route generation/check;
- database migration generation/check;
- database migration status/dry run;
- e2e tests;
- deployment dry run/build;
- browser smoke test for UI applications;
- document-path audit showing no obsolete `documentation/**` or `docs/tasks/**` references;
- skill-impact check confirming every mutable affected skill now points at `documents/**`;
- check that no task/documentation helper recreates a legacy root on the next run.

If the project lacks a validation command, say so and perform the strongest available equivalent.

### 11. Final structure report

Output:

1. before tree;
2. after tree;
3. moves completed;
4. root files removed/retained and why;
5. dependency-boundary changes;
6. config/script changes;
7. document namespace changes and legacy roots removed;
8. skills/instructions updated, with exact files and path mappings;
9. validation results with exact command/result;
10. unresolved exceptions;
11. remaining cleanup opportunities that are outside the requested structural migration.

## Language-aware rules

Consult `references/classification-rules.md`. Key principle: language syntax changes how dependencies and entry points are detected, but not the architectural destination.

Examples:

- TypeScript/JavaScript: imports, package manifests, JSX/TSX, server/client directives, bundler aliases.
- Python: package imports, `pyproject.toml`, framework apps/routers, ORM models, Alembic, task workers.
- Go: packages, `go.mod`, `cmd/` entry points, internal packages, generated files.
- Rust: crates/modules, Cargo workspace, `src/bin`, build scripts, migrations.
- PHP: Composer autoload, controllers/views/services, framework conventions, WordPress plugin/theme constraints.
- Ruby: Bundler/Rails autoloading and conventional app paths.
- Java/Kotlin: Maven/Gradle modules and package namespace implications.
- C#: solution/project files, namespaces, generated partials, ASP.NET conventions.
- Swift: SwiftPM/Xcode groups/targets and application entry points.

## Framework-aware exception rule

Every exception must satisfy the evidence table in `references/conformance-and-completion.md`. Investigate compatible alternatives. A running service is a sequencing constraint; deferred required moves or activation remain incomplete. Do not relabel them as permanent framework exceptions.


The canonical architecture is the goal, but some frameworks derive behavior from physical paths. Do not break those conventions merely to make the tree prettier.

For each exception choose one:

1. configure the framework to point at the canonical folder;
2. keep a thin framework adapter/forwarder in the required conventional location;
3. keep the required folder but constrain it to entry/view glue and document the exception;
4. if none are safe, retain the path and explicitly mark it as a framework exception.

Never duplicate core business logic to satisfy both structures.

## Monorepo rule

Do not flatten a real monorepo into one `app/`. Preserve workspace and package identities while enforcing canonical responsibilities inside every application. Monorepo preservation does not authorize keeping product pipelines in scripts, unexplained shared roots, or unclassified source containers. Record a complete owner/current/target/disposition map for each application and independent package. See [the monorepo example](examples/monorepo-dashboard-workflow.md).

Use the canonical architecture per deployable/product unit, for example:

```text
apps/
├── web/
│   ├── app/business
│   ├── app/view
│   └── app/entry
└── worker/
    ├── app/business
    └── app/entry

packages/
├── domain-contracts/
└── design-system/

db/
documents/
config/
```

Only extract a shared package when multiple deployable units genuinely share a stable contract. Do not create packages merely to make the tree look sophisticated.

## Source-of-truth and generated-code rules

For every generated folder/file, identify:

- generator;
- source-of-truth input;
- generation command;
- whether generated output is committed;
- whether output path is configurable;
- imports/references to generated output.

Never move generated output without changing its generator configuration. Never hand-edit generated output as the primary migration strategy.

## Documentation and task-path rule

Keep root `README.md`. Put durable project knowledge under the single root `documents/`.

Default namespaces:

```text
documents/
├── documentation/
│   ├── application/
│   ├── architecture/
│   ├── specifications/
│   ├── decisions/
│   └── agent-observations/
├── tasks/
├── research/
├── audits/
├── reports/
├── notes/
└── archive/
```

The internal layout of `documents/documentation/` and `documents/tasks/` is project-aware. Preserve an installed documentation/task system's existing internal contract unless redesigning that system is part of the request.

Treat all old path references as dependencies. Search and update skills, agent instructions, helper scripts, code generators, package scripts, CI, source literals, and links—not only Markdown files.

When moving docs, repair relative links and references and prove that recurring automation will not recreate `docs/` or `documentation/` at the next run.

## Naming rule

Prefer names that communicate architectural responsibility:

Good:

```text
domain
services
workflows
repositories
providers
database
routes
pages
components
layouts
migrations
```

Avoid creating ambiguous containers:

```text
misc
stuff
helpers
common
lib
other
temp
new
old
```

A narrowly defined `shared/` is acceptable only when its ownership and allowed contents are documented.

## Output quality gate

Reconcile every original target row against actual paths and evidenced target revisions. State `complete`, `partially_implemented`, `blocked`, or `audit_only`. Required moves, activation or verification still pending forbid `complete`; file counts, successful tests and clean commits cannot substitute for target conformance. Include exception proof and concrete remaining actions.


A project-structure recommendation is incomplete if it contains only a pretty target tree.

It must demonstrate:

- understanding of the current real project;
- where current capabilities move;
- what references must change;
- what cannot safely move;
- how configuration discovery still works;
- how database migrations remain valid;
- how framework routing/entry points remain valid;
- how tests/build/deploy remain valid;
- which installed skills/instructions reference moved paths and whether they were updated;
- whether future skill/task/documentation runs will create only canonical `documents/**` paths;
- how the new boundary will be kept clean over time.

## Supporting references

Read as needed:

- `references/canonical-architecture.md`
- `references/classification-rules.md`
- `references/framework-and-tool-adapters.md`
- `references/migration-playbook.md`
- `references/verification-matrix.md`
- `references/output-contract.md`
- `references/document-and-skill-path-migration.md`

Use `scripts/project_inventory.py` for a deterministic first-pass inventory. Use `scripts/document_path_audit.py` to discover legacy documentation/task roots and every affected skill/path consumer. After migration, rerun the document-path audit and use `scripts/architecture_guard.py` as an additional heuristic boundary check before the project-specific compiler/linter/tests.
