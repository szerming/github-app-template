#!/usr/bin/env bash
# Forward live GitHub deliveries to the local service, signing with the same
# secret the service verifies with. Forwarding is live: something has to happen
# on the repository, and it needs an authenticated `gh`. It is the demo; the
# hermetic suite stays the gate.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

# shellcheck source=scripts/_env.sh
. "$repo/scripts/_env.sh"
load_env "$repo/.env"

secret="${WEBHOOK_SECRET:?WEBHOOK_SECRET is not set: the forwarded signature has to be the one the service verifies with}"
host="${HOST:-127.0.0.1}"
port="${PORT:-8000}"
target_repo="${GITHUB_REPO:-szerming/github-app-template}"
events="${WEBHOOK_EVENTS:-*}"

exec gh webhook forward \
    --repo="$target_repo" \
    --events="$events" \
    --secret="$secret" \
    --url="http://${host}:${port}/"
