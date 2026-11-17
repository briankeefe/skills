---
name: execute
description: Project-neutral development workflows for `execute <command>`: tickets, PR summaries/reviews/updates, E2E tests, sanity checks, project planning, documentation, release membership and local reproduction. Also use for questions about whether an issue/PR/commit is in a release, how to reproduce a change locally, or project operations. Discover the repository, issue provider and tools from current context rather than assuming an organization or stack.
---

# Execute Toolkit

Use the matching workflow with active harness/repository rules and the user's current authorization.

## Dispatch

Match the longest named command prefix below before interpreting a ticket and pass remaining
arguments unchanged. Empty input or `help` shows this table without starting work.
A bare PR URL routes to `pr-review.md`; a bare issue URL, provider-recognized ID (for example
`ENG-2612`, not a required prefix), or resolvable ticket name routes to `ticket.md`.
Resolve names with the configured tracker and ask when a name is ambiguous. Unknown commands or
unrecognized URLs show help. An explicit command wins: `local-repro <PR_URL>` reproduces; it
does not post a review.

| Invocation | Reference doc | Purpose |
|---|---|---|
| `execute help` | (this file) | Show commands |
| `execute <ticket-ID/name/issue-URL>` | `reference/ticket.md` | Fetch, plan, implement, verify, review, PR |
| `execute pr summary [scope]` | `reference/pr-summary.md` | Summarize your open PRs |
| `execute pr review [PR_URL]` | `reference/pr-review.md` | Review with Conventional Comments |
| `execute pr review [PR_URL] --sanity` | `reference/pr-review.md` | Review plus the canonical requirements sanity assessment |
| `execute update-pr [PR_URL]` | `reference/update-pr.md` | Address actionable reviewer feedback |
| `execute shepherd-pr [PR_URL]` | `reference/review-loop.md` | Run Cursor review/fix cycles, then mark the PR ready |
| `execute actionable pr [scope]` | `reference/actionable-pr.md` | Find PRs with unaddressed feedback |
| `execute e2e test [flow]` | `reference/e2e-test.md` | Exercise a flow and generate a test |
| `execute sanity check` | `reference/sanity-check.md` | Check completed work against requirements |
| `execute init project NAME` | `reference/init-project.md` | Plan project dependencies and execution |
| `execute next task NAME` | `reference/next-task.md` | Identify the next available task, do not start it |
| `execute update project NAME` | `reference/update-project.md` | Refresh project documentation |
| `execute docs [topic]` | `reference/docs.md` | Draft project documentation |
| `execute release-check <ticket/PR/sha> [target]` | `reference/release-check.md` | Check release membership or missing changes |
| `execute staging-check <ticket/PR/sha>` | `reference/staging-check.md` | Check whether a change has deployed to staging |
| `execute local-repro <ticket/PR>` | `reference/local-repro.md` | Bring up the relevant local stack and verify |
| `execute ops [question]` | `reference/ops-facts.md` | Consult project-local operational guidance |

Reference paths resolve as `skill://execute/reference/<doc>`.

"Has this commit landed on staging?" routes to `staging-check.md`: `release-check` proves branch
reachability, while `staging-check` correlates the change with actual deployment provenance.

Standalone `execute sanity check` runs in one fresh reviewer session; see **Fresh reviewer for
standalone checks** in `reference/sanity-check.md`. Built-in acceptance verification and
`pr review --sanity` stay in the working session, except for the one fresh assessment required
before marking an executed PR ready.

## How the gates fit together

Read-only commands (reviews, sanity checks, release/staging checks, summaries) stay read-only and
end at their verdict or answer, unless the user authorizes further action. Authorized
implementation owns its work through acceptance. The verification sections below share one
evidence pass per relevant state rather than each adding its own round of checks, and none of
them grants data, spend, publication or tracker-write authority beyond what the user gave.

## Consult Fable before planning

Before settling a substantive plan, gather minimal read-only context and get one read-only
planning consultation from Fable:

1. **T3 first.** If T3 tools are available, find Fable in `orchestrator_capabilities` and use
   `delegate_task` with the exact advertised provider/model. Follow the returned waiting contract
   and read the completed result before finalizing the plan.
