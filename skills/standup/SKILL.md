---
name: standup
description: Prepare a concise standup update from evidence of the user's recent work. Use when the user asks to prep for standup, asks what they worked on since the previous weekday at 11:00 AM, asks what they are working on today, or invokes /standup.
argument-hint: "[optional scope]"
---

# Standup

Produce a standup-ready update covering:

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

## Synthesis

- Deduplicate commits, PRs, tickets, and sessions that describe the same work into one outcome-oriented item.
- Prefer user-visible or engineering outcomes over commit-by-commit narration.
- Include ticket or PR links when available.
- Put unfinished work under **Today**, even if it began before today.
- Put merged, shipped, completed, or materially advanced work under **Since last standup**.
- Report a blocker only when evidence shows progress is blocked. Do not turn uncertainty, pending review, or ordinary follow-up into a blocker.
- If evidence conflicts, prefer the newest direct evidence and state the uncertainty briefly.
- Omit categories with no supported items. Never invent activity to make the update look complete.

Before drafting, read `skill://brian-voice` and write the update in Brian's voice. Keep the evidence requirements and compact standup format below; do not add unsupported claims or forced slang.

## Output

Use this compact format:

**Since last standup**
- <past-tense outcome, with ticket/PR link when useful>

**Today**
- <current focus and next concrete step>

**Blockers**
- <blocker and what is needed>

Keep it speakable in under one minute. Use first person, plain language, and at most five bullets total unless the user asks for detail. End with one short evidence note naming the sources checked and the exact local-time window.
