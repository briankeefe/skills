---
name: brew-test
description: Create or refresh a local Brew testing guide containing only UI-driven E2E actions and explicit visual checks. Runs at full execute ticket handoffs and after published revisions.
argument-hint: "[ticket, task, or existing guide]"
---

# Local Brew testing handoff

Turn the task's existing acceptance evidence into a short browser-only E2E checklist someone
can follow without the chat. Every test step pairs an exact UI action with an unambiguous
visible result. Reuse the running app, Brew renderer and verification artifacts. This is a
handoff, not a new acceptance system or permission to fix, publish, deploy, seed data or make
paid calls. Setup and renderer commands below are for the agent, never the reader-facing page.

## When to run

- Full `execute <ticket>`: prepare the page after runtime verification, include it in the initial
  draft-PR handoff, and refresh it before the final completion or blocker handoff. Don't wait
  for the user to ask. If publication is blocked, mark affected journeys blocked.
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

The reader-facing page contains only minimal starting context, numbered UI journeys and
brief blocked/not-UI-verifiable notices. No implementation explanation, evidence appendix,
source files to inspect, code blocks, shell commands, scripts, SQL, API calls, browser console
or developer-tools steps. Do not ask the reader to start services, set environment variables,
switch branches, seed data, change roles/feature flags, or otherwise configure an environment.
Keep engineering evidence and operator procedures in the existing private task record, not
in hidden/collapsed sections or linked prerequisites the reader must execute.

1. **Start here.** A checked app link, explicitly local/preview/staging, required existing
   tenant/role, safe test record and ordinary browser sign-in/navigation steps. Briefly name
   the current revision/PR and which journeys the agent exercised or could not verify.
   The agent must prepare authorized prerequisites before handoff. If the app, account,
   fixture or gate is unavailable, mark the affected journey **Blocked** with the missing
   prerequisite. Do not offer a setup command or ask the reader to repair the environment.
2. **Actions and visual checks.** Group related cases into short numbered journeys. For
   every step use **Action:** followed by **Visual check:**. Name exact UI labels, selection
   order, hidden-field activation, full input values, blur/commit actions and where the
   result appears. State exact expected text, values, selected/disabled state, or presence/
   absence of a named element. No "looks correct," "works as expected," "configure the
   override" or "check the merged row." Put long input sets in a field/value table.
3. **Scope and persistence.** Cover every UI-observable sourced criterion, including named
   negative, unchanged-sibling and save/reload/reopen cases. Ordinary app edits/saves are
   allowed on prepared, authorized task-owned records, not environment/admin setup or
   paid/destructive/shared-data operations. If restoration is needed, give exact UI actions,
   original values and visual confirmation. If safe UI-only restoration is impossible,
   mark the journey blocked rather than supplying a script or database procedure.
4. **Non-UI criteria and limits.** Never invent a visual proxy for backend-only behavior or
   silently drop a required case. Mark it **Not UI-verifiable** with a short reason and keep
   the actual engineering verification in the acceptance record. A blocked or non-UI case
   does not become PASS because the rest of the UI journey worked. Distinguish actions for
   the reader to try from results the agent already observed. Prepared links need a checked
   blank-form UI fallback if they depend on saved state.

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
  `skill://execute/reference/tool-recipes.md`. Check desktop and narrow widths, images and
  links. Look at screenshots; HTTP 200 alone isn't visual proof.
- Audit the rendered reader-facing content: every numbered test step has an **Action** and
  **Visual check**, with no code, commands, engineering evidence or environment-mutation
  instructions, including inside collapsed sections. Remove or rewrite violations before
  returning the guide; do not merely label a mixed technical runbook "UI-only."
- Follow the written journey on the real app from its stated starting point, not an agent's
  prefilled tab. Reuse existing acceptance observations only when they cover those exact
  actions and current inputs. Check required refresh/reopen behavior and restore test values.
  If a prerequisite prevents execution, label that check blocked rather than asserting PASS.
- Close verification tabs, not the preview server. Return the local Brew URL plus the first
  action, essential browser access context and any blocker. Keep execute's chat handoff requirements;
  a localhost page isn't reviewer-accessible remotely, so don't use it as the PR's only checklist.

A guide can document blocked work. It cannot make a failed task complete or replace the agent's
own acceptance gate, review workflow or deployment evidence.
