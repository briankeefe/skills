---
name: brew-test
description: Create or refresh a local Brew testing guide at the end of a full task execution. Use for local testing instructions, verification walkthroughs, or a Brew testing handoff, including automatic execute ticket closeout and published revisions.
argument-hint: "[ticket, task, or existing guide]"
---

# Local Brew testing handoff

Turn the task's existing acceptance evidence into a short page someone can follow without the
chat. Reuse the running app, Brew renderer and verification artifacts. This is a handoff, not a
new acceptance system or permission to fix, publish, deploy, seed data or make paid calls.

## When to run

- Full `execute <ticket>`: prepare the page after runtime verification, include it in the initial
  draft-PR handoff, and refresh it before the final completion or blocker handoff. Don't wait
  for the user to ask. If publication is blocked, describe the local work and remaining blockers.
- Published revisions: update the same page and URL with affected steps and current evidence.
  After a confirmed staging deployment during the active task, add a clearly separate staging
  section; do not turn local evidence into staging proof.
- Direct requests: create or update the requested testing guide. Read-only reviews, summaries,
  sanity checks and other execute commands don't create pages unless explicitly requested.

## 1. Reuse the task context

Read `skill://brew-clear` and its required writing/authoring guidance. Resolve the active Brew
renderer and its current `AUTHORING.md` from repository and personal project instructions.
Don't use an obsolete content checkout's guide when the renderer has moved into a monorepo.

Use the task's sourced acceptance criteria, later decisions, current worktree/revision, PR,
verified app URLs, tenant/role, fixtures and observations. For projects with an acceptance
handoff exporter, reuse its private output after checking for secrets and sensitive data.
Don't invent a second checklist, rerun applicable acceptance checks for reassurance, or claim
that screenshots prove live behavior. Missing runtime/data/access stays visibly blocked.

Reuse a guide for this task instead of creating another competing page. Keep machine paths,
accounts and environment coordinates in local project guidance or private task artifacts,
not in this public skill. Never copy credentials, tokens, cookies or patient data into a page.

## 2. Write one concise Markdown page

Default slug: `<task-id>-test`, or a descriptive task slug when there is no ID. Keep the existing
slug when updating. Use the renderer's standard front matter and shared styles. Quote YAML
values containing colons. Prefer Markdown; no custom page layout or diagram for a checklist.

The page needs:

1. **Start here.** A working app link, explicitly local/preview/staging, required tenant/role,
   test record and prerequisites. Explain local auth bypasses and the actual test identity
   when relevant. Include exact startup/access instructions if the app isn't running.
2. **Numbered actions and visible pass criteria.** Cover every sourced acceptance criterion,
   including named negative, scope and persistence cases. Group related checks into a few
   short journeys; don't drop required cases just to meet a step count. Put long input sets
   in a field/value table. Name exact UI labels, selection order, hidden-field activation,
   full input values, blur/commit actions and where the result appears. Don't say just
   "configure the override" or "check the merged row."
3. **Restore what changed.** For mutating checks, state the safe target and exact original
   values or restoration procedure. Warn before paid, destructive or shared-environment
   actions; leave unauthorized steps blocked. Don't create users or fixtures just to write
   a guide. Prepared links need a checked blank-form fallback if they depend on saved state.
4. **Evidence and limits.** Current revision/PR, verification date, what was actually exercised
   in this environment and what remains unverified. Distinguish archived fixtures, replayed
   events and fresh/live runs. Put suggested checks in future tense, observations in past tense.

Use a few actual screenshots when they clarify a hard-to-find control or expected result.
Reuse still-applicable captures; label older captures and replays. Keep local images alongside
the page using the renderer's supported asset convention, with useful alt text and full-size
links where needed. Don't upload media, record a video or publish hosted Brew as a side effect.
`draft: true` hides an index entry; it does not protect private content.

## 3. Serve locally without publishing

Reuse a healthy task preview and stable URL. Otherwise use the installed Brew renderer's local
entry point, an isolated pages directory outside application source, a free port and a named
long-lived service. Bind to `127.0.0.1`, not `0.0.0.0`; don't kill another task's server.
Keep cloud page/media stores disabled. For the Node Brew renderer exposing `createApp`, after
resolving and exporting absolute `BREW_ROOT`, `PAGES_DIR` and a free `PORT`, use:

```sh
env -u BREW_PAGES_BUCKET -u BREW_MEDIA_BUCKET node -e '
  const { createApp } = require(process.env.BREW_ROOT + "/build/server.js");
  createApp({ pagesDir: process.env.PAGES_DIR }).listen(
    Number(process.env.PORT), "127.0.0.1",
    () => console.log("Local Brew ready on " + process.env.PORT)
  );
'
```

Confirm that API/build location before using this recipe; build with the repository's existing
command only if needed. If images need a separate route, reuse the existing preview's narrow
per-slug asset mount. Never expose the whole worktree or acceptance directory as static files.
Save the actual source path, URL and restart command in the existing private task record so
another session can resume without reconstructing them. Leave the preview running for review.

## 4. Verify the handoff, then return it

- Run the renderer's content validator against the authored page using its supported API.
  Some versions reject asset directories; validate page sources in a temporary directory and
  check served images separately. Don't run a cloud publisher to validate local Markdown.
- Inspect the rendered page in a managed headless browser using
  `skill://execute/reference/tool-recipes.md`. Check desktop and narrow widths, images,
  expanded setup sections and links. Look at screenshots; HTTP 200 alone isn't visual proof.
- Follow the written journey on the real app from its stated starting point, not an agent's
  prefilled tab. Reuse existing acceptance observations only when they cover those exact
  actions and current inputs. Check required refresh/reopen behavior and restore test values.
  If a prerequisite prevents execution, label that check blocked rather than asserting PASS.
- Close verification tabs, not the preview server. Return the local Brew URL plus the first
  action, essential access/setup and any blocker. Keep execute's chat handoff requirements;
  a localhost page isn't reviewer-accessible remotely, so don't use it as the PR's only checklist.

A guide can document blocked work. It cannot make a failed task complete or replace the agent's
own acceptance gate, review workflow or deployment evidence.
