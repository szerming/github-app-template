#!/usr/bin/env python3
"""Rebuild the payload models from GitHub's published description.

One command, one artifact (spec 0001, user story 35: "a script that rebuilds the
models from a pinned upstream revision and records its digest, so that a rebuild
is reproducible and a silent upstream change fails loudly"):

    scripts/rebuild_models.sh              # fetch the pinned revision, rebuild
    scripts/rebuild_models.sh --offline    # rebuild from the vendored copy

The published description is Octokit's OpenAPI 3.1 rendering of GitHub's webhook
payloads (ADR 0002). Everything this script writes is derived from it:

- the models, scoped to the shapes reachable from the deliveries in ``SCOPE``;
- the dispatch table, which the description cannot supply because it carries no
  ``discriminator`` and keys payloads by event+action, so the mapping is ours and
  is emitted here rather than hand-maintained beside the models.

Three transformations are applied to the description before generation, each one
a decision recorded in the spec rather than a convenience:

- generation is scoped to the reference closure of the scoped deliveries'
  request bodies, so REST-API-only shapes are absent from the artifact;
- ``enum`` and ``const`` are dropped, so no generated model can refuse a value
  GitHub adds later;
- the ``uri``/``uri-template``/``email`` formats are dropped, so a URL stays a
  string and validation never rejects a payload over a formatting nicety.
  ``date-time`` is kept: timestamps are timezone-aware datetimes.

After generation, one deterministic post-process tightens the ``action`` on each
event+action model to its literal, and the dispatch table is appended. If a
regeneration changes the shape either step depends on, the script fails loudly
rather than emitting an artifact that quietly lost the property.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION_PATH = REPO_ROOT / "vendor" / "openapi-webhooks" / "api.github.com.json"
DEFAULT_OUTPUT = REPO_ROOT / "src" / "github_webhooks" / "models" / "generated.py"

UPSTREAM_REPOSITORY = "octokit/openapi-webhooks"
UPSTREAM_PATH = "packages/openapi-webhooks/generated/api.github.com.json"
UPSTREAM_REVISION = "d9af91f9ddbad97e5b5765d4b5931c75063c7e22"
UPSTREAM_DIGEST = "375906eeeace26486c6aecf5869a5e5ad4bba72c6571481ef54fa8c1cada3aae"
UPSTREAM_URL = (
    f"https://raw.githubusercontent.com/{UPSTREAM_REPOSITORY}"
    f"/{UPSTREAM_REVISION}/{UPSTREAM_PATH}"
)

# The deliveries this slice types (ticket #2). Ticket #3 removes the filter: the
# command is the same, only this tuple grows to every published key.
SCOPE: tuple[str, ...] = (
    "push",
    "pull-request-opened",
    "pull-request-review-submitted",
    "pull-request-closed",
)

# Formats that would make a model stricter than GitHub's own documentation.
DROPPED_FORMATS = frozenset({"uri", "uri-template", "email"})

SCHEMA_REF_PREFIX = "#/components/schemas/"


def class_name(component: str) -> str:
    """``webhook-pull-request-opened`` -> ``WebhookPullRequestOpened``.

    The name datamodel-codegen derives from a component name, so the dispatch
    table can name a class the rebuild also asserts exists.
    """
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[-_]", component))


# --------------------------------------------------------------------------- #
# The description
# --------------------------------------------------------------------------- #


def fetch_description() -> bytes:
    """The published description at the pinned revision, as bytes."""
    with urllib.request.urlopen(UPSTREAM_URL, timeout=60) as response:
        return bytes(response.read())


def read_description(path: Path) -> bytes:
    return path.read_bytes()


def verify_digest(content: bytes, origin: str) -> str:
    """Fail loudly when the content is not the revision this script pins.

    The digest is the whole point of the pin: without it a rebuild silently
    produces models from a description nobody chose.
    """
    digest = hashlib.sha256(content).hexdigest()
    if digest != UPSTREAM_DIGEST:
        raise SystemExit(
            f"{origin} is not the pinned description.\n"
            f"  pinned revision: {UPSTREAM_REVISION}\n"
            f"  expected sha256: {UPSTREAM_DIGEST}\n"
            f"  actual   sha256: {digest}\n"
            "Refusing to rebuild: the models would come from a description this "
            "script did not pin."
        )
    return digest


@dataclass(frozen=True)
class ScopedDelivery:
    """One delivery in scope, and what the generated code needs to know about it."""

    webhook_key: str
    event_type: str
    action: str | None
    component: str
    class_name: str
    dispatch_key: str


def dispatch_key(event_type: str, action: str | None) -> str:
    """The registry key for a delivery: its event header plus its action.

    The models package builds the same key at runtime from the same two values
    (``github_webhooks.models.registry``); the two cannot call each other -- the
    build tool cannot import the service, and the service must not import its
    build tool -- so the format is written twice and held together by a test that
    derives each key from the description and looks it up in the registry.
    """
    return f"{event_type}.{action}" if action else event_type


def dispatch_facts(document: dict[str, Any]) -> dict[str, ScopedDelivery]:
    """What the description says about each delivery in scope.

    The event type is the value GitHub's own ``X-Github-Event`` header example
    carries -- ``pull-request`` in the key is ``pull_request`` in the header --
    and the action is the single value the payload schema enumerates, so both
    come from the description rather than from a table kept beside it.
    """
    webhooks = document.get("webhooks", {})
    facts: dict[str, ScopedDelivery] = {}
    for key in SCOPE:
        if key not in webhooks:
            raise SystemExit(
                f"the published description has no {key!r} webhook: the pinned "
                "revision no longer keys this delivery the way the scope assumes"
            )
        operation = webhooks[key].get("post")
        if not isinstance(operation, dict):
            raise SystemExit(f"the {key!r} webhook has no POST operation")
        event_type = _header_example(operation, "X-Github-Event")
        component = _request_body_ref(operation, key)
        action = _action_literal(document, component, key)
        facts[key] = ScopedDelivery(
            webhook_key=key,
            event_type=event_type,
            action=action,
            component=component,
            class_name=class_name(component),
            dispatch_key=dispatch_key(event_type, action),
        )
    return facts



def _header_example(operation: dict[str, Any], name: str) -> str:
    for parameter in operation.get("parameters", []):
        if str(parameter.get("name", "")).lower() == name.lower():
            example = parameter.get("example")
            if isinstance(example, str) and example:
                return example
    raise SystemExit(
        f"the {name!r} header example is missing from a scoped webhook: the "
        "event type in the dispatch key would be a guess"
    )


def _request_body_ref(operation: dict[str, Any], key: str) -> str:
    content = operation.get("requestBody", {}).get("content", {})
    for media_type, body in content.items():
        ref = body.get("schema", {}).get("$ref")
        if isinstance(ref, str) and ref.startswith(SCHEMA_REF_PREFIX):
            return ref[len(SCHEMA_REF_PREFIX) :]
        raise SystemExit(
            f"the {key!r} webhook's {media_type} body is not a schema reference "
            f"({ref!r}): the closure cannot be computed from it"
        )
    raise SystemExit(f"the {key!r} webhook publishes no request body")


def _action_literal(document: dict[str, Any], component: str, key: str) -> str | None:
    """The one value the payload's ``action`` enumerates, if it enumerates one."""
    schema = document["components"]["schemas"][component]
    action = schema.get("properties", {}).get("action")
    if action is None:
        return None
    values = action.get("enum")
    if not isinstance(values, list) or len(values) != 1 or not isinstance(values[0], str):
        raise SystemExit(
            f"the {key!r} payload's action is not a single published value "
            f"({values!r}): a literal cannot be pinned to it"
        )
    return values[0]


