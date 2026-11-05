# Execute Ticket

`execute <ticket ID, URL, or name>` requests implementation. Use discovery and authorization rules in `skill://execute`.

## Establish context and plan

1. Read the ticket description, acceptance criteria, relevant comments, attachments and dependencies through the configured provider. Locate the affected behavior and existing repository patterns.
   Trace each named example's available history through the relevant grouping, identity,
   ordering and selection rules before proposing the fix. Use existing evidence or bounded,
   authorized read-only inspection, not broad scans, setup or paid generation before agreement.
   Label missing inputs/oracles and actual contradictions; do not imply a possible relationship
   is verified or replace the ticket's example with a convenient passing one.
2. Resolve missing requirements from available evidence. Ask only if the intended outcome, scope or required dependency remains unclear; do not invent acceptance criteria or silently narrow the request.
   Apply **Evidence before edge-case escalation** in `skill://execute` before raising a
   hypothetical domain question or adding defensive scope. Preserve explicit requirements
   and reported failures; lack of a matching data example does not waive them.
3. Resolve the assigned repository/worktree and intended PR base from available context under
   `skill://execute`'s **Discover once, reuse**; do not ask for facts already supplied there.
4. Prepare a proportionate proposed plan covering affected files, every acceptance criterion,
   risks and verification. Complete `skill://execute`'s **Pre-work Socratic checkpoint** with
   the user before implementation, setup, tests or delegated work. Use read-only discovery
   for the current-state explanation; do not present an unexamined design as settled.
   Apply **Plan before adding complexity** in `skill://execute/reference/code-quality.md`:
   identify canonical ownership/reuse, a simpler framing, affected callers and contracts, file-size
   crossings and structural risks before production edits.
5. If materially different solutions satisfy the wording but not the same user outcome, resolve that distinction before building the larger one.
6. Record the agreement and source-backed invariants under `skill://execute`'s **Working agreement
   and handoffs** in the existing plan. Carry later additions forward without dropping scope,
   then proceed without another generic plan-approval round.

## Implement, verify and review

- Follow the red/green TDD contract in `skill://execute`: capture the failing behavior before
  production edits, make the minimum fix, then prove the same check passes.
- Make the smallest complete change following existing patterns; fix the root cause and migrate affected callers.
- Apply **Implement against the same bar** in `skill://execute/reference/code-quality.md` as the
  change develops; do not postpone design cleanup until external review.
- Before broad recomputation, a large-data run or expensive verification, exercise the named
  example with the smallest complete authorized probe. Compare the actual selection and outcome
  with its declared oracle; surface policy ambiguity before scaling. If the example fails,
  resolve its cause within scope or report its blocker, while continuing independent work.
  This ordering never waives required broad coverage or authorizes otherwise forbidden calls.
- For bugs, confirm the reported reproduction no longer fails after green. Keep a useful regression
  test when practical; otherwise remove the throwaway check and report the smoke check and its
  limitations. Do not repeat a user-reported failure manually merely to confirm it.
- Apply `skill://execute`'s **Acceptance gate for publishing and revisions** after stabilizing
  the revision. Use its runtime-coverage and evidence rules; record actual commands, environment,
  results and gaps in the existing task record. Builds/tests do not replace observed behavior.
  Run separately required repository/CI checks; do not turn the built-in sanity pass into an
  unrelated broad CI sweep (see **Keep sanity separate from broad CI** in `reference/sanity-check.md`).
- Review correctness and scope against the request and run **Review the complete change before
  publication** in `skill://execute/reference/code-quality.md`. Fix or substantiate presumptive
  quality blockers, record dispositions, and repeat affected acceptance verification after any
  restructuring. Keep an environment needed for the user's visual review.
- Prepare and verify the first testing guide under `skill://brew-test` and `skill://execute`'s
  **Testing handoffs** within the same acceptance pass. Reuse applicable journey evidence and
  re-walk only affected steps; do not create another assessment or repair loop.

## Feature demo video (when requested)

Use the existing `playwright-demo-kit` checkout and read its `README.md` before recording. Confirm the frontend **and backend** target are safe for demo actions; do not hardcode credentials or record secrets. From the kit root, set `PLAYWRIGHT_BASE_URL` and any existing demo auth variables as needed, then select the one feature spec and run test plus render under **one** lock:

```bash
DEMO_SLUG=<ticket-or-work-slug> python3 scripts/with-recording-lock.py -- sh -c 'npx playwright test -c playwright.demo.config.ts tests/demo/<feature>.demo.spec.ts && npm run demo:render'
```

Replace both placeholders with the actual work identifier and spec path. `DEMO_SLUG=<slug> npm run demo:flow` is only for deliberately recording **all** kit specs; its render selects the newest video. Do not start capture via bare `npx playwright test`, run separate test/render steps for a feature showcase, delete the lock file, or bypass a busy lock. The macOS file lock spans the recorder child and releases when it exits; the JSON slug/time is informational, not a stale timeout. This protects recordings on this Mac only. Report the actual video path and observed result, not just a test listing.

## Deliver

Update existing documentation when the contract requires it. Follow the publication authorization in `skill://execute`; an existing instruction to commit/push/publish needs no repeat confirmation.

Follow `skill://execute`'s **PR descriptions** and **Testing handoffs** for initial publication,
revisions and completion/blockers, using the same verified guide. Send the initial handoff as
soon as the draft is published, then continue `skill://execute/reference/review-loop.md`;
do not stop merely because the PR exists. Report the final review result or exact blocker.
