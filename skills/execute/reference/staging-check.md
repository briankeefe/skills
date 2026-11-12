# Staging Check

Use for `execute staging-check <ticket/PR/sha>` and natural-language questions such as
“has this commit landed on staging yet?” Apply `skill://execute`. This is a read-only,
one-shot deployment check, not a release-branch membership check or a request to deploy.

## Resolve the change and environment

1. Resolve the repository and staging environment from the request, assigned worktree and
   project-local deployment guidance. Reuse `tool-recipes.md` for provider reads. Keep account,
   profile, region, pipeline and environment URLs in project-local instructions, not this skill.
2. Resolve the requested full commit SHA. For a PR, retrieve its current merge state and merge
   commit using `release-check.md`; do not confuse its pre-merge head with a squash merge SHA.
   For a ticket, include every linked PR relevant to the requested scope. Report unmerged work
   separately; a merged PR alone is not deployment evidence.
3. Identify which deployment stages/artifacts serve the changed surface. If frontend and API
   deploy separately, check each applicable component. Do not infer coverage from an unrelated
   successful stage or repository.

## Match deployment evidence to the change

Retrieve fresh execution status and source/artifact revisions from the actual staging deployment
provider. Use the existing CodePipeline recipe in `ops-facts.md` where applicable. Check the
requested revision against the deployed source revision, not just the staging source branch.

- An execution may deploy the requested commit **or a later descendant containing it**. Fetch
  the necessary objects and use `git merge-base --is-ancestor <requested-sha> <execution-sha>`.
  Exit 0 proves exact ancestry, 1 means not reachable, and other exits or incomplete history mean
  unknown. Inspect known reverts or cherry-picks using `release-check.md`; ancestry alone does
  not prove the feature remains enabled or equivalent changes are absent.
- For CodePipeline, select an execution whose source revision contains the requested change,
  then inspect that execution's status and relevant action results. If waiting was requested,
  pass **the execution's full source revision**, not an older ancestor, to the bundled waiter.
  Preserve execution/revision identity throughout diagnostics. Do not stop at the first exact
  SHA miss or substitute an unrelated latest successful execution.
- A successful build, merged PR, source-branch membership, queued execution or running deploy
  is not a completed staging deployment. Require the project's successful deployment stages
  and artifact/source provenance for every applicable component.
- Distinguish **deployed at least once** from **currently on staging**. Inspect subsequent
  deployments, rollbacks and any available runtime revision/artifact identity. An old successful
  execution does not prove the current environment still contains the change. Concurrent,
  partial or failed deployments can leave mixed state; report that limit rather than guessing.
- Use the project's documented deployed-revision check when available. A healthy page or an
  endpoint without revision metadata cannot identify a commit. If only deployment provenance
  is available, label it as such; never invent runtime SHA proof.
- Paginate or explicitly bound execution history. No match in a truncated history, expired
  credentials, missing objects or unavailable deployment metadata means **UNKNOWN**, not absence.
  A failed/superseded execution is not proof the change never reached staging through another one.

## Verdict and boundaries

Return the requested SHA, environment, deployment SHA, execution ID/link, observed status and
check time, using one of these verdicts with the deciding evidence:

- **DEPLOYED:** Successful applicable deployment provenance contains the change. Say whether
  current runtime identity was confirmed or only a historical deployment was established.
- **DEPLOYING:** An identified queued/running execution contains the change; completion unproven.
- **NOT DEPLOYED:** The verified current deployed revision excludes the change, with no unresolved
  equivalence/history gap. Mention a failed attempt or unmerged PR separately when relevant.
- **UNKNOWN:** Evidence cannot establish inclusion/current state; name the exact missing proof.

Keep the response concise. Deployment status is not behavioral acceptance. During an active ticket
workflow, confirmed staging arrival triggers execute's existing staging acceptance and testing
handoff; a standalone status question does not start application tests, setup or repairs.

Do not merge, push, retry, dispatch, deploy, change tracker state or create a watcher/schedule.
“Yet?” requests one fresh check, not indefinite monitoring. If the user explicitly requests a
wait or notification, reuse the bounded execution-specific waiter or authorized scheduling tools,
carry the repository/environment/requested SHA and provenance rules into that task, and stop
once its requested condition or failure boundary is reached.
