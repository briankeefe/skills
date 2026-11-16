#!/usr/bin/env python3
"""Flag edits to acceptance oracles that are missing from the oracle-change list.

Usage: oracle-tripwire.py --base <ref> [--oracle <path>]... [--list <oracle-change-list>]

Compares the working tree with the merge base of <ref>. Flags:
  - tests that existed at the base and were deleted, or whose changed lines touch
    assertions, expectations, waits, retries, timeouts, mocks or skips;
  - any change to an --oracle file (acceptance record, testing guide).
Exit 1 when a flagged path is not mentioned in --list (or no list was given), else 0.
"""
import argparse
import re
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


def flagged(base, oracles):
    findings = {}
    for line in git("diff", "--name-status", "--merge-base", base).splitlines():
        status, path = line.split("\t")[0], line.split("\t")[-1]
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
    parser.add_argument("--base", required=True)
    parser.add_argument("--oracle", action="append", default=[])
    parser.add_argument("--list", help="oracle-change list; flagged paths must appear in it")
    args = parser.parse_args()

    declared = open(args.list, encoding="utf-8").read() if args.list else ""
    findings = flagged(args.base, set(args.oracle))
    undeclared = [p for p in findings if p not in declared]
    for path, reason in sorted(findings.items()):
        print(f"{'UNDECLARED' if path in undeclared else 'declared  '}  {path}: {reason}")
    if not findings:
        print("No pre-existing test or oracle edits.")
    sys.exit(1 if undeclared else 0)


if __name__ == "__main__":
    main()
