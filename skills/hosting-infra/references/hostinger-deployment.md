<!-- distilled from alfa skills/hostinger-deployment -->
<!-- Static site and Node.js deployment on Hostinger via SFTP/Git, cPanel/hPanel config, and PM2 process management -->
# 088 — Hostinger Deployment {DevOps}

## Purpose
Deploy static sites and Node.js applications to Hostinger infrastructure. Configure SFTP/Git-based deployment pipelines, VPS hosting with PM2, and hPanel/cPanel management. [EXPLICIT]

**In scope**: static SPA/SSG to shared `public_html/`; long-running Node.js on a Hostinger VPS under PM2; CI/CD via GitHub Actions over SSH. [EXPLICIT]
**Anti-scope** (do NOT attempt here): Node.js on *shared* hosting — Hostinger shared plans give no persistent process; use a VPS or KVS plan [DOC]; Docker/Kubernetes orchestration; managed Postgres provisioning; DNS registrar changes. [SUPUESTO]

## Physics — 3 Immutable Laws

1. **Law of Reproducible Deploy**: Every deployment is scripted — no manual file uploads. SFTP scripts or Git hooks handle file transfer. [EXPLICIT]
2. **Law of Zero Downtime**: PM2 handles graceful restarts. Static sites use atomic directory swaps. Users never see a broken state. [EXPLICIT]
3. **Law of Environment Isolation**: Production config never touches development data. Separate `.env` files, separate database connections. [EXPLICIT]

## Protocol

### Phase 1 — Static Site Deployment
1. Build locally: `npm run build` → `dist/` directory. [EXPLICIT]
2. Configure SFTP credentials in CI secrets (host, user, SSH key). [EXPLICIT]
3. Deploy via `rsync` or `lftp`: sync `dist/` to `public_html/`. [EXPLICIT]
4. Verify `.htaccess` for SPA routing: `RewriteRule ^(.*)$ /index.html [L]`. [EXPLICIT]

**Atomic swap pattern** (satisfies Law 2 — rsync into `public_html/` directly leaves a window of half-copied files): rsync into a sibling `releases/<sha>/`, then `ln -sfn releases/<sha> public_html` (or rename). Rollback = re-point the symlink. [INFERENCIA]
**Worked example** — deploy + atomic swap via lftp:
```bash
lftp -u "$SFTP_USER","$SFTP_PASS" sftp://"$SFTP_HOST" -e "
  mirror -R --delete --verbose dist/ releases/$GITHUB_SHA/;
  rm -f public_html; symlink releases/$GITHUB_SHA public_html; bye"
```

### Phase 2 — Node.js VPS Deployment
1. SSH into VPS. Install Node.js via `nvm`. Install PM2 globally. [EXPLICIT]
2. Clone repo or pull via Git. Run `npm ci --production`. [EXPLICIT]
3. Configure PM2 ecosystem file: `ecosystem.config.js` with `name`, `script`, `env`. [EXPLICIT]
4. Start: `pm2 start ecosystem.config.js --env production`. Save: `pm2 save`. Setup startup: `pm2 startup`. [EXPLICIT]

> `pm2 startup` prints a `sudo env PATH=... pm2 startup systemd -u <user>` line you must copy-run once; without it PM2 does NOT survive VPS reboot, and `pm2 save` only persists the list, not the boot hook. [DOC]
> Bind the app to `127.0.0.1:<port>` and front it with Nginx/Apache reverse proxy + Let's Encrypt — never expose the Node port publicly. [SUPUESTO]

### Phase 3 — CI/CD Integration
1. GitHub Actions workflow: build → test → deploy via SSH. [EXPLICIT]
2. Use `appleboy/ssh-action` for remote commands. [EXPLICIT]
3. PM2 pull and reload: `cd /app && git pull && npm ci && pm2 reload all`. [EXPLICIT]
4. Verify deployment: HTTP health check on deployed URL. [EXPLICIT]

> `pm2 reload` (cluster, zero-downtime) requires `instances > 1` + `exec_mode: cluster`; on a single fork-mode process it falls back to a restart with a brief drop. Prefer `reload` but assert mode first. [INFERENCIA]
> Gate the reload behind `npm ci` success: if `npm ci` fails after `git pull`, the old process keeps serving — never `pm2 stop` before the new build is proven. [INFERENCIA]

## I/O

