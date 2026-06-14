# Meta prompt — hosting-infra (reasoning & self-check)

Use this to steer the model's reasoning before and during a hosting-infra run.

## Routing self-check
- Did I land on EXACTLY ONE `topic`? If two are entangled (e.g. "move the domain
  AND renew the cert"), split into `domain-management` then `ssl-management` and
  sequence — do not invent a merged plan. [EXPLICIT]
- Is this even in scope? App-code architecture, CI/CD business logic, and cloud
  cost modeling route elsewhere. A non-Hostinger provider uses the generic
  dns/ssl/design playbooks, not `hostinger-deployment`. [INFERENCIA]

## Depth calibration
- `quick`: deliver the essential records/config/runbook only.
- `deep`: verify at each step (`dig +trace` from ≥2 geos, full-chain `openssl`
  check, restore-to-running drill, `pm2 status` online) and enumerate trade-offs.

## Evidence self-audit
- Every non-obvious sentence carries ONE Alfa tag — no untagged claims, no
  double-tagging.
- Any value I did not receive from the user (IP, host, cert path, price) is
  marked `[SUPUESTO]` and flagged for verification, never fabricated.

## Failure-mode pre-mortem (per topic)
- DNS: did I avoid apex CNAME? Are TTLs staged for the cutover? SPF/DKIM/DMARC + CAA?
- SSL: full chain, not just leaf? Renewal automated? HSTS only post-HTTPS?
- DR: RTO/RPO owned by the business? Failback covered? Drilled?
- Serverless: handlers idempotent + order-independent? Saga inverses defined?
- Hostinger: deploy scripted? `pm2 startup` set? Node port not exposed?

## Stop conditions
Escalate (do not invent) when business RTO/RPO is unset, registrar/DNS access is
missing, or an untested backup is offered as a recovery option.
