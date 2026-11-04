# Skills

Brian Keefe's agent skills and development workflows. This repository is the source of truth; machine configuration and personal project guidance remain in [dotfiles](https://github.com/briankeefe/dotfiles).

## Install in Oh My Pi

```sh
git clone https://github.com/briankeefe/skills.git ~/code/skills
sh ~/code/skills/install.sh
```

The installer symlinks each `skills/<name>` directory into `~/.omp/agent/skills`. It checks all collisions first and refuses to replace existing directories or unrelated links. Preserve local edits and move conflicting skills aside before retrying. Other installed skills are untouched. Set `SKILLS_DIR` to install into another directory.

Update the checkout, not copies in the installation directory:

```sh
git -C ~/code/skills pull --ff-only
sh ~/code/skills/install.sh
```

Restart OMP or reload skills after installing or updating. Edit files in this checkout; installed symlinks immediately point to the same source. Other agent runtimes can use the Markdown instructions but may need adaptation for OMP-specific `skill://` references and tools.

## Included skills

- **execute:** Ticket implementation, PR review/revision, acceptance verification, testing handoffs, releases and operations. Mutating workflows begin with a concrete before/after and architecture flowchart on a local Brew page every time, discussed together with one agreement instead of repeated confirmations. Keeps original and expanded scope in the task plan, continues when no user action is needed, and names where changes happened. Substantive explanations, plans and reports default to local Brew pages regardless of length; chat carries the takeaway, link and decision needed. Built-in and explicit sanity checks follow the rendered testing guide through the UI. Includes [verified tool recipes](skills/execute/reference/tool-recipes.md) and a read-only, execution/revision-specific CodePipeline waiter.
- **execute-update:** `/skill:execute-update <change>` updates execute locally in its canonical source, verifies it, then commits and pushes only the scoped change to the owning personal repos. Keeps the pipeline in skills and personal configuration/shims in dotfiles.
- **provision-account:** Create and invite tenant-scoped accounts using project runbooks; verify identity membership and application roles without exposing temporary passwords.
- **brian-voice:** Brian's writing style.
- **pr-description:** Fresh, stateless PR drafting from the current diff and observed verification. First-person reviewer notes, compact testing and preserved material risks, without internal process logs. Includes synthetic trial examples, a claim/audience check and saved-body readback; applies to create, revisions and readiness, not a CLI/CI enforcement gate.
- **brew-clear:** Clear Brew articles and diagrams; uses `brian-voice` and the content repository's `AUTHORING.md`.
- **brew-update:** `/skill:brew-update <page or change>` edits and previews locally before committing and pushing to the owning personal repos. Meaningful shared Brew changes also require an app PR; ordinary page edits do not. Hosted publication remains explicit and separate.
- **brew-test:** Concise local UI testing walkthroughs, not acceptance inventories. Handoff requires a measured 900-word maximum (unless the user approves another budget), a repetition review and a private map covering every sourced criterion. Actions and visual checks render separately; shared checkboxes save personal progress, not acceptance evidence. Coverage/budget conflicts block delivery instead of silently expanding the guide or dropping cases. No reader-facing code or environment setup. Runs at full `execute` handoffs, after published revisions, or on request; verifies written journeys on the real app.
- **square-image:** Center-crop and resize square images.
- **standup:** Ticket-by-ticket standup briefing with Linear titles/statuses, recent outcomes, today's work, and genuine blockers. Includes a reference layout with collapsed planning-only work and engineering follow-up, plus a bundled read-only Git/GitHub/Linear collector. CI and routine review follow-up are not standup blockers.
- **pointing:** Historically calibrated, agent-assisted ticket estimates; two-sentence summaries, independent guesses, one-at-a-time comparison and durable saved answers. Start with `/skill:pointing kubera <ticket IDs or URLs>`; Kubera's scale and examples live in local project guidance.

Repository-specific accounts, environments, reviewer actions and tooling must be resolved from the target project's instructions. No credentials or private repository history are included here.

Execute approach pages teach the task's domain model and normal behavior before the bug.
They carry one worked example through before and after, then explain the engineering fix.
Size follows understanding rather than a word target; remove repetition before essential context.
The existing local Brew handoff and single agreement checkpoint remain unchanged.

The optional feature-video workflow in `execute` requires a separately installed `playwright-demo-kit` checkout with its recording-lock wrapper; it is not bundled here. `ponytail`, when installed separately, supplements the review workflow's minimum-complexity guidance.

`execute` applies a shared [thermo-nuclear quality standard](skills/execute/reference/code-quality.md)
during planning, implementation, full-change pre-publication review, PR review and sanity checks.
It prioritizes structural simplification, canonical ownership, explicit contracts and cohesive
files over cosmetic cleanup or extra abstractions. These local passes never replace the post-PR
`/check` cycle, either required Cursor approval, or the existing two-round cap.

Sanity checks verify sourced requirements and changed behavior, reusing applicable evidence and
running only missing targeted checks. Broad backend/frontend suites and other CI sweeps are not
default sanity work; CI status and publication/merge gates remain separate. Unrelated or flaky
suite failures do not become sanity blockers, while affected-path regressions and missing required
behavioral evidence still do.

## Reuse instead of rediscovering

The installed skill entry points route agents to version-scoped CLI/JSON recipes and explicit
managed-browser selection. Reuse recipes, not stale issue/review/auth/deployment results.
Project-specific startup, database, tenant and account facts remain in local project guidance.

For standup, set `CODE_ROOT` to a repository or the directory containing your checkouts:

```sh
python3 ~/.omp/agent/skills/standup/scripts/collect.py --root "$CODE_ROOT"
```

The collector emits timestamped evidence separately from untimed worktree/assignment context,
and reports unavailable or truncated sources. Use its records with session/memory evidence;
it does not write issues or decide what work is complete. Python 3.9+ and the existing Git,
GitHub CLI and optionally Linear CLI are used; no new Python dependencies are needed.

The [CodePipeline monitoring recipe](skills/execute/reference/ops-facts.md#aws-codepipeline-one-execution-one-revision)
uses the bundled waiter with an explicit pipeline, execution, revision, AWS profile and region.
It reports terminal failure or timeout without starting/retrying deployments.

PR bodies use the shared [PR-description contract](skills/pr-description/SKILL.md), also linked
from `brian-voice` for callers outside execute. Try `/skill:pr-description` with a current diff,
purpose and verified results to draft without publishing. The [offline trial cases](skills/pr-description/reference/examples.md)
cover a version bump, connected changes, a data repair and deliberately misleading drafts.
Candidate examples need Brian's style feedback; they are not labeled approved. The next five
authorized PRs track first-draft acceptance in the existing local workflow record, not this repo.


## Check the workflows

```sh
python3 tests/install.py
python3 tests/standup.py
python3 tests/pipeline.py
```
