# Example Input — devops-deploy

## User request
> "Here is our GitHub Actions workflow. We deploy to AWS from it. Review it and
> harden it before we turn on branch protection — I want it production-safe."

```yaml
name: ci
on:
  pull_request_target:
  push: { branches: [main] }
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm test
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: aws s3 sync ./dist s3://app --region us-east-1
        env:
          AWS_ACCESS_KEY_ID: AKIA-hardcoded-in-yaml
          AWS_SECRET_ACCESS_KEY: hunter2-literal
```

## Context
- Node 20, npm with a committed `package-lock.json`.
- Deploy target: AWS S3 static site, `us-east-1`.
- Intent: harden, then enable branch protection.

## Expected routing
- Topic: `github-actions-ci` (workflow review/hardening — not a generic checklist).
- Depth: `deep` (review + harden + handoff before go-live).
