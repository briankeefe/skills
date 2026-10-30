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

The reader-facing page contains a brief change summary, minimal starting context, numbered
UI journeys with checkable steps, and brief blocked/not-UI-verifiable notices. No implementation
explanation, evidence appendix, source files to inspect, code blocks, shell commands, scripts, SQL, API calls, browser console
or developer-tools steps. Do not ask the reader to start services, set environment variables,
switch branches, seed data, change roles/feature flags, or otherwise configure an environment.
Keep engineering evidence and operator procedures in the existing private task record, not
in hidden/collapsed sections or linked prerequisites the reader must execute.

**What changed comes first.** Use 1–3 complete sentences immediately below the page title,
before access context. Explain the previous behavior and what the user can do now, naming the
concrete objects involved. Prefer a short paragraph for one connected change; use bullets
for genuinely separate changes, not fragments of the same explanation. Clarity wins over
word count: don't replace meaningful nouns with "it," "that revision" or "the selection"
before explaining what they refer to. Don't turn the summary into test instructions or a
list of every fix. Someone without the ticket/chat should understand the main change.
Reject a summary that could double as checklist headings: "Find the policy. Open results.
Disable empty arrows." Explain the changed behavior, not a set of commands or testing goals.
For example: "Historical policy revisions now show their own stored summaries and extracted
rules instead of the latest revision's content. The selected revision stays aligned across
its PDF, Details view, shared links and page reloads."
Front-matter `summary` is an index description, not a substitute for this visible explanation.
Immediately below the explanation, link the original tracker ticket using its sourced URL and
identifier (for example, **Linear: ENG-1234**). Keep that link on revisions; include the PR
nearby when available. Follow `brew-clear`'s fresh-tab behavior for every authored link.

1. **Start here.** A checked app link, explicitly local/preview/staging, required existing
   tenant/role, safe test record and ordinary browser sign-in/navigation steps. Briefly name
   the current revision/PR and which journeys the agent exercised or could not verify.
   The agent must prepare authorized prerequisites before handoff. If the app, account,
   fixture or gate is unavailable, mark the affected journey **Blocked** with the missing
   prerequisite. Do not offer a setup command or ask the reader to repair the environment.
2. **Actions and visual checks.** Group related cases into short numbered journeys. Each
   independently checkable action/result pair gets a native checkbox and a short title.
   Put **Action:** and **Visual check:** in separate rendered paragraphs with a blank line
   between them. A newline in Markdown source alone renders as a space. Don't put another
   action after the expected result; make it the next checkpoint. Keep related clicks
   together when there is no meaningful intermediate result to verify.
   Variants with the same action and expected result can share one checkpoint with an exact
   input/link list. Don't repeat the same error-result paragraph for each invalid value.
   Name exact UI labels, selection order, hidden-field activation, full input values,
   blur/commit actions and where the result appears. State exact expected text, values,
   selected/disabled state, or presence/absence of a named element. No "looks correct,"
   "works as expected," "configure the override" or "check the merged row." Put long input
   sets in a field/value table.
3. **Scope and persistence.** Cover every UI-observable sourced criterion, including named
   negative and unchanged-sibling cases. Add save/reload/reopen checks only when a sourced
   requirement, the changed state flow or a concrete reported failure makes persistence
   relevant. A read-only result doesn't need a refresh check just because it is displayed.
   Prefer one representative reload after the meaningful state change; add reopen or another
   reload only if it exercises a different failure mode. Keep the reason in the private
   criterion mapping, not a repeated explanation on the page. Don't drop explicitly required
   reload behavior. Ordinary app edits/saves are allowed on prepared, authorized task-owned
   records, not environment/admin setup or paid/destructive/shared-data operations.
   If restoration is needed, give exact UI actions, original values and visual confirmation.
   If safe UI-only restoration is impossible, mark the journey blocked rather than supplying
   a script or database procedure.
