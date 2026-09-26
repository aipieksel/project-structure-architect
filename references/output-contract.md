# Output Contract

## Audit / plan report

Use this order unless the user requests another format.

### 1. Executive assessment

State whether the repository is already close to the canonical architecture and the largest structural risks.

### 2. Current repository structure

Show a useful tree, excluding vendor/build/cache directories.

### 3. Detected project profile

Include:

- languages;
- frameworks;
- runtimes;
- package/build systems;
- database/ORM;
- external providers;
- testing;
- deployment;
- monorepo status.

### 4. Current architecture map

Explain how requests/data flow today based on source evidence.

### 5. Structural findings

Rank findings by impact. Include specific paths.

### 6. Recommended final structure

Show the actual proposed tree with discovered product domains/features inserted.

### 7. Move map

Required table:

| Current | Recommended | Action | Confidence | Why | References to update | Risk |
|---|---|---|---|---|---|---|

Actions:

- `MOVE`
- `MOVE+RENAME`
- `MOVE+EXTRACT`
- `KEEP`
- `KEEP_ROOT_SHIM`
- `GENERATE_TO_NEW_PATH`
- `DELETE_GENERATED` only when safe and regenerated
- `REVIEW`

### 8. Root/config cleanup matrix

Show every meaningful root config and whether/how it moves.

### 9. Document namespace and skill-impact matrix

Show:

- physical legacy roots (`docs/`, `documentation/`, task roots, etc.);
- canonical destination for each;
- every installed skill/instruction that names an affected path;
- old path literal -> new path literal;
- scripts/CI/generators/package commands that must also change;
- whether each rewrite is safe or requires semantic review.

### 10. Dependency boundary plan

Show intended allowed dependency directions and current violations.

### 11. Migration sequence

Dependency-safe phases with validation after each.

### 12. Verification commands

Use actual repository scripts/commands; do not provide generic placeholders if the repo already defines them.

### 13. Exceptions and unresolved items

Framework-required paths, generated paths, ambiguous ownership, externally configured paths.

## Apply-mode final report

Include all of the above plus:

- exact moves completed;
- import/config/script/CI changes;
- document namespace moves;
- skills/instructions updated and exact path mappings;
- final tree;
- exact verification commands and results;
- remaining exceptions;
- Git diff/stat overview.

## Mandatory target reconciliation

Apply the [conformance contract](conformance-and-completion.md). Start final reports with `complete`, `partially_implemented`, `blocked`, or `audit_only`. Include a row for every original requirement/current root: planned path, actual path, verified result, exception ID or remaining action. List per-application responsibility coverage, remaining misplaced production modules, root shims with named consumers, target metrics and evidenced target revisions. Deferred activation is not an accepted technical exception. Required unfinished moves or checks forbid a complete claim.
