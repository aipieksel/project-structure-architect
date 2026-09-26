# Project Reorganization Ledger

| Phase | Scope | Status | Validation | Notes |
|---|---|---|---|---|
| 00 | Baseline inventory | PENDING | | |
| 01 | Documents namespace + skill/path consumers | PENDING | | |
| 02 | DB artifacts/config | PENDING | | |
| 03 | Business source | PENDING | | |
| 04 | View source | PENDING | | |
| 05 | Entry/framework glue | PENDING | | |
| 06 | Build/test/deploy config | PENDING | | |
| 07 | Boundary enforcement | PENDING | | |
| 08 | Full verification | PENDING | | |

## Baseline failures

## Move decisions

| Current | Target | Action | Status | Validation |
|---|---|---|---|---|

## Skill/instruction path updates

| Skill/instruction | File | Old path | New path | Status | Verification |
|---|---|---|---|---|---|

## Legacy document-root regression check

- `documentation/**` references remaining: 
- `docs/tasks/**` references remaining: 
- helpers/generators verified not to recreate legacy roots: 

## Exceptions

## Mandatory target and completion reconciliation

Status: `audit_only | partially_implemented | blocked | complete`

| Requirement / owner | Original current path | Planned target | Actual path | Result / verification | Exception ID or remaining action |
| --- | --- | --- | --- | --- | --- |

| Exception ID | Exact consumer/version | Constraint evidence | Alternatives tested | Why alternatives fail | Verification | verified_exception / deferred_required / unresolved |
| --- | --- | --- | --- | --- | --- | --- |

| Application/workspace | Business responsibilities | View responsibilities | Entry points | Independent package consumers | Coverage gaps |
| --- | --- | --- | --- | --- | --- |

Record original targets, evidenced revisions and before/after metrics. Name every root-shim consumer. List required pending activation, moves and checks explicitly. Do not mark complete while any required row is deferred or unresolved. Preserve monorepo identities; do not exempt their contents from responsibility-based organization.