def schema_closure(document: dict[str, Any], roots: Iterator[str]) -> set[str]:
    """Every shape reachable from ``roots`` through reference, as schema names.

    A shape only the REST API uses is not reachable from a delivery's request
    body, so it never enters the artifact (spec 0001, user story 28).
    """
    schemas = document["components"]["schemas"]
    seen: set[str] = set()
    stack = list(roots)
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        if name not in schemas:
            raise SystemExit(f"the description references {name!r}, which it does not define")
        seen.add(name)
        for ref in _refs(schemas[name]):
            if not ref.startswith(SCHEMA_REF_PREFIX):
                raise SystemExit(
                    f"{name!r} references {ref!r}, which is not a schema: the "
                    "closure would be incomplete rather than closed"
                )
            stack.append(ref[len(SCHEMA_REF_PREFIX) :])
    return seen


def _refs(node: Any) -> Iterator[str]:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            yield ref
        for value in node.values():
            yield from _refs(value)
    elif isinstance(node, list):
        for value in node:
            yield from _refs(value)


def scoped_document(
    document: dict[str, Any], facts: Mapping[str, ScopedDelivery]
) -> dict[str, Any]:
    """The description reduced to the scoped deliveries' reachable shapes."""
    schemas = document["components"]["schemas"]
    closure = schema_closure(document, (delivery.component for delivery in facts.values()))
    reduced = {
        "openapi": document["openapi"],
        "info": document["info"],
        # The ``webhooks`` object contributes no code -- datamodel-codegen emits
        # models from ``components/schemas`` alone -- so it is dropped here and
        # the dispatch table is emitted from the facts read above.
        "components": {"schemas": {name: schemas[name] for name in sorted(closure)}},
    }
    return _loosen(reduced)


