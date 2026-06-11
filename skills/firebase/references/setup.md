<!-- distilled from alfa skills/firebase-setup -->
<!-- > -->
# Firebase Setup

> "A well-configured Firebase project is the foundation that prevents a hundred future headaches." — Unknown

## TL;DR

Guides Firebase project initialization — from `firebase init` through emulator configuration, environment-specific settings, and project aliases for dev/staging/prod. Use when starting a new Firebase project or restructuring an existing one for multiple environments. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check if Firebase CLI is installed and authenticated (`firebase --version`)
- Identify required Firebase services (Firestore, Auth, Functions, Hosting, Storage)
- Determine environment strategy (dev, staging, production projects)
- Review existing `firebase.json` and `.firebaserc` if migrating

### Step 2: Analyze
- Plan project structure: monorepo vs separate repos for functions/hosting
- Determine emulator needs (Firestore, Auth, Functions, Storage, Hosting)
- Design environment variable strategy (`.env.local`, `.env.production`, runtime config)
- Evaluate billing plan requirements (Blaze for Functions, Extensions)

### Step 3: Execute
- Run `firebase init` selecting required services
- Configure project aliases in `.firebaserc` (dev, staging, prod)
- Set up emulator suite in `firebase.json` with fixed ports
- Create `.env` files for each environment with Firebase config values
- Initialize Firestore with `firestore.rules` and `firestore.indexes.json`
- Set up Functions with TypeScript, ESLint, and proper `package.json` scripts
- Add emulator data export/import scripts for consistent dev data

### Step 4: Validate
- Start emulators and verify all services run locally (`firebase emulators:start`)
- Confirm project switching works (`firebase use dev`, `firebase use prod`)
- Check that environment variables load correctly per environment
- Verify `.gitignore` excludes sensitive files (`.env`, service account keys)

## Quality Criteria

- [ ] All required Firebase services initialized and configured
- [ ] Emulator suite runs locally with fixed ports and seed data
- [ ] Environment aliases configured for dev/staging/prod
- [ ] Sensitive credentials excluded from version control
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Using the same Firebase project for development and production
- Hardcoding Firebase config values instead of using environment variables
- Skipping emulator setup and testing directly against production

## Related Skills

- `firestore-modeling` — data modeling follows project setup
- `cloud-functions` — Functions initialization is part of Firebase setup

## Usage

Example invocations:

- "/firebase-setup" — Run the full firebase setup workflow
- "firebase setup on this project" — Apply to current context


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
