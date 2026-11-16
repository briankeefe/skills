"""Run with python3 tests/execute_evals.py; uses a fake model, no API calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
runner = root / "evals/execute/run.py"
data = json.loads((root / "evals/execute/scenarios.json").read_text())
assert all({"id", "source", "situation", "correct", "wrong"} <= s.keys() for s in data["scenarios"])
assert len({s["id"] for s in data["scenarios"]}) == len(data["scenarios"])

# Fake model: answers with whichever letter labels the option containing MARK.
fake = f"""{sys.executable} -c "import re,sys; t=sys.stdin.read(); print('{{\\"option\\": \\"%s\\"}}' % re.search(r'^([A-D]): .*MARK', t, re.M).group(1))" """
with tempfile.TemporaryDirectory() as directory:
    scenarios = Path(directory) / "s.json"

    def run(correct, wrong):
        scenarios.write_text(json.dumps({"scenarios": [
            {"id": "x", "source": "t", "situation": "s", "correct": correct, "wrong": wrong}]}))
        return subprocess.run([sys.executable, str(runner), "--model", fake, "--no-skill",
                               "--scenarios", str(scenarios), "--k", "4"],
                              capture_output=True, text=True)

    good = run("right MARK", ["wrong one", "wrong two"])
    assert good.returncode == 0 and "PASS  4/4" in good.stdout, good.stdout + good.stderr
    bad = run("right", ["wrong MARK", "wrong two"])
    assert bad.returncode == 1 and "FAIL  0/4" in bad.stdout, bad.stdout + bad.stderr
    broken = run("right", ["wrong one", "wrong two"])  # fake finds no MARK and crashes
    assert broken.returncode == 2 and "ERROR 0/4" in broken.stdout, broken.stdout + broken.stderr

print("PASS: scenario schema, shuffled option grading and pass^k exit status, errors kept separate from wrong answers")
