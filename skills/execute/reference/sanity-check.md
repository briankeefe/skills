# Execute Sanity Check

Use for `execute sanity check [scope]` to assess completed work against its requirements. Apply shared defaults from `skill://execute`. This is a review, not automatic authorization to edit or publish.

## Bounded assessment and closeout

This contract also applies to acceptance closeout in ticket implementation and PR revisions.
Use the existing task plan, acceptance record or PR report; no separate budget artifact.

- **Freeze the baseline.** Record the sourced A/C, approved decisions, named examples and material
  affected-behavior checks at the start. Add a required check only for a new sourced requirement,
  a concrete material defect, or a newly identified material correctness/safety verification gap
  in the changed path. Record its evidence and impact once. Reviewer suggestions, cosmetic polish
  and unrelated pre-existing debt stay nonblocking findings outside the required case table.
  Existing required cases cannot be removed or downgraded without a sourced owner-approved revision.
- **Keep prerequisites local to the criterion.** Name the exact missing input, oracle, access or
  authorization each BLOCKED case actually needs. A missing clinical benchmark rubric does not
  block deterministic selection, deduplication or quote checks. Finite named examples use their
  declared source-backed expectations; a quantitative accuracy benchmark needs its own approved
  corpus, denominator, rubric and threshold. Keep an unresolved benchmark visible and blocking
  whole-scope readiness unless the owner explicitly revises or splits its scope.
- **One evidence pass per relevant state.** Reuse applicable observations after checking relevant
  code, requirements, fixtures/data, runtime/role and model/prompt/context identities. Exercise
  missing feasible cases once; retry a transient infrastructure failure at most once. Do not
  regenerate paid outputs or launch another independent reviewer merely to get green. Required
  safety preflight and evidence integrity checks still apply; stale receipts stay unverified,
  not PASS by explanation. Reassess only affected cases after a relevant change or new material
  evidence. An unchanged invocation returns the applicable prior verdict and remaining gaps.
- **Two acceptance repair rounds total.** After initial implementation, record `Closeout: 0/2`
  alongside the baseline and findings. Each separately authorized grouped repair attempt consumes
  one round: increment before editing, then record affected verification, even when it fails.
  Persist the count across publication, revisions, new heads, reviewers, agents and invocations
  for the same ticket/PR closeout; recover existing rounds from task history rather than assuming
  zero. If that history is unavailable, report the missing count instead of silently resetting it.
  The final allowed round may finish affected verification and required current-head reviews
  within their existing authorization and Cursor cap; it may not start another repair attempt
  or optional independent review. At two rounds, hand over remaining blockers and smallest next
  actions. Only explicit owner approval for a stated number of additional rounds extends the limit.
  New material safety/correctness evidence still requires safe assessment and escalation, not
  automatic extra repair rounds. This limit neither consumes nor resets Cursor's separate
  two-round cap and never substitutes for its current-head approvals or publication gates.

An explicit `execute sanity check` invocation never starts a repair round or additional independent
review, even when implementation was previously authorized. PASS, WARNING and FAIL all complete
that read-only command: report the finite findings and next actions, then stop. Repairs belong to
a separately authorized implementation/revision workflow under the same persisted closeout limit.
This command-only stop rule does not halt a ticket's built-in verification pass; that workflow
continues already-authorized work within the same repair limits, without a second assessment loop.

## 1. Establish what is being checked

Read the original request/ticket, approved plan and subsequent decisions, relevant repository instructions, the complete in-scope change, and available verification evidence. Derive the comparison base and files from the current assignment or PR; do not assume the last commit is the whole change.

Reconcile the existing plan's **Must deliver**, **Must preserve** and **Not included** with the
original request, ticket/comments and subsequent approved changes. Do not treat a relaxed
expectation or a newer requirement as permission to drop the rest of the scope.

If requirements or the intended scope cannot be established from available context, **STOP** and ask for the specific missing information. Do not invent acceptance criteria or report a pass based only on code style.

### PR readiness versus rollout completion

Default code/PR sanity checks to **implementation readiness**, not production rollout completion.
A data-repair PR can **PASS** when the implemented repair is demonstrated to meet every in-scope
A/C on representative isolated data, with reviewed target/record selection, preserved invariants,
and an explicit operator procedure. Exercise applicable stale-input, repeat/resume and recovery
behavior; require backup/rollback or another concrete recovery path appropriate to the operation.
A script's existence, unit tests alone or an unexercised plan is not sufficient proof.

Production deployment/execution and its approval are separate **pending rollout** items. Their
absence alone must not turn a demonstrated PR implementation into WARNING, FAIL or BLOCKED.
This does not authorize production writes or claim that live data has changed. Incomplete repair
coverage, unreviewed mappings and unapproved scope exclusions still block PR readiness.

State the stage in the verdict. If explicitly checking rollout or completion of an operational
task, require actual results in the named target. Project case oracles/gates must reflect the same
stage: record an owner-approved stage correction for an existing baseline, reconcile applicable
evidence, and track rollout prerequisites outside the PR-required case table. Never merely flip a
blocked row to PASS or ignore a failing gate.

