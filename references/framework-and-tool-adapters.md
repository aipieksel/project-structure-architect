# Framework and Tool Adapter Reference

This reference provides patterns, not permission to assume. Always inspect the exact installed version and current invocation.

## General config relocation strategy

Preferred order:

1. native config path option (`--config`, `-c`, manifest field);
2. tool-specific config path setting in another root manifest;
3. root shim that imports/extends real config;
4. retain root config and document why.

Whenever a config moves, update all invocations: local scripts, CI, Docker, deployment, codegen, docs, editor tasks, and automation.

## Vite

Modern Vite supports an explicit config path:

```bash
vite --config config/build/vite.config.ts
vite build --config config/build/vite.config.ts
```

A Vite config may therefore usually move away from root when every invocation is controlled.

Potential path-sensitive concerns:

- `root` option;
- aliases resolved relative to config location vs project cwd;
- env directory;
- plugin paths;
- build output paths;
- Vitest inheritance from Vite config;
- framework wrappers that invoke Vite indirectly.

## Drizzle Kit

Drizzle Kit supports explicit config paths:

```bash
drizzle-kit generate --config=config/database/drizzle.config.ts
drizzle-kit migrate --config=config/database/drizzle.config.ts
```

Use Drizzle config to point ORM source at application database schema and migration output at root `db/`:

```ts
export default defineConfig({
  schema: './app/business/database/schema/*',
  out: './db/migrations/sqlite',
  // dialect / credentials / other options...
})
```

Do not move generated migration metadata independently from the migration output format expected by Drizzle.

## Cloudflare Wrangler

Wrangler supports explicit config paths for Worker commands:

```bash
wrangler dev --config config/deployment/wrangler.jsonc
wrangler deploy --config config/deployment/wrangler.jsonc
```

Inspect platform integrations and hosted build settings before removing a conventional root file.

## Vitest

Vitest supports explicit config paths:

```bash
vitest --config config/testing/vitest.config.ts
```

If Vitest currently inherits from `vite.config`, moving/splitting configs may change behavior. Preserve shared plugins/aliases explicitly.

## Playwright

Playwright supports `--config` / `-c`:

```bash
playwright test --config config/testing/playwright.config.ts
```

Remember that some paths inside Playwright config are resolved relative to the config file or process cwd depending on the option. Verify test discovery and reporter output after moving.

## TypeScript

A root `tsconfig.json` is frequently useful to editors, frameworks, and tools even when the substantive config is elsewhere.

Preferred pattern when compatible:

```json
{
  "extends": "./config/typescript/app.json"
}
```

Keep a tiny root file only when a named editor/framework consumer demonstrably requires discovery and cannot be updated within scope; otherwise use the supported explicit project path. Record the evidence in the mandatory exception table.

## ESLint / formatters / linters

Many modern tools support explicit config paths, but editor extensions may rely on conventional discovery. Use explicit paths for owned callers. Retain a root shim only for an identified consumer whose discovery requirement is verified and cannot be updated within scope. Convenience or hypothetical editor compatibility is insufficient; follow the mandatory conformance contract.

## Framework route conventions

Frameworks such as Next.js, Remix-style routers, Rails, Laravel, Django, and others can attach semantics to physical directories.

Do not mechanically relocate those paths. Choose:

- configure route/source directory if supported;
- keep route files as thin view/entry adapters;
- isolate business logic outside the framework-conventional folder;
- document a framework exception.

## ORM and migration tools beyond Drizzle

Use the same three-part distinction:

```text
runtime ORM/database code -> app/business/database
migration artifacts        -> db
ORM/migration config        -> config/database when safely relocatable
```

Examples include Prisma, Alembic, Django migrations, EF Core, Flyway, Liquibase, Rails migrations, Laravel migrations, Diesel, sqlx, Atlas, Goose, and others. Exact conventions differ; inspect the current tool.

## Containers and CI

A config move is not complete until these are checked:

- Docker `COPY` paths;
- Docker build context;
- Compose volume paths;
- GitHub Actions/GitLab/Circle/Buildkite scripts;
- hosting platform build/deploy commands;
- cache keys/path filters;
- artifact upload paths;
- monorepo working-directory settings.

## Official references for relocation examples

Re-check these against the installed versions when using the skill:

- Vite config / CLI: https://vite.dev/config/ and https://vite.dev/guide/cli
- Drizzle Kit configuration: https://orm.drizzle.team/docs/drizzle-config-file
- Cloudflare Wrangler commands/config flag: https://developers.cloudflare.com/workers/wrangler/commands/workers/
- Vitest configuration / CLI: https://vitest.dev/config/ and https://vitest.dev/guide/cli
- Playwright configuration / CLI: https://playwright.dev/docs/test-configuration and https://playwright.dev/docs/test-cli
