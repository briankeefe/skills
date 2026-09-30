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

- **execute:** Ticket implementation, PR review/revision, acceptance verification, testing handoffs, releases and operations.
- **brian-voice:** Brian's writing style.
- **brew-clear:** Clear Brew articles and diagrams; uses `brian-voice` and the content repository's `AUTHORING.md`.
- **square-image:** Center-crop and resize square images.
- **standup:** Evidence-based standup preparation.

Repository-specific accounts, environments, reviewer actions and tooling must be resolved from the target project's instructions. No credentials or private repository history are included here.

The optional feature-video workflow in `execute` requires a separately installed `playwright-demo-kit` checkout with its recording-lock wrapper; it is not bundled here. `ponytail`, when installed separately, supplements the review workflow's minimum-complexity guidance.

## Check the installer

```sh
python3 tests/install.py
```