## 2. Check requirements, correctness, and scope

- Account for **every acceptance criterion** as satisfied, missing, or unverified, with a source location and evidence level: unit, real API/database, local UI, staging, or unverified. Distinguish implementation inspection and deployment status from runtime proof.
- Check relevant happy paths, boundaries, failures, and preserved behavior. Review security and authorization boundaries, state ownership, data integrity, and performance-sensitive paths where affected.
- Compare with existing repository patterns and instructions, not universal preferences about languages, frameworks, mutation, component styles, or syntax. Separate genuine defects from stylistic suggestions.
- Identify unnecessary features, abstractions, dependencies, refactors, or unrelated edits. Do not revert user work or silently expand the approved scope.
- Separate in-scope defects from pre-existing issues. Ground findings in affected files and explain the observable impact; give calibrated confidence for diagnoses rather than presenting guesses as facts.
- Apply `skill://execute/reference/code-quality.md` to the complete change; include structural
  regressions and demonstrated complexity-deleting alternatives, not just behavioral defects.
  Report blocking quality findings and any substantiated structural waivers.

A checklist or reviewer opinion is not runtime evidence.

## 3. Assess verification

Reuse current, applicable results without repeating checks just to reconfirm reported observations.
Apply the bounded evidence pass above. If evidence is missing or invalidated by later changes, run
the smallest relevant check in a safe, isolated environment and report the exact outcome. Use
documented project commands and installed CLI help, not assumed package managers or test runners.

For bug fixes, check that the original failure is prevented. For UI changes, inspect the actual surface and relevant screenshots; passing logic tests alone do not prove appearance or interaction.

For stateful behavior, look for one complete same-record journey through save, reload, and reopen or cancel where relevant; check the affected summary and unchanged peers. Probe the change's most likely boundary or negative case, not an exhaustive matrix. If this cannot be exercised before staging, make the gap explicit rather than promoting isolated tests to end-to-end proof.

### Walk the testing guide

For UI work, this pass is part of both the built-in ticket sanity check and an explicit sanity
check. Use the current rendered testing guide as the route through the real app, not a separate
happy-path walkthrough. Ticket implementation prepares it with `skill://brew-test` first.
A read-only sanity check inspects an existing guide; it does not create or edit one unless
explicitly requested. If a required ticket handoff guide is missing, report the gap.

- Open the guide and follow its numbered actions in order from the stated starting link,
  tenant/role and record state, not an agent's prefilled tab. Follow links and filters as written;
  find the exact named controls and compare each visible result with its written expectation.
- Do not silently compensate for missing navigation, hidden prerequisites, ambiguous labels or
  incorrect expected results using implementation knowledge. Record the step and what prevented
  following it. Distinguish an instruction defect from an app defect or unavailable prerequisite.
- In the existing acceptance record, map each journey to its criteria and record observed
  results, environment/revision and any blocked steps. Reuse evidence only when it demonstrates
  following those exact written actions at the current relevant state. Feature checks alone do
  not prove the guide is usable; re-walk affected steps after guide or app changes.
- Exercise only actions already authorized on safe records, including restoration where needed.
  A guide is not permission for production/shared-data mutations, paid calls or destructive actions.
  Block unsafe or unavailable steps. Non-UI criteria retain their engineering checks, not a
  fabricated visual proxy.
- A required journey that cannot be followed is not PASS. Report its smallest correction or
  prerequisite. Fix the guide/app only within an explicitly authorized implementation or revision
  workflow and existing repair limits, then verify affected steps. A read-only sanity invocation
  reports the finding without editing. Do not add another review or repair cycle for this pass.

Do not force a browser, E2E test generation, or a new test suite for changes they cannot meaningfully verify. Report unavailable runtime access or missing required CI-equivalent checks as gaps, not passes.

## 4. Give the verdict

Lead with **PASS**, **WARNING**, or **FAIL**, followed by only material findings:

- **PASS:** all requirements for the stated stage have evidence, relevant checks passed, and no
  blocking correctness, structural quality or scope issue was found. PR implementation can PASS
  while a demonstrated repair still awaits production rollout.
- **WARNING:** only nonblocking concerns or optional verification gaps remain; name what is not
  established. Required criteria must still pass the stage-appropriate project acceptance gate.
- **FAIL:** required behavior for the stated stage is missing, a blocking correctness or structural
  quality defect exists, or required verification failed or is blocked.

For each material finding, record its criterion/source, location, actual evidence, impact, kind
(`defect`, `verification gap` or `suggestion`), blocking disposition with reason, and smallest next
action. Include exact checks and unverified criteria. A failed evidence gate is a verification
gap, not by itself proof of a product defect; it still prevents PASS/WARNING where required.
FAIL completes this read-only check, not the ticket, and never authorizes fixes or publication.