| Input | Output |
|-------|--------|
| Built static files (`dist/`) | Files deployed to `public_html/` |
| Node.js application source | PM2-managed process on VPS |
| SFTP/SSH credentials | Automated deployment pipeline |
| `ecosystem.config.js` | PM2 process configuration |

## Quality Gates — 5 Checks

1. **Build succeeds locally before deploy** — CI runs full build + test. [EXPLICIT]
2. **SSH keys rotated quarterly** — no password-based SSH access. [EXPLICIT]
3. **PM2 status shows online** — `pm2 status` verifies process running. [EXPLICIT]
4. **Health check passes** — HTTP 200 on root URL after deploy. [EXPLICIT]
5. **Rollback tested** — previous version deployable within 5 minutes. [EXPLICIT]

## Acceptance Criteria (deploy is "done" only when all hold)

- New release reachable at production URL returning HTTP 200, serving the new build hash (verify a hashed asset filename, not just status). [INFERENCIA]
- `pm2 status` (VPS) shows `online`, `restarts` unchanged from pre-deploy, memory under the configured `max_memory_restart`. [INFERENCIA]
- Previous release artifact still present and one command/symlink-flip away from restore. [INFERENCIA]
- No secret printed in CI logs; `.env` exists only on the server, never in the repo or build output. [SUPUESTO]
- TLS cert valid for ≥ 14 days (`openssl s_client -connect host:443 | openssl x509 -noout -enddate`). [INFERENCIA]

## Edge Cases

- **PHP coexistence**: Hostinger shared hosting may run PHP. Ensure `.htaccess` doesn't conflict with Node.js reverse proxy.
- **SSL renewal**: Hostinger auto-renews Let's Encrypt. Verify cron job exists.
- **Memory limits**: Shared hosting has RAM limits. Monitor PM2 memory with `pm2 monit`; set `max_memory_restart` in the ecosystem file so OOM self-heals. [INFERENCIA]
- **File permissions**: Set `chmod 755` for directories, `644` for files in `public_html`.
- **`--delete` data loss**: `rsync/mirror --delete` removes server files absent locally — exclude `public_html/.well-known/` and any user-upload dir, or it wipes them. [INFERENCIA]
- **Node version drift**: VPS `nvm` default may differ from CI build version → native-module ABI mismatch. Pin via `.nvmrc` + `nvm use` in the deploy step. [INFERENCIA]
- **Concurrent deploys**: two CI runs racing on the same VPS corrupt `git pull`/`npm ci`. Serialize with a GitHub Actions `concurrency` group per environment. [INFERENCIA]

## Self-Correction Triggers

- Deploy fails → check SSH connectivity, disk space (`df -h` — a full disk fails `npm ci` silently), Node.js version. [INFERENCIA]
- PM2 process crashes → check logs `pm2 logs`, increase memory limit or fix crash.
- SSL expired → re-run certbot or check Hostinger auto-renewal config.
- Site returns 500 → check `.htaccess` rules, Node.js process status, error logs.
- Site returns 502/504 → reverse proxy is up but Node port is down/wrong; confirm app bound to the proxied `127.0.0.1:<port>` and `pm2 status` online. [INFERENCIA]

## Failure Modes & Trade-offs

- **SFTP/rsync vs Git-on-server**: rsync ships only built artifacts (smaller attack surface, no toolchain on host) but needs a CI builder; Git-on-server is simpler but puts source + build deps on the box. Default to rsync for static, Git for VPS apps that already need Node present. [SUPUESTO]
- **`reload` vs `restart`**: `reload` = zero-downtime but only in cluster mode and assumes graceful shutdown handling; `restart` = guaranteed clean state but drops in-flight requests. Choose per app's statefulness. [INFERENCIA]
- **Symlink atomic swap vs in-place rsync**: symlink swap is instant + trivially reversible but doubles transient disk use (two releases); in-place is disk-cheap but non-atomic. On RAM/disk-constrained shared plans, prune to last 2 releases. [INFERENCIA]

## Usage

Example invocations:

- "/hostinger-deployment" — Run the full hostinger deployment workflow
- "hostinger deployment on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Assumes a Hostinger plan with shell/SFTP access (Premium+ shared, Cloud, or VPS); entry shared plans without SSH break Phases 2–3. [SUPUESTO]
- Secrets live in CI store + server `.env` only; this doc does not cover secret-manager integration. [SUPUESTO]
