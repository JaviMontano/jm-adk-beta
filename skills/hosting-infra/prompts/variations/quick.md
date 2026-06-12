# Quick variation — hosting-infra (depth=quick)

Fast path: one topic, essentials only, still gated.

1. **Route** to one enum (records→dns, cert→ssl, registrar→domain, caching→cdn,
   fan-out/saga→serverless, sizing→infra, snapshots→backup, failover→dr,
   Hostinger→hostinger). Read that single playbook.
2. **Deliver the minimum that is correct**: e.g. the apex/sub record set with
   staged TTLs; or the cert chain + renewal command; or the PM2 ecosystem + atomic
   swap snippet.
3. **Skip** exhaustive multi-geo verification and full trade-off enumeration —
   but DO keep the non-negotiables: apex never CNAME, full cert chain, idempotent
   handlers, scripted deploy, RTO/RPO owned by business.
4. **Tag** every non-obvious claim (one Alfa tag). Never invent values.
5. **Gate**: single playbook used? topic matched? secrets safe? Emit verdict.

Use `deep` instead when the change is a production cutover, a DR design, or any
irreversible/blast-radius operation.
