---
name: execute
description: Project-neutral development workflows for `execute <command>`: tickets, PR summaries/reviews/updates, E2E tests, sanity checks, project planning, documentation, release membership and local reproduction. Also use for questions about whether an issue/PR/commit is in a release, how to reproduce a change locally, or project operations. Discover the repository, issue provider and tools from current context rather than assuming an organization or stack.
---

# Execute Toolkit

Use the matching workflow with active harness/repository rules and the user's current authorization.

## Dispatch

Match the longest named command prefix below before interpreting a ticket. Pass remaining
arguments unchanged. Empty input or `help` shows this table without starting work.
A bare PR URL routes to `pr-review.md`; a bare issue URL, provider-recognized ID (for example
`ENG-2612`, not a required prefix), or resolvable ticket name routes to `ticket.md`.
Resolve names using the configured tracker; ambiguous names require clarification before
work starts. Unknown commands or unrecognized URLs show help rather than inventing a ticket.
An explicit command wins: `local-repro <PR_URL>` reproduces, it does not post a review.

| Invocation | Reference doc | Purpose |
|---|---|---|
| `execute help` | (this file) | Show commands |
| `execute <ticket-ID/name/issue-URL>` | `reference/ticket.md` | Fetch, plan, implement, verify, review, PR |
| `execute pr summary [scope]` | `reference/pr-summary.md` | Summarize your open PRs |
| `execute pr review <PR_URL>` | `reference/pr-review.md` | Review with Conventional Comments |
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
| `execute local-repro <ticket/PR>` | `reference/local-repro.md` | Bring up the relevant local stack and verify |
| `execute ops [question]` | `reference/ops-facts.md` | Consult project-local operational guidance |

Reference paths resolve as `skill://execute/reference/<doc>`.

## Pre-work Socratic checkpoint

Before starting an implementation or other mutating execute workflow, explain the task-specific
before, after and architecture. This **socraticQuiz** is a discussion to understand the work,
not three rounds of "is this ok?" Read-only commands do not require this checkpoint.

Only do the minimum read-only discovery needed to ground the discussion: read the request,
ticket, relevant code and existing evidence. Except for creating and locally previewing the
explanation page below, do not edit files, delegate implementation, run tests or setup, start
services, change data, or publish anything before the checkpoint closes. Do not ask the user
to supply facts available in the repository.

Present these together so the user can understand and discuss the complete change:

1. **Before.** What happens today, where the behavior lives, and one concrete example of the
   evidenced problem. Separate observed facts from assumptions; define unfamiliar terms.
2. **After.** The intended user-visible behavior, what stays unchanged, and how success will
   be recognized. Use the same example to make the difference clear.
3. **Flow.** Show a readable flowchart of the current and/or proposed end-to-end architecture,
   labeled clearly as current or proposed. Include the important decision/failure branches,
   canonical components to reuse and affected boundaries/callers. Explain the simplest viable
   approach, material tradeoffs and verification, not an exhaustive code tour.

Ask about unresolved requirements or material tradeoffs, not for a confirmation after each
topic. Answer questions and incorporate corrections. If there is no unresolved decision,
ask once for agreement to the complete approach before implementation. Silence, a preselected
option or the initial execute request is not agreement. Explicit agreement after the discussion
closes the checkpoint; do not ask again for topics already agreed.

Keep chat explanations to about five sentences. When more is needed, create or update a concise
local Brew explanation page using `skill://brew-clear`, with the before/after and flowchart;
send the takeaway, page link and any decision needed in chat. Creating and locally previewing
this explanation is permitted during discovery, but does not authorize app setup, tests, data
changes, implementation or publication. Keep it separate from the UI-only testing guide.

Record the agreed before, after and architecture in the existing task plan. Reuse an existing
agreement for the same scope, including on resume; reopen only a material change. An explicit
request to skip the quiz waives only this checkpoint, not authorization or safety requirements.

## Working agreement and handoffs

- Keep **Must deliver**, **Must preserve** and **Not included** in the existing task plan.
  Source them from the request, ticket/comments and later decisions. Carry the full original
  and expanded scope through implementation and sanity checking. An approved change to one
  expectation does not waive other requirements. Show agreement changes, not repeated copies.
- If no user action is needed, continue authorized work. A progress update is not a request
  for "continue", and an intermediate milestone is not a stopping point. Before yielding,
  identify completion, the exact user decision needed, or the external prerequisite that
  blocks all remaining authorized work. Continue independent work when only one part is blocked.
