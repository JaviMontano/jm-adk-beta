# Example input — security router

A developer hands the skill a concrete request and a target file.

> "Can you audit our `hooks/` directory before we publish the plugin? Here's the
> one script. I think it's fine but I want a second pass — and please don't change
> anything."

Attached target `hooks/post-commit.sh`:

```bash
#!/usr/bin/env bash
# deploy token (example, replace before use): <YOUR_TOKEN>
USER_INPUT="$1"
eval "$USER_INPUT"                       # run the passed command
curl -s "https://api.example.com/notify?key=ghp_aB3dF6hJ9kL2mN5pQ8rS1tU4vW7xY0zAbCd"
```

Expected routing: `topic = audit-security`, `depth = deep` (full report
requested, pre-publish gate). Read-only — the developer explicitly forbade
mutation. The script mixes a placeholder token, a real-looking live token in an
executed `curl`, and an `eval` of unsanitized input, so the audit must classify
each by *exploitable context*, not by pattern shape.
