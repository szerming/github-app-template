# Spec 0001 — GitHub webhook ingress, V1

Status: ready for implementation
Glossary: `CONTEXT.md` (Delivery, Event Type, Payload, Action, Envelope, Unmodelled Event, Acknowledgement)
Decisions this spec implements: `docs/adr/0001-payload-models-are-a-lens-not-a-gate.md`, `docs/adr/0002-models-are-generated-from-githubs-openapi-spec.md`

## Problem Statement

GitHub sends webhook deliveries describing things that happened, and everything I might want to do about them depends on knowing exactly what arrives. GitHub documents 76 event types and 274 event+action payload shapes, and it changes them without notice. Reading that documentation is not the same as having it typed: hand-writing the shapes against a moving target is a way to be wrong slowly, and there is currently no code here to be wrong with — the project is an empty scaffold.

What I want first is not behaviour. It is the delivery itself, typed and recorded, so that the decision about what to do with it is made against real payloads rather than against the documentation's summary of them.

## Solution

An ingress that accepts GitHub deliveries, proves they came from GitHub, types them against models generated from GitHub's own published description, writes them to the log, and acknowledges them. It does nothing else, and it acts on nothing.

Every event type GitHub documents has a model. A delivery whose event type has no model, or whose payload does not fit one, is still accepted and still logged — the log is the product of V1.

Behaviour on top of the deliveries is a later decision. The single call one would enter through is `parse_event`, which is why V1 already has it: the handler uses it to produce the log record, and whatever comes next will use it instead.

## Scope

In scope for V1:

- One delivery endpoint and one health endpoint.
- HMAC-SHA256 verification of the delivery against the raw request bytes.
- A JSON-only content-type contract, with the misconfiguration diagnosed rather than absorbed.
- Lenient body parsing: an unparseable body is a delivery that concerns nothing, not a failure.
- Generated, owned pydantic models covering every documented event type, with dispatch on the delivery's event header plus the payload's action.
- An Unmodelled Event path: accepted, raw payload retained, never a refusal.
- One log record per delivery, carrying the payload.
- A typed acknowledgement, and the settings and scripts needed to run and rebuild the whole thing.

Out of scope for V1 is in its own section below.

## User Stories

Receiving and acknowledging:

1. As the service operator, I want GitHub's deliveries accepted at a single endpoint, so that I have one URL to configure.
2. As the service operator, I want the endpoint to answer inside GitHub's ten-second window, so that a delivery is never recorded as failed.
3. As the service operator, I want an accepted delivery answered with a 202 and a small typed body naming the delivery and its event type, so that I can see what arrived from a curl or from GitHub's Recent Deliveries view.
4. As a developer, I want that acknowledgement to carry no server timestamp, so that a response is deterministic and a test can assert it exactly.
5. As a developer, I want the acknowledgement to say whether the payload was modelled, so that a schema gap can be told from an unmodelled event without reading the log.
6. As the service operator, I want a health endpoint reporting readiness, so that a harness or a platform can know the service is serving before it sends anything.

Proving the delivery:

7. As the service operator, I want a delivery whose signature does not verify refused with 401, so that nobody else can write into my log.
8. As the service operator, I want a missing signature header refused exactly like a wrong one, so that there is one refusal path rather than a validation error for one case and a refusal for the other.
9. As the service operator, I want the legacy SHA-1 signature header refused, so that a weaker algorithm is never accepted for compatibility.
10. As a developer, I want the signature compared over the exact request bytes, so that a body which was parsed and re-encoded cannot be mistaken for one that verifies.
11. As a developer, I want a signature header that cannot be encoded refused with 401 rather than raising, so that forged input cannot turn a refusal into a 500.
12. As the service operator, I want the service to refuse to start without a webhook secret, so that a misconfigured deployment fails at startup instead of accepting anything that arrives.
13. As the service operator, I want the secret read through the service's own settings with explicit variable names, so that an unrelated machine-wide variable cannot be picked up by a field name.
14. As the service operator, I want a committed example environment file naming every variable, and the real one git-ignored, so that I know what to set and know what must not be committed.

The delivery's shape:

15. As the service operator, I want a non-JSON content type refused with 415 after the signature check, so that a webhook left configured as form-encoded is diagnosed as a configuration error rather than reported as an unknown event type.
16. As the service operator, I want an unparseable body accepted and logged raw rather than refused, so that a delivery is never lost to a parse error.
17. As the service operator, I want the legacy SHA-1 refusal logged distinctly from a forgery, so that a misconfiguration does not read as an attack.

Typing:

