# Vendored: GitHub's published webhook description

`api.github.com.json` — Octokit's OpenAPI 3.1 rendering of GitHub's webhook
payloads, at a pinned revision:

    repository  octokit/openapi-webhooks
    revision    d9af91f9ddbad97e5b5765d4b5931c75063c7e22  (2026-10-05)
    path        packages/openapi-webhooks/generated/api.github.com.json
    licence     MIT
    274 webhook keys across 76 event types, 459 component schemas

    curl -o api.github.com.json \
      https://raw.githubusercontent.com/octokit/openapi-webhooks/d9af91f9ddbad97e5b5765d4b5931c75063c7e22/packages/openapi-webhooks/generated/api.github.com.json
    sha256sum api.github.com.json
    # 375906eeeace26486c6aecf5869a5e5ad4bba72c6571481ef54fa8c1cada3aae  api.github.com.json

It is held here so that a rebuild and the tests that assert what the models
cover need no network. `scripts/rebuild_models.py` pins the same revision and
digest and refuses any content that does not match, whether it fetched it or was
pointed at this file, so the copy cannot drift from the pin silently.
