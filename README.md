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

- **execute:** Ticket implementation, PR review/revision, acceptance verification, testing handoffs, releases and operations. Includes [verified tool recipes](skills/execute/reference/tool-recipes.md) and a read-only, execution/revision-specific CodePipeline waiter.
- **brian-voice:** Brian's writing style.
- **brew-clear:** Clear Brew articles and diagrams; uses `brian-voice` and the content repository's `AUTHORING.md`.
- **square-image:** Center-crop and resize square images.
- **standup:** Evidence-based standup preparation with a bundled read-only Git/GitHub/Linear collector.

Repository-specific accounts, environments, reviewer actions and tooling must be resolved from the target project's instructions. No credentials or private repository history are included here.

The optional feature-video workflow in `execute` requires a separately installed `playwright-demo-kit` checkout with its recording-lock wrapper; it is not bundled here. `ponytail`, when installed separately, supplements the review workflow's minimum-complexity guidance.

`execute` applies a shared [thermo-nuclear quality standard](skills/execute/reference/code-quality.md)
during planning, implementation, full-change pre-publication review, PR review and sanity checks.
It prioritizes structural simplification, canonical ownership, explicit contracts and cohesive
files over cosmetic cleanup or extra abstractions. These local passes never replace the post-PR
`/check` cycle, either required Cursor approval, or the existing two-round cap.

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


## Check the workflows

```sh
python3 tests/install.py
python3 tests/standup.py
python3 tests/pipeline.py
```
