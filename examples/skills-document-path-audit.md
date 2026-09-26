# Document Path and Skill Reference Audit

**Root:** `/mnt/data/skills-corpus`  
**Text files scanned:** 7  
**Skills found:** 6  
**Skills requiring path updates:** 6

## Canonical document namespaces

```text
documents/
├── documentation/    # current/stable project documentation
├── tasks/            # task lifecycle, plans, evidence, task configuration, lessons
├── research/
├── audits/
├── reports/
├── notes/            # only when the project genuinely uses durable notes
└── archive/
```

## Skills requiring updates

| Skill | Files | References | Safe rewrites | Manual classification |
|---|---|---:|---:|---:|
| `document-task` | `document-task/SKILL.md` | 6 | 6 | 0 |
| `execute-plan` | `execute-plan/SKILL.md` | 1 | 1 | 0 |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 13 | 13 | 0 |
| `plan-task` | `plan-task/SKILL.md` | 8 | 8 | 0 |
| `task-manager` | `task-manager/SKILL.md` | 2 | 2 | 0 |
| `update-documentation` | `update-documentation/SKILL.md` | 8 | 8 | 0 |

## Skill policy review candidates

These lines mention documentation ownership/placement together with task, evidence, log, report, migration, backup, or similar operational concepts. Review their semantics after path normalization; a literal rewrite alone may preserve the wrong ownership rule.

| Skill | File | Line | Policy text |
|---|---|---:|---|
| `document-task` | `document-task/SKILL.md` | 33 | Do not create competing roots, folder indexes, search indexes, templates, schemas, or reports under `documentation/`. |
| `document-task` | `document-task/SKILL.md` | 69 | When no durable documentation file changed, omit `--scope-path`; the command still validates the current structure while historical ledger drift is reported according to policy. Use `--mode full` only when configured or when the task itself reorganized/adopted documentation. |
| `document-task` | `document-task/SKILL.md` | 71 | A stale hash belonging only to another task or an unrelated dirty file is not a reason to park or block this task. Block only when the current task's required documentation, route, source accuracy, preservation evidence, or configured strict global contract cannot pass. |
| `update-documentation` | `update-documentation/SKILL.md` | 13 | When this skill is invoked from `.agents/skills/document-task/SKILL.md`, update only the routed current documentation and return a concise documentation result for the task plan. The task lifecycle files under `docs/tasks/planning/` remain owned by the task-system roles. |
| `update-documentation` | `update-documentation/SKILL.md` | 15 | When `.agents/skills/plan-task/SKILL.md` is installed and a requested documentation change is broad, structural, or user-facing beyond a completed approved task, route through the task planning workflow first unless the user explicitly authorizes immediate documentation maintenan |
| `update-documentation` | `update-documentation/SKILL.md` | 17 | This skill owns documentation routing and current documentation accuracy. It does not own browser verification policy, proof screenshot storage, task lifecycle movement, or commit boundaries. |
| `update-documentation` | `update-documentation/SKILL.md` | 83 | Exit code 0 is mandatory. In task-scoped mode, warnings caused solely by unrelated historical ledger drift do not prevent completion when task configuration allows warnings. The agent MUST NOT refresh unrelated hashes, overwrite another task's documentation, or wait for unrelated |
| `task-manager` | `task-manager/SKILL.md` | 201 | Unrelated pre-existing dirty files, stale hashes in historical documentation-ledger entries, optional cleanup, user-verification waiting, and another task's unmerged work are not blockers for the current item. Apply `documentationCloseout`: validate current-task documentation str |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 13 | When `.agents/skills/plan-task/SKILL.md` is installed and this skill is invoked outside an installer-driven setup/update, do not bypass the task workflow for broad documentation restructuring. Create or follow an approved task plan unless the user explicitly authorizes immediate  |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 15 | This skill owns documentation structure only. It must not create, move, or close task lifecycle plans under `docs/tasks/planning/`, and it must not replace browser verification policy owned by `.agents/skills/browser-verification/SKILL.md`. |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 26 | - Separate search-index JSON, keyword-only indexes, source-context maps, documentation workflow pages, templates, schemas, reports, and generator tests MUST NOT exist under `documentation/`. |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 32 | The agent MUST read root and applicable nested instructions, project/package/build manifests, source entrypoints, configuration, schemas, migrations, tests, scripts, runtime data boundaries, and existing documentation outside the excluded agents tree. |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 38 | Before any write, the agent MUST create `.agents/documentation-system/audits/reorganization-ledger.json` from the package template. Every documentation file considered MUST have a classification, source authority, final disposition, and planned final path. Every moved, renamed, e |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 81 | The index MUST route exact user/task wording and close aliases to primary documentation, supporting documentation, authoritative source paths, and verification context. It MUST link every application Markdown document. It MUST describe each operational root without treating it as |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 85 | Before writing `documentation/project-overview.md`, the agent MUST build a project-facts matrix from current evidence. At minimum, inspect and reconcile: |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 120 | Root `AGENTS.md` MUST direct agents to the root index and project overview, establish the root index as the only documentation router, require source inspection and verification-aware planning, and require same-task index synchronization after documentation-routing changes. A sem |
| `one-shot-documentation` | `one-shot-documentation/SKILL.md` | 129 | An extra root beneath `documentation/` is permitted only for active task ledgers, generated QA evidence, migrations, backups, logs, or comparable operational/historical records. The agent MUST declare the root in the ledger, explain it in `Operational and Historical Records`, and |

