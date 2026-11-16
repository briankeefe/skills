---
name: pr-description
description: Draft or refresh a short, first-person PR description from the current diff and observed verification. Use before creating or editing any PR body, including release PRs; separates reviewer notes from internal work records.
---

# PR description

Write a note to the reviewer, not a report of the agent's work. Read `skill://brian-voice`
and `reference/examples.md`. This skill drafts text; it grants no permission to publish,
change PR state, run a release or modify a tracker.

## Build the source packet

Before drafting, inspect the current base-to-head diff, required repository template,
ticket purpose and relevant scope decisions. Gather actual verification and material gaps.
Use the existing task evidence; don't rerun valid checks just to write the description.

Give a fresh, stateless, tool-free drafting call only:

- The **Drafting prompt** below and Brian's voice guidance, plus the reference examples.
- The current diff and its base/head identities, purpose and required template. Include
  every changed area; don't silently truncate a large diff. Split it into factual area
  summaries with the relevant hunks if necessary, then personally check the final claims.
- Observed verification, its environment/revision and any limitations on its applicability.
- Decisions that affect behavior, unusual scope, rollout requirements and material risks.
- Ticket/release links and any existing reviewer-authored body content that must survive.

The packet contains writing instructions, not this entire skill: the source gathering,
fresh-call invocation and publication steps belong to the publishing agent. Never ask the
drafting call to invoke another model or use tools. The model returns text; you own the rest.

Do not inherit the implementation conversation or send raw logs, acceptance ledgers,
reviewer verdicts, repair-round counts, owner-approval history or the old agent-written body.
An existing body is evidence to inspect for useful context, not a draft to append to.
Use the available stateless model-call facility, not another implementation/review worker.
If unavailable, report the missing drafting capability rather than claiming a fresh pass.

## Drafting prompt

> Write only the proposed PR body from the supplied sources. Start in first person with
> what I changed and why. Explain unusual scope or a non-obvious decision only when useful
> to review. Add a specific review pointer only if there is something worth calling out;
> don't force a file list or a Review focus section. Follow the required repository template
> and omit optional empty sections. Add a compact Testing section with checks actually run,
> their meaningful result and environment when it matters. Clearly distinguish suggested
> checks from completed ones. End with the ticket or release link when supplied.
>
> Prefer a short paragraph or 1–3 bullets, then Testing. Roughly 120–180 words is a soft
> ceiling, not a target or permission to omit a material risk. A version bump can be much
> shorter. Use everyday words and contractions. No em dashes or forced slang.
>
> Keep safety boundaries, exclusions, unapplied data repairs, rollout prerequisites and
> relevant verification gaps. Don't turn isolated checks into production/staging claims.
> Don't invent intent, behavior, results, coverage or approval. Exclude agent attribution,
> review status/history, approval bookkeeping, acceptance IDs/counts, raw logs, exhaustive
> test/file inventories and incidental execution numbers. Full handoffs belong elsewhere;
> link longer details only if reviewers can access them. A localhost page is not such a link.
> Return only the body, with no explanation of your writing process.

## Check before using the draft

The publishing agent owns the final check, not the drafting call:

1. Match every behavior/scope claim to the current diff or sourced decision and every
   testing claim to applicable observed evidence. Restore any omitted material limitation.
   A clear short draft with false or overbroad claims fails.
2. Read it as a reviewer: can they explain the change and why these areas belong together?
   Cut details that only explain how the agent worked. Keep a real risk even if it adds words.
3. Check first-person voice, template requirements and useful testing detail. Flag process
   leakage such as “closeout 1/2,” “maintainability review: approve,” and Cursor approval
   status. These checks guide editing; word counts and phrase checks do not prove quality.

Refresh the whole body on revisions and recheck it before readiness, not just Testing.
Do not publish a draft that fails these checks. Don't create another code-review cycle.

When publication is separately authorized, use the checked body for create/edit. Preserve
reviewer-authored content and integration-owned footers without rewriting them. Read back the
saved body using the host's API/CLI; verify the intended text and preserved content survived.
This is a workflow instruction, not an enforced CLI wrapper or CI gate.

## Trial

Use `reference/examples.md` for the offline drafting and rejection cases. Its synthetic
examples are candidate style anchors, not examples Brian has approved. Record actual trial
outputs and accuracy, usefulness, voice and unnecessary-detail findings in the existing local
workflow page. Don't publish fixtures or rewrite real PRs as part of a trial.

For the next five authorized PR descriptions, record first-draft accepted versus rewritten
and the reason in that same local record. Ask for style feedback at the normal handoff, not
as an additional permission gate. Don't treat five drafts or a model's own approval as proof
of reliability. A publication wrapper remains out of scope until the trial and actual write
routes justify it.
