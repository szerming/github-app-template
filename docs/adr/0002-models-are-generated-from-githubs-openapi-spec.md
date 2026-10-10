# Payload models are generated from GitHub's published OpenAPI spec, and owned in-repo

GitHub publishes a machine-readable description of every webhook payload: the OpenAPI 3.1 document that Octokit generates from GitHub's own REST description (`octokit/openapi-webhooks`, MIT, 274 event+action operations across 76 event types, self-contained). We generate pydantic v2 models from it, commit the generated module, and keep a script that rebuilds it from a pinned upstream commit. The models are generated with every field optional, which is ADR 0001's posture applied to the generator's flags: the models describe what GitHub sends, not what it promises.

## Considered Options

- **Hand-write the models.** Total control over quality, at the cost of maintaining 274 payload shapes against a target that moves without notice.
- **Depend on a library.** `githubkit` is the strongest candidate — 160 typed webhook models, pydantic v2, actively maintained — but it drags in a whole REST client and its licence is undeclared in its package metadata. `github-webhook-types` has 260 payload models but is at version 0.0.1a3. `github-events` ships 278 classes with no pydantic models at all (TypedDict-first). `gh-webhooks` is pydantic v1 and cannot be imported (a generated model has a field named `from`). `safir` covers six event types. `octomachinery` and PyGithub ship no incoming-payload models.
- **Generate from the deprecated `@octokit/webhooks-schemas` set** (draft-07, frozen 2024-10-03, 66 event types, npm-marked unsupported). The most directly codegen-friendly format, and stale.
- **Generate from GitHub's own REST description.** Its webhook payloads live under the vendor extension `x-webhooks`, which generic OpenAPI tooling ignores, so it needs preprocessing before it is a codegen input at all.
- **Generate from `octokit/openapi-webhooks`** (chosen). Standard OpenAPI 3.1 with a real top-level `webhooks` object, all references internal (so no cross-file resolution), coverage identical to GitHub's authoritative spec.

## Consequences

- The published spec contains no `discriminator` keyword and keys payloads by event+action, so the mapping from a delivery to its model is ours: a registry keyed on the delivery's event header plus the payload's action. Nothing about that mapping can be generated from the spec's own structure.
- Field-level `required` information is discarded by generation (see ADR 0001), so the spec remains the only record of which fields GitHub always sends.
- The generated output is large — roughly 1.7 MB and 2,500 classes at full coverage — so it is a build artifact with a deterministic rebuild, not a surface anyone edits.
- A GitHub-side payload change reaches this repo only when someone re-runs the rebuild, and the rebuild is what records which upstream revision the models came from.
