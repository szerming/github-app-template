"""Configuration: the refusal to start, the example file, and what must not be committed."""

from __future__ import annotations

import os
import subprocess
import sys

from conftest import REPO_ROOT

ENV_EXAMPLE = REPO_ROOT / ".env.example"


def test_the_service_refuses_to_start_without_the_secret(tmp_path) -> None:
    """Started in a directory with no .env, so the guard proved is the service's own."""
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
