# Body of Knowledge: email-comms

Stable domain knowledge for the email-comms router. Organized by the four
topics, then the decision rules that pick between them. [DOC]

## 1. Core distinction: deliverability vs render vs content

Email work splits into three independent problem spaces that fail for different
reasons:

- **Deliverability** (`email-sending`) — *does the mail arrive and stay out of
  spam?* Governed by domain authentication and sender reputation. [DOC]
- **Render** (`email-template-builder`, `email-templates`) — *does it look right
  in 2003-era render engines?* Governed by table layout and inline CSS. [DOC]
- **Content/measurement** (`newsletter-design`) — *does it earn the subscriber's
  attention and can you prove it?* Governed by one job-to-be-done and CTOR. [DOC]

A common error is treating a deliverability problem (falling opens) as a content
problem (rewriting copy). CTOR steady + opens falling ⇒ deliverability. [DOC]

## 2. email-sending — deliverability standards

- **SPF** (TXT, `include:` the provider) authorizes sending hosts. [DOC]
- **DKIM** (CNAME/TXT) cryptographically signs the message. [DOC]
- **DMARC** ties SPF/DKIM to the From domain and sets policy. Ramp
  `p=none → quarantine → reject`; never publish `reject` before SPF/DKIM
  align, or legitimate mail is silently dropped. [DOC]
- **IP strategy**: shared IP (warmed reputation) below sustained volume;
  dedicated IP only at high sustained volume, with gradual warm-up. Exact
  thresholds are vendor-specific [ASSUMPTION]. [INFERENCE]
- **Reputation hygiene**: suppress on hard bounce; retry-then-suppress on
  repeated soft bounce; honor complaints via the feedback loop. [DOC]
- **Compliance**: `List-Unsubscribe` + `List-Unsubscribe-Post` one-click;
  CAN-SPAM / GDPR consent. [DOC]
- **Engineering**: queue sends (never inline on the request path); make sends
  idempotent on (user, event); escape variables; no PII in plaintext logs. [INFERENCE]

## 3. email-template-builder & email-templates — render standards

- **Email ≠ web**: tables for layout, inline CSS for styling. No `div` grids,
  flex, grid, JS, lazy-load, or web fonts as the only family. [INFERENCE]
- **Inline-first**: Gmail strips `<head><style>`; keep `<style>` only for
  `@media` and `prefers-color-scheme`. [DOC]
- **Width**: ≤600px content; single-column on mobile. Fluid-hybrid is the robust
  responsive default (works without media queries). [INFERENCE]
- **Outlook (Word engine)**: ignores float/flex/grid/most margin. Use `padding`
  on `<td>`, MSO conditional comments, VML ghost tables, and the VML
  bulletproof button. [DOC]
- **Gmail clip**: HTML over ~102 KB is clipped, hiding the unsubscribe link and
  tracking pixel — cap near 100 KB. [DOC]
- **Accessibility (WCAG 2.1 AA)**: `role="presentation"` on layout tables, `alt`
  on every image, `lang` on `<html>`, 4.5:1 contrast, real text over image-text. [DOC]
- **Firebase trigger**: write a doc to the `mail` collection (`to`,
  `message.subject`, `message.html`) consumed by `firestore-send-email`. [CODE]
- **Validation toolchain**: Litmus / Email on Acid render matrix — NOT
  Lighthouse (it scores web pages). Always send a live seed test. [DOC]

## 4. newsletter-design — content & measurement standards

- **Content architectures**: single-feature (one story/CTA, highest CTOR);
  digest (3–6 curated items, scannable); editorial (lead + links, highest
  authoring cost). Fewer sections by default. [DOC]
- **Subject + preheader** are a pair; the preheader is the second subject line. [DOC]
- **One primary CTA** per issue; secondary links are navigation, not goals. [DOC]
- **Metrics**: open rate (deliverability signal, inflated by Apple MPP), CTR
  (clicks/delivered), CTOR (clicks/opens — the honest content signal),
  unsubscribe rate, spam-complaint rate. Judge content by CTOR. [DOC]
- **Instrumentation**: UTM on every link or downstream CTR is unmeasurable. [DOC]
- **List health**: grow opt-in only; sunset/re-engage inactive subscribers;
  never buy or scrape addresses. [DOC]

## 5. Routing decision rules

| Request signal | Topic |
|----------------|-------|
| "emails go to spam", DNS/SPF/DKIM/DMARC, bounces, provider setup | email-sending |
| "build the HTML email", Firebase `mail` doc, inline CSS, 600px | email-template-builder |
| "renders broken in Outlook", MJML, dark mode, bulletproof button | email-templates |
| "stand up a newsletter", open/click rates, cadence, subject lines | newsletter-design |

If two apply, run the prerequisite first: builder → templates → sending;
newsletter-design hands layout to email-template-builder. [INFERENCE]

## 6. Evidence taxonomy

Alfa core EN only: `[DOC]` (documented), `[INFERENCE]` (reasoned),
`[CODE]` (from code/markup), `[CONFIG]` (from config/DNS), `[ASSUMPTION]`
(unconfirmed, must be verified). Never the Jarvis `{…}` family. An unresolvable
topic is stop-and-ask, not an `[ASSUMPTION]`. [DOC]
