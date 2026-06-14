# Deep variation — hosting-infra (depth=deep)

Exhaustive path with verification at every step. Use for cutovers, DR designs,
and irreversible operations.

1. **Route** to one enum and read its single playbook (never the cluster).
2. **Discover fully**: inventory zones/records/TTLs, registrars, certs/chains,
   cache rules, function triggers, service tiers with current vs target RTO/RPO,
   plan/PM2 state, and who controls each. Capture SLA + traffic geography.
3. **Analyze with trade-offs**: enumerate the alternatives the playbook names —
   DNS-failover vs anycast/LB; backup-restore vs warm-standby vs active-active;
   `pm2 reload` vs `restart`; symlink swap vs in-place rsync — and justify the pick
   against the tier.
4. **Execute** with each playbook phase, staging changes (lower TTL 24–48h before
   a cutover; rsync into a release dir then symlink-flip; gate reload on `npm ci`).
5. **Validate empirically**, not on faith:
   - DNS: `dig +trace`, resolve from ≥2 geos, confirm propagation before raising TTL.
   - SSL: `openssl s_client -connect host:443 | openssl x509 -noout -enddate` ≥14 days; full chain served.
   - Serverless: emulator test incl. one duplicate-delivery case.
   - DR: game-day drill measuring actual RTO/RPO; failback rehearsed.
   - Hostinger: HTTP 200 + new build-hash asset; `pm2 status` online; rollback proven.
6. **Gate**: run the playbook quality criteria AND the skill validation gate;
   list any unmet item as a finding. Tag everything; invent nothing.
