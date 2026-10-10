#!/usr/bin/env bash
# Start the GitHub webhook ingress. This is the one way in: the tests start the
# service through this script too, so the path run by hand is the path covered.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

# shellcheck source=scripts/_env.sh
. "$repo/scripts/_env.sh"
load_env "$repo/.env"

# Nothing must sit in a buffer while a test reads the log the moment the POST
# returns.
export PYTHONUNBUFFERED=1

if [ -x "$repo/.venv/bin/python" ]; then
    exec "$repo/.venv/bin/python" -m github_webhooks "$@"
fi
exec uv run python -m github_webhooks "$@"