- When a decision is needed, state the concrete question, recommendation and consequence.
  Ask only after exhausting relevant available evidence. Do not return "nothing needed"
  while actionable work remains. These rules do not authorize repairs in a read-only workflow;
  completing the requested assessment is completion even when its verdict is FAIL.
- When reporting applied changes, name where they happened: local worktree, isolated data
  branch, staging or production. Do not say only "applied". This is clearer reporting, not
  another approval gate or permission to cross an existing authorization boundary.
- Do not add progress estimates, a progress dashboard or periodic status messages. Give
  decision/completion handoffs and answer requested status questions using observed facts.

## Discover once, reuse

- Read applicable repository instructions and the relevant project docs before editing.
  Resolve repository/host from an explicit URL, assigned worktree, remotes and ticket links.
  Do not silently substitute the current repo for a different repo named by a URL.
- Resolve the issue provider/workspace and ID format from the URL and local configuration.
  Reuse verified local recipes and `skill://execute/reference/tool-recipes.md` for structured
  issue/PR reads, Linear 2.6.0 and managed OMP browsers. Check versions once; inspect targeted
  `--help` only for an unfamiliar operation, version drift or a contradictory result.
  Fresh authentication, issue/review state and deployment evidence still require fresh reads.
  Never assume authentication, flags, JSON fields or a database integration exists.
- Reuse the assigned branch/worktree. Otherwise discover the default base from repository
  metadata and any documented project branch; never assume `master`, `main` or a release name.
  Verify remotes before network writes. If release timing changes the strategy and is unstated,
  ask whether this targets the normal next release or something faster.
- Derive runtime/package manager from repo instructions, manifests, lockfiles and pinned versions.
  Reuse existing install, dev, test, lint and CI commands; do not install a runner merely to fit
  this toolkit. Resolve documentation locations from the repository, not a global personal path.
- Missing context: exhaust repo/tool evidence, then ask one focused question. Report unavailable
  credentials or services without guessing values or exposing secrets.

## Evidence before edge-case escalation

Before raising a speculative domain/edge-case question, adding defensive logic for it, or
promoting it into a required acceptance case:

- Check the requirements, reported incidents, relevant code/tests and applicable existing
  evidence first. A user-reported failure is evidence; do not reproduce it merely to confirm
  the report or demand a new database example for an already-established requirement.
- If occurrence is still uncertain, look for a real example using existing project tools and
  a narrowly scoped, authorized read-only data search when needed. Bound the environment,
  tenant, date range, predicates and returned rows as appropriate; prefer counts and minimal
  fields. Do not perform broad production scans, mutate data, generate fixtures or make paid
  calls just to give a hypothetical substance. This rule grants no new data access.
- If found, bring a sanitized example, the observed count/frequency with its search scope or
  denominator, and the concrete impact. Do not expose credentials, patient/customer data or
  private record details in chat, public PRs or documentation.
- If not found, record **not observed in the searched scope**, not **impossible**. Without a
  sourced requirement or concrete material correctness, security or data-integrity concern,
  skip speculative defensive code and domain escalation; do not expand the acceptance baseline.
- Missing access, incomplete searches and unavailable data mean **unverified**, not absent.
  Name that limit and continue independent work; ask only the focused question or prerequisite
  needed when an in-scope decision is genuinely blocked.
- Explicit requirements and concrete correctness/security/data-integrity evidence remain
  actionable without an observed production occurrence. Preserve required validation and
  acceptance checks; never use an empty search to dismiss a reported bug or a material risk.

## Proactive thermo-nuclear quality

For ticket implementation, PR revisions/shepherding, E2E code generation, project planning,
PR reviews and sanity checks, read `skill://execute/reference/code-quality.md` before planning
or evaluating code. Apply its structural quality bar during design and implementation, then
review the complete in-scope change before initial publication and each code revision.
Record material design decisions and finding dispositions in the existing plan/review report,
not a separate checklist for every trivial edit. Read-only workflows remain read-only.

This proactive pass never replaces the post-PR `/check` cycle or either required Cursor approval
in `reference/review-loop.md`. Keep its existing round cap, authorization and acceptance gates.

## Red/green TDD

Every behavior-changing implementation workflow MUST use red/green TDD:

