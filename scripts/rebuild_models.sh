#!/usr/bin/env bash
# Rebuild the payload models from GitHub's published description. This is the
# one command: it runs the generator that fetches the pinned revision, verifies
# its digest, and writes both the models and the dispatch table.
#
# Like start.sh, the project's own interpreter comes first -- so the path run by
# hand is the path the tests cover, and neither needs the network. uv resolves
# the dev dependency group (datamodel-code-generator) from the lockfile only when
# there is no interpreter to use.
#
# No .env is loaded: a rebuild reads no configuration, and the description it
# takes is the pinned one rather than anything the environment could point it at.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

if [ -x "$repo/.venv/bin/python" ]; then
    exec "$repo/.venv/bin/python" "$repo/scripts/rebuild_models.py" "$@"
fi
exec uv run --quiet python "$repo/scripts/rebuild_models.py" "$@"
