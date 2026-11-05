# Usage measurement

Use the harness's session index to discover paths. Resolve attribution from actual prompts and
parent/child records, not filenames alone. Read the history API documentation once; retain selected
IDs/paths instead of repeating discovery. Historical semantic review uses the supported history
reviewer. A fresh app run is neither needed nor authorized for this retrospective.

## OMP JSONL mechanical extraction

Inspect one record's keys without printing content before assuming this shape. In the observed
OMP format, `type: message`, `message.role: assistant`, `message.usage` contains `input`, `output`,
`cacheRead` and `cacheWrite` separately. `input` is uncached input in this format; confirm other
providers' semantics rather than applying this interpretation to all formats.

For each explicitly selected session file:

1. Parse JSONL with the existing runtime/stdlib. Select assistant messages in `[start, end)` using
   the record timestamp with an explicit timezone. This is usage incurred during the window, not
   necessarily the lifetime cost of work completed during it. Exclude the audit's own session.
2. Deduplicate known session IDs across discovery sources; within/across copied histories,
   deduplicate nonempty response IDs. If response IDs are absent, retain the records and disclose
   the limitation rather than guessing identity from identical text. A retry with a different
   response ID is a separate request, not a duplicate.
3. Sum the four usage fields independently. Count records with missing usage or missing fields
   separately. A zero-usage cancellation is zero recorded usage, not a missing-data estimate.
   Do not add `totalTokens` or `model_usage` aggregates to these fields. Do not silently count
   malformed records as zero; report the source and affected coverage.
4. Record model/provider coverage and mixed models. Stored `usage.cost` can reflect configured
   rates rather than an invoice; omit dollars unless their provenance is established.
5. Count compaction records separately. Their context sizes are not additional billable usage.
   Parent messages can contain child summaries without accounting for child usage. Never claim
   full-ticket totals unless separately discovered child/external usage is included without overlap.
6. For repeat-load candidates, extract only tool name, timestamp, message ID and requested path.
   Normalize supported read aliases and selectors cautiously; a different range may be new evidence.
   Do not hash today's source and claim it proves historical contents were unchanged. Check nearby
   compactions, source edits and requirements before calling a reread avoidable.

Keep the compact measurement artifact private, outside served pages. Include the window/timezone,
selected session IDs/paths and selection basis, per-session fields, missing/duplicate record counts,
exclusions and source anchors. Link the report to a sanitized summary, not raw private transcripts.

## Interpretations to reject

- A 500-call pricing change is not automatically less efficient than a 100-call column removal.
- Five skill loads across five compactions are not five proven unnecessary loads.
- A same-head browser retry after a tenant/fixture change is not an unchanged-state rerun.
- A new reviewer requested by the user is authorized scope, even if it repeats inspection.
- A broad CI sweep unrelated to the changed behavior can be churn; a targeted check finding a
  real regression is useful verification. Inspect what each actually established.
- Repeated user prompts are evidence of friction, not automatically agent failure. Distinguish
  new requirements, teaching questions, sensitive-action approval and reminders of prior directions.
- A missing staging outcome is unknown, not zero defects. No improvement claim without the
  comparable observation window, denominator and required evidence.

If usage is unavailable, deliver the sourced qualitative audit with that limit. Do not invent token
counts from transcript length, launch another history collector merely for nicer numbers, or
build telemetry/accounting infrastructure as part of the audit.
