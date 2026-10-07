"""Run with python3 tests/standup.py; no network, credentials or real repos."""
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import tempfile
from zoneinfo import ZoneInfo

script = Path(__file__).resolve().parents[1] / "skills/standup/scripts/collect.py"
spec = importlib.util.spec_from_file_location("standup_collect", script)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)

zone = ZoneInfo("America/New_York")
for current, expected in [
    ("2026-03-09T10:00:00", "2026-03-06T16:00:00+00:00"),
    ("2026-03-08T10:00:00", "2026-03-06T16:00:00+00:00"),
    ("2026-03-07T10:00:00", "2026-03-06T16:00:00+00:00"),
    ("2026-11-02T10:00:00", "2026-10-30T15:00:00+00:00"),
    ("2026-10-07T10:00:00", "2026-10-06T15:00:00+00:00"),
]:
    start, end, today = collector.time_window(datetime.fromisoformat(current).replace(tzinfo=zone))
    assert start.astimezone(timezone.utc).isoformat() == expected
    assert today.hour == today.minute == today.second == 0
    assert end.isoformat().startswith(current)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    first, linked = root / "repo", root / "linked"
    first.mkdir()
    linked.mkdir()
    (first / ".git").mkdir()
    (linked / ".git").write_text("gitdir: ../repo/.git/worktrees/linked\n")
    common = first / ".git"
    calls = []
    now = datetime(2026, 10, 7, 14, tzinfo=timezone.utc)
    start = "2026-10-06T15:00:00Z"
    inside = "2026-10-07T13:00:00Z"
    outside = "2026-10-06T14:59:59Z"
    future = "2026-10-07T14:00:01Z"

    def run(argv, cwd=None):
        calls.append((argv, cwd))
        if argv[0] == "git":
            if "rev-parse" in argv:
                if cwd == root:
                    raise collector.SourceError("not a repository")
                return str(common) + "\n"
            if "worktree" in argv:
                return f"worktree {first}\0HEAD abc\0branch refs/heads/main\0\0worktree {linked}\0HEAD abc\0branch refs/heads/topic\0\0"
            if "config" in argv:
                return "person@example.test\n"
            if "log" in argv:
                return "\n".join(f"{sha}\x1f{stamp}\x1f{title}" for sha, stamp, title in [
                    ("boundary", start, "At boundary"),
                    ("recent", inside, "Recent work"),
                    ("recent", inside, "Recent work"),
                    ("old", outside, "Too old"),
                    ("future", future, "Future"),
                ])
            if "status" in argv:
                return " M local.py\0"
        if argv[:3] == ["gh", "auth", "status"]:
            return json.dumps(["github.example.test"])
        if argv[:3] == ["gh", "api", "user"]:
            return '{"login":"person"}'
        if argv[:3] == ["gh", "api", "graphql"]:
            pr = {
                "id": "PR_1", "number": 1, "title": "Feature", "url": "https://github.example.test/o/r/pull/1",
                "state": "OPEN", "author": {"login": "person"}, "createdAt": outside, "updatedAt": inside,
                "repository": {"nameWithOwner": "o/r"},
                "comments": {"nodes": [
                    {"author": {"login": "person"}, "createdAt": inside, "updatedAt": inside, "url": "https://example.test/comment"},
                    {"author": {"login": "someone-else"}, "createdAt": inside, "updatedAt": inside, "url": "https://example.test/other"},
                    {"author": {"login": "person"}, "createdAt": future, "updatedAt": future, "url": "https://example.test/future"},
                    {"author": {"login": "person"}, "createdAt": outside, "updatedAt": inside, "url": "https://example.test/old-comment"},
                ], "pageInfo": {"hasPreviousPage": False}},
                "reviews": {"nodes": [], "pageInfo": {"hasPreviousPage": True}},
                "commits": {"nodes": [
                    {"commit": {"oid": "sha1", "authoredDate": inside, "url": "https://example.test/commit",
                                "author": {"user": {"login": "person"}}}},
                    {"commit": {"oid": "sha2", "authoredDate": future, "url": "https://example.test/future-commit",
                                "author": {"user": {"login": "person"}}}},
                ], "pageInfo": {"hasPreviousPage": False}},
                "timelineItems": {"nodes": [], "pageInfo": {"hasPreviousPage": False}},
            }
            reviewed_pr = {**pr, "id": "PR_2", "number": 2, "url": "https://example.test/pull/2",
                           "author": {"login": "someone-else"},
                           "comments": {"nodes": [], "pageInfo": {"hasPreviousPage": False}},
                           "commits": {"nodes": [], "pageInfo": {"hasPreviousPage": False}},
                           "reviews": {"nodes": [
                               {"author": {"login": "person"}, "submittedAt": inside,
                                "url": "https://example.test/review", "state": "APPROVED"},
                           ], "pageInfo": {"hasPreviousPage": False}}}
            return json.dumps({"data": {
                "search": {"nodes": [pr, pr], "pageInfo": {"hasNextPage": False}},
                "reviewed": {"nodes": [pr, reviewed_pr], "pageInfo": {"hasNextPage": False}},
            }})
        if argv[:2] == ["linear", "--version"]:
            return "linear 2.6.0\n"
        if argv[:3] == ["linear", "issue", "query"]:
            return json.dumps({"nodes": [
                {"id": "issue1", "identifier": "TEAM-1", "title": "Assigned context", "url": "https://example.test/issue", "updatedAt": inside, "state": {"name": "Started"}},
                {"id": "old", "identifier": "TEAM-2", "title": "Old context", "updatedAt": outside},
                {"id": "future", "identifier": "TEAM-3", "title": "Future context", "updatedAt": future},
            ], "pageInfo": {"hasNextPage": True}})
        raise AssertionError(f"Unexpected command: {argv}")

    result = collector.collect(root, zone, now, limit=10, linear_assignee="person", linear_workspace="workspace", run=run)
    assert {item["sha"] for item in result["records"]["git"]} == {"boundary", "recent"}
    assert len([argv for argv, _ in calls if argv[0] == "git" and "log" in argv]) == 1
    assert len(result["context"]["worktrees"]) == 2
    assert all(item["timed"] is False and item["dirty_paths"] == ["local.py"] for item in result["context"]["worktrees"])
    assert len(result["records"]["github"]) == 3
    assert {item["activity"] for item in result["records"]["github"]} == {"commented", "commit_authored", "reviewed"}
    assert len([argv for argv, _ in calls if argv[:3] == ["gh", "api", "user"]]) == 1
    assert len(result["context"]["linear_assigned"]) == 1
    assert not result["records"].get("linear"), "Assignment/update metadata is not proof of personal activity"
    assert any(item["source"] == "linear" for item in result["truncated"])
    assert any(item["source"] == "github" for item in result["truncated"])
    assert result["window"]["start_utc"] == start
    assert result["window"]["timezone"] == "America/New_York"
    assert not result["unavailable"]
    capped = collector.collect(root, zone, now, limit=2, linear_assignee="person", run=run)
    assert any(item["source"] == "git" for item in capped["truncated"])

    def missing(argv, cwd=None):
        if argv[0] == "gh":
            raise collector.SourceError("command unavailable")
        if argv[:2] == ["linear", "--version"]:
            return "linear 9.0.0\n"
        return run(argv, cwd)

    partial = collector.collect(root, zone, now, limit=10, linear_assignee="person", run=missing)
    assert partial["records"]["git"] == result["records"]["git"]
    assert {item["source"] for item in partial["unavailable"]} == {"github", "linear"}
    assert "revalidate" in next(item["error"] for item in partial["unavailable"] if item["source"] == "linear")

print("PASS: weekday/weekend/DST windows, bounded evidence, filtering, deduplication and unavailable sources")
