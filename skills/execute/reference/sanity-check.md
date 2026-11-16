# Execute Sanity Check

Use for `execute sanity check [scope]` to assess completed work against its requirements, with
shared defaults from `skill://execute`. The assessment is read-only: it reports, and any edits or
publication come from an execution that is already authorized.

## Fresh reviewer for standalone checks

Run an explicit `execute sanity check [scope]` in one fresh reviewer session with no inherited
conversation or implementing-agent transcript, through the harness's supported delegation and a
self-contained brief (no fork, resume or reuse of the implementing session). If context isolation is
unavailable, report that blocker instead of checking in the current conversation. Isolation covers
conversation only; files, credentials, runtime targets and safety rules are unchanged.

The parent resolves the target and hands over sources, not a verdict:

- the original request/ticket and requirement sources, approved decisions and scope changes;
- repository/worktree, comparison base and exact head, plus any in-scope uncommitted diff, labeled
  as uncommitted;
- applicable repository/personal instructions and authorization limits, this workflow, and the
  complete in-scope diff/code locations;
- verification records (actions, observed results, environment/revision, known gaps), the testing
  guide, frozen acceptance baseline and repair history;
- the oracle-change list (below) and the tests that existed at the base and changed since
  (`git diff --stat <base>...<head>` filtered to them). The reviewer checks each against its source;
  an oracle change without one is a finding.

Leave out the implementer's conclusions, proposed verdict, reassurance and narrative of why the
fix works: a reviewer handed a hypothesis tends to confirm it. Where records mix facts and
conclusions, pass the factual sections and keep approved decisions, known failures and required
cases intact. Pass approved revisions with their reasons as claims to verify, never as settled.

The reviewer reads the sources and change itself, checks evidence applicability before reuse, and
returns the stage, PASS/WARNING/FAIL, sourced findings, observed verification and exact gaps. The
reviewer stays read-only. The parent relays the result as-is and does not launch another reviewer
to get a better verdict on the same head. Repair, publication and tracker writes stay with an already-active
execution owner under its existing authorization; the assessment resets neither repair history nor
Cursor's review limit. An unchanged invocation returns the applicable prior verdict and gaps.

Built-in ticket/PR-revision verification and `execute pr review [PR_URL] --sanity` run in the
working session. The exception is the readiness gate: before marking an executed PR ready, the
owner runs this fresh-session assessment once on the final head. The implementer's checks are
self-graded and tend to be built around the change; a reviewer that did not write it catches
regressions in preserved behavior.

**Independent verdicts stand.** An independent FAIL or BLOCKED stays in force for that head. The
implementer's recheck, explanation or summary cannot overturn it or report PASS over it. After an
evidence-backed repair, a fresh assessment of the new head (affected cases plus the original
finding) replaces it. Label self-verification as such; only a fresh-session verdict is independent.

## Bounded assessment and closeout

This contract also governs acceptance closeout in ticket implementation and PR revisions. Keep it in
the existing task plan, acceptance record or PR report.

- **Freeze the baseline.** At the start, record the sourced A/C, approved decisions, named examples
  and material affected-behavior checks. Add a required check only for a new sourced requirement, a
  concrete material defect, or a material correctness/safety gap in the changed path, recording its
  evidence and impact once. Reviewer suggestions, polish and unrelated pre-existing debt are
  nonblocking findings outside the case table. Removing or downgrading a required case needs a
  sourced owner-approved revision. Keep the original failing action/input and its independent
  expected outcome, including natural requests and conversation order for LLM behavior. A request
  to "adjust" a failure authorizes repair, not swapping in an easier journey.