2. **Vanilla Claude Code fallback.** If T3 or its Fable model is unavailable or the consultation
   fails on access/model availability, use the installed `claude` CLI with its own authentication
   and an explicit Fable model (not an OMP provider/proxy or an Opus substitute). When the CLI
   supports these options, run it as a background job in the assigned worktree:

   ```sh
   env -u ANTHROPIC_OAUTH_TOKEN -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL \
     claude --model fable --print --permission-mode plan --output-format json "<planning brief>"
   ```

   Model access is proven only by a consultation that succeeds without substitution. Wait for that
   process to exit and read its full output and exit status. Leave out `--bare`, permission bypass,
   `--resume`, `--continue`, credential extraction and any second session to retrieve the result.
3. **Normal model last.** If neither route provides Fable, note the concrete failures in the plan
   and plan with the current model. Keep going without retrying, switching the session's model
   or asking the user for access.

Brief the consultant with the request, requirements/invariants, inspected code flow, repo/worktree
and base, applicable instructions, unrelated changes to preserve, and evidence constraints. Ask for
the simplest complete approach, material risks and missing decisions, and limit it to reading:
no edits, setup, tests, services, data changes, tracker writes, publication or delegation. Its
advice is input: check claims against evidence, own the plan and take product questions to the
user. The consultation does not authorize implementation or replace user agreement, acceptance
checks or Cursor reviews. Reuse a completed consultation on resume; consult again only after a
material change.

## Pre-work Socratic checkpoint

Before an implementation or other mutating workflow, the user and agent agree on the task's
before, after and architecture. This is a discussion that builds understanding, not repeated
"is this ok?" rounds. Read-only commands skip it.

Until it closes, limit work to the read-only discovery needed to ground it (request, ticket,
relevant code, existing evidence, the Fable consultation) plus creating and locally previewing the
explanation page. Answer repository facts yourself rather than asking the user.

Always explain on a local Brew page written per `reference/explain-approach.md`: context, a
before/after worked example, a flowchart and the recommendation. An inline chat explanation does
not replace it. Chat carries the takeaway, link and the agreement question.

Ask about unresolved requirements or material tradeoffs; otherwise ask once for agreement to the
complete approach. Agreement must be explicit: silence, a preselected option or the original
execute request does not count. Once agreed, record the before, after and architecture in the task
plan and proceed; reuse that agreement on resume and reopen only for a material change. A request
to skip the quiz waives only this checkpoint.

## Working agreement and handoffs

- Put substantive explanations, plans, decisions and reports on concise local Brew pages; chat
  carries the takeaway, link and exact question or blocker. Brief acknowledgments can stay in
  chat, and an explicit request for inline content wins. Reuse the task's page. A local page grants
  no publication authority.
- Keep **Must deliver**, **Must preserve** and **Not included** in the task plan, sourced from the
  request, ticket/comments and later decisions, and carry the full scope through implementation
  and sanity checking. An approved change to one expectation leaves the others in force. Record
  source-backed invariants (grouping/order, identity, precedence, preserved behavior), known
  failures and working verification commands there too. Consult them before a repair or handoff
  so settled contracts and failed invocations are not rediscovered; update only facts that new
  evidence invalidates.
- Own authorized execution through acceptance under **Bounded assessment and closeout** in
  `reference/sanity-check.md`: failures, stale evidence and review findings are work to resolve.
  A progress update, finished review or milestone does not end that ownership. Before yielding, name one of: completion, an evidence-backed no-progress stop, the exact user
  decision needed, or the external prerequisite blocking all remaining work. Continue independent
  work when only one criterion is blocked. Read-only commands complete on their verdict.
- After a verified fix, ask once what was learned that the code and tests won't explain. Capture
  only a non-obvious, durable, material lesson whose loss risks a repeated mistake or substantial
  rediscovery; most tasks yield none and none is required. Prefer an existing regression test or
  runbook update over prose. Otherwise write a short lesson where the repository already keeps
  such knowledge (fallback `docs/lessons/<topic>.md`): constraint, evidence, failed approach when
  relevant, working approach, and a retirement condition when applicable. Update the canonical
  record instead of adding a duplicate, and write it with the change before final evidence binds.
  Project knowledge stays with the project inside the task's existing change and authorization;
  private machine/environment coordinates stay in local runbooks, and credentials and
  patient/customer data stay out of both. This adds no per-ticket document, agent, or
  approval/acceptance gate. Read-only commands may name a candidate lesson in their answer but
  never write one.
