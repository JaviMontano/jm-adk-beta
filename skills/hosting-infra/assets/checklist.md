# hosting-infra — pre-flight & gate checklist

Reusable checklist the guardian/support agents run per invocation.

## Routing pre-flight
- [ ] Resolved to EXACTLY ONE topic enum value.
- [ ] If two topics entangled → split and sequence (e.g. domain → dns → ssl).
- [ ] Confirmed in scope (not app-code architecture / CI-CD logic / cost modeling).
- [ ] Non-Hostinger provider → using generic dns/ssl/design playbook, not hostinger.
- [ ] Read exactly one `references/*.md`; did not load the cluster.

## Execution pre-flight
- [ ] Depth chosen (`deep` for cutovers/DR/irreversible ops).
- [ ] Discovery inventory captured (records/certs/triggers/tiers/plan).
- [ ] SLA targets (RTO/RPO/geography) captured or escalated as a blocking gap.
- [ ] All deploys scripted; no manual file uploads.

## Verification (run, don't assume)
- [ ] DNS: `dig +trace`, resolve from >=2 geos before raising TTL.
- [ ] SSL: `openssl s_client ... | openssl x509 -noout -enddate` >=14 days; full chain.
- [ ] Serverless: emulator test incl. one duplicate-delivery case.
- [ ] DR: game-day drill measured actual RTO/RPO; failback rehearsed.
- [ ] Hostinger: HTTP 200 + new build-hash asset; `pm2 status` online; rollback proven.

## Governance gate
- [ ] Every non-obvious claim carries one Alfa tag.
- [ ] No invented hostnames/IPs/cert-paths/auth-codes/registrar-prices.
- [ ] No secrets echoed; single-brand output.
- [ ] Verdict emitted: `gate=pass | gate=fail` with unmet items listed.