- **Treat oracles as locked.** Guide expectations, acceptance cases, fixtures and the assertions,
  inputs and waits of tests that existed at the base are the grader. Editing the grader to reach
  green is the most common way agents hide regressions. Navigation/copy corrections that keep the
  required action and outcome need no approval. Any other change to an existing oracle (expected
  result, required action/input, removed case, or an added wait/retry in a pre-existing test) goes
  in an **oracle-change list** in the acceptance record with its source. Changes to an expected
  outcome or required action need owner approval before they count; the agent's own reading of a
  contract is a proposal, not a source. Report the list in every handoff and PR revision.
  Several pre-existing tests needing the same new wait or mock means the product likely gained an
  unwanted gate: diagnose the product first.
- **Keep prerequisites local to the criterion.** Name the exact input, oracle, access or
  authorization each BLOCKED case needs, and keep checking cases that don't need it: a missing
  clinical rubric does not block deterministic selection, deduplication or quote checks. Named
  examples use their declared source-backed expectations; a quantitative accuracy benchmark needs
  its own approved corpus, denominator, rubric and threshold, and an unresolved one blocks
  whole-scope readiness until the owner revises or splits it. In authorized execution, starting an
  owned local service safely and running ordinary missing checks are the agent's work: attempt the
  documented action, or name the concrete access/safety/authorization boundary, before calling
  something external. An unsafe fixture probe blocks only that probe. Read-only assessments report
  gaps without gaining setup, paid-call or data-mutation authority.
- **One evidence pass per relevant state.** Reuse an observation after checking that code,
  requirements, fixtures/data, runtime/role and model/prompt/context still match. Exercise missing
  feasible deterministic cases once; nondeterministic journeys use the batch below. Retry a
  transient infrastructure failure at most once and keep the interrupted attempt; a completed
  behavioral failure is never infrastructure. Paid outputs are not regenerated and reviewers are
  not relaunched just to get green. Safety preflight and evidence-integrity checks still
  apply, and stale receipts stay unverified. After a relevant change or new evidence, reassess only
  affected cases.
- **Three independent runs for nondeterministic acceptance.** Each required affected journey that
  depends on nondeterministic behavior needs at least three independent end-to-end runs at the same
  implementation/runtime/model/prompt state, because one good sample says little about consistency.
  - Predeclare the batch in the acceptance record: natural inputs, conversation/action sequence,
    expected outcomes and configuration, frozen before the first run.
  - Start each run from a fresh chat or equivalent safe reset, following any required history
    within the run. Reopened answers, replayed output or a fixed seed are not independent.
  - In each run, check the user-visible result and every required downloaded/persisted artifact:
    semantic values, identities, distinct rows and required columns, not counts alone.
  - All three must pass. A behavioral failure fails the batch: stop admissions, keep every outcome
    and diagnose. Inputs and the system stay as frozen between runs (no coaching or tuning), and
    failures are never discarded or outvoted by extra samples. After an evidence-backed repair, run a new batch; successes from
    different states never combine.
  - Deterministic contract checks are still required. A complete applicable batch is reused on
    later assessments. If safety, paid-call or spend limits allow fewer than three runs, the
    criterion stays unverified and the boundary is reported. Three passes are a minimum sample,
    not statistical proof or a benchmark.
- **Own repairs through acceptance.** Once implementation or revision is authorized, its owner
  fixes in-scope defects and verification/guide gaps without asking again, looping implement →
  check → repair → recheck until every required criterion passes or an evidence-backed blocker
  remains. There is no default repair-round cap; owner-imposed limits, scope, spend and
  sensitive-action boundaries still hold. If a repair breaks connected behavior, reconcile both
  failures through the shared owner/state contract (see coupled consumers in `code-quality.md`)
  before another edit; a narrower green check is not progress while preserved behavior is broken.