- When reporting applied changes, name where (local worktree, isolated data branch, staging or
  production) rather than saying only "applied".
- Give decision/completion handoffs and answer status questions from observed facts, without
  progress estimates, dashboards or periodic status messages.

## Discover once, reuse

- Read repository instructions and relevant project docs before editing. Resolve the repo/host
  from an explicit URL, the assigned worktree, remotes and ticket links; a URL naming a different
  repo wins over the current one. The assigned project/worktree is the default; ask which
  repository only when evidence conflicts or leaves the target ambiguous, not because a new
  session began.
- Resolve the issue provider, workspace and ID format from the URL and local configuration. Use
  verified local recipes and `reference/tool-recipes.md` for issue/PR reads, Linear 2.6.0 and
  managed OMP browsers. Check versions once; read targeted `--help` only for an unfamiliar
  operation, version drift or a contradictory result. Authentication, issue/review state and
  deployment evidence always need fresh reads; verify that auth, flags, JSON fields and database
  integrations exist before relying on them.
- Reuse the assigned branch/worktree. Otherwise discover the base from repository metadata and any
  documented project branch rather than assuming `master`, `main` or a release name. Verify remotes
  before network writes. If release timing changes the strategy and is unstated, ask whether this
  targets the normal next release or something faster.
- Derive runtime and package manager from repo instructions, manifests, lockfiles and pinned
  versions, and reuse existing install/dev/test/lint/CI commands rather than installing a runner
  to fit this toolkit. Resolve documentation locations
  from the repository. Reuse instructions already in context; after compaction or changed guidance,
  reload only what is missing and keep its source pointer in the task record. Authorization,
  authentication and live task state are never cached.
- Before planning, retrieve durable lessons relevant to the affected area from where the
  repository keeps them (regression tests, runbooks, project docs and agent guidance, any lessons
  location such as `docs/lessons/`) and from local runbooks for machine/environment facts. A
  lesson is a lead, not a fact: validate it against the current tree before relying on it. Fix
  or retire a stale canonical record under the closeout rule in **Working agreement and
  handoffs**, within authorized execution only; retrieval itself is read-only and grants no
  write authority.
- Missing context: exhaust repo/tool evidence, then ask one focused question. Report unavailable
  credentials or services without guessing values or exposing secrets.

## Evidence before edge-case escalation

Before raising a speculative edge case, adding defensive logic for it, or making it a required
acceptance case, look for evidence:

- Check requirements, reported incidents, relevant code/tests and existing evidence first. A
  user-reported failure is already evidence; it needs no reproduction or new data example.
- If occurrence is still uncertain, search for a real example with existing tools and a narrow,
  authorized read-only query bounded by environment, tenant, dates, predicates and rows; prefer
  counts and minimal fields. Skip broad production scans, mutations, fixtures and paid calls for
  hypotheticals. This grants no new data access.
- If found, report a sanitized example, count with its search scope, and impact. Keep credentials
  and patient/customer data out of chat, PRs and docs.
- If not found, record **not observed in the searched scope** and, absent a sourced requirement
  or concrete correctness/security/data-integrity concern, skip the defensive code and keep the
  baseline unchanged. Missing access or incomplete searches mean **unverified**, not absent.
  Name that limit and continue independent work, asking only the focused question an in-scope
  decision needs.
- Explicit requirements and concrete correctness/security/data-integrity evidence stay actionable
  without a production occurrence; an empty search never dismisses a reported bug or material risk.

## Feasible live verification

Before proposing live/paid verification limits or admitting the first case:

- Use the smallest complete set of required cases and existing API/UI/database observations.
  Name the remaining checks and a stop condition in the plan.
- Nondeterministic journeys need the three-run batch under **Three independent runs for
  nondeterministic acceptance** in `reference/sanity-check.md`; one good output is not acceptance.
- Check whole-path resource bounds, including retries and already-admitted async work. Separate
  observed usage from a conservative bound, and stopping admissions from enforcing a ceiling inside
  a running job. Unknown or unenforceable bounds are not guarantees.