## Non-canonical references

| File | Line | Consumer | Current | Recommended | Status |
|---|---:|---|---|---|---|
| `document-task/SKILL.md` | 20 | skill | `documentation/AGENTS.md` | `documents/documentation/AGENTS.md` | SAFE_REWRITE |
| `document-task/SKILL.md` | 20 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `document-task/SKILL.md` | 28 | skill | `documentation/application/` | `documents/documentation/application/` | SAFE_REWRITE |
| `document-task/SKILL.md` | 29 | skill | `docs/tasks/` | `documents/tasks/` | SAFE_REWRITE |
| `document-task/SKILL.md` | 30 | skill | `documentation/agent-observations/` | `documents/documentation/agent-observations/` | SAFE_REWRITE |
| `document-task/SKILL.md` | 66 | skill | `documentation/application/<changed-document>.md` | `documents/documentation/application/<changed-document>.md` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 76 | skill | `docs/tasks/task-system.config.yaml` | `documents/tasks/task-system.config.yaml` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 85 | skill | `docs/tasks/verification-system.config.yaml` | `documents/tasks/verification-system.config.yaml` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 86 | skill | `docs/tasks/verification-capabilities.json` | `documents/tasks/verification-capabilities.json` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 243 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 256 | skill | `docs/tasks/lessons-active.md` | `documents/tasks/lessons-active.md` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 257 | skill | `docs/tasks/lessons-index.json` | `documents/tasks/lessons-index.json` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 258 | skill | `docs/tasks/lessons.md` | `documents/tasks/lessons.md` | SAFE_REWRITE |
| `plan-task/SKILL.md` | 436 | skill | `docs/tasks/task-system-helpers/create-plan-folder.py` | `documents/tasks/task-system-helpers/create-plan-folder.py` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 13 | skill | `docs/tasks/planning/` | `documents/tasks/planning/` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 21 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 22 | skill | `documentation/application/` | `documents/documentation/application/` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 23 | skill | `documentation/project-overview.md` | `documents/documentation/project-overview.md` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 26 | skill | `documentation/agents/` | `documents/documentation/agents/` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 27 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 31 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `update-documentation/SKILL.md` | 54 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `execute-plan/SKILL.md` | 91 | skill | `docs/tasks/lessons-active.md` | `documents/tasks/lessons-active.md` | SAFE_REWRITE |
| `task-manager/SKILL.md` | 16 | skill | `docs/tasks/task-system.config.yaml` | `documents/tasks/task-system.config.yaml` | SAFE_REWRITE |
| `task-manager/SKILL.md` | 18 | skill | `docs/tasks/verification-system.config.yaml` | `documents/tasks/verification-system.config.yaml` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 15 | skill | `docs/tasks/planning/` | `documents/tasks/planning/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 20 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 21 | skill | `documentation/application/` | `documents/documentation/application/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 22 | skill | `documentation/project-overview.md` | `documents/documentation/project-overview.md` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 23 | skill | `documentation/agent-observations/` | `documents/documentation/agent-observations/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 27 | skill | `documentation/agents/` | `documents/documentation/agents/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 28 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 44 | skill | `documentation/application/` | `documents/documentation/application/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 46 | skill | `documentation/agents/` | `documents/documentation/agents/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 67 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 85 | skill | `documentation/project-overview.md` | `documents/documentation/project-overview.md` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 116 | skill | `documentation/application/` | `documents/documentation/application/` | SAFE_REWRITE |
| `one-shot-documentation/SKILL.md` | 118 | skill | `documentation/0-index.md` | `documents/documentation/0-index.md` | SAFE_REWRITE |

> SAFE_REWRITE means the path prefix has an unambiguous canonical equivalent. REVIEW means the reference is document-related but its contents must be classified before moving or rewriting it.
