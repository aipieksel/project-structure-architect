# Project Structure Audit

## Executive assessment

## Current structure

```text
<tree>
```

## Detected project profile

| Category | Detected |
|---|---|
| Languages | |
| Frameworks | |
| Runtime | |
| Database / ORM | |
| Build | |
| Tests | |
| Deployment | |
| Workspace / monorepo | |

## Current architecture / request flow

## Structural findings

### Critical

### High

### Medium

### Low

## Recommended final structure

```text
<tree>
```

## Move map

| Current | Recommended | Action | Confidence | Why | References to update | Risk |
|---|---|---|---|---|---|---|

## Root and configuration cleanup

| File | Tool | Status | Recommended path | Invocation/reference changes | Shim? |
|---|---|---|---|---|---|

## Document namespace migration

| Current root/path | Canonical path | Classification | References to update | Status |
|---|---|---|---|---|

## Skills and agent instructions requiring updates

| Skill/instruction | File | Current path literal(s) | Canonical path literal(s) | Update required? | Verification |
|---|---|---|---|---|---|

## Other document-path consumers

| Consumer | File | Old path | New path | Risk |
|---|---|---|---|---|

## Dependency boundaries

## Migration phases

## Verification plan

## Exceptions / unresolved items

## Mandatory target and completion reconciliation

Status: `audit_only | partially_implemented | blocked | complete`

| Requirement / owner | Original current path | Planned target | Actual path | Result / verification | Exception ID or remaining action |
| --- | --- | --- | --- | --- | --- |

| Exception ID | Exact consumer/version | Constraint evidence | Alternatives tested | Why alternatives fail | Verification | verified_exception / deferred_required / unresolved |
| --- | --- | --- | --- | --- | --- | --- |

| Application/workspace | Business responsibilities | View responsibilities | Entry points | Independent package consumers | Coverage gaps |
| --- | --- | --- | --- | --- | --- |

Record original targets, evidenced revisions and before/after metrics. Name every root-shim consumer. List required pending activation, moves and checks explicitly. Do not mark complete while any required row is deferred or unresolved. Preserve monorepo identities; do not exempt their contents from responsibility-based organization.
