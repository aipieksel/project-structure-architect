# Source Classification Rules

## Classification method

Do not decide placement from names alone. For each material path, inspect:

1. who imports/calls it;
2. what it imports/calls;
3. whether it executes in browser, server, worker, CLI, build, test, or migration context;
4. whether it contains business policy, persistence code, provider integration, UI rendering, configuration, or generated output;
5. whether a framework/tool discovers it by physical location;
6. whether the file is source-of-truth or generated;
7. whether moving it changes public/module/package identity.

## Confidence levels

- **HIGH**: role is directly supported by code/runtime/manifest evidence.
- **MEDIUM**: role is strongly suggested but cross-cutting or mixed.
- **LOW**: ambiguous ownership; investigate callers and runtime before moving.

## TypeScript / JavaScript

Inspect:

- `package.json` dependencies/devDependencies/scripts/exports/imports;
- workspace configuration;
- `tsconfig*` paths, references, rootDir/include/exclude;
- `vite`, `webpack`, `rollup`, `esbuild`, `rolldown`, framework config;
- `.tsx/.jsx` and UI-framework imports;
- server/client directives;
- route generation;
- ORM imports;
- API/provider SDK imports;
- alias imports (`@/`, `~/`, etc.);
- codegen output.

Heuristics:

- JSX/TSX + React/Vue/Solid UI rendering → likely `view`.
- route file containing loader/action plus component → may need split: framework route adapter in `view/routes`, business use case in `business/services`.
- Drizzle/Prisma/Kysely/Knex/SQL runtime imports → `business/database` or repository implementation, not view.
- long-running pipeline/retry/queue code → `business/workflows`.
- API vendor client → `business/providers/<provider>`.

## Python

Inspect:

- `pyproject.toml`, `requirements*`, Poetry/PDM/uv config;
- package layout and import paths;
- Django apps, FastAPI/Flask routers;
- SQLAlchemy/Django ORM models;
- Alembic migrations;
- Celery/RQ/Dramatiq jobs;
- Jinja/templates/static assets;
- pytest config and fixtures.

Potential mapping:

```text
routers/controllers -> app/view/routes or app/entry boundary
Jinja/templates -> app/view
services/usecases -> app/business/services
domain/models (non-ORM) -> app/business/domain
SQLAlchemy runtime/models -> app/business/database
Alembic versions -> db/migrations
Celery tasks/workflows -> app/business/jobs or workflows
```

Preserve Python package importability; add `__init__.py` only when appropriate to the package strategy.

## Go

Inspect packages, `go.mod`, `cmd/`, `internal/`, generated files, embed directives, SQL generators, migration tools.

Do not blindly eliminate idiomatic `cmd/` or `internal/`. Map intent to canonical ownership while preserving package boundaries. A deployable Go binary may use a thin `cmd/<name>/main.go` as a root-framework exception that composes `app/entry/...`.

## Rust

Inspect Cargo workspace/crates, `src/main.rs`, `src/lib.rs`, `src/bin`, build scripts, migrations, generated code. Respect crate boundaries and module visibility. Use canonical architecture within a crate or through clearly owned workspace crates.

## PHP

Inspect Composer autoload/PSR mappings, Laravel/Symfony conventions, WordPress plugin/theme conventions, framework bootstraps, templates/views, database migrations.

For WordPress, do not force theme presentation and plugin business functionality into one physical application folder if WordPress deployment conventions require separate theme/plugin packages. Apply the canonical business/view separation inside the deployable plugin/theme or workspace package and document the exception.

## Ruby

Inspect Rails/Bundler conventions, Zeitwerk autoloading, jobs, services, models, migrations, views. Rails physical conventions can be framework exceptions; prefer dependency boundaries and service/domain extraction over breaking autoloading.

## Java / Kotlin

Inspect Maven/Gradle modules, source sets, package declarations, Spring controllers/services/repositories, resources, migrations. Moving files may require package declaration changes. Treat package names/public APIs as migration risk.

## C# / .NET

Inspect `.sln`, `.csproj`, SDK-style globbing, namespaces, ASP.NET controllers/pages, EF Core migrations, generated partials. A clean physical tree must not silently alter namespace/public API expectations unless requested.

## Swift

Inspect SwiftPM manifests, Xcode project/workspace/targets, app lifecycle entry points, generated assets, tests. Prefer logical target boundaries and do not assume filesystem-only moves are reflected safely in Xcode projects.

## UI-vs-business decision tests

Ask:

- Would this code still make sense if the product switched from React to another UI? If yes, it probably belongs in business.
- Does it decide *what should happen*, or only *how to present/interact with it*?
- Does it require browser/UI state, DOM, CSS, rendering primitives? Likely view.
- Does it enforce product eligibility, scoring, workflow, authorization, persistence, provider calls? Likely business.

## Mixed files

Do not preserve a bad mixed responsibility just because it exists.

Example:

```text
route.tsx
  - validates request
  - authorizes project
  - queries DB
  - computes audit score
  - renders page
```

Recommended split:

```text
app/view/routes/route.tsx                 # framework/view boundary
app/business/services/load-audit.ts       # use case
app/business/domain/audit/score.ts        # scoring rule
app/business/repositories/audit.ts        # persistence contract/impl
```

Structural reorganization may include responsibility-preserving extraction when needed to achieve the requested separation, but avoid unrelated refactors.
