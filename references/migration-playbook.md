# Migration Playbook

## Goal

Change structure without turning a filesystem cleanup into an uncontrolled rewrite.

## Recommended commit/migration phases

### Phase 1 — Inventory and baseline

- current tree;
- detected stack;
- source classification;
- git status;
- baseline validation results;
- migration ledger.

### Phase 2 — Documents namespace normalization

Normalize project knowledge before runtime source:

- `documentation/** -> documents/documentation/**`;
- `docs/tasks/** -> documents/tasks/**`;
- classify remaining generic `docs/**` by content;
- preserve documentation/task-system internal topology;
- update skills, agent instructions, helper scripts, generators, package scripts, CI, Docker/deployment paths, and links;
- rerun the document path audit before continuing.

Then move other passive research/audits/reports and non-runtime assets.

### Phase 3 — Database artifacts/config

Move migrations/seeds/snapshots to `db/`. Move ORM tool configuration to `config/database/` when supported. Update commands before moving runtime DB code.

### Phase 4 — Business core

Move stable domain logic/services first, then repositories/providers/database/auth/validation/jobs/workflows. Keep batches small enough that broken imports are attributable.

### Phase 5 — View

Move pages/routes/layouts/components/hooks/styles/assets. Preserve route URLs and server/client execution semantics.

### Phase 6 — Entry/framework glue

Centralize composition where safe. Leave thin conventional adapters if the framework requires them.

### Phase 7 — Config cleanup

Move build/test/deploy/lint/format configs. Update every caller.

### Phase 8 — Boundary enforcement

Add import/layer rules, aliases, or tests that prevent business↔view leakage.

### Phase 9 — Final verification

Run full available checks and compare behavior/build outputs where appropriate.

## Move-map rules

Every move should record:

- source path;
- destination path;
- reason;
- semantic role;
- confidence;
- known importers;
- config/manifests referencing it;
- skill/agent-instruction references to it;
- script/CI/generator references to it;
- whether generated;
- whether path is framework-sensitive;
- validation required after move.

## Avoid mega-moves when imports are complex

Do not move hundreds of source files at once merely because Git can track renames. Move coherent dependency slices and repair them before proceeding.

## Preserve history

Use filesystem/Git moves rather than recreate/delete when practical so diffs remain reviewable.

## Case-only renames

On case-insensitive filesystems, use an intermediate rename when changing only capitalization.

## Symlinks and generated directories

Record before moving. Avoid replacing a tool-required generated directory with a symlink unless the tool officially tolerates it and the target platforms support it.

## Path aliases

After target folders are stable, define aliases around architectural ownership, for example:

```text
@business/* -> app/business/*
@view/*     -> app/view/*
@entry/*    -> app/entry/*
```

Avoid dozens of feature aliases with no architectural value.

## Compatibility shims

A good shim is tiny and declarative:

```ts
export { default } from './config/build/vite.config'
```

or:

```json
{ "extends": "./config/typescript/app.json" }
```

A bad shim duplicates logic and creates two sources of truth.

## When to split a file during reorganization

Split only when a single file directly violates the requested architecture and cannot be placed correctly as-is.

Examples:

- route component contains DB query + UI;
- UI hook contains core pricing/ranking policy;
- database module contains provider API calls unrelated to persistence.

Keep the split behavior-preserving and document it in the move map as `MOVE+EXTRACT`, not a pure move.

## Document-path regression check

After the physical move, run `scripts/document_path_audit.py` again. A migration is not complete while mutable skills or task/documentation helpers still reference `documentation/**` or `docs/tasks/**`, because those instructions can recreate the old roots on the next run.
