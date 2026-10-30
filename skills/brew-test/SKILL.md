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
For a fresh drafting call, supply concise sourced requirements and verified UI fixtures,
not raw observation traces: record names, search values, controls, starting states and visible
oracles. Keep incidental counts, API/SQL details and harness click/reload sequences private.
Tie each oracle to its search/filter context; changing the query can change matching rules.

Reuse a guide for this task instead of creating another competing page. Keep machine paths,
accounts and environment coordinates in local project guidance or private task artifacts,
not in this public skill. Never copy credentials, tokens, cookies or patient data into a page.

## 2. Write one concise Markdown page

Default slug: `<task-id>-test`, or a descriptive task slug when there is no ID. Keep the existing
slug when updating. Use the renderer's standard front matter and shared styles. Quote YAML
values containing colons. Prefer Markdown; no custom page layout or diagram for a checklist.
The front-matter title is rendered automatically; don't repeat it as an H1 in the body.

The reader-facing page contains a brief change summary, minimal starting context, numbered
UI journeys with checkable steps, and brief blocked/not-UI-verifiable notices. No implementation
explanation, evidence appendix, source files to inspect, code blocks, shell commands, scripts, SQL, API calls, browser console
or developer-tools steps. Do not ask the reader to start services, set environment variables,
switch branches, seed data, change roles/feature flags, or otherwise configure an environment.
Keep engineering evidence and operator procedures in the existing private task record, not
in hidden/collapsed sections or linked prerequisites the reader must execute.
Keep access context to the minimum needed to start. Don't narrate generation, missing tools,
the review process or pending authoring checks in the testing page; record those privately.

**What changed comes first.** Use 1–3 complete sentences immediately below the page title,
before access context. Explain the previous behavior and what the user can do now, naming the
concrete objects involved. Prefer a short paragraph for one connected change; use bullets
for genuinely separate changes, not fragments of the same explanation. Clarity wins over
word count: don't replace meaningful nouns with "it," "that revision" or "the selection"
before explaining what they refer to. Don't turn the summary into test instructions or a
list of every fix. Someone without the ticket/chat should understand the main change.
Reject a summary that could double as checklist headings: "Find the policy. Open results.
Disable empty arrows." Explain the changed behavior, not a set of commands or testing goals.
Don't present unchanged regression coverage as a new capability. Name the affected record
when it makes the change recognizable.
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
2. **Actions and visual checks.** Organize journeys around the reader's next visible result,
   not one checkbox per acceptance criterion. A criterion may need several checkpoints.
   Each checkpoint ends while its expected result is still on screen: action, immediate
   visual check, then check it off. Separate independently failing behaviors or meaningful
   state changes. Don't bundle source, status, bookmark, filter and pagination behaviors
   into one progress marker just to shorten the page.
   Don't create a checkbox for mechanical setup, returning to the list, closing a source
   tab or opening a menu on the way to its real check. Put that navigation at the start of
   the next relevant action. A separate box needs its own meaningful verification outcome.
   Never ask the reader to close, undo, navigate away from or replace a result before its
   check. Restoration follows the original check, not before it.
   Combine equivalent inputs with the same expected result (search spellings or ways to
   open the same policy): run Action then Visual check for each variant in one checkpoint.
   Opposite states with different expected results (apply/clear, save/restore) need separate
   checkpoints. Don't use "check, then undo, then check again" to compress them into prose.
   Put **Action:** and **Visual check:** in separate rendered paragraphs, with a blank line
   between them and both indented inside the checkbox's list item. A source newline alone
   is not a paragraph break. Use the complete markup example below, not inline label pairs.
   Group equivalent variants only when their action/result pattern is the same. Don't hide
   an action-then-undo sequence behind a single final check or omit its intermediate result.
   Keep **Visual check:** for observations only. Closing a tab, restoring a value or any
   other next action belongs at the start of the following checkpoint's **Action:**.
   Name exact UI labels, selection order, hidden-field activation, full input values,
   blur/commit actions and where the result appears. State exact expected text, values,
   selected/disabled state, or presence/absence of a named element. No "looks correct,"
   "works as expected," "configure the override" or "check the merged row." Put long input
   sets in a field/value table.
   Don't carry a rule name or expected child row from one search into another without
   evidence for that query. Use the verified query-specific name or its supported visibility check.
