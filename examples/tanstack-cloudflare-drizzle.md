# Example: TypeScript + TanStack + Cloudflare + Drizzle

This example illustrates how the canonical architecture can absorb a modern full-stack TypeScript project without organizing the repository around vendor names.

## Recommended shape

```text
project/
├── app/
│   ├── business/
│   │   ├── domain/
│   │   │   ├── projects/
│   │   │   ├── audits/
│   │   │   ├── pages/
│   │   │   ├── findings/
│   │   │   └── rank-tracking/
│   │   ├── services/
│   │   ├── workflows/
│   │   │   ├── site-audit/
│   │   │   └── rank-tracking/
│   │   ├── repositories/
│   │   ├── providers/
│   │   │   ├── dataforseo/
│   │   │   ├── search-console/
│   │   │   ├── analytics/
│   │   │   ├── openrouter/
│   │   │   └── ahrefs/
│   │   ├── database/
│   │   │   ├── client/
│   │   │   ├── schema/
│   │   │   ├── queries/
│   │   │   └── adapters/
│   │   │       ├── d1/
│   │   │       └── postgres/
│   │   ├── auth/
│   │   ├── validation/
│   │   └── jobs/
│   ├── view/
│   │   ├── routes/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── charts/
│   │   ├── styles/
│   │   └── assets/
│   └── entry/
│       ├── client/
│       ├── server/
│       ├── router/
│       └── worker/
├── db/
│   ├── migrations/
│   │   ├── sqlite/
│   │   └── postgres/
│   ├── seeds/
│   └── snapshots/
├── config/
│   ├── build/vite.config.ts
│   ├── database/drizzle.config.ts
│   ├── deployment/wrangler.jsonc
│   ├── testing/vitest.config.ts
│   ├── testing/playwright.config.ts
│   └── typescript/
├── documents/
│   ├── documentation/
│   │   ├── application/
│   │   ├── architecture/
│   │   └── specifications/
│   ├── tasks/
│   ├── research/
│   ├── audits/
│   └── reports/
├── tests/
├── scripts/
├── public/
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json           # small root shim if editor/framework compatibility needs it
└── README.md
```

## Example package scripts

Illustrative only; preserve actual project commands/options:

```json
{
  "scripts": {
    "dev": "vite --config config/build/vite.config.ts",
    "build": "vite build --config config/build/vite.config.ts",
    "db:generate": "drizzle-kit generate --config=config/database/drizzle.config.ts",
    "db:migrate": "drizzle-kit migrate --config=config/database/drizzle.config.ts",
    "test": "vitest --config config/testing/vitest.config.ts",
    "test:e2e": "playwright test --config config/testing/playwright.config.ts",
    "worker:dev": "wrangler dev --config config/deployment/wrangler.jsonc",
    "worker:deploy": "wrangler deploy --config config/deployment/wrangler.jsonc"
  }
}
```

## Important caveat

TanStack/framework route generation, Vite integration, Cloudflare platform files, or hosting automation may depend on configured roots and generated files. Inspect installed versions and current configuration before applying this exact physical layout.