18. As a developer, I want a pydantic model for every event type GitHub documents, so that I never read a raw dictionary to find out what a delivery said.
19. As a developer, I want those models generated from GitHub's published description and owned in this repository, so that their provenance is a dated artifact rather than someone else's release cadence.
20. As a developer, I want every generated field optional, so that a payload omitting a field the published description requires is still typed instead of refused.
21. As a developer, I want unknown fields kept rather than dropped, so that a field GitHub adds is visible in my log before anyone models it.
22. As a developer, I want the action typed exactly on each event+action model, so that the action is not a stringly-typed guess.
23. As a developer, I want timestamps typed as timezone-aware datetimes and URLs left as strings, so that validation never rejects a payload over a formatting nicety.
24. As a developer, I want a delivery matched to its model by the event header plus the payload's action, so that the union of all 274 shapes is never asked to guess which one it is.
25. As a developer, I want a delivery whose event type has no model accepted as an Unmodelled Event carrying its raw payload, so that a newly introduced GitHub event is visible rather than refused.
26. As a developer, I want a payload that fails validation logged with its error and still acknowledged, so that a gap in the models is a log line rather than a lost delivery.
27. As a developer, I want the dispatch table generated by the same script as the models, so that it cannot drift from them.
28. As a developer, I want generation scoped to the shapes a delivery can carry, so that the artifact is webhook models rather than a copy of the whole REST API surface.

Seeing it:

29. As the service operator, I want exactly one log record per delivery carrying the delivery ID, event type, action, sender and repository, plus the payload as compact single-line JSON, so that one delivery is one greppable, parseable line.
30. As the service operator, I want the payload logged even though nothing consumes it yet, so that this service's only output is the evidence for designing what comes next.
31. As the service operator, I want the log level configurable from the environment with a sane default, so that I can turn the payload volume down without a code change.
32. As the service operator, I want a validation failure logged at WARNING together with the raw body, so that a modelling gap is visible without losing what GitHub sent.
33. As the service operator, I want logging to happen inline before the acknowledgement rather than after it, so that nothing has to be polled for once the POST returns.

Running and rebuilding:

34. As the service operator, I want one script that starts the service, and I want the tests to start it the same way, so that the path I run by hand is the path that is covered.
35. As a developer, I want a script that rebuilds the models from a pinned upstream revision and records its digest, so that a rebuild is reproducible and a silent upstream change fails loudly.
36. As a developer, I want the generated artifact and its generation script both committed, so that a reader can see what the models are and where they came from.
37. As a developer, I want no body-size cap invented below GitHub's own 25 MB, so that a delivery GitHub considers fine is never silently dropped.
38. As a developer, I want the models to import nothing from the application, so that the typing can be used without running the service.

Testing:

39. As a developer, I want the behavioural tests to assert only status codes and log lines from a real running process, so that they survive any refactor of the handler.
40. As a developer, I want GitHub's published signature vector recomputed inside the test rather than stored, so that agreement between my test and my server cannot hide a wrong algorithm.
41. As a developer, I want every published example payload asserted against the model it dispatches to, so that model coverage is a number rather than an opinion.
42. As a developer, I want a structural test asserting every key in the published description resolves to a class, so that a generation which silently dropped a shape fails the build.
43. As a developer, I want the example payloads vendored rather than fetched, so that the tests do not depend on the network.

## Implementation Decisions

Delivery handling is a fixed order, and each step is a decision rather than an accident: read the raw bytes, verify, check the content type, parse leniently, dispatch, validate, log, acknowledge.

Signature verification:

- The check is over the request bytes as received, before any parsing. Nothing downstream of it runs for input that did not verify.
- Both sides of the comparison are encoded to bytes; an unencodable header is simply invalid. Comparison is constant time.
- Only the `sha256=` scheme is accepted. A missing header and a wrong signature are the same refusal: 401, never a request-validation error.
- The legacy `sha1` header is refused and logged with its own distinct warning, so that a webhook configured before this service existed is diagnosable.

Acknowledgement:

- A pydantic response model, not an ad-hoc dictionary, carrying the delivery ID, the event type, the action when there is one, and a boolean saying whether the payload was modelled. No timestamp: it is the one field that would make responses non-deterministic.
- 202 Accepted. GitHub reads only the status, so the body exists for the operator and the tests.

Logging:

- Inline in the handler, not handed to a background task. The handoff pattern exists to protect a ten-second acknowledgement window from slow work, and a log write is not slow work; making it a background task would only introduce a race for every test to poll around.
- One record per delivery at INFO: delivery ID, event type, action, sender login, repository full name, and the payload as compact single-line JSON. The failure paths add the validation error and the raw body at WARNING.
- Level configurable from the environment, defaulting to INFO.

Settings:

- Read through `pydantic-settings` with explicit environment aliases, so that a bare host/port/secret field cannot silently pick up an unrelated machine-wide variable.
- Startup fails when the secret is absent. A committed example environment file names every variable, including the non-secret ones; the real file is git-ignored.

Models:

