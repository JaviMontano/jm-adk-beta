# Example input — session-workspace

A real session-lifecycle request handed to the router.

---

**User message:**

> "Context is at about 6% left and auto-compaction is about to fire. I'm mid-fix
> on the flaky auth test on branch `fix/auth-flake`, PR #214 is open and CI is
> red on `test_login_retry`. Make sure the next session doesn't lose where I am
> before it compacts."

**Ambient state available to the router:**
- Repo `jm-adk-beta` @ branch `fix/auth-flake`, working tree dirty (1 path). [CONFIG]
- PR #214 OPEN; CI red on `test_login_retry`. [CONFIG]
- No explicit `topic` or `depth` supplied by the user. [OPEN]

**What the router must decide:**
- Which single `topic` owns "preserve state across an imminent compaction"?
- Is this ambiguous against `session-end-cleanup` (close the session) or
  `session-manager` (write stage state)? Apply the boundary ruling.
- What `depth` is warranted given the time pressure and the active blocker?
