# Firebase Deliverable — {{topic}}

> Resolved topic: `{{topic}}` · depth: `{{quick|deep}}` · spine: Discover → Analyze → Execute → Validate

## 1. Request & scope
- **Ask:** <one-line restatement of the user request>
- **Topic resolution:** why this topic and not the adjacent ones. [INFERENCE]
- **Out of scope:** what was deliberately excluded (e.g. raw GCP IAM, multi-cloud).

## 2. Service / context matrix
| Requirement (FR-XXX) | Firebase service | Adjacent GCP | Notes |
|----------------------|------------------|--------------|-------|
| | Firestore / Auth / Functions / Hosting / Storage | Pub/Sub / Tasks / Secret Mgr | |

## 3. Design
### Firestore schema (if applicable)
- Collections / subcollections, denormalized fields + the reconciling trigger.
### Composite indexes
```json
// firestore.indexes.json entries for each compound query
```
### Security Rules (if applicable)
```
// get/list/create/update/delete per collection; deny-by-default
```
### Cloud Functions topology (if applicable)
- Trigger → handler → idempotency marker. Region, memory, concurrency, minInstances.

## 4. Config diffs applied
```jsonc
// firebase.json / firestore.rules / storage.rules — read before change
```

## 5. Cost estimate (no prices)
| Feature | Reads/day | Writes/day | Invocations/day | Driver / mitigation |
|---------|-----------|------------|-----------------|---------------------|
| | | | | |
> Estimate at stated scale, not a quote. Verify current quotas in the pricing console. [SUPUESTO]

## 6. Validation Gate
- [ ] Schema designed for actual read patterns [EXPLICIT]
- [ ] Every collection + subcollection has an explicit rule (deny-by-default) [EXPLICIT]
- [ ] Compound queries backed by composite indexes [INFERENCIA]
- [ ] Triggers idempotent (at-least-once safe) [EXPLICIT]
- [ ] Emulator tests cover allow AND deny per path [EXPLICIT]
- [ ] Deploy dry-run / preview channel run before prod [INFERENCE]
- [ ] Cost estimate present; no price quoted [DOC]
- [ ] No AWS/Azure / Docker/K8s; single brand; no client PII

## 7. Evidence log
- `[EXPLICIT]` … `[CONFIG]` … `[INFERENCE]` … `[SUPUESTO]` …