4. **Non-UI criteria and limits.** Never invent a visual proxy for backend-only behavior or
   silently drop a required case. Mark it **Not UI-verifiable** with a short reason and keep
   the actual engineering verification in the acceptance record. A blocked or non-UI case
   does not become PASS because the rest of the UI journey worked. Distinguish actions for
   the reader to try from results the agent already observed. Prepared links need a checked
   blank-form UI fallback if they depend on saved state.

**Full feature, minimum repetition.** Reconcile every sourced criterion and named case to a
journey or explicit limitation in the existing private task record before shortening.
Keep the mapping out of the reader-facing page. On revisions, update affected steps within
the full guide; never replace it with only the latest fix. State shared setup and expected
values once, then refer back unambiguously for reload/reopen checks. Keep distinct required
negative, sibling and persistence cases; don't repeat navigation or outcomes just to mirror
the acceptance record's rows. No fixed step/word limit. Optional checks belong in a separate
section, clearly labeled optional; don't add unsupported platforms as required coverage.
Missing browser fixtures are **Blocked**, not inherently **Not UI-verifiable**.

Use the renderer's shared checklist convention, not a per-page script or stylesheet:

```markdown
## 1. Historical policy details

- <label><input type="checkbox" data-brew-check> Open the August revision</label>

  **Action:** Under **08/01/2026**, click **Open policy details**.

  **Visual check:** The banner says **Viewing version 1 · Effective 08/01/2026**.
```

Author every box unchecked. Tell the reader once to check only after the visual check passes.
Saved boxes are browser-local place markers, not the agent's verification or an acceptance PASS.
Use the shared renderer's small completion animation and reduced-motion behavior; no confetti,
sound, custom page layout or animation dependency. Keep completed instructions readable.

Use a few actual screenshots when they clarify a hard-to-find control or expected result.
Reuse still-applicable captures; label older captures and replays. Keep local images alongside
the page using the renderer's supported asset convention, with useful alt text and full-size
links where needed. Don't upload media, record a video or publish hosted Brew as a side effect.
`draft: true` hides an index entry; it does not protect private content.

## 3. Serve locally without publishing

Reuse a healthy task preview and stable URL only after confirming it serves the current shared
styles and client behavior, not an obsolete worktree's built renderer. Check the actual asset
responses and rendered theme control; a healthy HTTP response is not proof of current styles.
If stale, replace the affected preview with the current renderer while preserving its pages
directory, port, per-slug assets and URLs; never kill an unrelated task's server.
Otherwise use the installed Brew renderer's local entry point, an isolated pages directory
outside application source, a free port and a named long-lived service. Bind to `127.0.0.1`,
not `0.0.0.0`. Keep cloud page/media stores disabled. For the Node Brew renderer exposing
`createApp`, after resolving and exporting absolute `BREW_ROOT`, `PAGES_DIR` and a free `PORT`, use:

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
- Audit the rendered reader-facing content: a self-contained before-and-after summary precedes access context;
  every checkpoint has separate **Action** and **Visual check** paragraphs and an unchecked
  labeled checkbox. No code, commands, engineering evidence or environment-mutation instructions,
  including inside collapsed sections. Remove or rewrite violations before returning the guide.
  Compare the rewritten journeys to the private criterion mapping: shorter must not mean partial.
- Exercise checkbox click/keyboard behavior and reload persistence; check that a changed action
  or expected result invalidates saved completion and another page doesn't inherit it. Verify
  reduced motion and readable completed text. Don't mark boxes on the user's behalf or equate
  a personal completion count with successful feature verification.
- Apply **Walk the testing guide** in `skill://execute/reference/sanity-check.md` to the rendered
  page on the real app. Check required refresh/reopen behavior and restore test values. Its
  recorded journey evidence is shared with ticket sanity checking, not a second walkthrough
  or repair loop. This reference grants no authority to fix the guide/app or perform unsafe steps.
- Close verification tabs, not the preview server. Return the local Brew URL plus the first
  action, essential browser access context and any blocker. Keep execute's chat handoff requirements;
  a localhost page isn't reviewer-accessible remotely, so don't use it as the PR's only checklist.

A guide can document blocked work. It cannot make a failed task complete or replace the agent's
own acceptance gate, review workflow or deployment evidence.