3. **Scope and persistence.** Cover every UI-observable sourced criterion, including named
   negative and unchanged-sibling cases. Add save/reload/reopen checks only when a sourced
   requirement, the changed state flow or a concrete reported failure makes persistence
   relevant. A read-only result doesn't need a refresh check just because it is displayed.
   Combine compatible saved changes into one persistence checkpoint: one reload can verify
   several changed fields, then another can verify their restored states. Don't reload per
   field when those combined checks satisfy every required saved-state oracle. Add another
   reload or reopen only for a different sourced failure mode; keep the reason in the private
   mapping. Don't drop explicitly required reload behavior. Ordinary app edits/saves are allowed on prepared, authorized task-owned
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
Use acceptance expectations as the coverage contract, not the observation trace as a script.
An earlier verification may have repeated a reload or used separate harness steps unnecessarily;
those actions aren't required unless the expectation or reported failure makes them necessary.
A checkpoint can satisfy several criteria. Merge overlapping coverage before drafting:
verify a behavior once in the journey and map every applicable criterion to that checkpoint.
Don't repeat an enabled control's expand/collapse checks in both a controls section and a
disabled-sibling section, or repeat the same positive search after every negative case.
Keep the mapping out of the reader-facing page. On revisions, update affected steps within
the full guide; never replace it with only the latest fix. State shared setup and expected
values once, then refer back unambiguously for reload/reopen checks. Keep distinct required
negative, sibling and persistence cases; don't repeat navigation or outcomes just to mirror
the acceptance record's rows. No fixed step/word limit. Optional checks belong in a separate
section, clearly labeled optional; don't add unsupported platforms as required coverage.
Missing browser fixtures are **Blocked**, not inherently **Not UI-verifiable**.

**Draft for resuming, then compress.** First map the sourced outcomes to the UI states where
they can actually be seen. Write those checkpoints before shortening their wording. Read
each checkpoint in isolation: can someone returning after an interruption identify the record,
perform the next action and verify it without remembering an earlier transient result?
Use named records and nearby section context instead of "the original one" or "repeat above."
Name a long record once per section, then use its unambiguous short name. Default each action
and visual-check paragraph to one or two short sentences. Don't repeat access warnings,
verification history or unchanged-peer expectations in every checkpoint; state shared
conditions once beside that group. Brevity comes from removing repeated context, not hiding
several changing results in one paragraph.
For an ordinary single-feature handoff, aim for roughly 600–900 words; this is a drafting
default, not a cap or permission to omit cases. Before adding length, remove repeated names,
setup and equivalent checks. Use descriptive link labels, not long raw URLs or duplicate
address text; when source identity matters, name the domain and filename beside the link.
Keep the exact values that identify the result, not incidental totals or snapshot counts
unless the requirement is about those counts. Lead the summary with the user-visible problem,
not implementation exceptions or scope exclusions. Keep scope notes beside the relevant check.

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
- Audit the rendered DOM, not just the Markdown: for every checklist item, require exactly
  one labeled unchecked checkbox, one **Action:** paragraph and one later **Visual check:**
  paragraph that is a different element in the same item. Fail the handoff if labels share
  a paragraph; fix the Markdown and rerender before continuing.
- Read the rendered instructions in order, including the intermediate screen states.
  Reject a checkpoint if its result has already been closed, undone or replaced when the
  reader reaches the check, or if its checkbox conceals independently resumable outcomes.
  Verify the self-contained before-and-after summary precedes access context. No code,
  commands, engineering evidence or environment-mutation instructions, including collapsed
  sections. Compare all sourced cases with the private mapping; don't trade coverage for brevity.
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
