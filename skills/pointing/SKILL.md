---
name: pointing
description: Estimate engineering tickets using recent team history and agent-assisted delivery. Use for pointing tickets, story-point estimates, estimation calibration, or a one-ticket-at-a-time guessing exercise, including Kubera pointing. Summarize each ticket in two sentences, save an independent estimate before the user guesses, compare, and persist the selected answers without skipping tickets.
argument-hint: "[project] <ticket IDs or URLs>"
---

# Pointing

Estimate the requested work, not a hypothetical manual implementation. Read-only planning: do not change application code, post estimates, grant access, backfill data, or deploy unless separately authorized.

## Calibrate first

1. Resolve project, tracker workspace, team and the supplied ticket order from context. Read project-local estimation guidance. For Kubera, read `~/.omp/agent/kubera.md`, especially **Point estimation**; company-specific examples and scale belong there, not in this skill.
2. Use the verified Linear recipes in `skill://execute/reference/tool-recipes.md`. Discover unfamiliar cycle/query commands with targeted help. Never print credentials.
3. Unless this session already has fresh calibration, read the two most recently completed team cycles, not the active cycle. Inspect recorded estimates and representative ticket descriptions at low, medium and high values, especially comparable pricing, UI, data and infrastructure work. Include resolved scope decisions. Follow pagination to completion or disclose the limit.
4. Distinguish positive estimates, zero-valued records, missing estimates, canceled tickets and completed tickets. Zero is valid but does not prove no effort; do not silently turn missing estimates into zero. Report the cohort and exclusions.
5. Use recorded points as relative-scope anchors. They are not tracked hours, and cycle duration, ticket age and elapsed review/deploy time do not establish engineering effort. Preserve the project's stated point/time convention unless the user changes it.

For an agentic shop, include agent-assisted implementation, human decisions, review, necessary runtime verification and active rollout coordination. Do not estimate manual coding time and then add generic QA or uncertainty buffers. Name a concrete unknown instead; do not inflate every ticket because it touches money or has many acceptance criteria. Do not subtract security, permissions, data integrity or required verification.

## Save the session

Create a private, durable local ledger before presenting the first ticket, using the project's existing estimation record if available; otherwise use `~/.omp/agent/pointing/<workspace>/<session>.json`. Do not publish this file or overwrite another session. Do not use only chat memory or an ephemeral scratchpad.

Record:

- Project/team, point scale, ordered ticket IDs, current ticket and calibration sources/date.
- Per ticket: source URL, relevant scope/unknowns, frozen initial assistant estimate and rationale, confidence, initial user guess, explicit revisions, selected planning value and whether discussion is pending.
- Final selected values, total and whether tracker updates occurred.

Keep initial guesses when either party revises. Save the assistant estimate privately before the user's guess; do not expose it in chat or progress messages. A user's selected value is not a claim both independently agreed. Treat zero as an answer, not a falsy missing value. Save answers as they arrive; memory retention may supplement the ledger.

## Work one ticket at a time

1. Fetch the actual ticket and relevant discussion, not just its title. Follow material linked requirements; if inaccessible, state what remains unverified rather than inventing the scope. Distinguish required work, suggestions, optional extras and separate/dependent tickets.
2. Choose an independent estimate using comparable historical scope, existing patterns and the simplest solution satisfying the ticket. Where an assumption about reusable code, a frontend/backend boundary or an existing matcher materially changes the estimate, inspect the relevant code narrowly or label that assumption unverified. Never claim a code-backed estimate from ticket text alone.
3. Freeze the estimate in the ledger, then present **N/total**, a ticket link/title and **exactly two plain-language summary sentences**, followed by **Your estimate?** Do not reveal your value yet. Explain domain jargon through concrete behavior, not more jargon.
4. On the user's guess, save it and compare it with the frozen estimate. One short reason for the difference is enough. If equal, or the user explicitly selects a value, record it and proceed. For a small unchallenged difference, retain the user's value as the selected planning answer without claiming consensus.
5. For a material gap (two or more points), pause on this ticket: explain the different scope/reuse/testing assumptions and get the user's selection before proceeding. A user question, objection or request to stay also pauses advancement. Never recalibrate merely to mirror the user's guess; explain any evidence-based revision and preserve the original.
6. Do not skip a ticket. If asked to skip, keep it pending and ask for a value or explicit bounded-assumption estimate. Zero counts. An unresolved dependency or unavailable document may justify a provisional estimate with a caveat, not silently dropping the ticket.

Waiting for a user's guess is an intentional pause, not incomplete autonomous work. Mark interactive tasks blocked while waiting, and do not let task bookkeeping advance the conversation prematurely.

## Explain and close

- A bare ticket ID during the exercise or after the table means explain that ticket's estimate: selected points, actual scope/reuse, substantial verification and the historical anchor or material uncertainty. Stay concise and state confidence when asserting an inference. Preserve the distinction between the user's selection and your initial estimate.
- If asked to rephrase, use an example and remain on the current ticket; do not reveal the hidden estimate.
- If asked for the table, return it immediately from saved answers, with links, short scope labels and selected points. Do not refetch every ticket or recalculate known rationale. Clearly identify any still-pending rows without exposing hidden estimates.
- At completion, verify every supplied ticket has a selected value, including zero, and sum those exact values. Save the completed ledger; return the ordered table and total, or a short completion notice if the user only wants answers saved for later. Do not conflate total engineer effort with calendar delivery time or team capacity.
- Tracker writes require explicit authorization. A request to estimate or save answers locally is not permission to update Linear.
