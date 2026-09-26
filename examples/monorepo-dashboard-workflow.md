# Example: dashboard and research workflow monorepo

Illustrative responsibilities for a repository with a browser dashboard, local research API, cloud review worker and genuinely independent packages. Preserve actual workspace identities, stack, public exports and deployable units. Names below are examples, not instructions to create new packages or empty layers.

```text
project/
├── apps/
│   ├── dashboard/
│   │   ├── app/
│   │   │   ├── view/
│   │   │   │   ├── pages/
│   │   │   │   ├── components/
│   │   │   │   ├── features/{topic-finder,blog-writer,component-gallery}/
│   │   │   │   ├── hooks/
│   │   │   │   └── assets/
│   │   │   └── entry/client/
│   │   └── package.json             # only if this is an existing workspace
│   ├── workflow-api/
│   │   ├── app/
│   │   │   ├── business/
│   │   │   │   ├── domain/{opportunities,keywords,content}/
│   │   │   │   ├── workflows/{discovery,missing-research,drafting}/
│   │   │   │   ├── providers/{dataforseo,ai-cli,competitor-pages}/
│   │   │   │   ├── repositories/
│   │   │   │   ├── database/
│   │   │   │   └── jobs/
│   │   │   └── entry/server/
│   │   └── package.json
│   └── review-worker/
│       ├── app/
│       │   ├── business/{auth,workflows,repositories,providers}/
│       │   └── entry/{worker,queue}/
│       └── package.json
├── packages/
│   ├── ui/                         # independently reusable components
│   ├── workflow-contracts/         # only if stable real consumers justify it
│   ├── ai-cli-integration/
│   └── other-existing-packages/    # retain actual public identities
├── db/
│   ├── migrations/{workflow-sqlite,review-postgres}/
│   └── seeds/
├── config/
│   ├── build/
│   ├── deployment/
│   ├── database/
│   ├── testing/
│   └── typescript/
├── data/topic-finder/{runs/<run-id>,shared}/  # durable product results
├── tmp/{screenshots,logs,research-diagnostics}/
├── backups/<operation>/<timestamp>/
├── documents/{documentation,tasks,audits}/
├── tests/{integration,e2e,fixtures}/
├── scripts/                        # thin start/build/operator commands
├── public/
├── package.json
├── package-lock.json               # retain the project's actual package manager
├── tsconfig.json                   # only with an evidenced discovery consumer
├── README.md
└── LICENSE
```

This remains a monorepo: multiple units and shared packages are developed in one repository. A browser-only dashboard does not need an empty business layer. The research service owns business behavior; the dashboard calls HTTP and shared contracts. Independent package internals retain an appropriate cohesive package structure; they are not forced into application folders.

## Responsibility map

| Existing item | Intended owner | Completion evidence |
| --- | --- | --- |
| scripts containing discovery, classification, scoring and drafting | workflow application's business domain/workflows | imports, request paths, resume/budget semantics and persistence tests preserved |
| local HTTP server bootstrap | application's entry/server | same endpoints and configured runtime roots; activation verified when required |
| shared offer/proposal contracts | existing owning application or independently justified shared package | real browser/server consumers and public contract preserved; no junk-drawer exemption |
| UI library | existing independent package | exports and consuming applications verified |
| SQL migrations | owned DB artifact tree | same migration bytes/history; packaging and invocation updated |
| root Vite/Vitest configs | config with explicit command paths | all owned callers repaired; any remaining shim has named consumer evidence |

A DB package that distributes migrations independently needs its packaging contract investigated. If a compatible packaging change can preserve distribution, perform the proven-safe change within scope. If a physical path is technically required, retain it with an exception ID and verification. “It is in package.json” alone is not proof that every alternative fails.

## Active-service example

The research API is running. Inventory its resources, preserve data, prepare relocations and compatibility launchers, and verify isolated code paths. Do not restart without task authority. If activation is required but pending, report `partially_implemented` with the remaining action. Do not leave the whole research engine under scripts and declare the target complete.

## Honest final comparison

| Required outcome | Actual outcome | Status |
| --- | --- | --- |
| Preserve all workspace identities | Identities and consumers verified | implemented |
| Move research implementation to business owner | Production modules still under scripts | deferred_required |
| Activate repaired entrypoint | Existing process still runs old implementation | deferred_required |
| Validate dashboard and service contracts | Compiler and isolated tests pass | passed within stated boundary |

Overall status: `partially_implemented`. Passing tests or moving hundreds of other files cannot erase the two pending requirements. Once those requirements and their necessary verification are satisfied, completion may be reported. Do not demand a deployment that the task never requested.

For runtime contents, apply [runtime-storage.md](../references/runtime-storage.md). Keep screenshots/debug logs out of the product data tree, backups separate, and the shared catalog distinct from per-run records. Run directories must participate in the storage read/write path; one-time exports do not complete the change.
