# PR description trial cases

Synthetic, project-neutral cases. These are candidate anchors, not Brian-approved examples
or claims about a real PR. They contain no private ticket/customer history. Supply the source
packet to a fresh drafting call without the candidate answer; inspect its output against the
stated expectations. Wording need not match. Judge accuracy, usefulness, voice and unnecessary
detail separately; any unsupported claim or omitted material risk fails regardless of length.

## 1. Small version bump

**Source packet:** Purpose: prepare version 42.0.0. Only diff: root package.json version
41.0.0 → 42.0.0. Lockfile unchanged. Observed: local production build succeeded. No deployment
run. Required template: none. Release link: https://example.com/releases/42.

**Candidate answer:**

> I'm bumping the app to 42.0.0 for the next release. No application code changed.
>
> ## Testing
> The local production build passed.
>
> https://example.com/releases/42

**Check:** Keep the version, narrow scope, build result and supplied link. Don't add an
approval/review verdict, claim deployment or invent UI verification.

## 2. Connected changes in two areas

**Source packet:** Purpose: make sorted search results stable between pages. Diff: shared
SQL order changes from score DESC to score DESC, id ASC; UI next-page request now forwards
the current sort instead of resetting to default. Default sort is unchanged. Observed: one
real database check returned every matching record once across tied-score pages; isolated
local UI retained the chosen sort on Next. Saved-search flow was not exercised. Required
template: Summary and Testing. Ticket: https://example.com/issues/SEARCH-12.

**Candidate answer:**

> ## Summary
> I made search pagination keep the selected sort and use a stable order when scores tie.
> The query and next-page request both needed changes so paging doesn't repeat or skip results.
>
> ## Testing
> I checked tied-score pagination against the database and kept a selected sort through Next
> in the isolated local UI. I haven't checked the saved-search flow.
>
> https://example.com/issues/SEARCH-12

**Check:** Explain why both areas changed. Keep the saved-search verification gap. Don't
claim all search flows passed, list every file or repeat the task history.

## 3. Data repair with a rollout boundary

**Source packet:** Purpose: restore missing report summaries in a demo tenant. Diff: operator
script copies a successful summary only between reports with the same source-document hash;
selection is pinned to the demo schema and fee-for-service contracts. Capitated contracts
are excluded. Script inserts only, skips already-repaired reports and journals inserted IDs
for rollback. Observed on an isolated production-data fork: dry run, apply, rerun, UI inspection
and rollback succeeded. Production repair has not run and needs separate operator approval.
Required template: none. Ticket: https://example.com/issues/DEMO-7.

**Candidate answer:**

> I'm restoring missing demo report summaries by reusing a successful summary of the same
> source document. The repair only covers fee-for-service contracts in the demo tenant;
> capitated contracts are excluded.
>
> The script skips repaired reports and supports rollback. Production hasn't been updated
> and still needs separate operator approval.
>
> ## Testing
> On an isolated production-data fork, I checked dry run, apply, rerun, the UI result and rollback.
>
> https://example.com/issues/DEMO-7

**Check:** Retain same-document matching, tenant/contract scope, rerun/rollback behavior,
isolated verification and unapplied production/approval boundary. Do not imply the source
summary was newly generated or the repair has shipped.

## Rejection cases

Use the case 3 packet and change only the indicated candidate text. The checker should reject
each for the stated reason, not because it differs from the candidate's exact wording:

| Candidate text or mutation | Why it fails |
| --- | --- |
| Add “Independent sanity check: PASS. Closeout 1/2. Cursor approval pending.” | Internal process and mutable review status, not change context. |
| Replace the production boundary with “The demo tenant is repaired in production.” | Contradicts observed execution. |
| Remove the fee-for-service restriction and capitated exclusion. | Hides a material scope boundary. |
| Replace Testing with “All tenant isolation and end-to-end tests passed.” | Broader verification than the packet supports. |
| Replace the ticket with “Full instructions: http://127.0.0.1:3398/demo-test”. | Invents a link and treats a local-only page as reviewer-accessible evidence. |

Also check a revision: if the new packet says rollback failed, the new body must report that
limitation rather than preserving the old successful rollback claim. If the existing body
contains reviewer-authored notes or a bot-owned footer, keep them outside the generated draft
and preserve them when composing an authorized update. Do not post any of these examples.
