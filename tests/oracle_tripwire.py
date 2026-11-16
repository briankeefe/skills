"""Run with python3 tests/oracle_tripwire.py; uses a temporary git repository."""
from pathlib import Path
import subprocess
import sys
import tempfile

script = Path(__file__).resolve().parents[1] / "skills/execute/scripts/oracle-tripwire.py"


def sh(*args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


with tempfile.TemporaryDirectory() as directory:
    repo = Path(directory)
    sh("git", "init", "-q", "-b", "main", cwd=repo)
    (repo / "src").mkdir()
    (repo / "src/chat.test.ts").write_text("render(chat)\nexpect(composer).toBeVisible()\n")
    (repo / "src/old.test.ts").write_text("expect(1).toBe(1)\n")
    (repo / "src/chat.ts").write_text("export const x = 1\n")
    (repo / "guide.md").write_text("Click Run. Report starts.\n")
    sh("git", "add", "-A", cwd=repo)
    sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base", cwd=repo)
    sh("git", "checkout", "-qb", "work", cwd=repo)

    def run(*extra):
        return subprocess.run([sys.executable, str(script), "--base", "main", *extra],
                              cwd=repo, capture_output=True, text=True)

    assert run().returncode == 0, "clean tree is not flagged"

    # Production and non-oracle test lines are not flagged.
    (repo / "src/chat.ts").write_text("export const x = 2\n")
    (repo / "src/chat.test.ts").write_text("render(chatView)\nexpect(composer).toBeVisible()\n")
    (repo / "src/new.test.ts").write_text("expect(2).toBe(2)\n")
    sh("git", "add", "src/new.test.ts", cwd=repo)
    assert run().returncode == 0, run().stdout

    # An added wait in a pre-existing test, a deleted test and a guide edit are flagged.
    (repo / "src/chat.test.ts").write_text(
        "render(chatView)\nawait waitFor(() => loaded)\nexpect(composer).toBeVisible()\n")
    (repo / "src/old.test.ts").unlink()
    (repo / "guide.md").write_text("Click Retrieve. Results appear.\n")
    result = run("--oracle", "guide.md")
    assert result.returncode == 1, result.stdout
    for text in ["UNDECLARED  src/chat.test.ts", "UNDECLARED  src/old.test.ts", "UNDECLARED  guide.md"]:
        assert text in result.stdout, result.stdout

    # Declaring them in the oracle-change list clears the failure but still reports them.
    (repo / "oracle-changes.md").write_text(
        "- src/chat.test.ts: owner approved\n- src/old.test.ts: dup\n- guide.md: owner approved\n")
    result = run("--oracle", "guide.md", "--list", "oracle-changes.md")
    assert result.returncode == 0 and "declared    src/chat.test.ts" in result.stdout, result.stdout

print("PASS: ignores non-oracle edits; flags added waits, deleted tests and guide edits; honors the list")
