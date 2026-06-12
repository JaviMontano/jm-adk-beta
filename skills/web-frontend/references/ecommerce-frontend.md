<!-- distilled from alfa skills/ecommerce-frontend -->
<!-- > -->
# E-commerce Frontend

> "Every page is a landing page when the customer arrives from a search engine." — Unknown

## TL;DR

Guides implementation of e-commerce frontend features — product listing pages (PLP) with filtering/sorting, product detail pages (PDP), persistent cart, multi-step checkout, and payment UI integration. Use when building online stores or adding commerce features to existing apps. Out of scope: payment backend, order fulfillment, tax engines, inventory authority, ERP/CRM sync — those live server-side and in `payment-integration`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Catalog structure: categories, variants (size/color), attributes, SKU vs parent-product model
- Payment provider + requirements (Stripe Elements, PayPal SDK) — confirm hosted-fields support [EXPLICIT]
- Inventory and stock rules: backorder, pre-order, low-stock thresholds, oversell tolerance
- Shipping, tax, and discount calculation requirements + which side computes each (server is authority)
- Auth model: guest vs logged-in cart, and merge behavior on login

### Step 2: Analyze
- PLP UX: grid/list toggle, faceted filters, infinite scroll vs pagination (see trade-offs below)
- Cart persistence strategy: localStorage (guest), DB (logged-in), cookie (session id) — see trade-offs
- Checkout flow: cart review → shipping → payment → confirmation; decide single-page vs stepped
- SEO needs: JSON-LD Product schema, canonical URLs, meta tags, server-rendered PLP/PDP for crawlability

### Step 3: Execute
- PLP: filter sidebar, sort dropdown, responsive grid; sync filter/sort/page state to the URL (shareable, back-button safe)
- PDP: image gallery, variant selector (disable/grey out-of-stock combos), add-to-cart with stock check
- Cart: quantity updates, remove items, price calculation; show per-line and order subtotal
- Checkout: address form, shipping options, payment form via hosted fields
- Add JSON-LD Product schema (name, image, price, availability) for rich results
- Order confirmation page: summary, order id, tracking info

### Step 4: Validate
- E2E purchase flow: browse → cart → checkout → confirmation, including a guest path
- Cart persists across sessions and devices (logged-in) and merges guest cart on login without dupes
- Prices, taxes, totals correct on edge cases (see table); final total always re-verified server-side
- Screen-reader pass: product info, cart count/updates (aria-live), and form errors are announced

## Quality Criteria

- [ ] PDP/PLP load within 2s with optimized, correctly-sized, lazy-loaded images
- [ ] Cart updates reflect instantly via optimistic UI, with rollback + visible error on server reject
- [ ] Checkout form validates inline; errors are specific, adjacent to the field, and focus-managed
- [ ] Payment uses PCI-compliant hosted fields/tokenization — raw PAN never touches your DOM or JS [EXPLICIT]
- [ ] Filter/sort/pagination state is URL-encoded and restores on reload and back-navigation
- [ ] Out-of-stock and price changes are reconciled at checkout, not silently honored from a stale cart
- [ ] Evidence tags applied to all claims

## Decisions & Trade-offs

| Decision | Option A | Option B | Guidance |
|----------|----------|----------|----------|
| PLP paging | Infinite scroll — fluid browse, weak deep-linking/SEO, footer unreachable | Pagination — SEO-friendly, addressable, slower browse | Pagination (or "load more" + real URLs) when SEO/footer matter; infinite scroll for discovery feeds [EXPLICIT] |
| Cart store | localStorage — fast, offline, device-local, lost on clear | DB-backed — cross-device, survives, needs auth + round-trips | Guest → localStorage; logged-in → DB; merge on login [EXPLICIT] |
| Checkout | Single-page — fewer steps, less drop-off, dense | Stepped — clearer, easier validation, more clicks | Stepped for complex shipping/tax; single-page for digital/simple carts [EXPLICIT] |
| Price source | Client estimate — instant, can drift | Server-computed — authoritative, a round-trip | Show client estimate for UX; server is the source of truth at checkout [EXPLICIT] |

## Worked Example: Variant Selector (PDP)

A T-shirt has color × size. On select, resolve the SKU and reflect stock so users can't add unavailable combos. [EXPLICIT]

```js
// variants: [{ sku, color, size, stock, price }]
function resolveVariant(variants, { color, size }) {
  const v = variants.find(x => x.color === color && x.size === size);
  if (!v) return { state: 'invalid' };                 // combo doesn't exist
  if (v.stock <= 0) return { state: 'oos', sku: v.sku }; // exists, out of stock
  return { state: 'available', sku: v.sku, price: v.price, stock: v.stock };
}
// UI: disable add-to-cart unless state === 'available'; grey OOS swatches;
// announce the resolved price/availability via an aria-live region.
```

## Anti-Patterns

- Handling raw credit card numbers instead of tokenized/hosted payment elements (PCI scope explosion) [EXPLICIT]
- Requiring account creation before checkout — always offer guest checkout (top abandonment driver)
- Recalculating prices/discounts client-side and trusting them without server verification [EXPLICIT]
- Filter/sort state held only in component memory — breaks sharing, deep-linking, and the back button
- Loading full-resolution images into thumbnail grids; no `width`/`height` → layout shift (CLS)
- Optimistic cart update with no failure path — quantity desyncs from server silently
- Blocking add-to-cart on a full page reload instead of an async, announced update

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Inventory race | Two buyers add the last unit | Re-check stock at add-to-cart and again at payment; fail clearly |
| Price drift | Cart shows stale price after a catalog change | Re-price at checkout; surface "price updated" before charge |
| Payment double-submit | Duplicate orders on slow networks | Disable submit on click + idempotency key on the order request |
| Coupon stacking | Negative or under-charged total | Validate discount server-side; clamp totals to >= 0 |
| Abandoned 3DS/redirect | Order stuck "pending" after bank redirect | Reconcile via webhook/return URL; show pending state, never "paid" |

## Related Skills

- `payment-integration` — Stripe/PayPal backend integration
- `image-optimization` — product image loading performance

## Usage

Example invocations:

- "/ecommerce-frontend" — Run the full ecommerce frontend workflow
- "ecommerce frontend on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Frontend only — payment capture, settlement, fraud, fulfillment, and tax calculation are server-side and out of scope [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Empty cart at checkout | Block checkout; route back to PLP with a clear message |
| Item goes out of stock in cart | Flag the line, prevent purchase of it, let the rest proceed |
| Currency / locale formatting | Format via Intl; never hand-roll decimal or symbol placement |
| Price/stock changed since add | Reconcile and require explicit user re-confirm before charge |