1. **Red:** Before editing production code, add or update the smallest behavior-level test or
   throwaway executable check. Run it against the current code and verify it fails for the intended
   reason. A user-reported failure is ground truth; encode it without repeating the manual
   reproduction merely to confirm it.
2. **Green:** Make the minimum source change, then rerun the exact red check and verify it passes.
3. **Refactor:** Clean up only after green, then rerun the affected check.

Keep the regression test only when it meets the repository's test-value bar; otherwise remove the
throwaway check after verification. Documentation-only, metadata-only and purely mechanical changes
are exempt. Behavior-preserving refactors use a passing characterization check before and after
instead of fabricating a failure.

For retrospective workflow comparisons, use OMP session usage records to track uncached input
tokens per single-ticket session alongside staging-discovered defects and user corrections. Keep
multi-ticket sessions separate; cached reads and raw transcript size are not token-cost estimates.

## Acceptance gate for publishing and revisions

Apply **Bounded assessment and closeout** in `skill://execute/reference/sanity-check.md` to
implementation, revisions and readiness: criterion-local prerequisites, a frozen required-case
baseline, applicable evidence reuse and two persisted acceptance repair rounds. Required
verification still blocks publication/readiness; reaching the limit means an honest blocker
handoff, not a waiver, another reviewer or an automatic restart. Keep optional findings outside
the required case table; never silently remove existing required cases.

For data-repair PRs, apply **PR readiness versus rollout completion** in that reference. Demonstrate
the complete repair against the A/C on representative isolated data, with reviewed selection and
operator/recovery steps. Production execution or its approval is a separate rollout prerequisite,
not a reason by itself to fail PR sanity or require live mutations before publication.

Before creating a draft PR, enumerate every acceptance criterion from the ticket and later decisions.
Personally exercise each feasible criterion on the running surface where its behavior is observable;
include the named negative, scope and persistence cases rather than treating a happy-path video as
coverage. For stateful work, check the same record through edit, visible result, save, reload and
reopen where applicable. Record what happened and the environment for each criterion. Automated
tests, builds, demos, code inspection and reviewer approvals supplement but never replace this pass.
If any criterion fails or cannot be exercised, do not publish the draft as complete: fix it or
report the exact blocker and keep the work local until verification is possible.

If evidence shows a criterion remains unmet within the authorized approach and the next credible
remedy exceeds authorized architecture, scope, spend or a stated constraint, pause only that remedy
and report a feasibility blocker: the criterion and source, failing evidence, attempted in-scope
fixes and why further work is out of bounds. State what remains unproven; failed trials alone do
not prove impossibility. Offer the owner concrete choices: authorize the remedy, explicitly revise
the criterion or constraint, or split/defer the work. Keep unmet criteria FAIL/BLOCKED; do not
silently narrow acceptance or mark partial work complete. Record an approved revision and its
source as a requirements change, preserve the original requirement/decision history, update the
applicable cases and scope boundaries, and invalidate/re-exercise affected evidence. A decision
does not substitute for passing verification; ordinary authorized fixes remain actionable within
the persisted closeout limit. At exhaustion, report the blockers and request a bounded owner
decision rather than starting another autonomous fix/review cycle.

After PR revisions, personally re-exercise affected criteria and any connected behavior the edits
could change; reconcile the full criterion list against the current head before claiming feedback
addressed or marking the PR ready. Do not accept a revision, post a fix reply, or transition a PR
based only on a green check or a previous head's evidence. Repeat on staging when the change reaches
it; staging catches environment differences, not skipped pre-PR acceptance checks.

## PR descriptions

For every new or updated PR description, read `skill://brian-voice` and write in Brian's voice:
plain, direct and conversational. Use short sentences and contractions, without corporate phrasing,
forced slang or em dashes. Follow required repository templates, but omit optional empty sections.

- Lead with what changed and why the reviewer should care. Default to a short paragraph or 1–3
  bullets, then a compact testing section and the ticket link. Add detail only when it helps review
  behavior, scope, a non-obvious decision or a material risk. Include UI evidence only when useful.
- Check every claim against the current base-to-head diff and observed verification before initial
  publication, after revisions and before marking ready. Remove stale claims when scope changes.
  Distinguish checks actually run from suggested steps; never imply unverified behavior, staging
  deployment or broader coverage. Keep review-relevant limitations even when shortening.
- Exclude agent/process narration, review-round history, internal acceptance bookkeeping, raw logs,
  exhaustive file lists, repeated ticket text and unrelated caveats. Link reviewer-accessible details
  when needed rather than copying them into the body.

