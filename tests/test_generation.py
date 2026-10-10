"""The rebuild command: the pin, the provenance, and reproducibility.

The artifact has to be reconstructible by anyone who has the description it
names, so these run the command itself -- the wrapper the operator runs, through
the same generator, minus the network -- and read what it wrote.

A note on the seam, because spec 0001 says its seams are settled and there are
two: those two are the running service and the models package, and they carry the
wire and the typing. Neither can carry the claims that are about the *build* -- that
the command verifies the digest of the description it pins, that the artifact is
what that description produces, and that two runs agree byte for byte. Those are
observable only by running the command and comparing what it wrote, which is what
this module does, and it stays off the network by reading the vendored copy.
"""

from __future__ import annotations

import hashlib
import json
import subprocess

from conftest import (
    DESCRIPTION_PATH,
    GENERATED_MODULE_PATH,
    REBUILD_COMMAND,
    rebuild_module,
)


def rebuild(*args: str) -> subprocess.CompletedProcess[str]:
    """The operator's one command, so the path run by hand is the path covered."""
    return subprocess.run(
        ["bash", str(REBUILD_COMMAND), *args],
        capture_output=True,
        text=True,
        timeout=300,
    )


def test_the_rebuild_refuses_a_description_that_is_not_the_pinned_revision(tmp_path):
    """The digest is the whole point of the pin: whoever rebuilt the models got
    them from this revision or the rebuild has to fail, loudly."""
    document = json.loads(DESCRIPTION_PATH.read_text(encoding="utf-8"))
    document["info"]["title"] = "a description nobody pinned"
    tampered = tmp_path / "api.github.com.json"
    tampered.write_text(json.dumps(document), encoding="utf-8")
    output = tmp_path / "generated.py"

    result = rebuild("--description", str(tampered), "--output", str(output))

    assert result.returncode != 0
    reported = result.stdout + result.stderr
    assert rebuild_module().UPSTREAM_DIGEST in reported
    assert hashlib.sha256(tampered.read_bytes()).hexdigest() in reported
    assert not output.exists()


def test_running_the_rebuild_twice_produces_identical_output(tmp_path):
    first = tmp_path / "first.py"
    second = tmp_path / "second.py"

    for output in (first, second):
        result = rebuild("--offline", "--output", str(output))
        assert result.returncode == 0, result.stderr

    assert first.read_bytes() == second.read_bytes()


def test_the_committed_artifact_is_what_the_pinned_description_produces(tmp_path):
    """Otherwise the committed models and the description they name have parted
    ways, and every claim made about their coverage is about the wrong file."""
    output = tmp_path / "generated.py"

    result = rebuild("--offline", "--output", str(output))

    assert result.returncode == 0, result.stderr
    assert output.read_bytes() == GENERATED_MODULE_PATH.read_bytes()


def test_the_artifact_records_the_revision_and_digest_it_was_built_from():
    module = rebuild_module()
    digest = hashlib.sha256(DESCRIPTION_PATH.read_bytes()).hexdigest()
    artifact = GENERATED_MODULE_PATH.read_text(encoding="utf-8")

    # The vendored copy, the pin, and the artifact's own header agree.
    assert digest == module.UPSTREAM_DIGEST
    assert digest in artifact
    assert module.UPSTREAM_REVISION in artifact