- Generated from GitHub's published OpenAPI description of the webhook payloads, and owned in this repository. Rationale, the sources considered, and why a library was not adopted: ADR 0002.
- Generated with every field optional. Rationale: ADR 0001 — the models describe what GitHub sends, not what it promises.
- Generation is scoped to the shapes reachable from the published webhook request bodies, so REST-API-only object shapes are not carried into the artifact.
- A deterministic post-process step tightens the action on each event+action model to its literal value, and a test asserts it, so that a regeneration cannot silently revert it.
- The dispatch registry is emitted by the same script as the models. The published description contains no discriminator, so this mapping is ours and must not be hand-maintained alongside the models.
- Dispatch is keyed on the event header plus the payload's action. The fallback, for an unmatched key and for a payload that fails validation, is an Unmodelled Event carrying the raw payload.
- Type richness: timezone-aware datetimes for timestamps; strings for URLs and actions, with the exception of the pinned action literals; no URL types and no enums that could reject a value GitHub adds later.
- Unknown fields are retained rather than dropped.

Structure:

- Modules: a settings module, the application, a signing module, and a models package holding the generated models, the generated registry, and the re-exported entry point.
- `parse_event(event_type, action, payload)` returning the typed event is the single front door. Nothing else calls it yet.
- One start script and one rebuild script. The console script entry point is removed: two ways to start the service is one too many, and the tests drive the script.

## Testing Decisions

What makes a good test here: it asserts external behaviour only — status codes returned and lines written to the log — and never imports the application's internals to inspect them. A test coupled to the handler's shape breaks on every refactor and proves nothing about the wire.

Seams — proposed, and the one thing in this spec I want confirmed rather than assumed:

1. The running service, started as a real process on a free port through the start script. This is the highest seam and carries the whole wire contract: signature acceptance and refusal, the content-type gate, the acknowledgement's shape and status, and what the log says for each case. A readiness probe against the health endpoint is part of the harness, not decoration.
2. The models package, exercised directly through its entry point, for the two claims that are about model fidelity rather than wire behaviour: that every published example payload validates against the model it dispatches to, and that every key in the published description resolves to a class.

Two seams rather than one, and the cost of that is stated plainly: the acceptance criterion for "the models are right" is a count over hundreds of fixtures, and asserting it through HTTP would mean computing a signature and scraping a log line per fixture to reach the same fact. A source scan asserting that the models import nothing from the application is not a seam; it is a property of the code, and it says so in its docstring.

No separate signing seam: signing is tested through the process, which is where its behaviour is observable and where a malformed header's 401-instead-of-500 is a real difference.

Prior art: there is none in this repository yet — these are the first tests. The two patterns worth naming are the vendor's published signature vector, recomputed in the test rather than stored, and the vendored bundle of published example payloads that make coverage countable.

One consequence of logging inline: the effect is present the moment the POST returns, so the tests assert immediately after the 202 rather than polling. That is a direct benefit of the logging decision and the reason no polling helper exists.

## Out of Scope

- Anything acting on a delivery. V1's only side effect is a log record.
- Persistence: no database, no queue, no delivery store.
- Retries and redelivery: GitHub does not redeliver a failed delivery automatically, and V1 does not add a mechanism of its own.
- Anything calling back to GitHub: App authentication, installation tokens, check runs, comments. An ingress that only receives is deliberately half a service.
- Delivery deduplication or idempotency. Nothing consumes a delivery, so nothing can be processed twice.
- Multiple endpoints, multiple repositories, or any multi-tenant routing.
- Authentication beyond the HMAC signature check. No OAuth, no API tokens, no inbound allow-list.
- Deployment: TLS termination, reverse proxy, container, platform. The service is a process on a port.
- Configuring the webhook on GitHub's side. Creating the webhook with a secret and the JSON content type is the operator's step, and it is the one thing this spec cannot do for them.
- Writing operational documentation beyond what the settings and scripts already encode.

## Further Notes

- The published description over-declares `required` relative to GitHub's own published example payloads — fields such as a repository's visibility, a pull request's auto-merge setting and a comment's reactions are required by the description and absent from the examples. Whether the examples are stale or the description is over-strict is not determinable from outside GitHub. Making every field optional means the question cannot bite, and the delivery log answers it empirically within a week of real traffic, because the acknowledgement's modelled flag and the log record separate "no model for this event type" from "the model rejected this payload".
- Field-level required information is discarded by the generation decision. The published description remains the only record of which fields GitHub always sends, and that is a real cost accepted in exchange for never refusing a delivery over it.
- No ADR was written for dispatching on the event header rather than building a discriminated union on the action. That choice fails the hard-to-reverse test — it is confined to the models package and cheap to change — and it is recorded as a consequence of ADR 0002 instead, because it follows from the chosen source having no discriminator.
- The URL types and enums that would make these models prettier are deliberately absent. A URL field that GitHub populates with a non-HTTP scheme, or an enum that meets a value added after generation, converts a typing convenience into a rejected delivery.
