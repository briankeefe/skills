---
name: t3-upgrade
description: Upgrade or rebuild Brian's local T3 Code fork. Make changes in a separate worktree, merge into fork main, and build the installable artifacts from main only.
---

# Upgrade local T3 Code

Read `~/.omp/agent/t3code-runtime.md` for the canonical checkout, runtime paths, and rollback and verification recipes. Older deployment entries are evidence, not alternative build instructions.

## Worktree → merge → build

1. For any source change, start in a separate feature worktree based on the current fork `main`. Use the environment's supported worktree workflow. Do not edit source in the canonical `main` checkout or reuse an unrelated dirty worktree. An upgrade that only installs a revision already on `main` needs no feature worktree.
2. Verify and commit the change in that worktree. Merge it into the intended fork's `main` using the authorized merge and publication path. If the merge is not authorized or is blocked, stop before building anything for installation. Feature-worktree builds are for verification only.
3. In the canonical build checkout, confirm the branch is `main`, the source tree is clean, and its exact revision contains the merged change. If the merge happened on the remote, bring local `main` to that revision by fast-forward only. Build installable artifacts from this checkout, never from a feature branch, a dirty checkout, or a copied feature build. If rebuilding both desktop and backend, use the same revision for both. Stage outputs away from the running backend until cutover.
4. Before replacing anything, verify artifact provenance and preserve rollback inputs. Rehearse database migrations on isolated state and prepare a verified backup if the upgrade requires a schema change. Only apply and restart the affected surfaces with authorization; see `skill://t3-restart`. After cutover, verify the revision actually loaded by each affected surface. A healthy HTTP response alone doesn't prove a desktop upgrade.
