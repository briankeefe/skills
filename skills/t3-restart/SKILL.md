---
name: t3-restart
description: Restart Brian's local T3 Code desktop or backend. Restart installed artifacts as-is, and route any source change or rebuild through the T3 upgrade workflow first.
---

# Restart local T3 Code

Read `~/.omp/agent/t3code-runtime.md` for the canonical service, app, and verification recipes. Confirm the target and current state first. Desktop relaunch and backend restart are separate actions; restart only the requested or affected surface. A backend restart can interrupt active turns, including your own.

- **Restart only:** Relaunch the already installed artifact. Do not pull, merge, rebuild, or swap artifacts. Verify the requested surface came back and the other surface was left alone when applicable.
- **Restart to pick up changes:** Use `skill://t3-upgrade` first. Make source changes in a separate worktree, merge into fork `main`, and build installable artifacts from clean canonical `main`. Do not restart into a feature-worktree or dirty build. Follow the upgrade's verification and rollback steps before cutover.

If a restart command errors or the session is interrupted, check the process, service health, and loaded artifact before retrying. Resume only the unfinished step; never infer a failed cutover from the command's exit code alone.
