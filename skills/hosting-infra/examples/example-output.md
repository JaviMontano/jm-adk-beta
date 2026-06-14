# Example output — hosting-infra (worked: app.acme.io cutover)

> Cross-cutting request → **sequenced**, not merged. Pass 1 = dns-architecture,
> Pass 2 = ssl-management. depth=deep. VPS IP withheld → `<NEW_VPS_IP>` `[SUPUESTO]`.

## 1. Request & routing
- Resolved topics (sequenced): `dns-architecture` then `ssl-management`. [INFERENCIA]
- Depth: `deep` — production cutover. [CONFIG]
- One playbook read per pass; no cluster loading. [EXPLICIT]

## Pass 1 — dns-architecture (read `references/dns-architecture.md`)

### Discover
| Item | Current | Owner |
|------|---------|-------|
| `app.acme.io` A record | old host, TTL 3600 | registrar DNS [SUPUESTO] |
| Target | `<NEW_VPS_IP>` (from change ticket) | user — not guessed [SUPUESTO] |

### Analyze
- Apex vs subdomain: `app.acme.io` is a subdomain → CNAME is legal, but here we
  bind directly to the VPS IP, so use an **A record**. [EXPLICIT]
- Minimize downtime by **staging TTL** before the switch, not by editing during it. [EXPLICIT]

### Execute (staged cutover)
```text
# T-48h: lower TTL so resolvers stop caching the old answer
app.acme.io.  A  <OLD_IP>   TTL 300        # was 3600 [EXPLICIT]

# T-0: flip to new VPS
app.acme.io.  A  <NEW_VPS_IP>  TTL 300      # [SUPUESTO] IP from user ticket

# T+propagation-verified: raise TTL back
app.acme.io.  A  <NEW_VPS_IP>  TTL 3600     # [EXPLICIT]
```

### Validate
- `dig +trace app.acme.io` and resolve from ≥2 geos; confirm `<NEW_VPS_IP>`
  before raising TTL. Recovery ≈ TTL + check interval, not instant. [EXPLICIT]

## Pass 2 — ssl-management (read `references/ssl-management.md`)

### Execute
```bash
# On the new VPS, issue/renew and serve the FULL chain (leaf + intermediates)
certbot --nginx -d app.acme.io          # 90-day cert → renewal must be automated [DOC]
systemctl list-timers | grep certbot    # confirm auto-renew timer exists [INFERENCIA]
```
- Enable HSTS only AFTER HTTPS verified end-to-end on the new box. [DOC]
- Confirm `app.acme.io` has a CAA record allowing the issuing CA. [EXPLICIT]

### Validate
```bash
openssl s_client -connect app.acme.io:443 -servername app.acme.io \
  | openssl x509 -noout -enddate        # expect ≥14 days [INFERENCIA]
```

## Gate verdict
- [x] One playbook per pass; cross-cutting work sequenced not merged [EXPLICIT]
- [x] Apex/subdomain record correct; TTL staged; propagation verified from ≥2 geos
- [x] Full cert chain served; renewal automated; HSTS gated on HTTPS
- [x] `<NEW_VPS_IP>` carried as `[SUPUESTO]`, never invented; no secrets echoed

**Verdict**: `gate=pass`

## Follow-ups
- `[SUPUESTO]` Replace `<NEW_VPS_IP>` with the value from the change ticket before applying. [SUPUESTO]
