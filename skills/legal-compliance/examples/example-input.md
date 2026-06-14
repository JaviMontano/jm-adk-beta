# Example input — contract-review lane

A procurement lead pastes the risk-bearing excerpts of an executed SaaS Master
Services Agreement and asks for a pre-signature risk read.

## Request
"Before we counter-sign the DataFlux MSA, walk the liability, confidentiality, and
auto-renewal terms and tell me where we're exposed. Governing law is Delaware. depth=quick."

## Provided contract excerpts
- **Clause 8.2** — "Each party's aggregate liability shall not exceed the fees paid
  in the twelve (12) months preceding the claim."
- **Clause 8.4** — "The limitation in 8.2 shall not apply to any breach of
  confidentiality obligations under Section 11."
- **Clause 11** — "Confidential Information includes all data processed on behalf of
  Customer, including personal data." Return/destruction within 30 days of
  termination; breach notice "as soon as practicable."
- **Clause 14.1** — "This Agreement renews automatically for successive 12-month
  terms unless either party gives written notice of non-renewal no later than 60
  days before the end of the then-current term." Renewal price may increase up to 7%.
- **Schedule C (Data Processing Addendum)** — referenced in Clause 11 but **not
  attached** to the copy provided.

## Resolved route
- topic = `contract-review` · depth = `quick`
- Scope: DataFlux SaaS MSA, governing law Delaware (single jurisdiction).
- Note flagged at intake: Schedule C (DPA) missing — obligations may live there.
