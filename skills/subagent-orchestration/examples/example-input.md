# Example input — subagent-orchestration

A growth team has a list of 40 companies and wants, for each, the company's
careers page found, the open engineering roles extracted, and the companies
ranked by hiring velocity. The finder may sometimes hit a careers page behind a
login wall it cannot reach. The team can tolerate a few companies being skipped
as long as the run still ranks the rest and reports which companies were missed.
Available models: Haiku and Sonnet. Available tools: `WebFetch`, `Read`, `Grep`.

Design a deterministic hub-and-spoke orchestration plan: finder, extractor, and
ranker spokes, each using `AgentDefinition` + `Task`, fresh-session isolation,
typed errors that separate a careers page that is genuinely empty
(`valid_empty`) from one that could not be reached (`access_failure`), and a hub
that continues on partial failure while recording `coverage_gaps`.
