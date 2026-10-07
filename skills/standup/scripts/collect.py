#!/usr/bin/env python3
"""Read-only standup evidence; Python 3.9+, git, optional gh and Linear 2.6.0."""
import argparse
from datetime import datetime, time, timedelta, timezone
import heapq
import json
import os
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo


class SourceError(Exception):
    pass


def command(argv, cwd=None):
    # Never include stderr, environment, tokens or raw authentication output in JSON.
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                                errors="replace", timeout=30, stdin=subprocess.DEVNULL,
                                env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GH_PAGER": "cat"})
    except FileNotFoundError:
        source = "working directory" if cwd is not None and not Path(cwd).is_dir() else argv[0]
        raise SourceError(f"{source} unavailable") from None
    except subprocess.TimeoutExpired:
        raise SourceError(f"{argv[0]} timed out after 30 seconds") from None
    if result.returncode:
        raise SourceError(f"{argv[0]} exited {result.returncode}; inspect this scoped command separately")
    return result.stdout


def local_zone():
    if os.environ.get("TZ"):
        return ZoneInfo(os.environ["TZ"].lstrip(":"))
    path = Path("/etc/localtime")
    resolved = str(path.resolve())
    if "/zoneinfo/" in resolved:
        return ZoneInfo(resolved.split("/zoneinfo/", 1)[1])
    # Read transition rules, not today's fixed UTC offset, so DST boundaries remain correct.
    with path.open("rb") as handle:
        return ZoneInfo.from_file(handle, key="local (/etc/localtime)")


def time_window(now):
    previous = now.date() - timedelta(days=1)
    while previous.weekday() >= 5:
        previous -= timedelta(days=1)
    return (datetime.combine(previous, time(11), now.tzinfo), now,
            datetime.combine(now.date(), time(), now.tzinfo))


