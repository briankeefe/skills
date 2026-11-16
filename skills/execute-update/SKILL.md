---
name: execute-update
description: Update the execute workflow or its docs locally, verify the requested change, then commit and push to Brian's owning personal repositories. Use for execute framework, pipeline, instructions, or command-shim maintenance, not for executing a ticket.
---

# Update execute

Invoke with `/skill:execute-update <change>`. A concrete invocation authorizes the scoped local
update, verification, commit and push to the owning personal repositories. Discussion or a request
for recommendations alone is not publication authorization. Honor explicit local-only limits.

## Change the source locally first

1. Read `skill://execute` and the relevant references. Resolve installed symlinks to their tracked
   source before editing. Inspect the branch, remotes and existing changes; preserve unrelated work.
2. Keep ownership explicit: `briankeefe/skills` owns the execute pipeline and references. Brian's
   dotfiles owns machine configuration, personal authorization/runbooks and the command shim.
   Resolve the current checkouts and tracked destinations from local guidance and repository state;
   do not duplicate the pipeline into dotfiles or edit only an installed/generated copy.
3. Apply the requested change locally in the canonical owner. Update affected dispatch entries,
   references and README usage together. Change dotfiles only when its owned behavior must change.
   Preserve existing scope, authorization, acceptance and review limits unless explicitly changed.
4. Verify before committing: trace affected routes and instructions for conflicts, check links and
   command syntax, and run the existing relevant checks. For executable changes, exercise the changed
   path with the repository's red/green and runtime requirements. Documentation-only changes need
   source/contract review and relevant loading checks, not a fabricated runtime claim.

## Preserve and publish the verified change

- Commit only the requested diff in each affected personal repository, never unrelated dirty files
  or all staged changes blindly. Verify the remote and branch before pushing; do not force-push,
  merge, reset, or switch away from someone else's active work.
- Push the commits to the verified personal remotes. If several repos changed, report each result
  separately; a successful push in one does not complete a failed publication in another.
- Install new skill entry points with the existing installer and verify the installed source.
  Symlinked existing skills need no copied replacement. Note any runtime reload needed.
- Return the changed behavior, commit/branch links, checks actually run and any exact blocker.
  Do not claim that a prose instruction enforces runtime behavior unless it was exercised.

This is maintenance of execute, not an instruction to run a ticket, open an app PR, update Linear,
merge, deploy or publish a Brew page. Use `skill://brew-update` when the change also affects Brew.
