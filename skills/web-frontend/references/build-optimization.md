<!-- distilled from alfa skills/build-optimization -->
<!-- Vite/Webpack config tuning with tree shaking, code splitting, dynamic imports, Brotli/gzip compression, and source maps -->
# 095 — Build Optimization {DevOps}

## Purpose
Optimize the build pipeline to produce the smallest, fastest-loading production bundles. Configure tree shaking, code splitting, compression, and source maps. [EXPLICIT]

**In scope**: bundler config, chunk strategy, compression, source-map handling. **Anti-scope** (use another skill): runtime perf profiling, image/font optimization, CDN/cache-header tuning, SSR/streaming, server cost. Optimize the build only after a measured baseline exists — never optimize on a hunch. [INFERENCIA]

## Physics — 3 Immutable Laws

1. **Minimal Payload**: every shipped byte must justify itself. Unused code is eliminated; large deps are lazy-loaded. [EXPLICIT]
2. **Parallel Loading**: code splitting enables parallel chunk downloads. Route-based splitting ships only the current page's code. [EXPLICIT]
3. **Compression**: all production assets are Brotli-compressed (preferred) or gzip. An uncompressed production deploy is a bug. [EXPLICIT]

## Protocol

### Phase 1 — Bundler Configuration
1. Vite: set `build.rollupOptions.output.manualChunks` for vendor splitting in `vite.config.ts`. [EXPLICIT]
2. Webpack: set `optimization.splitChunks.cacheGroups` for vendor/common/async chunks. [EXPLICIT]
3. Tree shaking: set `"sideEffects": false` in `package.json`, or an array listing files with side effects (CSS, polyfills) — `false` on a module that mutates globals silently drops it. [EXPLICIT]
4. Set `build.target: 'es2020'` — no needless transpilation for modern browsers; raise the floor only if analytics show older clients. [EXPLICIT]

### Phase 2 — Code Splitting Strategy
1. Route-based: `React.lazy(() => import('./pages/Dashboard'))` per route. [EXPLICIT]
2. Feature-based: heavy features (charts, editors, PDF, markdown) loaded on demand. [EXPLICIT]
3. Vendor: separate chunks for `react`, `firebase`, `lodash-es`. [EXPLICIT]
4. Shared: utilities used by 3+ routes go into one shared chunk. Below that threshold, duplication beats an extra request. [EXPLICIT]

**Decision — manual vs automatic chunking** [INFERENCIA]: start with the bundler default (route-level `import()`). Add `manualChunks` only when the analyzer shows a vendor lib duplicated across routes or a single chunk over the gate. Trade-off: manual chunks improve long-term cache hit rate (vendor hash stable across app deploys) but over-splitting adds request overhead and HTTP/2 head-of-line cost — net loss below ~20KB/chunk.

### Phase 3 — Compression & Source Maps
1. Install `vite-plugin-compression` or `compression-webpack-plugin`. [EXPLICIT]
2. Generate Brotli (`.br`) and gzip (`.gz`) for assets > 1KB; below that the header overhead exceeds the saving. [EXPLICIT]
3. Firebase Hosting auto-compresses, but pre-compressed assets ship faster (no per-request CPU). [EXPLICIT]
4. Source maps: `hidden-source-map` for production — uploaded to the error tracker, never referenced from or served to the browser. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Application source code | Optimized production bundle |
| Vite/Webpack config | Split chunks (vendor, routes, shared) |
| Built assets | Brotli/gzip compressed files (`.br`, `.gz`) |
| Source maps config | Hidden source maps for error tracking |

## Quality Gates — 5 Checks (each with its verifier)

1. **Initial bundle < 250KB gzipped** — `size-limit` (`npx size-limit`). [EXPLICIT]
2. **No single chunk > 100KB gzipped** — split further if exceeded. [EXPLICIT]
3. **Tree shaking verified** — named imports (`import { specific }`), never `import *`, for all deps. [EXPLICIT]
4. **Brotli enabled** — `.br` files present in build output (`find dist -name '*.br' | head`). [EXPLICIT]
5. **No source maps on production CDN** — `hidden-source-map` only; assert no `.map` is fetchable. [EXPLICIT]

Gate budgets are thresholds, not targets: a 120KB initial bundle that passes still warrants the analyzer if it grew >10% in one PR. [INFERENCIA]

## Worked Example — vendor split + lazy route (Vite)
```ts
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2020',
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          firebase: ['firebase/app', 'firebase/firestore/lite'],
        },
      },
    },
  },
  plugins: [compression({ algorithm: 'brotliCompress', threshold: 1024 })],
});
```
Effect [INFERENCIA]: `react`/`firebase` get stable-hash chunks (cache survives app-code deploys); the lazy `Dashboard` route stays out of the initial bundle. Verify with `npx vite-bundle-visualizer` before/after.

## Edge Cases

- **Firebase SDK size**: the modular/`lite` SDK (`firebase/firestore/lite`) cuts the Firestore bundle ~60%; `lite` drops realtime listeners, so only use it on read-once paths. [SUPUESTO — confirm against current Firebase release notes]
- **Dynamic import failure**: wrap `React.lazy` in an error boundary with retry — a chunk 404 after a redeploy (hash changed) must recover, not white-screen. [EXPLICIT]
- **CSS extraction**: `mini-css-extract-plugin` (Webpack) or Vite's built-in CSS splitting; never inline large CSS into JS. [EXPLICIT]
- **Polyfills**: include only for features actually used; `@vitejs/plugin-legacy` only when supporting IE11 — it roughly doubles output. [EXPLICIT]
- **`sideEffects: false` over-prunes**: if CSS imports or global setup vanish, list those files in the `sideEffects` array instead of blanket-`false`. [INFERENCIA]
- **manualChunks circular ref**: a util pulled into a vendor chunk that imports app code creates a cycle Rollup warns on — keep manual chunks dependency-leaf only. [SUPUESTO — confirm with `--debug` build]

## Failure Modes & Self-Correction

| Symptom | Likely cause | Action |
|---|---|---|
| Bundle > 250KB | unsplit large dep | run analyzer (skill 099), split/lazy-load the offender |
| Chunk > 100KB | coarse splitting | add `manualChunks` or a dynamic `import()` |
| Tree shaking inert | bad `sideEffects` / CJS dep | fix `sideEffects`; confirm dep ships ESM |
| Build > 60s | no cache / slow transpile | use Vite cache default; `esbuild` for transpilation |
| Chunk 404 post-deploy | stale hashed reference cached | retry boundary + immutable-hashed filenames |
| `.br` absent | compression plugin not wired | reinstall plugin, re-check Phase 3 |

## Usage

- "/build-optimization" — run the full build optimization workflow
- "build optimization on this project" — apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Assumes a target/CI that can run the bundler and the verifiers above; gate numbers assume a typical SPA, not an MPA or micro-frontend. [SUPUESTO — confirm app shape before applying budgets]
- English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain-expert judgment for final decisions. [EXPLICIT]
