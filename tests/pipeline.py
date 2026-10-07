"""Run with python3 tests/pipeline.py; AWS is replaced by a temporary local fixture."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

script = Path(__file__).resolve().parents[1] / "skills/execute/scripts/wait-codepipeline.py"
revision = "a" * 40
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    aws = root / "aws"
    aws.write_text(f"#!{sys.executable}\n" + '''import json, os
from pathlib import Path
counter = Path(os.environ['COUNTER'])
index = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(index + 1))
steps = json.loads(os.environ['STEPS'])
print(json.dumps({'pipelineExecution': steps[min(index, len(steps) - 1)]}))
''')
    aws.chmod(0o755)

    def run(steps):
        counter = root / "counter"
        counter.unlink(missing_ok=True)
        result = subprocess.run(
            [sys.executable, str(script), "--pipeline", "test", "--execution", "execution-1",
             "--revision", revision, "--profile", "test", "--region", "us-east-1",
             "--interval", "0.05", "--timeout", "3"],
            env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"],
                 "COUNTER": str(counter), "STEPS": json.dumps(steps)},
            capture_output=True, text=True,
        )
        return result

    def execution(status, sha=revision, identifier="execution-1"):
        return {"pipelineExecutionId": identifier, "status": status,
                "artifactRevisions": [{"revisionId": sha}]}

    result = run([execution("InProgress"), execution("Succeeded")])
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout.splitlines()[-1])["status"] == "Succeeded"
    for status in ["Failed", "Stopped", "Superseded"]:
        result = run([execution(status)])
        assert result.returncode != 0 and status in result.stderr, result
    result = run([execution("Succeeded", "b" * 40)])
    assert result.returncode != 0 and "revision" in result.stderr.lower(), result
    result = run([execution("Succeeded", identifier="other-execution")])
    assert result.returncode != 0 and "execution" in result.stderr.lower(), result
    result = run([execution("InProgress")])
    assert result.returncode != 0 and "timed out" in result.stderr.lower(), result

print("PASS: execution/revision identity, terminal failures, transition to success and bounded waiting")
