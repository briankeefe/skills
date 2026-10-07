# Project Operations

Use for `execute ops [question]` or project-specific logging, telemetry, deployment and version
questions. Apply `skill://execute`; this is a discovery workflow, not a universal deployment policy.

1. Identify the repository and environment from the question and current context. Read its
   operational docs, CI/deployment workflows, runtime configuration and logging helpers.
   Organization-specific architecture, provider keys, branch names, rollout rules and version-bump
   policies belong in project-local docs, not this shared toolkit. If absent, state what is unknown.
2. For logging, trace the actual client/server mutation and existing instrumentation before adding
   events. Avoid duplicate event counts. Distinguish public ingestion identifiers from privileged
   query/admin credentials using the provider's current documentation; never print or commit keys.
   Use the approved secret store. Recommend rotation for exposed credentials.
3. For deployment/version questions, determine the real artifact type (native build, bundle,
   container, etc.), compatibility requirements, target environment and release workflow. Do not
   infer deployment from branch membership or apply another project's version rules.
4. Inspect read-only deployment status with the configured provider tooling after checking its
   installed capabilities. Correlate the successful deployment's artifact/commit with the actual
   environment; a green build alone is not proof of rollout or current live state.
   When this confirms a tracked change has reached staging, apply `skill://execute`'s acceptance
   gate and immediately send its staging testing handoff with the staging URL, prerequisites,
   concrete steps and expected results, and observed verification or blockers.
5. Answer with source paths and observed artifact/commit/status. An operations question does not
   authorize a push, workflow dispatch, release, secret change or production mutation. Present any
   proposed action and its target/risk for explicit approval before acting.

## AWS CodePipeline: one execution, one revision

Use only when the project's deployment provider is CodePipeline. Resolve the profile, region,
pipeline and expected full source revision from local instructions and the requested change.
There is no `aws codepipeline wait` command. Do not substitute the latest successful execution
for the one containing the requested revision.

```bash
aws codepipeline list-pipeline-executions --pipeline-name "$PIPELINE" --profile "$AWS_PROFILE" --region "$AWS_REGION" --output json --no-cli-pager --query 'pipelineExecutionSummaries[].{id:pipelineExecutionId,status:status,revisions:sourceRevisions[].revisionId}'
```

Select `EXECUTION_ID` by the expected revision, then use the bundled read-only waiter rather
than constructing another polling loop. In OMP the installed path is:

```bash
python3 ~/.omp/agent/skills/execute/scripts/wait-codepipeline.py \
  --pipeline "$PIPELINE" --execution "$EXECUTION_ID" --revision "$EXPECTED_REVISION" \
  --profile "$AWS_PROFILE" --region "$AWS_REGION" --timeout 600
```

Other runtimes use the same `scripts/wait-codepipeline.py` beside this skill's `SKILL.md`.
The waiter validates execution/revision identity, emits status transitions and exits nonzero
on failure, stopped/superseded execution, unexpected state, credential/read error or timeout.
It never starts, retries, stops or deploys a pipeline. For a long wait, run that one process
as a finite background job and consume its completion, not repeated agent status calls.

For diagnostics, get action/build identifiers from **that execution**:

```bash
aws codepipeline list-action-executions --pipeline-name "$PIPELINE" --filter "pipelineExecutionId=$EXECUTION_ID" --profile "$AWS_PROFILE" --region "$AWS_REGION" --output json --no-cli-pager --query 'actionExecutionDetails[].{stage:stageName,action:actionName,provider:input.actionTypeId.provider,status:status,id:output.executionResult.externalExecutionId}'
aws codebuild batch-get-builds --ids "$BUILD_ID" --profile "$AWS_PROFILE" --region "$AWS_REGION" --output json --no-cli-pager --query 'builds[].{status:buildStatus,group:logs.groupName,stream:logs.streamName}'
```

Only pass identifiers from CodeBuild actions to `batch-get-builds`. Refresh expired SSO using
the project's documented login flow; never switch accounts/profiles silently or treat unrelated
GitHub deployment metadata as current rollout proof. A successful pipeline still needs the
project's actual runtime/deployed-revision and acceptance checks.