- **Bound attempts by evidence, not a counter.** Before each grouped repair, record the failing
  criterion, supported cause, next remedy and affected recheck in the closeout record, and keep
  attempts and outcomes across heads, agents and invocations (old `0/2`/`2/2` counters are history).
  Progress means new evidence supporting a materially different remedy; a new commit, rerun test or
  reworded explanation is not progress. When no credible authorized remedy remains, stop that
  criterion, finish independent work and report the evidence, attempts, missing prerequisite or
  decision, and the smallest options. PASS comes only from passing evidence, never from lowering
  the baseline, resampling paid output or collecting opinions. This policy neither consumes nor
  resets Cursor's two-round cap and never substitutes for current-head approvals or publication
  gates; at that cap, keep the PR draft, hand off unresolved blockers and start no further review
  cycle.

Standalone `execute sanity check` ends at PASS, WARNING or FAIL; that completes the assessment, not
the ticket, and does not resume implementation authorized in an earlier session. When the
assessment is a step inside an active authorized execution, the reviewer reports and the owner
continues in-scope repairs under the contract above, unless the user or parent asked for a pause
or report-only handoff.

## 1. Establish what is being checked

Read the original request/ticket, approved plan and later decisions, repository instructions, the
complete in-scope change and available verification evidence. Derive the base and files from the
assignment or PR rather than assuming the last commit is the whole change.

Reconcile the plan's **Must deliver**, **Must preserve** and **Not included** with the original
request, ticket/comments and approved changes. A relaxed expectation or newer requirement leaves
the rest of the scope in force.

If the requirements or intended scope cannot be established, **STOP** and ask for the specific
missing information. Acceptance criteria come from sources, and code style alone never earns PASS.

### PR readiness versus rollout completion

By default a code/PR sanity check assesses **implementation readiness**, not production rollout. A
data-repair PR can **PASS** when the repair is demonstrated against every in-scope A/C on
representative isolated data, with reviewed target/record selection, preserved invariants, an
explicit operator procedure, exercised stale-input/repeat/resume/recovery behavior, and a backup,
rollback or other concrete recovery path. A script's existence, unit tests alone or an unexercised
plan are not enough.

Production deployment/execution and its approval are separate **pending rollout** items and alone
do not make a demonstrated implementation WARNING, FAIL or BLOCKED. This grants no production
writes and claims no live change. Incomplete repair coverage, unreviewed mappings and unapproved
exclusions still block readiness.

State the stage in the verdict. When explicitly checking rollout or an operational task, require
actual results in the named target. Case oracles and gates follow the same stage: correct an
existing baseline's stage only with owner approval, reconcile evidence, and track rollout
prerequisites outside the PR case table. A blocked row moves to PASS only on evidence, and a
failing gate is never ignored.

## 2. Check requirements, correctness, and scope

- Account for **every acceptance criterion** as satisfied, missing or unverified, with its source
  and evidence level: unit, real API/database, local UI, staging or unverified. Code inspection
  and deployment status are not runtime proof.
- Re-check every approved revision that weakens or replaces a sourced expectation, especially a
  ticket's own named example. Verify its factual premise against actual data and the original
  sources. If the data contradicts it, or the revised result is still wrong by the ticket's intent,
  report a material finding with the evidence and decision needed: an approval records what was
  decided, not that it is correct.
- Check relevant happy paths, boundaries, failures and preserved behavior, plus security and
  authorization boundaries, state ownership, data integrity and performance-sensitive paths.
- Judge against repository patterns and instructions rather than universal style preferences, and
  separate defects from stylistic suggestions.
- Flag unnecessary features, abstractions, dependencies, refactors and unrelated edits, without
  reverting user work or expanding scope.
- Separate in-scope defects from pre-existing issues. Ground findings in affected files, explain
  observable impact and give calibrated confidence.
- Apply `code-quality.md` to the complete change, including structural regressions and
  demonstrated simpler alternatives; report blocking quality findings and substantiated waivers.

A checklist or reviewer opinion is not runtime evidence.

## 3. Assess verification

Reuse current, applicable results under the evidence pass above. If evidence is missing or
invalidated, run the smallest relevant check in a safe, isolated environment with documented
project commands and report the exact outcome.

### Keep sanity separate from broad CI

