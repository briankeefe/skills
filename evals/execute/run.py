#!/usr/bin/env python3
"""Replay execute decision scenarios against a model with the skill in context.

  python3 evals/execute/run.py --model claude --model codex       # current working tree
  python3 evals/execute/run.py --model codex --ref b5e0ce7         # an older skill version
  python3 evals/execute/run.py --model claude --no-skill           # baseline: is the skill needed?

Each scenario runs --k times (default 3) with a different option order. It passes only if
every trial picks the correct option (pass^k), matching the skill's own three-run rule.
Exit 0 all pass, 1 any wrong answer, 2 only errors (no answer parsed: auth, CLI or network).
Model calls cost tokens: scenarios x k x models.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import random
import re
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ["SKILL.md", "reference/sanity-check.md", "reference/review-loop.md", "reference/code-quality.md"]
COMMANDS = {
    "claude": "claude --print --tools ''",
    "codex": "codex exec --skip-git-repo-check --ephemeral --sandbox read-only -o {out} -",
}


def skill_text(ref):
    parts = []
    for name in CONTEXT:
        path = f"skills/execute/{name}"
        text = (subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, check=True,
                               capture_output=True, text=True).stdout
                if ref else (ROOT / path).read_text())
        parts.append(f'<file path="{name}">\n{text}\n</file>')
    return "\n".join(parts)


def prompt(scenario, trial, context):
    options = [scenario["correct"], *scenario["wrong"]]
    random.Random(f"{scenario['id']}:{trial}").shuffle(options)
    letters = "ABCD"[: len(options)]
    body = "\n".join(f"{letter}: {text}" for letter, text in zip(letters, options))
    preface = ("You are a coding agent operating under the execute skill below. Follow it.\n\n"
               f"{context}\n\n") if context else "You are a careful coding agent.\n\n"
    return (f"{preface}Situation: {scenario['situation']}\n\nWhich action do you take?\n{body}\n\n"
            'Reply with only JSON: {"option": "<letter>", "reason": "<one sentence>"}',
            letters[options.index(scenario["correct"])])


def ask(command, text):
    with tempfile.TemporaryDirectory() as directory:
        out = Path(directory) / "last.txt"
        args = shlex.split(command.replace("{out}", str(out)))
        result = subprocess.run(args, input=text, capture_output=True, text=True, cwd=directory,
                                timeout=600)
        reply = out.read_text() if out.exists() else result.stdout
    match = re.search(r'"option"\s*:\s*"([A-D])"', reply)
    return match.group(1) if match else None, reply.strip()[-300:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", action="append", required=True,
                        help="claude, codex, or a command reading the prompt on stdin")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--ref", help="git ref of the skill to evaluate (default: working tree)")
    parser.add_argument("--no-skill", action="store_true")
    parser.add_argument("--only", action="append")
    parser.add_argument("--scenarios", default=str(Path(__file__).with_name("scenarios.json")))
    parser.add_argument("--jobs", type=int, default=6)
    args = parser.parse_args()

    scenarios = [s for s in json.loads(Path(args.scenarios).read_text())["scenarios"]
                 if not args.only or s["id"] in args.only]
    context = "" if args.no_skill else skill_text(args.ref)
    jobs = [(model, s, t) for model in args.model for s in scenarios for t in range(args.k)]

    def run(job):
        model, scenario, trial = job
        text, expected = prompt(scenario, trial, context)
        chosen, reply = ask(COMMANDS.get(model, model), text)
        return model, scenario["id"], None if chosen is None else chosen == expected, reply

    with ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(run, jobs))

    failed = errored = False
    for model in args.model:
        print(f"\n{model}  (ref={args.ref or 'working tree'}, skill={'off' if args.no_skill else 'on'}, k={args.k})")
        for scenario in scenarios:
            trials = [r for r in results if r[0] == model and r[1] == scenario["id"]]
            passed = sum(r[2] is True for r in trials)
            wrong = [r for r in trials if r[2] is False]
            errors = [r for r in trials if r[2] is None]
            # A model/CLI error is not an answer: the scenario is unscored, not failed.
            status = "FAIL" if wrong else "ERROR" if errors else "PASS"
            failed |= bool(wrong)
            errored |= bool(errors)
            print(f"  {status:5} {passed}/{len(trials)}  {scenario['id']}")
            for r in wrong:
                print(f"        wrong: {r[3]!r}")
            for r in errors:
                print(f"        error: {r[3]!r}")
        total = sum(1 for s in scenarios
                    if all(r[2] is True for r in results if r[0] == model and r[1] == s["id"]))
        print(f"  pass^{args.k}: {total}/{len(scenarios)} scenarios")
    sys.exit(1 if failed else 2 if errored else 0)


if __name__ == "__main__":
    main()
