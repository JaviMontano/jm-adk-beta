# Example input — web-frontend

> "Our Vite + React SPA ships a 410KB-gzipped initial bundle. The Firestore SDK and the charting library are both in the main chunk, so the login screen pulls in code it never uses. I want the `/dashboard` route to lazy-load, the heavy vendor libraries split into cache-stable chunks, and production assets Brotli-compressed. Target is es2020 browsers. Don't break the existing routing."

## Context provided
- `vite.config.ts` present, no `manualChunks` configured.
- `package.json` deps: `react`, `react-dom`, `firebase`, `recharts`.
- Routes wired with `react-router`; `Dashboard` imported statically in the router.
- CI can run `npx size-limit` and `npx vite-bundle-visualizer`.
- No App Router / RSC (plain Vite SPA).

## Expected routing
- `topic = build-optimization` (the request is bundle shape + compression, not component structure or styling).
- `depth = deep` (multiple gates: lazy route, vendor split, compression, source-map safety).
