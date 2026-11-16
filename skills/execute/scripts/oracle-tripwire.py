#!/usr/bin/env python3
"""Flag edits to acceptance oracles that are missing from the oracle-change list.

Freeze once, when the acceptance baseline is recorded:
  oracle-tripwire.py --freeze --baseline-dir <dir> --oracle <guide> --oracle <cases>
Check before each handoff, revision and the readiness gate:
  oracle-tripwire.py --base <ref> --baseline-dir <dir> --oracle <guide> --oracle <cases> \
      --list <oracle-change-list>

Compares the working tree with the merge base of <ref>. Flags:
  - tests that existed at the base and were deleted, or whose changed lines touch
    assertions, expectations, waits, retries, timeouts, mocks or skips;
  - any --oracle file (testing guide, acceptance record; may live outside the repo) that differs
    from its frozen copy in --baseline-dir, or has no frozen copy. Without --baseline-dir,
    --oracle paths are compared through git instead.
Freezing never overwrites a snapshot, so the first frozen oracle stays the reference; approved
revisions are declared on the list rather than re-frozen.
Exit 1 when a flagged path is not mentioned in --list (or no list was given), else 0.
"""
import argparse
import filecmp
from pathlib import Path
import re
import shutil
import subprocess
import sys

TEST_PATH = re.compile(
    r"(^|/)(tests?|__tests__|e2e|specs?)/|[._-](test|spec)\.[A-Za-z]+$|_test\.go$|(^|/)test_[^/]+\.py$"
)
ORACLE_LINE = re.compile(
    r"\b(assert\w*|expect\w*|should|to(Be|Equal|Have|Match|Contain|Throw)\w*|waitFor\w*|"
    r"wait_for\w*|sleep|setTimeout|retr(y|ies)|timeout|mock\w*|stub|spyOn|skip|xfail|todo|"
    r"only|fixme)\b",
    re.IGNORECASE,
)


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def snapshot(baseline_dir, path):
    return Path(baseline_dir) / str(Path(path).resolve()).strip("/").replace("/", "__")


def freeze(baseline_dir, oracles):
    Path(baseline_dir).mkdir(parents=True, exist_ok=True)
    for path in oracles:
        copy = snapshot(baseline_dir, path)
        if copy.exists():
            print(f"kept existing snapshot  {path}")
        else:
            shutil.copyfile(path, copy)
            print(f"frozen  {path}")


def flagged(base, oracles, baseline_dir):
    findings = {}
    for path in oracles if baseline_dir else []:
        copy = snapshot(baseline_dir, path)
        if not copy.exists():
            findings[path] = "no frozen baseline"
        elif not Path(path).exists():
            findings[path] = "oracle file deleted"
        elif not filecmp.cmp(copy, path, shallow=False):
            findings[path] = "oracle file changed since freeze"
    for line in git("diff", "--name-status", "--merge-base", base).splitlines():
        status, path = line.split("\t")[0], line.split("\t")[-1]
        if path in oracles and baseline_dir:
            continue
        if path in oracles:
            findings[path] = "oracle file changed"
        elif TEST_PATH.search(path) and status.startswith("D"):
            findings[path] = "pre-existing test deleted"
        elif TEST_PATH.search(path) and status[0] in "MR":
            old = line.split("\t")[1]
            diff = git("diff", "--merge-base", base, "-U0", "--", old, path)
            hits = [
                l for l in diff.splitlines()
                if l[:1] in "+-" and not l.startswith(("+++", "---")) and ORACLE_LINE.search(l)
            ]
            if hits:
                findings[path] = f"{len(hits)} assertion/wait/mock line(s) changed"
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base")
    parser.add_argument("--oracle", action="append", default=[])
    parser.add_argument("--baseline-dir")
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--list", help="oracle-change list; flagged paths must appear in it")
    args = parser.parse_args()

    if args.freeze:
        if not args.baseline_dir or not args.oracle:
            parser.error("--freeze needs --baseline-dir and at least one --oracle")
        freeze(args.baseline_dir, args.oracle)
        return
    if not args.base:
        parser.error("--base is required unless --freeze")
    declared = open(args.list, encoding="utf-8").read() if args.list else ""
    findings = flagged(args.base, set(args.oracle), args.baseline_dir)
    undeclared = [p for p in findings if p not in declared]
    for path, reason in sorted(findings.items()):
        print(f"{'UNDECLARED' if path in undeclared else 'declared  '}  {path}: {reason}")
    if not findings:
        print("No pre-existing test or oracle edits.")
    sys.exit(1 if undeclared else 0)


if __name__ == "__main__":
    main()
