#!/usr/bin/env bash
# Rebuild the payload models from GitHub's published description. This is the
# one command: it runs the generator that fetches the pinned revision, verifies
# its digest, and writes both the models and the dispatch table. The dev
# dependency group (datamodel-code-generator) is resolved from the lockfile.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

exec uv run --quiet python "$repo/scripts/rebuild_models.py" "$@"
