# Runtime data, temporary output and backups

Use when the repository contains live state or mixed folders such as var, runtime, output or scratch. User instructions override these defaults. This reference does not authorize deleting retained material or interrupting services on its own; honor existing task-scoped authority without asking again.

## Classify contents before choosing destinations

| Responsibility | Default destination | Examples |
| --- | --- | --- |
| Durable product records and outcomes | data/<domain>/ | opportunities, articles, user uploads, saved research, history |
| Run-owned durable inputs/results/evidence | data/<domain>/runs/<stable-run-id>/ | input, run metadata, keyword results, opportunity results, citations, checkpoints and resume receipts |
| Shared cross-run product state | data/<domain>/shared/ or a named catalog/index | reusable evidence, catalog and deduplication index; document cross-run references |
| Temporary verification/debug output | tmp/<purpose>/, optionally grouped by task/run | development screenshots, browser captures, build/test output, request traces and diagnostics |
| Operational logs and disposable caches | tmp/logs/<service>/ and tmp/cache/<owner>/ | launcher logs, worker logs, regenerable caches |
| Recovery copies | backups/<operation-or-owner>/<timestamp>/ | database backups, pre-migration copies, restoration manifests |
| Local service internals and secrets | existing supported ignored service/secret location, e.g. .local/<service>/ | sessions, service clusters, encryption keys; do not present them as product run results |
| Source-controlled schema and migration artifacts | db/ | schema changes, seeds and migration metadata; never substitute live DB files |
| Tool-managed dependency installation | package manager's supported location | npm workspace node_modules normally belongs at the monorepo root, not config |

A screenshot can be a real product upload; a request receipt can be essential paid evidence. Inspect its producer, consumers and retention needs, not only its extension. Do not label unique research evidence or resume checkpoints disposable simply because they look like logs. Promote essential evidence into durable run storage before making debug traces disposable. Unknown provenance remains preserved and explicitly classified as unresolved.

## Required inventory and implementation

Record owner, current path, destination, producer, readers, retention, sensitivity, active-process use and recovery method for every material group. Expose mixed children: one row saying var → data does not satisfy this requirement.

Where run-based storage is required, update save AND load behavior. One-time exports or empty folders are not implementation. Define the source of truth, index/transaction role, atomic write behavior, interrupted-write recovery and handling of shared or legacy records with no surviving run. Preserve catalog entries independently of run retention; never manufacture research history from orphaned opportunities. Do not overwrite historical records or initiate new paid research to fill missing files.

Separate data, tmp and backups physically and update scripts, launchers, generators and active documentation so later runs continue writing to the right owners. Sensitive local files must remain untracked and keep restrictive permissions. Record necessary tool discovery paths rather than moving node_modules, virtualenvs or other installations into config without supported tooling evidence.

## Lifecycle and validation

- data is durable. Retain product records, evidence and history according to product behavior.
- tmp may be cleaned only after checking active users and durable dependencies. No blanket age-based deletion or automatic purging is introduced by reorganization. Retained old debug material can stay in tmp pending explicit cleanup, but document that it is not the sole copy of required business evidence.
- backups is a recovery boundary, not an application read/write store. Keep provenance, date, restoration instructions and retention status. Preserve existing backups during organization; do not call backups disposable scratch or silently delete them.
- Source test fixtures, approved reference images and durable task/audit records keep their documented ownership; do not move them into tmp based on file type.
- Before an authorized live move, take consistent backups, stop or quiesce owned writers, move without dropping data, compare file hashes and logical records, and activate repaired readers/writers. Do not initialize empty replacement stores when data is missing.
- Verify new run writes, existing run reads, restart/recovery, missing/corrupt file repair, shared-catalog preservation, ignored sensitive directories and no legacy destination recreation. Do not confuse a clean Git tree with a classified physical tree.

Completion requires both classified existing content and correct ongoing writers/readers. Report pending migrations, activation or required checks explicitly.
