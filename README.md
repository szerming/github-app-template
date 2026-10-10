# github-webhooks

The receiving surface for GitHub's webhook deliveries: every delivery arrives at one endpoint, is
proved to have come from GitHub, is typed against models generated from GitHub's own published
description of its payloads, and is recorded as one line of JSON.

## Objective

Everything worth doing about a GitHub delivery depends on knowing exactly what arrived, and "what
arrived" is 76 event types and 274 event+action payload shapes that GitHub changes without notice.
Reading the documentation is not the same as having it typed.

So this repository pins the shape down before anything acts on it:

- **One endpoint, one URL to configure.** `POST /` accepts a delivery; `GET /health` reports
  readiness.
- **Prove it came from GitHub.** HMAC-SHA256 over the exact request bytes
  (`X-Hub-Signature-256`), checked before anything else runs. Only the `sha256=` scheme is accepted.
- **Type it.** A pydantic model for every payload shape GitHub documents, generated from Octokit's
  OpenAPI 3.1 rendering of GitHub's webhook description (`octokit/openapi-webhooks`, MIT) and owned
  in this repository. Dispatch is on the delivery's `X-GitHub-Event` header plus the payload's
  `action`.
- **Record it.** Exactly one log record per delivery, carrying the payload as compact single-line
  JSON. This log is the product of V1.

**What it deliberately does not do (V1):** it acts on nothing. No persistence, no queue, no retries,
no deduplication, no calls back to GitHub, no authentication beyond the signature check, no
deployment. The models are a *lens*, never a gate — a delivery with no model, or one whose payload
no model can type, is still accepted and still logged. The single call future behaviour would enter
through already exists: `github_webhooks.models.parse_event`.

The scope, user stories and the reasoning behind each decision are in
[`docs/specs/0001-github-webhook-ingress.md`](docs/specs/0001-github-webhook-ingress.md) and
[`docs/adr/`](docs/adr/). The repository's vocabulary (Delivery, Event Type, Payload, Action,
Envelope, Unmodelled Event, Acknowledgement) is defined in [`CONTEXT.md`](CONTEXT.md).

> Note: the GitHub repository is named `github-app-template`; the Python package and distribution are
> `github_webhooks` / `github-webhooks`.

## How a delivery is handled

Fixed order, each step a decision rather than an accident:

1. Read the request body as **bytes**.
2. Verify `X-Hub-Signature-256` over exactly those bytes. Missing, wrong, unencodable or a legacy
   `sha1=` header → **401**, and nothing downstream runs.
3. Content type must be `application/json` → otherwise **415**, diagnosed as a webhook
   misconfiguration.
4. Parse the body leniently: an unparseable body is a delivery that concerns nothing, not a failure.
5. Dispatch on `X-GitHub-Event` + payload `action`, and validate against that one model.
6. Log one record; a payload no model could type is logged at WARNING with its validation error and
   the raw body.
7. Answer **202** with a small typed acknowledgement (`delivery_id`, `event_type`, `action`,
   `modelled`), and no timestamp, so a response is deterministic.

## Repository layout

    src/github_webhooks/
      app.py          the endpoint, the log record per delivery, the acknowledgement
      settings.py     configuration under explicit environment variable names
      signing.py      HMAC-SHA256 over the raw bytes; the legacy-header check
      __main__.py     `python -m github_webhooks` (wrapped by scripts/start.sh)
      models/
        events.py     Event base + the Unmodelled Event fallback
        registry.py   the dispatch key, and `parse_event` — the single front door
        generated.py  GENERATED: the payload models and the dispatch table (do not edit)
    scripts/
      start.sh             the one way to start the service (reads .env)
      forward.sh           forward live GitHub deliveries to the local service
      rebuild_models.sh    regenerate models/generated.py from the pinned description
      rebuild_models.py    the generator behind it
    tests/
      conftest.py          the harness: the real service on a free port, plus the vendored artifacts
      test_wire_contract.py  the HTTP contract, against a running process
      test_models.py         model fidelity: every published example payload, every published key
      test_generation.py     the rebuild: the pin, provenance, byte-reproducibility
      test_configuration.py  the refusal to start, the example env file, what must not be committed
      fixtures/example-payloads/  GitHub's published example payloads (273 files, 60 event types)
    vendor/openapi-webhooks/api.github.com.json   the pinned description the models come from
    docs/            spec 0001, ADRs, and the agent-facing notes in docs/agents/
    docs_github/     a local copy of the GitHub webhook documentation this was built against
    CONTEXT.md       the domain glossary

