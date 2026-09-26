# Mandatory architecture conformance and completion

Read this contract before designing a target tree and again before reporting completion. It governs every apply run, including monorepos. Examples illustrate the contract; they do not replace source inspection. User instructions remain authoritative.

## 1. Preserve the monorepo, reorganize each application

Preserve workspace membership, independent package identities, exports and deployable boundaries unless the user explicitly authorizes changing them. A monorepo is not an exception to the target architecture.

For every real application, assign its existing responsibilities to `app/business`, `app/view` and `app/entry` inside its application root. Omit only responsibilities the application does not have; do not create empty folders. A browser-only application may need view and entry only. A service may need business and entry only. Keep independently reusable packages under `packages`, with an evidenced owner and public contract. Do not merge all applications into a single root app or create new workspaces merely for appearance.

Record each application's identity, deployment/runtime entry, current source roots, target responsibilities, package consumers and verification commands. Moving `src` wholesale into another generic folder does not complete semantic classification. Review mixed files and split independently owned responsibilities where necessary to satisfy the target without changing behavior.

## 2. Responsibility takes precedence over inherited location

Classify research/discovery pipelines, scoring, validation, job lifecycle, providers and persistence as application business responsibilities. A file does not become repository automation merely because it lives under `scripts`. Keep thin operator commands, maintenance scripts and launchers there; move reusable product implementation into its actual application owner and repair the entrypoint.

Classify every `shared`, `lib`, `core`, `services` and similar container by exports, callers and runtime role. Keep an existing shared package when multiple real consumers use its stable contract. Do not retain a generic root because moving its imports is inconvenient, nor create a package for every helper. Database runtime and artifacts must have distinct ownership; preserve genuinely independent package distribution requirements with the evidence below.

## 3. Exceptions require proof

For every proposed deviation, record:

| ID | Required target | Retained path | Exact consumer/tool/version | Constraint evidence | Alternatives investigated | Why alternatives fail | Verification | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Valid dispositions are `verified_exception`, `deferred_required`, and `unresolved`. A verified exception requires concrete source/configuration/distribution evidence and a check that the retained path works. Test configurable paths, thin adapters or repaired callers where safe. Do not perform paid or production operations to prove an exception.

“Monorepo,” “existing convention,” “currently running,” “many imports,” “too risky,” or “tests pass” alone are not exception evidence. A package manifest shipping migrations is evidence of a distribution obligation, but investigate whether its packaging step can preserve that obligation after relocation before deciding the physical path must stay. Ambiguity stays unresolved; never guess or delete.

Record target revisions with the user's constraint or newly discovered technical evidence that justifies them. An agent cannot retroactively redefine the target to match incomplete work. User-requested exclusions remain excluded and must not be presented as implementation failures.

## 4. Running services affect sequence, not architectural ownership

Inspect process ownership and module-relative resources. Prepare safe changes, compatibility entrypoints, checkpoints, verification and an activation/rollback plan. Continue independent work while preserving running services and live data.

A running process is not permanent evidence that production code belongs under scripts. If a required move or activation cannot safely happen yet, record `deferred_required`, its exact remaining action, affected requirement and prerequisite. Obtain restart authority only when genuinely missing; never infer it from this skill, and never ask again if current task authority already covers it. Pending required activation means the migration is incomplete. Preserve unresolved files while continuing proven-safe work.

## 5. Explicit configuration paths first

Inspect installed tool versions and every caller: package scripts, CI, editors, launchers, generators, hosting and external commands. Use supported explicit configuration paths and update owned callers together.

Retain a root shim only for a named, verified consumer that requires discovery and cannot be updated within authorized scope. A general claim that editors or tools might prefer it is insufficient. Record the consumer and evidence; unknown external callers are unresolved, not an automatically accepted exception. Remove unused shims after reference and execution checks. Keep genuine root manifests and legal/discovery anchors.

## 6. Freeze a complete target before mutation

Before cleanup moves, record a specialized target tree and a coverage table for every material current source/config/database/test/docs/script root. Each row has an owner, current path, intended path, disposition, dependencies, verification and requirement ID. Group paths only when every matched item shares the role and migration behavior.

Set measurable targets for responsibility coverage, remaining misplaced production modules, competing roots, config relocations, shims and root surface. File counts are supporting evidence, not the primary goal. Audit-only or preview requests remain read-only; this rule does not introduce a new approval round into authorized unattended execution.

At handoff, compare actual paths to the original target plus explicitly evidenced revisions. Account for every row as implemented and verified, verified exception, deferred required or unresolved. Include remaining work with concrete next actions. No row disappears into “out of scope” without user authority or demonstrated irrelevance.

## 7. Completion is a requirement-level claim

Report one status prominently:

- `complete`: every in-scope target is implemented and verified, or satisfied by a verified technical exception with its evidence. No required move, activation or verification remains pending.
- `partially_implemented`: meaningful work landed but required moves/activation/checks remain. List them, even when tests pass and commits are clean.
- `blocked`: a concrete prerequisite prevents remaining progress. Preserve completed work and specify what resolves the blocker.
- `audit_only`: no implementation was requested or performed.

Do not label a migration complete because many files moved, the root looks cleaner, compiler/tests passed, time is short, or a commit exists. Do not count a waiver or unrun check as passed. Report code, activation, runtime verification, commits, push, deployment and user acceptance separately where relevant. In-scope verification is not optional merely because it is inconvenient; unrequested publication is not a completion prerequisite.

## 8. Review with contrasting scenarios

Before finalizing an audit or migration, check these cases against its ledger:

1. Multiple workspaces: preserve their identities and classify each application's responsibilities.
2. A research engine under scripts: move the implementation to its application business owner; retain a thin command if needed.
3. A claimed package exception: demand distribution/caller evidence and examine compatible alternatives.
4. An active worker: sequence safe preparation and authorized activation; pending activation stays incomplete.
5. An unused root shim: remove after checking callers; keep an editor shim only with evidence.
6. Hundreds of moves but untouched required business roots: report partial, not complete.
7. Passing tests with a missing required browser/runtime check: report the remaining verification, not success.
8. An application with no UI or database: omit empty layers; do not change its stack to imitate an example.

See the [monorepo example](../examples/monorepo-dashboard-workflow.md).

## 9. Runtime storage conformance

When runtime material exists, read runtime-storage.md and add separate coverage rows for durable domain/run data, temporary/debug output, recovery backups, local service state and dependency installations. A blanket var → data rename fails this gate. Require producer/reader repairs, run save/load integration when applicable, lifecycle/retention decisions and byte/record preservation. Screenshots, operational logs and backup copies must not be mixed into durable business data merely because their previous parent was named var. Do not move package-manager dependency installations into config without a supported, verified tool configuration.
