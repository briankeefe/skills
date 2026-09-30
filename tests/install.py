"""Run with python3 tests/install.py; uses only temporary installation targets."""
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[1]
skills = sorted(path for path in (repo / "skills").iterdir() if (path / "SKILL.md").is_file())


def install(target):
    return subprocess.run(
        ["sh", str(repo / "install.sh")],
        env={**os.environ, "SKILLS_DIR": str(target)},
        capture_output=True,
        text=True,
    )


with tempfile.TemporaryDirectory() as temp:
    target = Path(temp) / "installed skills"
    assert install(target).returncode == 0
    for skill in skills:
        assert (target / skill.name).is_symlink()
        assert (target / skill.name).resolve() == skill
        assert (target / skill.name / "SKILL.md").read_bytes() == (skill / "SKILL.md").read_bytes()
    assert install(target).returncode == 0

    collision = Path(temp) / "collision"
    conflicting = collision / skills[-1].name
    conflicting.mkdir(parents=True)
    (conflicting / "local.txt").write_text("preserve local work")
    result = install(collision)
    assert result.returncode != 0
    assert (conflicting / "local.txt").read_text() == "preserve local work"
    assert sorted(collision.iterdir()) == [conflicting], "Collision must prevent partial installation"

    (conflicting / "local.txt").unlink()
    conflicting.rmdir()
    conflicting.symlink_to(Path(temp) / "missing")
    assert install(collision).returncode != 0
    assert os.readlink(conflicting) == str(Path(temp) / "missing")
    assert sorted(collision.iterdir()) == [conflicting]

print("PASS: installed skill loading, repeat install, directory collisions and broken-link collisions")