- Settle feasibility/spending tradeoffs before requesting approval. If a limit cannot be honored,
  pause new admissions and present concrete options rather than exceeding it, dropping cases or
  building accounting/telemetry to justify the trial. Spending approval is not a PASS: unexercised
  cases stay unverified while independent work continues.

## Proactive thermo-nuclear quality

For ticket implementation, PR revisions/shepherding, E2E generation, project planning, PR reviews
and sanity checks, read `reference/code-quality.md` before planning or evaluating code. Apply its
bar during design, then review the complete in-scope change before initial publication and each
code revision. Record material decisions and finding dispositions in the existing plan or review
report. This local pass complements the post-PR `/check` cycle and both Cursor approvals in
`reference/review-loop.md`; it does not replace them.

## Red/green TDD

Behavior-changing implementation must use red/green TDD, because a test that never failed proves
nothing about the fix:

1. **Red:** Before editing production code, add the smallest behavior-level test or throwaway
   check and confirm it fails for the intended reason. Encode a user-reported failure directly.
2. **Green:** Make the minimum source change and rerun the exact red check until it passes.
3. **Refactor:** Clean up after green, then rerun the affected check.

Keep the test only if it meets the repository's test-value bar; otherwise remove the throwaway
check after verification. Documentation, metadata and
mechanical changes are exempt; behavior-preserving refactors use a characterization check that
passes before and after.

## Acceptance gate for publishing and revisions

**Bounded assessment and closeout** and **PR readiness versus rollout completion** in
`reference/sanity-check.md` are the canonical policy for baselines, locked oracles, evidence reuse,
blockers, repairs and stage. Required verification and current-head reviews block publication
and readiness. Project runbooks own helper syntax, not copies of this policy.

Bind final evidence to a settled state: finish code, generated output, formatting and mutating
hooks first, then commit (when authorized) or explicitly bind the uncommitted state without
claiming a committed head. Capture final evidence once the state is settled rather than
repeatedly while it changes; later changes invalidate affected evidence under the reuse policy,
and required checks are never skipped to avoid recapture.

Before creating a draft PR, list every acceptance criterion from the ticket and later decisions and
personally exercise each feasible one on the running surface where it is observable, including
named negative, scope and persistence cases. For stateful work, follow the same record through
edit, visible result, save, reload and reopen. Record the result and environment per criterion.
Tests, builds, demos, code reading and reviewer approvals support this pass; they do not replace it.
If a criterion fails or cannot be exercised, fix it or report the exact blocker and keep the work
local.

If a criterion stays unmet and the next credible remedy exceeds authorized architecture, scope,
spend or a stated constraint, pause that remedy and report a feasibility blocker: criterion and
source, failing evidence, fixes tried, why the next step is out of bounds and what remains unproven
(failed trials do not prove impossibility). Pause only that remedy and continue ordinary authorized
fixes. Offer: authorize the remedy, revise the criterion or constraint, or split/defer the work.
Unmet criteria stay FAIL/BLOCKED, never quietly narrowed or reported as complete. Record an
approved revision as a requirements change with its source, keep the original history, update
affected cases and re-exercise affected evidence; a decision is not passing verification.

After a PR revision, re-exercise the affected criteria and connected behavior the edit could
change, and reconcile the full criterion list against the current head before accepting a
revision, replying that feedback is addressed or marking ready. A green check or a previous
head's evidence is not enough for any of those. Repeat on staging when the change reaches it; staging
catches environment differences, not skipped pre-PR checks.

## PR descriptions

Write every new or updated PR body with `skill://pr-description`, as a fresh draft from the current
diff and verified results. It owns the writing contract, claim check and saved-body readback for
initial publication, revisions and readiness.

## Testing handoffs

Send a testing handoff in chat when the initial draft PR is published, after each published
revision, and when deployment evidence confirms the change reached staging, without waiting for
the review loop or a request. Authorized work and the agent's own verification continue.

For full ticket executions, `skill://brew-test` owns the guide's content, format, coverage and
verification. Prepare and verify it before the first draft-PR handoff and refresh the same page for
revisions, completion/blockers and staging. Read-only commands inspect an existing guide and
create one only on request.

