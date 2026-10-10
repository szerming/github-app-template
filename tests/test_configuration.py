"""Configuration: the refusal to start, the example file, and what must not be committed."""

from __future__ import annotations

import os
import subprocess
import sys

from conftest import REPO_ROOT, START_SCRIPT

ENV_EXAMPLE = REPO_ROOT / ".env.example"


def test_the_start_script_refuses_to_start_with_an_empty_secret() -> None:
    """The operator's entry point, started with a secret that cannot be used.

    The secret is exported as the empty string rather than left unset: the start
    script reads .env for variables that are unset, so an unset one would be
    filled in from a developer's local file and the refusal could not be
    observed here. Set-but-empty stays empty, and an empty secret is refused
    because it makes every signature forgeable.
    """
    environment = dict(os.environ, WEBHOOK_SECRET="")

    result = subprocess.run(
        ["bash", str(START_SCRIPT)],
        cwd=str(REPO_ROOT),
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode != 0
    assert "WEBHOOK_SECRET" in result.stdout + result.stderr


def test_the_service_refuses_to_start_with_the_secret_absent(tmp_path) -> None:
    """The unset case, run from a directory with no .env, so the guard is the service's own."""
    environment = dict(os.environ)
    environment.pop("WEBHOOK_SECRET", None)

    result = subprocess.run(
        [sys.executable, "-m", "github_webhooks"],
        cwd=str(tmp_path),
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode != 0
    assert "WEBHOOK_SECRET" in result.stdout + result.stderr


def test_the_example_environment_file_names_every_variable() -> None:
    names = {
        line.split("=", 1)[0].strip()
        for line in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines()
        if "=" in line and not line.lstrip().startswith("#")
    }
    assert {"WEBHOOK_SECRET", "HOST", "PORT", "LOG_LEVEL"} <= names


def test_the_real_environment_file_is_git_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-v", ".env"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert ".env" in result.stdout


def test_the_real_environment_file_is_not_tracked() -> None:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", ".env"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