Final pass: is it accurate for this head, does every sentence help the reviewer, and does it sound
like Brian? Cut anything that fails those checks; brevity must not hide a risk or verification gap.

## Testing handoffs

Send a testing handoff in chat as soon as the initial draft PR is published, after each published
PR revision, and when deployment evidence confirms the change has reached staging. Do not wait
for the review loop to finish or for the user to ask. This notification does not pause authorized
work or replace the agent's own acceptance verification.

For full ticket executions, use `skill://brew-test` after runtime verification to create or
refresh a local Brew testing page for the initial draft-PR handoff and final completion or
blocker handoff. Refresh the same page after published revisions and confirmed staging
deployment during the active workflow. The reader-facing page contains only browser UI actions
paired with explicit visual checks, plus minimal access/status context. No code, commands,
scripts, developer tools, environment setup or administrative mutation instructions. Ordinary
authorized UI edits/saves remain testable within `brew-test`'s safety limits. The agent handles
authorized setup separately; unavailable prerequisites stay blocked. Follow `brew-test`'s local-only and
rendered-page verification rules; this adds no publication/deployment authority or acceptance waiver.
The ticket's existing acceptance and quality checks, scope reconciliation and `brew-test`'s
verification form its built-in sanity check before initial publication and final completion.
Apply **Walk the testing guide** in `reference/sanity-check.md` as part of that same pass,
not a separate read-only invocation or duplicate walkthrough. Refresh the guide and re-walk
affected steps after revisions; do not defer checking instructions until the user tries them.
Read-only commands do not create testing pages unless requested; they inspect an existing guide
when applicable. Keep chat handoffs short: link the verified guide, give its first action and any
decision/blocker. A localhost guide is not a substitute for a reviewer-accessible PR checklist.

Each handoff MUST include:

- The PR link and the actual preview/local URL for PR testing, or the staging URL for staging
  testing. Identify the environment and current head or deployed revision; never invent a URL or
  imply branch membership proves deployment. If no test environment is reachable, name the blocker
  and the exact known startup/access steps instead of claiming it is ready for testing.
- Required tenant/account role, test records, setup and feature gates, without exposing credentials.
- A verified guide/checklist covering every acceptance criterion with concrete numbered actions
  and visible results, including relevant negative, scope and save/reload/reopen cases. In chat,
  give its link and first action rather than pasting the whole checklist. For revisions, name
  what changed and link the refreshed affected steps plus the still-applicable full checklist.
- What the agent actually verified in that environment and any remaining gaps or access/data
  blockers. Distinguish suggested user checks from checks already performed.

Keep concise verification results and reviewer testing steps in the PR's testing section. If the
full checklist or environment setup is long, link a current reviewer-accessible record there rather
than duplicating it; keep every acceptance criterion and prerequisite in that record. Refresh after
revisions and link from chat. Give the first concrete action in chat, not only a PR-body link.
Confirm staging deployment through project-local operational evidence, then repeat the acceptance
gate and send the staging handoff; do not claim staging verification from a build.
This rule adds no deployment authorization or indefinite background monitoring.

## Scope and authorization

`execute <ticket>` authorizes implementation after the **Pre-work Socratic checkpoint** closes.
That checkpoint replaces the former proceed-without-plan-approval default. Once the approach
is agreed, proceed without repeated approval rounds; ask again only for unresolved requirements,
material changes to the agreement, or sensitive actions not already authorized.

Use active harness tool/delegation rules, inline first. Native task subagents are not independent
Foreman workers; retain an assigned worker's worktree/session rather than creating a replacement.

When delegating, give each agent narrow ownership, already-inspected symbols and open acceptance
cases; return a short evidence handoff instead of duplicating broad reads or full transcripts.
In long sessions, keep a compact record of what was verified and what remains, rather than
reloading prior tool output.

Read-only commands do not start implementation or publish. Tracker updates are never automatic.
Publishing needs authorization, not repeated confirmation when already granted. Create draft PRs,
keep the author assigned, and follow the assigned publication mechanism unless explicitly overridden.
Reviewer identities/triggers are repository-local: report missing optional reviewers and proceed
with authorized publication, never borrow another project's configuration. Distinguish a posted
trigger, recorded request and completed review. Do not merge. The standing authorization in
`reference/review-loop.md` permits its exact review comments, fixes, pushes, replies and final
draft-to-ready transition only after both required approvals.