## Requirements

- **Python 3.13** — pinned in `.python-version`.
- **[uv](https://docs.astral.sh/uv/)** — dependency and environment management; the lockfile is
  committed.
- **The GitHub CLI (`gh`) with the `webhook` extension** — only for the live local delivery loop
  (see "Drive it with real GitHub deliveries"). `gh extension install cli/gh-webhook`.
- No database, no queue, no container needed.

## Developer setup

    git clone git@github.com:szerming/github-app-template.git
    cd github-app-template
    uv sync                     # creates .venv and installs the project + the dev dependency group
    cp .env.example .env        # then fill in a secret (below)

Generate the webhook secret — the same string you will later configure on GitHub's side:

    openssl rand -hex 32

Put it in `.env` as `WEBHOOK_SECRET=...`. `.env` is git-ignored (`.env.example` is committed and
names every variable); do not commit a real secret.

### Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `WEBHOOK_SECRET` | — (required) | The secret GitHub signs deliveries with. The service **refuses to start** when it is missing *or* empty, naming the variable: an empty secret would verify every forgery. |
| `HOST` | `127.0.0.1` | Address the service binds. |
| `PORT` | `8000` | Port the service binds. |
| `LOG_LEVEL` | `INFO` | `DEBUG`/`INFO`/`WARNING`/`ERROR`. `INFO` writes one record per delivery. |
| `GITHUB_REPO` | `szerming/github-app-template` | Used by `scripts/forward.sh` only — the repo whose live deliveries are forwarded. |
| `WEBHOOK_EVENTS` | `*` | Used by `scripts/forward.sh` only — which event types to forward. |

Two rules that trip people up:

- **Every variable is read under an explicit name** (a `validation_alias`), so an unrelated
  machine-wide variable such as `PORT` cannot be picked up by a field name. `PORT` here *is* the
  documented port variable, which is intentional.
- **The environment wins over `.env`.** `scripts/start.sh` loads `.env` only for variables that are
  not already set — including one that is set to the empty string — so
  `WEBHOOK_SECRET=... PORT=9999 scripts/start.sh` is what the process actually uses. This is what
  makes the tests (and the forwarding loop) able to control the secret and the port.

## Running the tests

    uv run pytest                 # add --no-sync to skip re-syncing first
    # or, with the project's own interpreter:
    .venv/bin/python -m pytest

40 tests, about 20 seconds, and **hermetic** — no network, nothing to start by hand. The suite
starts the service as a real process on a free port *through `scripts/start.sh`*, so the path a
developer runs by hand is the path that is covered, and asserts only what the outside shows: HTTP
status codes and the lines the process logs.

What each module covers:

- `test_wire_contract.py` — a signed delivery is answered 202 and logged; GitHub's published
  signature vector is recomputed in the test and accepted; no header, a wrong secret, a signature
  valid for other bytes, a non-ASCII header, the legacy `sha1=` header and a forged
  legacy-labelled delivery are each refused correctly and refused *distinguishably*; a non-JSON
  content type is 415; an unparseable body is accepted and logged raw; exactly one compact
  single-line record per delivery.
- `test_models.py` — every one of the 274 published keys resolves to a class, and every published
  example payload validates against the model it dispatches to (coverage is a number, not an
  opinion; the three examples that are not typed are named, with the reason).
- `test_generation.py` — the rebuild refuses a description that is not the pinned revision and names
  both digests; two rebuilds are byte-identical; the committed artifact is what the pinned
  description produces.
- `test_configuration.py` — the service refuses to start with the secret absent or empty; the example
  env file names every variable; `.env` is ignored *and* untracked.

There is no network test in the suite by design: forwarding live GitHub events is a demo, not the
gate. See "Drive it with real GitHub deliveries".

### Rebuilding the payload models

`src/github_webhooks/models/generated.py` is generated — never edit it.

    scripts/rebuild_models.sh              # fetch the pinned revision, verify its digest, rebuild
    scripts/rebuild_models.sh --offline    # rebuild from the vendored copy (no network)

The script pins one upstream revision and digest of `octokit/openapi-webhooks`; anything that does
not match fails loudly, so the committed models cannot drift from the description they name. It
emits *both* the models and the dispatch table, so the two cannot drift either. `--description` and
`--output` override the input and destination (used by the tests). Output is ~34,500 lines / ~1.2 MB
covering 274 dispatch entries across 76 event types.

## Running the application locally

One command, from the repository root, reading `.env`:

    scripts/start.sh

It prints the bound address and then one JSON record per delivery. Endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/` | The delivery endpoint. Configure this URL on GitHub's side. |
| `GET` | `/health` | Readiness. Returns `{"status":"ok"}`. |

A record looks like this (one greppable line, `LEVEL: {json}`):

    INFO: {"delivery_id":"1111-2222","event_type":"issues","action":"opened","sender":"smlee","repository":"szerming/github-app-template","modelled":true,"model":"WebhookIssuesOpened","payload":{...}}

An unmodelled or untypeable delivery adds a WARNING record carrying `unmodelled`
(`validation-failed` when a model was tried and failed) plus the raw body, and is still acknowledged.
Set `LOG_LEVEL=WARNING` to silence the per-delivery records; the 202 and its `modelled` flag still
tell you whether a model typed the payload.

### Post one delivery by hand

The service accepts only correctly signed requests, so sign the body with the same secret:

    secret=...                                   # the WEBHOOK_SECRET the service is running with
    body='{"action":"opened","issue":{"number":1},"repository":{"full_name":"szerming/github-app-template"},"sender":{"login":"smlee"}}'

    curl -i http://127.0.0.1:8000/ \
      -H "Content-Type: application/json" \
      -H "X-GitHub-Event: issues" \
      -H "X-GitHub-Delivery: 1111-2222" \
      -H "X-Hub-Signature-256: sha256=$(printf '%s' "$body" | openssl dgst -sha256 -hmac "$secret" | awk '{print $2}')" \
      --data "$body"

Expected: `202 Accepted` and
`{"delivery_id":"1111-2222","event_type":"issues","action":"opened","modelled":true}`.
Any other secret gives `401`, and a body sent as form data gives `415`.

## Wiring GitHub to the service

Three ways, in increasing order of GitHub-side setup. Pick the one that matches what you are doing;
they are independent, and the forwarding loop (C) needs no GitHub configuration at all.

### A. Register a GitHub App (the shape this repository is a template for)

Do this when you want GitHub to deliver to a real, reachable service with the App identity attached.

1. Go to **Settings → Developer settings → GitHub Apps → New GitHub App**
   (<https://github.com/settings/apps/new>). For an organization, use the organization's
   **Settings → Developer settings → GitHub Apps**.
2. **GitHub App name** and **Homepage URL**: anything sensible.
3. **Webhook**: tick **Active**.
4. **Webhook URL**: the publicly reachable `https://…/` of the deployed service. GitHub must be able
   to reach it over the internet — `http://localhost` is *not* reachable, which is exactly why
   option C exists for local work.
5. **Webhook secret**: the same value as `WEBHOOK_SECRET`. A mismatch means every delivery takes the
   401 path instead of the accept path.
6. **Permissions**: this service *receives* only and makes no API calls, so read-only is enough. A
   GitHub App must hold at least read-level access for the permission that owns each event it
   subscribes to; the ones most people want:

   | Event(s) | Permission (read-level) |
   | --- | --- |
   | `push`, `create`, `delete`, `fork`, `gollum`, `release`, `repository_dispatch`, `workflow_dispatch` | Contents |
   | `issues`, `issue_comment` | Issues |
   | `pull_request`, `pull_request_review`, `pull_request_review_comment`, `pull_request_review_thread` | Pull requests |
   | `label`, `public`, `repository`, `star`, `watch` | Metadata |
   | `status` | Commit statuses |
   | `workflow_run`, `workflow_job` | Actions |
   | `check_run`, `check_suite` | Checks (read lets you subscribe; `requested`/`rerequested` need write, and write subscribes you automatically) |
   | `installation`, `installation_repositories`, `github_app_authorization`, `ping` | none — these are delivered to the App itself, with no permission needed |

   Every event's exact requirement is listed on GitHub's webhook events page; a copy is vendored at
   `docs_github/events_page.html`, and the authoritative URL is
   <https://docs.github.com/en/webhooks/webhook-events-and-payloads>.
7. **Subscribe to events**: tick the events you want delivered. They must be covered by the
   permissions above, or GitHub will not deliver them.
8. **Where can this GitHub App be installed**: "Only on this account" for a private template.
9. **Create GitHub App**.
10. **Install it**: on the App's page, **Install App** → choose the account → **Only select
    repositories** → pick the repository (e.g. `szerming/github-app-template`). The App's webhook
    only receives events from repositories it is installed on. Installing sends the `installation`
    event, so it is the first thing you can watch land in the log.
11. **Verify**: on the App's page, **Advanced → Recent Deliveries** shows every delivery, its
    response code and, with **Redeliver**, a replay. You can also redeliver from a repository's
    **Settings → Webhooks → Advanced**. A configured webhook also receives a `ping` delivery
    immediately — that is the "the loop is live" signal, and it carries `hook`/`zen` rather than an
    event you caused.

Two things this service does not need yet, but the App registration gives you anyway: the **App
ID**, the **private key**, and each installation's ID. V1 makes no outbound calls, so nothing reads
them; they are what a later slice will need to authenticate as the App and report work back onto
GitHub. Keep them out of the repository.

### B. A repository or organization webhook

No App required, and fine for a single repo — but the payloads carry no App identity.

1. Repository: **Settings → Webhooks → Add webhook** (you need admin on the repo). Organization:
   **Organization Settings → Webhooks**.
2. **Payload URL**: the same `https://…/` as above.
3. **Content type**: **`application/json`**. This is not cosmetic — anything else is refused with
   415 so the misconfiguration is diagnosed rather than read as an unknown event type.
4. **Secret**: the same value as `WEBHOOK_SECRET`.
5. **Which events**: "Send me everything", or individual events.
6. **Add webhook**, then watch **Recent Deliveries** and expect an immediate `ping`.

### C. Drive it with real GitHub deliveries (local development, no public URL)

A local service has no public URL, so GitHub cannot reach it directly. The `gh webhook` extension
creates a *temporary* webhook on the repository and forwards its live deliveries to your local
service, signed with the secret you give it — which must be the one the service verifies with.

    gh extension install cli/gh-webhook     # once
    gh auth login                           # the forwarder is live and needs an authenticated gh
    scripts/forward.sh                      # reads .env: secret, host, port, GITHUB_REPO, WEBHOOK_EVENTS

which is exactly:

    gh webhook forward --repo="$GITHUB_REPO" --events="$WEBHOOK_EVENTS" \
        --secret="$WEBHOOK_SECRET" --url="http://$HOST:$PORT/"

What to expect and what the loop can and cannot do:

- It is **live**: something must actually happen on the repository, and the forwarder must not be
  the CI gate. The hermetic suite stays the gate; this loop is the demo.
- The moment it connects you get a **`ping`** delivery. Nothing was triggered, and `ping` is an event
  type you probably did not model — a live demonstration of the Unmodelled Event path in itself.
- **The forwarder never reports the per-delivery response.** Its output only says it connected, so
  the service's own log record is the only evidence a forwarded delivery got its 202. Watch the
  service's terminal, not the forwarder's.
- **Trigger something that leaves no state behind**: create and delete a label —

      gh label create demo-forward --repo "$GITHUB_REPO"
      gh label delete demo-forward --repo "$GITHUB_REPO" --yes

  — which fires two real deliveries and leaves the repository as it was.
- **Omitting `--url`** prints each event to stdout instead of forwarding it. That is the fastest way
  to see a payload GitHub publishes no example for; `--events='*'` forwards every event type.
- Use `--org=<org>` instead of `--repo=` to forward an organization webhook under the same flags.
- **GitHub will not let you approve your own pull request**, so a review-approval
  (`pull_request_review` with `state == "approved"`) delivery needs a second account. That is the one
  case where the vendored example payload in `tests/fixtures/` is the only coverage available.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `401` on every delivery, log line `{"rejected":"invalid-signature"}` | The secret the sender signs with is not the one the service verifies with. Compare the GitHub webhook's secret (or `--secret` on the forwarder) with the `WEBHOOK_SECRET` the service started with. |
| `401` with `{"rejected":"legacy-sha1-signature"}` | The webhook is configured to send the deprecated `X-Hub-Signature` (sha1) scheme, i.e. the current `sha256` header is absent. Reconfigure it to sha256 — and note that a forged delivery sending *both* headers cannot wear this benign label. |
| `415` with `{"rejected":"non-json-content-type"}` | The webhook's content type is `application/x-www-form-urlencoded`. Set it to `application/json`. |
| The delivery is acknowledged but logged at WARNING as `unmodelled: validation-failed` | The payload's shape is not one the models can type — a schema gap, logged with the error and the raw body. It is a log line, not a lost delivery. |
| `modelled: false` with no warning | The event type has no model at all (a newly introduced or undocumented event). Still accepted, still logged. |
| The service exits immediately, naming `WEBHOOK_SECRET` | The secret is unset or empty. Both are refusals by design, at startup rather than at the first delivery. |
| The port or secret used is not the one you exported | `.env` is being read for variables you did not set. The environment wins over the file; that is intentional. |
| Nothing arrives at all | Watch **Recent Deliveries** (App or repo webhook) or the forwarder's stdout. If the forwarder is silent nothing happened on the repository; if GitHub shows a failed delivery, the URL is unreachable or the content type is wrong. |

## Where to look next

- [`CONTEXT.md`](CONTEXT.md) — the domain glossary. Use these words (`Delivery`, `Event Type`,
  `Payload`, `Action`, `Envelope`, `Unmodelled Event`, `Acknowledgement`).
- [`docs/specs/0001-github-webhook-ingress.md`](docs/specs/0001-github-webhook-ingress.md) — scope,
  user stories, and the decisions behind the implementation.
- [`docs/adr/`](docs/adr/) — why the models are generated from GitHub's published description and
  why they are a lens rather than a gate.
- [`vendor/openapi-webhooks/README.md`](vendor/openapi-webhooks/README.md) and
  [`tests/fixtures/example-payloads/README.md`](tests/fixtures/example-payloads/README.md) — the
  pinned revision, digest and provenance of the vendored artifacts.
- [`docs_github/`](docs_github/) — a local copy of the GitHub webhook documentation (creating,
  validating, handling, redelivering, troubleshooting) this was built against.
- [`AGENTS.md`](AGENTS.md) — agent-facing notes: the issue tracker, triage labels, and the local
  webhook-testing loop.