def _loosen(node: Any) -> Any:
    """Drop the constraints that would let a model refuse a real delivery."""
    if isinstance(node, dict):
        node.pop("required", None)
        node.pop("const", None)
        enum = node.pop("enum", None)
        if enum is not None and "type" not in node:
            node["type"] = _enum_type(enum)
        if node.get("format") in DROPPED_FORMATS:
            node.pop("format")
        for value in node.values():
            _loosen(value)
    elif isinstance(node, list):
        for value in node:
            _loosen(value)
    return node


def _enum_type(values: Any) -> str:
    if isinstance(values, list):
        kinds = {type(value) for value in values if value is not None}
        if kinds == {bool}:
            return "boolean"
        if kinds and kinds <= {int}:
            return "integer"
        if kinds and kinds <= {int, float}:
            return "number"
    return "string"


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #


def generate_models(document: dict[str, Any]) -> str:
    """Run datamodel-codegen over the scoped description."""
    from datamodel_code_generator import DataModelType, InputFileType, generate

    code = generate(
        document,
        input_file_type=InputFileType.OpenAPI,
        input_filename="api.github.com.json",
        output_model_type=DataModelType.PydanticV2BaseModel,
        # Every generated field optional: the description marks fields required
        # that GitHub's own example payloads omit (ADR 0001).
        force_optional_for_required_fields=True,
        extra_fields="allow",
        # Reproducible output: datamodel-codegen would otherwise stamp the file
        # header with the time it ran.
        disable_timestamp=True,
        target_python_version="3.13",
        base_class="github_webhooks.models.events.Event",
        formatters=["builtin"],
        use_annotated=False,
    )
    if not isinstance(code, str):  # pragma: no cover - a single module was asked for
        raise SystemExit("datamodel-codegen did not return one module")
    return code


_ACTION_FIELD = "    action: str | None = None"


def pin_actions(code: str, facts: Mapping[str, ScopedDelivery]) -> str:
    """Tighten ``action`` to its literal on each event+action model.

    Deterministic and checked: a class the description no longer produces, or a
    field line it no longer emits, fails the rebuild instead of quietly leaving
    the action a bare string.
    """
    wanted = {
        delivery.class_name: delivery.action
        for delivery in facts.values()
        if delivery.action is not None
    }
    lines = code.splitlines()
    current: str | None = None
    pinned: set[str] = set()
    for index, line in enumerate(lines):
        if line.startswith("class "):
            current = line[len("class ") :].split("(", 1)[0].strip()
            continue
        if current is not None and current in wanted and line.rstrip() == _ACTION_FIELD:
            lines[index] = f'    action: Literal["{wanted[current]}"] | None = None'
            pinned.add(current)
    unpinned = sorted(set(wanted) - pinned)
    if unpinned:
        raise SystemExit(
            "the action could not be pinned on "
            + ", ".join(unpinned)
            + f": no {_ACTION_FIELD.strip()!r} line was found in the generated class"
        )
    return _ensure_import("\n".join(lines) + "\n", "Literal")


