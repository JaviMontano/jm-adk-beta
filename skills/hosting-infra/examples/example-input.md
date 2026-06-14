# Example input — hosting-infra

A real cross-cutting request that exercises routing + sequencing.

---

> We're cutting `app.acme.io` over to a new VPS this weekend. I need DNS pointed at
> the new box with the shortest safe downtime, and the TLS cert reissued so HTTPS
> doesn't break during the switch. I have registrar and DNS-provider access. The
> new VPS IP is the one I'll paste in the change ticket — don't guess it.

Signals:
- Two topics entangled: **dns-architecture** (cutover) + **ssl-management** (cert
  reissue). Router must **sequence**, not merge. [INFERENCIA]
- `depth=deep` — a production cutover is irreversible-ish and blast-radius heavy. [CONFIG]
- VPS IP is intentionally withheld → must be carried as `[SUPUESTO]`, never invented. [SUPUESTO]
