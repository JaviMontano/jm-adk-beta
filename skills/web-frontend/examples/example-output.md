# Example output — web-frontend

## 1. Routing decision
- **Topic resolved:** `build-optimization`
- **Depth:** `deep`
- **Why this topic:** the request is about bundle shape, chunking, and compression — not component boundaries (`component-architecture`) or styling (`css-architecture`). Dominant topic is unambiguous, no question needed. [INFERENCIA]
- **Playbook loaded:** `references/build-optimization.md` (exactly one)
- **Out-of-scope handed off:** none.

## 2. Stack confirmed
| Fact | Value | Source |
|------|-------|--------|
| Framework | React SPA on Vite (no RSC) | [CONFIG] |
| Bundler | Vite (`vite.config.ts`, no manualChunks) | [CONFIG] |
| Browser targets | es2020 | [SUPUESTO — per user] |
| Heavy deps | `firebase`, `recharts` in main chunk | [CÓDIGO] |

## 3. Decisions & trade-offs
| Decision | Chosen option | Trade-off accepted | Tag |
|----------|---------------|--------------------|-----|
| Chunking | `manualChunks` for `react`, `firebase`; lazy `recharts` via the Dashboard route | manual chunks raise long-term cache hit rate; over-splitting would add request overhead, so only the duplicated/oversized vendors are split | [INFERENCIA] |
| Route split | `React.lazy(() => import('./pages/Dashboard'))` wrapped in an error boundary with retry | keeps Dashboard out of the login bundle; a chunk 404 after redeploy must recover, not white-screen | [CÓDIGO] |
| Compression | Brotli (`threshold: 1024`) + gzip fallback | pre-compressed assets ship without per-request CPU; below 1KB the header overhead exceeds the saving | [CONFIG] |
| Source maps | `hidden-source-map` | uploaded to the error tracker, never fetchable from the CDN | [CONFIG] |

## 4. Implementation
```ts
// vite.config.ts
import { defineConfig } from 'vite';
import compression from 'vite-plugin-compression';

export default defineConfig({
  build: {
    target: 'es2020',
    sourcemap: 'hidden',
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
```tsx
// router.tsx — lazy the heavy route, wrap for chunk-404 recovery
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
// <Suspense fallback={<PageSkeleton/>}> + <ChunkErrorBoundary onRetry={reload}>
```
Effect: `react`/`firebase` get stable-hash chunks (cache survives app-code deploys); `recharts` loads only when `/dashboard` mounts; login bundle drops the unused charting + realtime-Firestore code. [CÓDIGO]

## 5. Validation gate report
| Gate | Threshold | Verifier | Evidence | Result |
|------|-----------|----------|----------|--------|
| Single playbook loaded | exactly 1 | review | only build-optimization read | pass |
| Build clean | no errors | `vite build` | exit 0 | pass |
| Initial bundle | < 250KB gz | `npx size-limit` | 188KB gz (was 410KB) | pass |
| No chunk > 100KB gz | true | `vite-bundle-visualizer` | max chunk 96KB | pass |
| Tree shaking | named imports only | review | `firebase/firestore/lite`, no `import *` | pass |
| Brotli present | `.br` in dist | `find dist -name '*.br'` | 7 files | pass |
| No prod source map fetchable | true | request `/assets/*.map` | 404 (hidden) | pass |
| Evidence tags | 1/claim | review | present | pass |

**Verdict:** `pass` — initial bundle cut 54% with cache-stable vendor chunks; lazy Dashboard recovers from post-deploy chunk 404 via retry boundary. [CÓDIGO]

## 6. Follow-ups / re-invoke
- If the Dashboard itself needs render-perf work (re-render storms on filter), re-invoke with `topic = react-development` — a separate concern, separate playbook. [INFERENCIA]