def _ensure_import(code: str, name: str) -> str:
    """Add ``name`` to the module's ``typing`` import, sorted."""
    pattern = re.compile(r"^from typing import (?P<names>[^\n]+)$", re.MULTILINE)
    match = pattern.search(code)
    if match is None:
        raise SystemExit(f"the generated module imports nothing from typing: cannot add {name!r}")
    names = [item.strip() for item in match.group("names").split(",")]
    if name in names:
        return code
    names.append(name)
    return code[: match.start()] + f"from typing import {', '.join(sorted(names))}" + code[match.end() :]


def dispatch_table(facts: Mapping[str, ScopedDelivery]) -> str:
    """The registry, emitted beside the models so the two cannot drift."""
    rows = "\n".join(
        f'    "{delivery.dispatch_key}": {delivery.class_name},'
        for delivery in sorted(facts.values(), key=lambda delivery: delivery.dispatch_key)
    )
    return (
        "\n\nDISPATCH: dict[str, type[Event]] = {\n"
        f"{rows}\n"
        "}\n"
    )


def assert_classes_exist(code: str, facts: Mapping[str, ScopedDelivery]) -> None:
    for delivery in facts.values():
        if f"class {delivery.class_name}(" not in code:
            raise SystemExit(
                f"the generated module has no {delivery.class_name}: generation "
                "renamed the class the dispatch table points at"
            )


def render(code: str, facts: Mapping[str, ScopedDelivery], digest: str) -> str:
    """The committed artifact: provenance, the models, the dispatch table."""
    body = _strip_codegen_header(code)
    summary = ", ".join(
        f"{delivery.webhook_key} -> {delivery.dispatch_key} ({delivery.class_name})"
        for delivery in sorted(facts.values(), key=lambda delivery: delivery.webhook_key)
    )
    header = (
        '"""The generated payload models, and the dispatch table that selects one.\n'
        "\n"
        "Generated -- do not edit. Rebuild with ``scripts/rebuild_models.sh``.\n"
        "\n"
        f"Source:  {UPSTREAM_URL}\n"
        f"Digest:  sha256:{digest}\n"
        f"Scope:   {summary}\n"
        "\n"
        "The models describe what GitHub sends, not what it promises (ADR 0001):\n"
        "every field is optional and unknown fields are kept.\n"
        '"""\n'
        "\n"
        "from __future__ import annotations\n"
        "\n"
    )
    body = body.replace("from __future__ import annotations\n", "", 1)
    return header + body.lstrip("\n") + dispatch_table(facts)


def _strip_codegen_header(code: str) -> str:
    lines = code.splitlines()
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines) + "\n"


def rebuild(document: dict[str, Any], digest: str) -> str:
    facts = dispatch_facts(document)
    code = generate_models(scoped_document(document, facts))
    code = pin_actions(code, facts)
    assert_classes_exist(code, facts)
    return render(code, facts, digest)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild the payload models from GitHub's description.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--description",
        type=Path,
        help="read the description from this file instead of fetching it",
    )
    source.add_argument(
        "--offline",
        action="store_true",
        help=f"read the vendored description ({DESCRIPTION_PATH.relative_to(REPO_ROOT)})",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="where to write the artifact")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.description is not None:
        origin = str(args.description)
        content = read_description(args.description)
    elif args.offline:
        origin = str(DESCRIPTION_PATH.relative_to(REPO_ROOT))
        content = read_description(DESCRIPTION_PATH)
    else:
        origin = UPSTREAM_URL
        content = fetch_description()

    digest = verify_digest(content, origin)
    artifact = rebuild(json.loads(content), digest)

    args.output.write_text(artifact, encoding="utf-8")
    print(f"wrote {args.output} from {origin} (sha256:{digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
