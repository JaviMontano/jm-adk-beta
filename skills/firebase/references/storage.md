<!-- distilled from alfa skills/firebase-storage -->
<!-- > -->
# Firebase Storage

> "Every uploaded file is a trust exercise — validate it before you store it." — Unknown

## TL;DR

Guides Firebase Storage implementation — resumable file upload with progress tracking, download URL generation, security rules for access control, automatic image resizing via extensions, and organized file path strategies. Use when your app needs to store and serve user-uploaded files (images, documents, media). [EXPLICIT]

## Scope & Anti-Scope

- **In scope:** upload/download flows, path design, Storage security rules, Resize Images extension, CORS, progress UX. [EXPLICIT]
- **Out of scope:** Firestore data modeling (see `firestore-security-rules`), CDN/cache tuning beyond CORS, video transcoding, virus scanning (use a Cloud Function trigger + 3rd-party scanner). [INFERENCIA]
- **Decision — store URL vs path:** persist the storage *path* (`users/{uid}/...`) in Firestore, not the download URL. Paths are stable and rule-checkable; download URLs embed a revocable token and break if regenerated. Resolve to a URL on read. Trade-off: one extra `getDownloadURL` call per fetch vs. stale/leaked URLs. [INFERENCIA]

## Procedure

### Step 1: Discover
- Identify file types to be stored (images, documents, audio, video) [EXPLICIT]
- Determine upload sources (form input, drag-and-drop, camera capture) [EXPLICIT]
- Check storage quota and bandwidth requirements [EXPLICIT]
- Review existing file organization strategy in storage buckets [EXPLICIT]

### Step 2: Analyze
- Design file path structure: `users/{uid}/profile/{filename}` or `posts/{postId}/images/`. Put the owner `uid` high in the path so rules can match on `request.auth.uid` without a Firestore lookup. [INFERENCIA]
- Plan file size limits and type validation (client-side + security rules — client checks are UX only, rules are the enforcement boundary). [INFERENCIA]
- Evaluate image processing needs (resize, thumbnail, watermark) [EXPLICIT]
- Determine access patterns (public via download URL, private via rules) [EXPLICIT]

### Step 3: Execute
- Implement file upload with `uploadBytesResumable` for progress tracking [EXPLICIT]
- Add client-side validation (file type, size) before upload [EXPLICIT]
- Generate download URLs with `getDownloadURL`; store the **path** in Firestore (see decision above). [INFERENCIA]
- Write Storage security rules matching auth requirements [EXPLICIT]
- Install Resize Images extension for automatic thumbnail generation [EXPLICIT]
- Configure CORS for cross-origin access if needed [EXPLICIT]
- Add upload progress UI (progress bar, cancel button via `uploadTask.cancel()`) [INFERENCIA]

## Worked Example: validated, owner-scoped upload

```js
// Client: validate THEN upload with progress + cancel. Client checks are UX, not security.
const MAX = 5 * 1024 * 1024;                 // 5 MB
const OK  = ["image/jpeg", "image/png", "image/webp"];
if (!OK.includes(file.type) || file.size > MAX) throw new Error("rejected");

const path = `users/${uid}/profile/${crypto.randomUUID()}`;  // unguessable, owner-scoped
const task = uploadBytesResumable(ref(storage, path), file, { contentType: file.type });
task.on("state_changed",
  s => setPct((s.bytesTransferred / s.totalBytes) * 100),
  err => report(err),                        // see Failure Modes for err.code values
  async () => { await setDoc(doc(db, "users", uid), { avatar: path }, { merge: true }); });
// task.cancel() wires the cancel button.
```

```
// storage.rules — rules are the real enforcement boundary. contentType/size live here too.
match /users/{uid}/{allPaths=**} {
  allow read:  if request.auth != null;
  allow write: if request.auth.uid == uid
               && request.resource.size < 5 * 1024 * 1024
               && request.resource.contentType.matches('image/(jpeg|png|webp)');
}
```
Tags: `[CONFIG]` rules block, `[CODE]` client snippet — both checkable in-repo.

### Step 4: Validate
- Test upload with various file types and sizes (including edge cases near limits) [EXPLICIT]
- Verify security rules deny unauthorized access — test as a *different* signed-in user and as anonymous, not just the owner. [INFERENCIA]
- Confirm image resize extension generates thumbnails correctly [EXPLICIT]
- Check download URLs work and files serve with proper content types [EXPLICIT]

## Acceptance Criteria

- [ ] File type and size validated on **both** client and Storage rules; rule rejects oversize/wrong-type even if client is bypassed. [INFERENCIA]
- [ ] Upload shows progress indicator and supports cancellation. [EXPLICIT]
- [ ] File paths include user ID for ownership-based security rules; filenames are unguessable (UUID/hash), not user-supplied. [INFERENCIA]
- [ ] Storage **path** (not download URL) persisted in Firestore. [INFERENCIA]
- [ ] Rules tested as owner, non-owner, and anonymous — non-owner write denied. [INFERENCIA]
- [ ] Resize extension verified to emit the expected thumbnail sizes/suffixes. [SUPUESTO]
- [ ] Evidence tags applied to all non-obvious claims. [EXPLICIT]

## Anti-Patterns

- Generating/persisting download URLs instead of paths — URLs carry revocable tokens and break on regeneration. [INFERENCIA]
- Allowing any file type/size without rule-side validation (security and storage-cost risk). [INFERENCIA]
- Using predictable file paths (e.g. `profile.jpg`) without auth checks — enables enumeration. [INFERENCIA]
- Trusting client-supplied `contentType`/filename — spoofable; constrain in rules. [INFERENCIA]
- Non-resumable `uploadBytes` for large files — no progress, no resume on flaky networks. [INFERENCIA]

## Failure Modes

| `error.code` / symptom | Cause | Handling |
|---|---|---|
| `storage/unauthorized` | Rules denied write | Re-check `request.auth.uid` vs path; confirm user signed in. [INFERENCIA] |
| `storage/canceled` | `task.cancel()` called | Expected — reset UI, no error toast. [INFERENCIA] |
| `storage/retry-limit-exceeded` | Network died mid-upload | Resumable upload auto-retries; surface retry CTA after limit. [INFERENCIA] |
| `storage/quota-exceeded` | Bucket over quota | Alert ops; do not silently drop the file. [SUPUESTO] |
| CORS error in browser console | Bucket CORS not set for origin | Apply CORS config to the bucket via `gsutil cors set`. [INFERENCIA] |
| Thumbnail missing | Resize extension async, runs post-upload | Poll for resized path or use extension's completion signal; don't assume sync. [INFERENCIA] |

## Related Skills

- `image-optimization` — optimize images before or after upload [EXPLICIT]
- `firestore-security-rules` — Storage security rules follow similar `match`/`allow` patterns [EXPLICIT]

## Usage

Example invocations:

- "/firebase-storage" — Run the full firebase storage workflow [EXPLICIT]
- "firebase storage on this project" — Apply to current context [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Resize extension behavior (sizes, path suffixes) depends on install-time config; verify per project. [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Zero-byte / corrupt file | Reject pre-upload; rule `request.resource.size > 0` |
| Filename collision | UUID/hash names avoid overwrite; never trust user filename |
| Upload interrupted mid-stream | Resumable task resumes; surface retry on `retry-limit-exceeded` |