This applies to standalone checks, `pr review --sanity` and built-in acceptance verification:
sanity checks changed behavior against sourced requirements; CI is a separate gate.

- For a missing criterion, run the smallest targeted check that establishes the behavior, on the
  real UI/API/database where appropriate.
- Run broad suites, full builds, lint/typecheck sweeps or CI reruns only when this assessment's
  request, a sourced requirement or a repository instruction mandates it; name that source and why
  targeted evidence can't satisfy it. A CI job's existence alone is not such a mandate.
- Report CI status and known unrelated, pre-existing or flaky failures separately from the verdict,
  without rerunning them to confirm. Required CI gates still apply to publication and merge.
- A demonstrated regression in the changed path, or missing required behavioral evidence, blocks
  sanity even when a fragile suite found it. Call a failure flaky only with evidence.

For bug fixes, confirm the original failure is prevented. For UI changes, inspect the actual surface
and screenshots; logic tests do not prove appearance or interaction.

For stateful behavior, look for one same-record journey through save, reload and reopen or cancel,
checking the affected summary and unchanged peers, and probe the most likely boundary or negative
case. If it can't be exercised before staging, state the gap rather than treating isolated tests as
end-to-end proof.

When shared behavior changes, exercise its preserved consumers and interacting states identified
under `code-quality.md`. For polling UI, observe repeated automatic checks in healthy and recovery
states; a manual click or geometry check does not prove the interaction. Simulated streams or
saved-state transitions prove their tested seams, not live model compliance or worker completion.

### Walk the testing guide

For UI work, the guide walk is part of both built-in and explicit sanity checks: the rendered
testing guide is the route through the real app, rather than a separate happy-path walkthrough.
Ticket implementation prepares it with `skill://brew-test`; a read-only check inspects the existing
guide, reports a missing one, and creates or edits one only on explicit request.

- Follow the numbered actions in order from the stated starting link, tenant/role and record state
  (not an agent's prefilled tab), using links and filters as written. Find the exact named controls
  and compare each visible result with its expectation.
- When navigation, prerequisites, labels or expected results are missing or wrong, record the step
  and what blocked it rather than compensating with implementation knowledge. Classify it as an
  instruction defect, app defect or unavailable prerequisite.
- In the acceptance record, map each journey to its criteria with observed results,
  environment/revision and blocked steps. Reuse evidence only if it followed these exact actions
  at the current state; feature checks alone don't prove the guide is usable. Re-walk affected
  steps after guide or app changes.
- Perform only already-authorized actions on safe records, restoring where needed. The guide grants
  no production/shared-data mutation, paid calls or destructive actions; block those steps. Non-UI
  criteria keep their engineering checks.
- A required journey that cannot be followed is not PASS; report its smallest correction or
  prerequisite. Inside an authorized implementation or revision, fix the guide/app and re-verify
  affected steps; a read-only assessment reports only.

Use a browser, generated E2E test or new suite only where it meaningfully verifies the change.
Report unavailable runtime access or missing behavioral evidence as criterion-local gaps.

## 4. Give the verdict

Lead with **PASS**, **WARNING** or **FAIL**, then only material findings:

- **PASS:** every requirement for the stated stage has evidence, relevant checks passed, and no
  blocking correctness, structural quality or scope issue was found. A demonstrated repair can PASS
  while awaiting production rollout.
- **WARNING:** only nonblocking concerns or optional verification gaps remain; name what is not
  established. Required criteria still pass the stage-appropriate gate.
- **FAIL:** required behavior for the stage is missing, a blocking correctness or structural
  quality defect exists, or required verification failed or is blocked.

For each material finding, give its criterion/source, location, evidence, impact, kind (`defect`,
`verification gap` or `suggestion`), blocking disposition with reason, and smallest next action.
List exact checks run and unverified criteria. A failed evidence gate is a verification gap, not
proof of a product defect, and still prevents PASS/WARNING where required. FAIL completes this
read-only check, not the ticket.
