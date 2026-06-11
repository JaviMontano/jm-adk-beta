<!-- distilled from alfa skills/firebase-storage -->
<!-- > -->
# Firebase Storage

> "Every uploaded file is a trust exercise — validate it before you store it." — Unknown

## TL;DR

Guides Firebase Storage implementation — file upload with progress tracking, download URL generation, security rules for access control, automatic image resizing via extensions, and organized file path strategies. Use when your app needs to store and serve user-uploaded files (images, documents, media). [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify file types to be stored (images, documents, audio, video)
- Determine upload sources (form input, drag-and-drop, camera capture)
- Check storage quota and bandwidth requirements
- Review existing file organization strategy in storage buckets

### Step 2: Analyze
- Design file path structure: `users/{uid}/profile/{filename}` or `posts/{postId}/images/`
- Plan file size limits and type validation (client-side + security rules)
- Evaluate image processing needs (resize, thumbnail, watermark)
- Determine access patterns (public via download URL, private via rules)

### Step 3: Execute
- Implement file upload with `uploadBytesResumable` for progress tracking
- Add client-side validation (file type, size) before upload
- Generate download URLs with `getDownloadURL` and store in Firestore
- Write storage security rules matching auth requirements
- Install Resize Images extension for automatic thumbnail generation
- Configure CORS for cross-origin access if needed
- Add upload progress UI (progress bar, cancel button)

### Step 4: Validate
- Test upload with various file types and sizes (including edge cases near limits)
- Verify security rules deny unauthorized access
- Confirm image resize extension generates thumbnails correctly
- Check download URLs work and files serve with proper content types

## Quality Criteria

- [ ] File type and size validated on both client and security rules
- [ ] Upload shows progress indicator and supports cancellation
- [ ] File paths include user ID for ownership-based security rules
- [ ] Download URLs stored in Firestore for efficient retrieval
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Generating download URLs on every page load (store them in Firestore instead)
- Allowing any file type without validation (security and storage risk)
- Using predictable file paths without auth checks in security rules

## Related Skills

- `image-optimization` — optimize images before or after upload
- `firestore-security-rules` — storage security rules follow similar patterns

## Usage

Example invocations:

- "/firebase-storage" — Run the full firebase storage workflow
- "firebase storage on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
