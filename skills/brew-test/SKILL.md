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

## 2. Write a walkthrough, not an acceptance inventory

**Delivery contract:** The reader-facing guide must be complete, concise and easy to resume.
The default maximum is **900 rendered body words**, not a target to fill or a suggestion.
A different budget requires explicit user approval. Length and repetition are handoff gates:
an over-budget or repetitive draft is unfinished, even when every criterion is mentioned.

**Map coverage privately before drafting.** In the existing task record, map every sourced
criterion and named case to a journey or explicit limitation. Several criteria can share a
checkpoint; do not turn acceptance rows or harness traces into separate reader-facing steps.
Preserve negative, sibling and required persistence cases. On revisions, update the whole
feature guide, not just the newest fix. Keep this inventory and engineering evidence private.
Don't add speculative cases or unsupported platforms. Label sourced optional checks optional.

Use the existing slug and standard front matter; default a new slug to `<task-id>-test`.
Preserve visibility and links on revisions. The renderer supplies the title, styles and
checklist behavior; no duplicate H1, custom layout, scripts or styles.

The page contains only:

1. **What changed:** 1–3 complete sentences explaining the previous behavior and the concrete
   user-visible change. Name the affected objects; don't use command fragments or call
   unchanged regression coverage a new feature. The front-matter summary is not a substitute.
   Follow with sourced ticket and PR links, opening fresh tabs.
2. **Start here:** A checked app link and environment, existing tenant/role, prepared record,
   and only the access context needed to begin. Distinguish prior observations from current
   verification. Missing access, fixtures or gates make affected journeys **Blocked**.
3. **Numbered UI journeys:** Checkpoints with a short title, native checkbox, exact **Action**
   and immediate **Visual check** in separate rendered paragraphs. Use blank lines and indent
   both paragraphs inside the list item, as below.
4. **Necessary limits:** Mark backend-only criteria **Not UI-verifiable** with a short reason.
   Missing UI fixtures are **Blocked**, not inherently non-UI-verifiable. Neither is PASS.

**Make each checkpoint earn its place.** Give independently failing behaviors a clear stopping
point, while merging equivalent inputs with the same oracle: perform Action then Visual check
for each variant before moving on. Don't create boxes for navigation, opening menus or closing
tabs on the way to the real check. Don't bundle unrelated controls into one progress marker.
Check a result while it is visible, before undoing, closing or replacing it. Put the next action
in the next appropriate Action paragraph; Visual check contains observations only.

**Remove repetition, not coverage.** State shared setup, record names and unchanged-peer
expectations once per group. Use unambiguous short names afterward. Verify overlapping behavior
once and map all relevant criteria to it privately. Retain exact inputs, required commit/blur
actions and query-specific visible oracles, not incidental counts or repeated expected text.
Use descriptive links instead of long raw URLs. Screenshots are optional navigation aids,
not a substitute for current instructions; label older captures and use supported local assets
with useful alt text.

**Reload only for a reason.** A sourced persistence requirement or concrete changed-state risk
can justify reload/reopen checks; a read-only result does not. Combine compatible saved changes
in one reload and verify restored states together when that meets all required oracles.
Keep the reason in the private map, not repeated on the page.

**Stay browser-only and safe.** No implementation discussion, evidence appendix, code, shell,
SQL, API calls, developer tools or environment/admin setup, including hidden sections or linked
prerequisites. The agent prepares authorized prerequisites. Ordinary app edits are limited to
authorized task-owned records, with exact UI restoration and confirmation. Block unsafe or
impossible restoration; never substitute scripts, paid calls or shared/production mutations.
Prepared links that depend on saved state need a checked ordinary-UI fallback.

```markdown
## 1. Historical policy details

- <label><input type="checkbox" data-brew-check> Open the August revision</label>

  **Action:** Under **08/01/2026**, click **Open policy details**.

  **Visual check:** The banner says **Viewing version 1 · Effective 08/01/2026**.
```

Author boxes unchecked. Tell the reader once to check after the visual check passes. Progress
is a browser-local place marker, not verification evidence. Use the shared completion animation,
reduced-motion behavior and readable completed text. Don't upload media, record video or publish
as a side effect. `draft: true` hides an index entry, not private content.

If a complete walkthrough cannot fit after deduplication and tightening, **block the handoff**.
Report the measured word count, budget and exact required cases causing the conflict. Ask the
user to decide the budget or scope; don't drop cases, silently raise the limit, hide overflow
in another page/collapsed section, or call an overlong draft ready.

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

Before handoff, record these gates in the existing private task record. All must pass:

- **Coverage:** Every sourced criterion and named case has a journey or explicit limitation.
- **Length:** Measure the entire rendered `.prose` body, including the summary, setup, headings,
  inputs, labels, tables and limits. Exclude only renderer chrome/front-matter metadata. Apply
  the 900-word maximum unless the user explicitly approved another budget; no minimum.
- **Repetition:** Review checkpoints against the coverage map. Reject repeated setup, oracles,
  equivalent variants split across boxes, or duplicate journeys justified only by separate
  acceptance rows. Merge overlapping coverage without hiding distinct outcomes.

Run the length gate in the browser; don't estimate it or count Markdown syntax:

```javascript
() => {
  const prose = document.querySelector(".prose");
  if (!prose) throw new Error("Testing guide body is missing");
  const text = prose.textContent.trim();
  const words = text ? text.split(/\s+/).length : 0;
  const limit = 900; // Change only for an explicitly approved budget.
  if (words > limit) throw new Error(`Guide handoff blocked: ${words}/${limit} words`);
  return { words, limit };
}
```

If any gate fails, revise before returning a testing handoff. If full coverage genuinely
conflicts with the budget, report the specific blocker described above, not a ready guide.

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
