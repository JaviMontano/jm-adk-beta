<!-- distilled from alfa skills/ecommerce-frontend -->
<!-- > -->
# E-commerce Frontend

> "Every page is a landing page when the customer arrives from a search engine." — Unknown

## TL;DR

Guides the implementation of e-commerce frontend features — product listing pages with filtering/sorting, product detail pages, persistent shopping cart, multi-step checkout flow, and payment UI integration. Use when building online stores or adding commerce features to existing applications. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify product catalog structure (categories, variants, attributes)
- Check payment provider requirements (Stripe Elements, PayPal SDK)
- Review inventory and stock management rules
- Determine shipping, tax, and discount calculation requirements

### Step 2: Analyze
- Plan product listing UX (grid/list toggle, faceted filters, infinite scroll vs pagination)
- Design cart persistence strategy (localStorage, database, cookies)
- Map checkout flow steps (cart review → shipping → payment → confirmation)
- Evaluate SEO needs for product pages (structured data, meta tags)

### Step 3: Execute
- Build product listing page with filter sidebar, sort dropdown, and responsive grid
- Implement product detail page with image gallery, variant selector, and add-to-cart
- Create persistent cart with quantity updates, remove items, and price calculation
- Build multi-step checkout with address form, shipping options, and payment form
- Add structured data (JSON-LD Product schema) for search engine rich results
- Implement order confirmation page with summary and tracking info

### Step 4: Validate
- Test complete purchase flow end-to-end (browse → cart → checkout → confirmation)
- Verify cart persists across sessions and devices (for logged-in users)
- Check that prices, taxes, and totals calculate correctly with edge cases
- Test with screen readers — product info, cart updates, and form errors must be announced

## Quality Criteria

- [ ] Product pages load within 2 seconds with optimized images
- [ ] Cart updates are reflected instantly with optimistic UI
- [ ] Checkout form validates inline and shows clear error messages
- [ ] Payment integration uses PCI-compliant hosted fields (never raw card inputs)
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Handling credit card numbers directly instead of using tokenized payment elements
- Requiring account creation before checkout (offer guest checkout)
- Recalculating prices client-side without server verification

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
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
