# Verification Matrix

Select checks based on the detected project. Never invent passing results.

| Area | What to verify | Typical evidence |
|---|---|---|
| Git safety | user changes preserved | `git status --short`, diff review |
| Dependencies | manifests/lockfiles coherent | package-manager frozen/immutable install or lock check |
| Types/compile | imports and module resolution work | `tsc`, compiler/build |
| Lint | boundary/import/path rules | project lint command |
| Format | config discovery still works | project format check |
| Unit tests | pure logic unaffected | project unit test command |
| Integration tests | DB/provider/service wiring | integration test suite |
| Routes | same route set and loaders/actions | route generation/build/smoke |
| UI | pages render after moves | browser smoke/e2e |
| DB schema | ORM schema still discovered | generate/introspect/check command |
| Migrations | migration output/history valid | generate dry run/status/test DB |
| Seeds | paths and imports valid | seed dry run/test environment |
| Build config | moved config discovered | build command with explicit config |
| Test config | tests still discovered | unit/e2e list/run |
| Deploy config | platform config discovered | deployment dry run/build |
| Docker | COPY/working dir paths valid | image build/compose config |
| CI | workflows reference new paths | grep + workflow/lint where available |
| Documents namespace | no unintended legacy `documentation/` or `docs/tasks/` roots/references | `document_path_audit.py`, targeted grep, tree review |
| Skills/instructions | affected skills point to canonical `documents/**` paths | skill-impact report + targeted read |
| Task/doc generators | future runs do not recreate legacy roots | run/list helper output or inspect generator configuration |
| Docs | internal links updated | link check/manual targeted scan |
| Generated code | generator emits to expected path | regeneration/diff |
| Boundaries | view/business separation persists | dependency graph/lint/import scan |

## Final result labels

- **PASS** — command completed successfully.
- **PASS_WITH_WARNINGS** — success with known non-structural warnings.
- **PRE_EXISTING_FAILURE** — failed before migration and remains equivalent.
- **REGRESSION** — migration introduced failure; must fix before declaring completion.
- **NOT_AVAILABLE** — repository provides no meaningful check.
- **NOT_RUN** — intentionally skipped; state exact reason.

## Minimum quality bar for apply mode

Do not call the migration complete while any known structural regression remains.
