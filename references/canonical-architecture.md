# Canonical Architecture Reference

## Design objective

Organize repositories by **product responsibility**, not by the vendor/tool that happens to implement that responsibility.

Technology can change without forcing the project tree to become a historical record of old frameworks.

## Top-level ownership

| Path | Owns | Does not own |
|---|---|---|
| `app/business` | domain rules, services, workflows, repositories, providers, auth, validation, jobs, DB runtime | UI rendering, generated migrations |
| `app/view` | routes/pages/layouts/components/hooks/styles/assets | DB clients, raw SQL, core business rules |
| `app/entry` | process/runtime/framework startup and composition | core business rules |
| `db` | migrations, seeds, snapshots, DB artifact metadata | runtime service logic |
| `config` | relocatable tool/build/test/deploy configuration | source code |
| `documents/documentation` | current/stable project documentation and documentation-system state | runtime source, task lifecycle |
| `documents/tasks` | task lifecycle, planning, evidence, task config/helpers/lessons | runtime source, current product documentation |
| `documents/research` | research material | runtime source |
| `documents/audits` | audit outputs | runtime source |
| `documents/reports` | generated/periodic project reports | runtime source |
| `tests` | cross-cutting integration/e2e/contract tests | product runtime |
| `scripts` | repository/operator automation | main app runtime unless explicitly a CLI product |
| `public` | public static assets | private source assets |

## Business internals

### `domain/`
Pure or mostly pure product concepts, policies, entities/value objects, domain calculations, eligibility rules, ranking/scoring rules, and stable domain contracts.

### `services/`
Application-level orchestration for user/system use cases that coordinate domain logic and dependencies.

### `workflows/`
Durable or multi-step execution, queues, long-running jobs, retries, pipeline definitions, workflow state machines.

### `repositories/`
Persistence abstraction contracts and implementations when the codebase benefits from explicit repository boundaries.

### `providers/`
External vendor/service adapters: payments, analytics, email, AI, SEO APIs, search, third-party storage, external authentication, etc.

### `database/`
Runtime database clients, ORM schema source, query code, persistence adapters, transactions.

### `auth/`
Server-side authentication and authorization policies, guards, session/access adapters.

### `validation/`
Boundary validation and reusable product validation that does not belong to one domain module.

### `jobs/`
Scheduled/background job definitions that are not better represented as durable workflows.

### `shared/`
Use sparingly for stable business primitives shared by multiple domains. Every item should have a clear reason it cannot live in one domain.

## View internals

### `routes/`
Framework route registration, route loaders/actions, route-level boundary code.

### `pages/`
Screen/page composition.

### `layouts/`
Shared page/application shells.

### `components/`
Reusable presentational and interaction components.

### `features/`
UI feature modules whose logic is presentation-specific (local state, feature-specific components, view models).

### `hooks/`
UI/runtime hooks. Business rules should not be hidden here.

### `charts/`
Chart-specific presentation components and formatting.

### `styles/`
CSS/theme/design-token implementation.

### `assets/`
Source-controlled UI assets imported by the application.

## Entry internals

`app/entry` may contain whichever startup boundaries the repository needs:

```text
client/
server/
router/
worker/
cli/
cron/
functions/
```

If a framework requires entry files elsewhere, keep only forwarding/composition glue there when possible.

## Database placement examples

```text
app/business/database/schema/users.ts   # ORM schema source
app/business/database/client/d1.ts      # runtime DB client
app/business/repositories/user.repo.ts  # application persistence behavior

db/migrations/sqlite/0001_init.sql      # migration artifact
db/seeds/dev.ts                          # seed artifact

config/database/drizzle.config.ts       # database tool config
```


## Documents namespace

Use one top-level project-knowledge root:

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

The default root normalization is:

```text
documentation/**      -> documents/documentation/**
docs/tasks/**         -> documents/tasks/**
```

Preserve the relative subtree of installed documentation/task systems during root normalization. Classify generic `docs/**` by content instead of moving it blindly. Installed skills and automation that reference the old paths are dependencies and must move with the filesystem contract.

## Root cleanliness

The root should answer “what repository is this and how is it built?” rather than containing application internals.

Expected root occupants can include:

- README/license/contributing metadata;
- package/build manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, solution files, etc.);
- lockfiles;
- `.gitignore`, `.gitattributes`, editor metadata where justified;
- minimal root config shims required for tool discovery;
- workspace manifests.

Everything else should justify why it cannot live in an owned folder.