One concise, head-specific handoff: **revision and environment; acceptance result and evidence
level (self-verified or independent); oracle changes, if any; PR state/link; guide link and first
action; next action or blocker**. Tenant/role, prepared records, numbered journeys and backend-only
limits live in the guide. Use only real URLs and confirmed deployments; a build does not prove
deployment and an unreachable runtime is not ready. For revisions, name the changed journeys and
reuse the still-applicable guide. Lead with the original user journey exercised and the preserved control, bound to
revision and environment; test counts are supporting detail. Keep evidence levels distinct: source
tests, simulated transitions, real saved results and live generation each prove only their own level.

Guide walkthroughs share the acceptance pass under **Walk the testing guide** in
`reference/sanity-check.md`. Confirm deployment provenance before the staging handoff. The PR body
stays short per `skill://pr-description`; link longer instructions only when reviewers can access them.
Handoffs add no deployment authority or indefinite monitoring.

## Wait for CI after publication

Authorized ticket execution, PR revisions and shepherding own current-head CI through completion
after initial PR publication and every subsequent push. Do not stop at "pushed", "checks running"
or reviewer approval, and do not wait for the user to request monitoring. Send the immediate
testing handoff as usual, then continue the work.

- Record the published head SHA and discover its applicable CI workflows and required checks from
  repository configuration and fresh host metadata. Wait for applicable CI to finish, including
  queued/in-progress checks; no checks reported yet is not proof of success.
  Allow for registration delays: wait at the normal monitoring interval and recheck fresh
  head/run metadata before diagnosing missing checks. A short registration delay is not a blocker.
- Use the host's blocking watcher or supported completion notifications at a reasonable interval,
  not a busy loop. Reuse **GitHub CI waiting** in `reference/tool-recipes.md`. Work on independent
  authorized tasks while CI runs, then consume its result before the completion handoff.
- Inspect failed jobs and logs. Fix and verify in-scope causes within existing authorization,
  push, and wait again for the new head. Do not blindly rerun failures, weaken checks or bypass
  required CI. Report unrelated/infrastructure failures with evidence; they do not authorize
  broader repairs or make required checks pass.
- Re-read the PR head and checks after the wait and immediately before readiness/completion.
  A changed head invalidates the old CI binding. Required checks must pass; cancelled, missing,
  skipped or neutral results satisfy a requirement only when the repository's rules allow them.
  Record non-required failures separately rather than calling all CI green.
- Ordinary pending CI is ongoing work, not a handoff blocker. A watcher/tool timeout does not
  mean CI timed out: retrieve fresh head/run state and resume watching, using a supported
  background wait or completion notification when needed. Reattach to a still-running watcher
  rather than starting duplicates. Do not rerun CI jobs merely to resume observation.
- Report a blocker only when access, required manual action, repeated infrastructure failure
  or a persistent inability to observe CI prevents further progress after those recovery steps.
  Include the exact head, check/run links, observed states and recovery attempts. Never treat
  a timeout as success or leave a required check pending while claiming readiness.

This is a publication gate, not another acceptance/review round or deployment watcher. It does
not reset Cursor's two-round cap, authorize merging/deployment or start monitoring for read-only
status/review/sanity commands. Explicit user stop/wait limits still apply.

## Scope and authorization

`execute <ticket>` authorizes implementation once the **Pre-work Socratic checkpoint** closes.
After that, proceed without further approval rounds; ask again only for unresolved requirements,
material changes to the agreement, or sensitive actions not yet authorized.

Follow the harness's tool and delegation rules, inline first. Native task subagents are not Foreman
workers; keep an assigned worker's worktree/session. Give delegates narrow ownership, the symbols
already inspected and the open acceptance cases, and ask for a short evidence handoff. In long
sessions, keep a compact record of what is verified and what remains.

Tracker updates are never automatic. Publishing needs authorization once, not repeated confirmation.
Create draft PRs, keep the author assigned and use the assigned publication mechanism unless told
otherwise. Reviewer identities/triggers are repository-local: report a missing optional reviewer
and proceed, without borrowing another project's configuration, and distinguish a posted trigger,
a recorded request and a completed review. Never merge. `reference/review-loop.md` grants its exact
review comments, fixes, pushes, replies and the draft-to-ready transition after its gate passes.
That transition is automatic, not another permission checkpoint: finish shepherding by marking
the PR ready for review and verifying its draft flag is false, unless the user explicitly asked
to keep it draft. Pending or failed gates keep it draft; never merge.
