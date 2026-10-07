# Verified tool recipes

Reuse the matching recipe before rediscovering CLI flags, output shapes or browser runners.
Keep provider/workspace/account/project choices in local instructions. Check installed versions
once; inspect targeted help only for an undocumented operation, a version mismatch, or a real
contract error. Always retrieve fresh issue, review, authentication and deployment state.

## Machine-readable issue and PR reads

A displayed artifact preview is not source JSON: it may contain line numbers, tables, ellipses
or truncated strings. Do not parse an Eval convenience `read('artifact://...')` preview.
Use the `read` tool's `artifact://<id>:raw` selector for unmodified text, or select fields in the
producing CLI before display. For programmatic use, capture the CLI's stdout directly and parse
that, not rendered tool output. Refetch only read-only commands, never replay a mutation to
recover output. Print only the fields needed; keep credentials, private bodies and tokens out
of logs and public guidance.

GitHub CLI structured reads:

```bash
gh pr view "$PR_URL" --json body --jq .body
gh pr view "$PR_URL" --json comments,reviews,headRefOid
```

For long JSON in Python Eval or a local Python script:

```python
import json, subprocess
result = subprocess.run(
    ["gh", "pr", "view", pr_url, "--json", "body,headRefOid"],
    check=True, capture_output=True, text=True, timeout=30,
)
pr = json.loads(result.stdout)
print(pr["headRefOid"])  # Inspect only the required fields; no rendered-preview parsing.
```

## Linear CLI 2.6.0

Confirm `linear --version` is `linear 2.6.0`; reuse these forms for that version.
Resolve the workspace, issue and assignee from project/local instructions or
`linear auth whoami` (human-readable output). `linear auth status` is not a command.
Do not print `linear auth token` or credential configuration.

```bash
# Include the final/resolved discussion when evaluating scope.
linear issue view "$ISSUE" --workspace "$WORKSPACE" --show-resolved-threads --json --no-pager --no-download
# Recent assigned issues across teams; state defaults include completed issues.
linear issue query --workspace "$WORKSPACE" --all-teams --assignee "$ASSIGNEE" --updated-after "$SINCE_UTC" --limit 100 --json --no-pager
```

`issue query` returns `{nodes, pageInfo}`, not a bare array or `.issues`.
States are `.state.name`; `pageInfo.hasNextPage=true` means the bounded result is incomplete.
Fetch further documented pages or disclose the limit. Assigned/recently updated is a candidate,
not proof the user did the work. For machine consumption capture stdout as above, or pipe
read-only JSON directly to `jq`, e.g. `jq '.nodes[] | {identifier,title,updatedAt,state:.state.name}'`.
Only request help for new operations or version drift; never guess write flags.

## Managed browser in OMP

Read `xd://eval/browser` once for the current API. For routine verification explicitly select
managed, non-relay, non-Tern headless Chromium so a configured/stale user relay cannot capture
this request. No executable hunt, user browser profile, OS focus change, or new runner needed:

```javascript
const tab = await browser.open({
  name: "task-verification", url: verificationUrl, headed: false,
  app: { relay: false, tern: false },
});
try {
  print(await tab.observe());
  // Exercise observed controls, then inspect the result and a screenshot.
  display(await tab.screenshot({ fullPage: false }));
} finally {
  await tab.close();
}
```

If this explicit selection still opens the relay or fails, report the tool-contract failure;
do not quietly attach the user's signed-in browser or rebuild a CDP launcher. Native repository
E2E tests still use their existing runner; this recipe is for observing the real surface.