def utc(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("source timestamp lacks timezone")
    return parsed.astimezone(timezone.utc)


def collect(root, zone, now=None, limit=50, linear_assignee=None, linear_workspace=None, run=command):
    root = Path(root).expanduser().resolve()
    start, end, today = time_window((now or datetime.now(timezone.utc)).astimezone(zone))
    lower, upper = start.astimezone(timezone.utc), end.astimezone(timezone.utc)
    result = {
        "window": {"timezone": str(zone), "start_local": start.isoformat(), "end_local": end.isoformat(),
                   "today_local": today.isoformat(), "start_utc": utc(start), "end_utc": utc(end),
                   "today_utc": utc(today), "inclusive": True},
        "records": {"git": [], "github": []},
        "context": {"worktrees": [], "github_authored": [], "linear_assigned": []},
        "unavailable": [], "truncated": [],
    }
    errors = (SourceError, OSError, ValueError, KeyError, TypeError, AttributeError)

    def unavailable(source, exc, scope=None):
        error = str(exc) if isinstance(exc, SourceError) else "unexpected response or inaccessible path; revalidate source"
        result["unavailable"].append({"source": source, "scope": scope, "error": error})

    def truncated(source, scope, reason):
        item = {"source": source, "scope": scope, "reason": reason}
        if item not in result["truncated"]:
            result["truncated"].append(item)

    def recent(value):
        return bool(value) and lower <= timestamp(value) <= upper

    # Scope is the current/root repo, or its immediate child repos; never recurse into home.
    repos = {}
    try:
        candidates = [root]
        try:
            common = run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=root).strip()
            repos[str(Path(common).resolve())] = root
        except SourceError:
            children = heapq.nsmallest(101, root.iterdir(), key=lambda item: item.name)
            if len(children) > 100:
                truncated("git", str(root), "repository discovery capped at 100 immediate entries")
            candidates = [item for item in children[:100] if (item / ".git").exists()]
        for candidate in candidates if not repos else []:
            try:
                common = run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=candidate).strip()
                repos.setdefault(str(Path(common).resolve()), candidate)
            except errors as exc:
                unavailable("git", exc, str(candidate))
    except errors as exc:
        unavailable("git", exc, str(root))

    seen_trees = set()
    for common, repo in sorted(repos.items()):
        try:
            raw = run(["git", "worktree", "list", "--porcelain", "-z"], cwd=repo)
            trees, tree = [], {}
            for field in raw.split("\0"):
                if not field:
                    if tree:
                        trees.append(tree)
                        tree = {}
                else:
                    key, _, value = field.partition(" ")
                    tree[key] = value
            if tree:
                trees.append(tree)
            if len(trees) > limit:
                truncated("git", common, "worktree limit reached")
            for tree in trees[:limit]:
                path = tree["worktree"]
                if path in seen_trees:
                    continue
                seen_trees.add(path)
                context = {"path": path, "common_repo": common, "branch": tree.get("branch", "detached").removeprefix("refs/heads/"),
                           "timed": False, "dirty_paths": []}
                result["context"]["worktrees"].append(context)
                try:
                    fields = iter(run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=normal"], cwd=path).split("\0"))
                    paths = []
                    for field in fields:
                        if field:
                            paths.append(field[3:])
                            if "R" in field[:2] or "C" in field[:2]:
                                paths.append(next(fields))
                    paths = sorted(set(paths))
                    context["dirty_paths"] = paths[:limit]
                    if len(paths) > limit:
                        truncated("git", path, "dirty path limit reached")
                except errors + (StopIteration,) as exc:
                    unavailable("git", exc, path)
        except errors as exc:
            unavailable("git", exc, common)
        try:
            email = run(["git", "config", "user.email"], cwd=repo).strip()
            if not email:
                raise SourceError("Git author identity unavailable; configure user.email in this repository")
            raw = run(["git", "log", "--all", "--fixed-strings", f"--author=<{email}>",
                       f"--max-count={limit + 1}", "--format=%H%x1f%aI%x1f%s"], cwd=repo)
            rows = raw.splitlines()
            if len(rows) > limit:
                truncated("git", common, "author history limit reached; older refs/author dates may be omitted")
            seen = set()
            for row in rows[:limit]:
                sha, date, subject = row.split("\x1f", 2)
                if recent(date) and sha not in seen:
                    seen.add(sha)
                    result["records"]["git"].append({"common_repo": common, "sha": sha, "timestamp": date,
                                                       "timestamp_kind": "author", "subject": subject})
        except errors as exc:
            unavailable("git", exc, common)

    # The auth command projects only hostnames; resolve the authenticated user once per host.
    try:
        hosts = json.loads(run(["gh", "auth", "status", "--active", "--json", "hosts", "--jq", ".hosts | keys"]))
        if not isinstance(hosts, list) or not all(isinstance(host, str) for host in hosts):
            raise ValueError("invalid host list")
        if not hosts:
            raise SourceError("No authenticated GitHub hosts")
        for host in sorted(set(hosts))[:limit]:
            try:
                user = json.loads(run(["gh", "api", "user", "--hostname", host]))["login"]
                if not re.fullmatch(r"[A-Za-z0-9-]+", user):
                    raise ValueError("invalid GitHub identity")
                search = f"is:pr involves:{user} updated:>={utc(start)} sort:updated-desc"
                reviewed = f"is:pr reviewed-by:{user} updated:>={utc(start)} sort:updated-desc"
                query = '''query($search: String!, $reviewed: String!, $limit: Int!) {
                  search(query: $search, type: ISSUE, first: $limit) {
                    pageInfo { hasNextPage } nodes { ...StandupPR }
                  }
                  reviewed: search(query: $reviewed, type: ISSUE, first: $limit) {
                    pageInfo { hasNextPage } nodes { ...StandupPR }
                  }
                }
                fragment StandupPR on PullRequest {
                  id number title url state createdAt updatedAt author { login } repository { nameWithOwner }
                  comments(last: 20) { pageInfo { hasPreviousPage } nodes { author { login } createdAt url } }
                  reviews(last: 20) { pageInfo { hasPreviousPage } nodes { author { login } submittedAt url state } }
                  commits(last: 20) { pageInfo { hasPreviousPage } nodes {
                    commit { oid authoredDate url author { user { login } } }
                  } }
                  timelineItems(last: 20, itemTypes: [MERGED_EVENT, CLOSED_EVENT, REOPENED_EVENT, READY_FOR_REVIEW_EVENT, CONVERT_TO_DRAFT_EVENT]) {
                    pageInfo { hasPreviousPage } nodes {
                      __typename
                      ... on MergedEvent { actor { login } createdAt }
                      ... on ClosedEvent { actor { login } createdAt }
                      ... on ReopenedEvent { actor { login } createdAt }
                      ... on ReadyForReviewEvent { actor { login } createdAt }
                      ... on ConvertToDraftEvent { actor { login } createdAt }
                    }
                  }
                }'''
                payload = json.loads(run(["gh", "api", "graphql", "--hostname", host, "-f", "query=" + query,
                                          "-f", "search=" + search, "-f", "reviewed=" + reviewed, "-F", f"limit={limit}"]))
                if payload.get("errors"):
                    raise SourceError("GitHub GraphQL errors; revalidate query/host support")
                found = []
                for name in ("search", "reviewed"):
                    connection = payload["data"][name]
                    found.extend(connection["nodes"])
                    if connection["pageInfo"]["hasNextPage"]:
                        truncated("github", host, f"{name} PR search has another page")
                seen_prs, seen_activity = set(), set()
                for pr in found:
                    if not pr or pr["id"] in seen_prs:
                        continue
                    seen_prs.add(pr["id"])
                    base = {"host": host, "repository": pr["repository"]["nameWithOwner"],
                            "number": pr["number"], "title": pr["title"], "url": pr["url"], "state": pr["state"]}
                    activities = []
                    if (pr.get("author") or {}).get("login") == user:
                        if recent(pr["createdAt"]):
                            activities.append(("authored", pr["createdAt"], pr["url"]))
                        if recent(pr["updatedAt"]):
                            result["context"]["github_authored"].append({**base, "updated_at": pr["updatedAt"],
                                "proof_of_user_activity": False})
                    for name in ("comments", "reviews", "timelineItems"):
                        connection = pr[name]
                        if connection["pageInfo"]["hasPreviousPage"]:
                            truncated("github", pr["url"], f"{name} history has an earlier page (last 20 fetched)")
                        for node in connection["nodes"]:
                            actor = node.get("author") or node.get("actor") or {}
                            if actor.get("login") != user:
                                continue
                            date = node.get("submittedAt") if name == "reviews" else node.get("createdAt")
                            activity = "reviewed" if name == "reviews" else "commented" if name == "comments" else node["__typename"]
                            if recent(date):
                                activities.append((activity, date, node.get("url", pr["url"])))
                    connection = pr["commits"]
                    if connection["pageInfo"]["hasPreviousPage"]:
                        truncated("github", pr["url"], "commit history has an earlier page (last 20 fetched)")
                    for node in connection["nodes"]:
                        commit = node["commit"]
                        if ((commit.get("author") or {}).get("user") or {}).get("login") == user and recent(commit["authoredDate"]):
                            activities.append(("commit_authored", commit["authoredDate"], commit["url"]))
                    for activity, date, url in activities:
                        key = (pr["id"], activity, date, url)
                        if key not in seen_activity:
                            seen_activity.add(key)
                            result["records"]["github"].append({**base, "activity": activity, "timestamp": date,
                                                                  "activity_url": url, "actor": user})
            except errors as exc:
                unavailable("github", exc, host)
        if len(hosts) > limit:
            truncated("github", None, "authenticated host limit reached")
    except errors as exc:
        unavailable("github", exc)

    try:
        version = run(["linear", "--version"]).strip()
        if not re.search(r"(?<![\d.])2\.6\.0(?![\d.])", version):
            raise SourceError("Linear version differs from verified 2.6.0; revalidate issue query/whoami flags")
        workspace = ["--workspace", linear_workspace] if linear_workspace else []
        if not linear_assignee:
            raise SourceError("Linear username required; supply --linear-assignee (whoami Display name is not a verified username)")
        payload = json.loads(run(["linear", "issue", "query", *workspace, "--all-teams", "--assignee", linear_assignee,
                                  "--updated-after", utc(start), "--limit", str(limit), "--json", "--no-pager"]))
        if payload["pageInfo"]["hasNextPage"]:
            truncated("linear", linear_workspace, "assigned issue query has another page")
        seen = set()
        for issue in payload["nodes"]:
            if recent(issue["updatedAt"]) and issue["id"] not in seen:
                seen.add(issue["id"])
                result["context"]["linear_assigned"].append({"id": issue["id"], "identifier": issue["identifier"],
                    "title": issue["title"], "url": issue.get("url"), "updated_at": issue["updatedAt"],
                    "state": (issue.get("state") or {}).get("name"), "proof_of_user_activity": False})
    except errors as exc:
        unavailable("linear", exc, linear_workspace)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository or directory of immediate repositories")
    parser.add_argument("--timezone", help="IANA timezone; defaults to local system transition rules")
    parser.add_argument("--limit", type=int, default=50, help="Per-repo/remote cap (1-100); partial sources are disclosed")
    parser.add_argument("--linear-assignee", help="Verified Linear username; required to enable assigned-issue collection")
    parser.add_argument("--linear-workspace", help="Configured Linear workspace slug; otherwise CLI default")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    try:
        zone = ZoneInfo(args.timezone) if args.timezone else local_zone()
    except (OSError, ValueError, KeyError):
        parser.error("Local timezone unavailable; provide --timezone with an installed IANA timezone")
    print(json.dumps(collect(args.root, zone, limit=args.limit, linear_assignee=args.linear_assignee,
                             linear_workspace=args.linear_workspace), separators=(",", ":")))


if __name__ == "__main__":
    main()
