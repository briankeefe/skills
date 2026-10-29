---
name: standup
description: Prepare a ticket-by-ticket standup briefing with Linear titles, status changes, recent work, today's focus, and genuine blockers. Use when the user asks to prep for standup, asks what they worked on since the previous weekday at 11:00 AM, asks what they are working on today, or invokes /standup.
argument-hint: "[optional scope]"
---

# Standup

Produce a factual, ticket-by-ticket standup briefing, not a script telling the user what to say, covering:

1. completed or materially advanced work since 11:00 AM on the previous weekday, in the user's local timezone;
2. work currently in progress today;
3. blockers that are evidenced by the available sources.

Do the research. Do not ask the user to remember their own work.

## Time window

Calculate the start in local time:

- Monday: previous Friday at 11:00 AM.
- Tuesday through Friday: previous calendar day at 11:00 AM.
- Saturday or Sunday: previous Friday at 11:00 AM.

The end is now. “Today” starts at local midnight.

## Evidence

### Default collector

When Python 3.9+, Git and a local checkout are available, gather bounded evidence in one read-only invocation:

```sh
python3 "${SKILLS_DIR:-$HOME/.omp/agent/skills}/standup/scripts/collect.py" --root "$PWD"
```

Use the actual installed standup directory if your harness installs skills elsewhere. This is an ordinary
Python script, not a `skill://` shell API. Set `--root` to the repository or code directory being considered;
discovery checks that repository or its immediate children and linked Git worktrees, never a recursive home scan.
Use `--timezone America/New_York` (or the user's IANA zone) to override local system transition rules.
The window includes both endpoints and retains DST rules across weekends.

For optional Linear evidence, add `--linear-assignee <verified-username>` and, when needed,
`--linear-workspace <configured-slug>`. Linear 2.6.0's `whoami` displays a human name, not a guaranteed
assignee username; never guess the username from it. Other versions are reported unavailable until
the query recipe is revalidated. Git author identity comes from each repository's `user.email`;
GitHub identity comes from each authenticated `gh` host, once per host.

The compact JSON separates timestamp-filtered `records` from `context`: worktree branch/dirty paths are
explicitly untimed, and assigned Linear issues or recently updated authored PRs are not proof of personal
activity. Git history is collected once per common repository, including linked worktree refs.
GitHub searches recently updated involved/reviewed PRs and records the authenticated actor's creation,
comments, reviews, authored commits and lifecycle events, not an unattributed PR `updatedAt`.

Read `unavailable` and `truncated` before synthesizing. Missing tools/authentication or one failed source
leave other evidence intact. `--limit` defaults to 50 (maximum 100); repository discovery checks at most
100 immediate entries and GitHub nested activity fetches the last 20 entries per connection.
An exhausted cap or provider `pageInfo` is disclosed, so never describe a partial result as complete.
No credentials, environment dumps, commit bodies, diffs or tracker mutations are collected.

In OMP Eval, capture stdout directly, parse once, and first display only the window, `records`,
`unavailable` and `truncated`. Keep `context` in memory; select only task-relevant worktrees/issues
when needed rather than dumping every old branch/dirty path into the transcript. Never parse a
rendered artifact preview or rerun the collector solely to recover hidden fields. Use
`skill://execute/reference/tool-recipes.md` for the direct-stdout JSON recipe.

Comment creation identifies its author; comment `updatedAt` does not identify its editor.
Do not count an old comment's recent edit as the author's activity without separate actor evidence.

Conversation/archive and memory research remain separate supplements. If the collector is unsupported,
use the sources below directly, retaining the same attribution, time-window and partial-evidence rules.

Use available authenticated and local sources, preferring direct evidence:

1. Recent OMP conversation/session context and durable memories.
2. Git commits, uncommitted changes, and active worktrees under the current code directory.
3. Pull requests authored, reviewed, commented on, merged, or updated by the user during the window.
4. Assigned or recently updated issue-tracker work, including status changes and comments.

Discover repository hosts, issue providers, identities, and supported CLI flags from the environment. Reuse authenticated integrations. Do not assume a specific organization, repository, tracker, default branch, or CLI syntax.

Use timestamps to enforce the window. Repository directory modification time is discovery evidence only, never proof of work. An assigned issue alone is not proof that the user worked on it. An open worktree alone is not proof that it is today's focus.

### Ticket titles and status changes

For each ticket supported by personal activity in the window, fetch its current Linear identifier,
exact title, URL, and status. Reuse fresh collector context where available; fetch individual tickets
when fields are missing. Do not list every assigned issue.

Show `Previous → Current` only when dated issue history, an earlier recorded status, or other direct
evidence establishes that transition during the window. Otherwise show just the current status and
explain once in the evidence note that status transitions were not verified. Do not repeat that caveat per ticket.
An issue's `updatedAt`, a merged PR, or a branch name does not prove a Linear status change. Never
substitute PR lifecycle states for Linear statuses. If Linear is unavailable, retain supported work
and mark the ticket title/status unavailable rather than guessing. All tracker access remains read-only.

## Synthesis

- Deduplicate commits, PRs, and sessions by Linear ticket. Give each relevant ticket its own entry with its identifier, exact title, status or evidenced status change, and a short work note.
- Prefer user-visible or engineering outcomes over commit-by-commit narration. Link the ticket identifier to Linear; add a PR link only when useful.
- Put completed or materially advanced work under **Since last standup**. Put unfinished, actively supported work and its next concrete step under **Today**, even if it began before today.
- A ticket may appear in both sections only when they describe different facts: a recent outcome and a remaining next step. Do not repeat the same work note.
- Foreground substantive implementation, merged outcomes, and active delivery work. Sizing-only discussions are planning, not implementation: group them in a collapsed **Planning only** section, retaining each ticket's title, status, and estimate inside it.
- Put secondary unticketed engineering follow-up in its own collapsed section. Do not inflate the main list with planning or routine follow-up, or imply that every listed ticket was an implementation effort.
- Report only genuine impediments requiring a decision, access, missing input/data, or another dependency that prevents the next meaningful step. Name the affected ticket and what is needed to unblock it.
- CI failures, pending CI, ordinary code fixes, merge conflicts, review feedback, and waiting for routine review are engineering follow-up, not standup blockers. Mention them briefly in the ticket's work note only when useful; do not promote them to **Blockers**.
- If evidence conflicts, prefer the newest direct evidence and state the uncertainty briefly.
- Omit categories with no supported items. Never invent activity or blockers to make the update look complete.

Before drafting, read `skill://brian-voice`. Use plain, concise factual notes, not first-person speech or a rehearsed standup script.

## Output

Use the sample below as the layout reference. Keep the three main sections, separate each ticket's
linked identifier/title from its short status/work note with a blank line, and collapse secondary work.
The sample is illustrative, not evidence or a fixed ticket count; replace all facts and links.
Retain exact Linear titles even when long. Show verified status transitions in place of current
statuses when available. Omit unsupported or empty sections, including optional collapsed groups.

```markdown
**Since last standup**

- [ENG-101](https://example.test/ENG-101) · Automate document intake

  **Staging.** Merged automatic intake and pipeline visibility.

- [ENG-102](https://example.test/ENG-102) · Align submission and remittance details

  **Ready for Release.** Merged source-alignment and pagination fixes.

- [ENG-103](https://example.test/ENG-103) · Align database permissions

  **Ready for Release.** Merged access alignment; on staging, not production.

<details>
<summary>Planning only: estimated two search improvements (3 points total)</summary>

- [ENG-107](https://example.test/ENG-107) · Find exact document titles

  **Ready for Work.** Local estimate: 1 point.

- [ENG-108](https://example.test/ENG-108) · Open documents from search results

  **Ready for Work.** Local estimate: 2 points.

Estimates were saved locally, not posted to Linear. These were sizing discussions, not implementation work.

</details>

**Today**

- [ENG-104](https://example.test/ENG-104) · Preserve excluded-service payments

  **In Progress.** Review fixes addressed. Next: PR closeout.

- [ENG-105](https://example.test/ENG-105) · Link document version histories

  **In Progress.** Linking and isolated repair implemented. Next: finish verification.

- [ENG-106](https://example.test/ENG-106) · Verify demo readiness

  **In Progress.** Repairs resumed. Next: invoice-cost cases, then the remaining sanity check.

**Blockers**

- [ENG-102](https://example.test/ENG-102) · One payment-posting staging check needs a populated staging record. Other checks can proceed.

<details>
<summary>Other engineering follow-up</summary>

Unticketed workspace-build fix: removed nested prerequisite builds. PR remains open.

</details>

*Statuses are current Linear states, not verified transitions. Evidence: Git, GitHub, Linear, and dated sessions; <exact local-time start and end>. <Material source limits, if any>.*
```

Keep notes factual and short, not first-person speech. Include every supported relevant ticket,
but distinguish planning from implementation and keep secondary detail collapsed. Never invent
a ticket mapping. Follow the user's delivery preference for local Brew versus inline output.
For Brew, authored links must open fresh tabs; use explicit `target="_blank" rel="noopener"`
HTML links if the renderer does not supply those attributes.
