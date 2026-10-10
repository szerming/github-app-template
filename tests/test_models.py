"""Model fidelity: the claims that are about the models rather than the wire.

This is the second of spec 0001's two seams. Asserting these facts through HTTP
would mean computing a signature and scraping a log line per fixture to reach the
same answer, so the models package is exercised directly, through its entry
point, and the published description and example payloads it is checked against
are the vendored ones, so nothing here needs the network.
"""

from __future__ import annotations

import ast
import json
import typing

import pytest
from conftest import (
    GENERATED_MODULE_PATH,
    REPO_ROOT,
    UNDOCUMENTED_EVENT_TYPE,
    delivery_of,
    description,
    example_entry,
    example_manifest,
    example_payload,
    rebuild_module,
    sha256,
)
from pydantic import BaseModel, ValidationError

from github_webhooks.models import (
    REGISTRY,
    Event,
    UnmodelledEvent,
    dispatch_key,
    generated,
    parse_event,
)

# The description is pinned, so how much it carries is a fact rather than a
# filter: every key GitHub documents is modelled, not a chosen subset.
PUBLISHED_KEYS = 274

# The published examples the models do not type, and there are three causes:
#
#   * ``check_run.rerequested`` -- the example carries naive timestamps, and a
#     timestamp is timezone-aware (spec 0001, user story 23);
#   * ``projects_v2_item.*`` -- the description's own header example for these
#     reads ``project-v2-item`` while GitHub sends ``projects_v2_item``, so the
#     delivery dispatches to a key no model covers;
#   * ``repository_dispatch.on-demand-test`` -- the description leaves
#     repository_dispatch's action open, because it is the caller's own event type.
#
# Reporting them is the point -- coverage is a number, not an opinion -- and every
# one is a delivery the lens records rather than refuses (ADR 0001).
EXPECTED_UNMODELLED = {
    ("check_run", "rerequested"),
    ("projects_v2_item", "archived"),
    ("projects_v2_item", "converted"),
    ("projects_v2_item", "created"),
    ("projects_v2_item", "edited"),
    ("projects_v2_item", "reordered"),
    ("projects_v2_item", "restored"),
    ("repository_dispatch", "on-demand-test"),
}

MODELS_PACKAGE = REPO_ROOT / "src" / "github_webhooks" / "models"


def examples() -> list[dict]:
    entries = example_manifest()["examples"]
    assert entries, "no vendored example payloads: the coverage claims below would be vacuous"
    return entries


# --- the vendored fixtures --------------------------------------------------


def test_the_vendored_examples_are_the_published_ones():
    """An edited fixture would change what the models are said to cover."""
    for entry in examples():
        assert sha256(example_payload(entry)) == entry["sha256"], entry["path"]


def test_the_vendored_examples_are_every_published_one():
    """A partial set would make every coverage claim below a claim about a subset."""
    assert len(examples()) == 273


# --- coverage is a number, not an opinion -----------------------------------


def test_every_published_example_is_typed_or_recorded_as_unmodelled():
    """Each published example ends in one of exactly two places.

    Either the model its delivery dispatches to types it, or it is recorded as an
    Unmodelled Event -- never refused, and never unaccounted for. The count in
    each bucket is the coverage number (spec 0001, user story 41).
    """
    typed: list[tuple[str, str | None]] = []
    unmodelled: list[tuple[str, str | None]] = []
    for entry in examples():
        event_type, action = delivery_of(entry)
        event = parse_event(event_type, action, json.loads(example_payload(entry)))
        (typed if event.modelled else unmodelled).append((event_type, action))

    report = f"{len(typed)}/{len(examples())} published examples typed, {len(unmodelled)} unmodelled"
    print(report)

    assert len(typed) + len(unmodelled) == len(examples())
    assert typed, "no published example was typed"
    assert set(unmodelled) == EXPECTED_UNMODELLED


# --- every key resolves to a real model class -------------------------------


def test_every_key_the_description_publishes_resolves_to_a_real_model_class():
    """A generation that silently dropped a shape fails here (spec 0001, story 42).

    Every key the description carries names a class the artifact defines, and the
    dispatch table points at that same class -- no key is left without a model.
    """
    module = rebuild_module()
    document = description()
    facts = module.dispatch_facts(document)

    assert len(document["webhooks"]) == PUBLISHED_KEYS
    assert len(facts) == PUBLISHED_KEYS

    for key, delivery in facts.items():
        model = getattr(generated, delivery.class_name, None)
        assert model is not None, f"{key} -> {delivery.class_name} is not in the artifact"
        assert issubclass(model, Event), key
        assert REGISTRY[delivery.dispatch_key] is model, key

    assert len(REGISTRY) == len({delivery.dispatch_key for delivery in facts.values()})


def test_the_artifact_carries_a_class_for_every_shape_a_delivery_can_reach():
    """Generation is scoped to the shapes reachable from the deliveries' bodies.

    At full coverage that closure is the description's whole schema set, so the
    ticket-#2 claim that REST-only shapes are absent has nothing left to exclude;
    what remains to assert is that every reachable shape is in the artifact.
    """
    module = rebuild_module()
    document = description()
    facts = module.dispatch_facts(document)
    schemas = document["components"]["schemas"]
    reachable = module.schema_closure(document, (delivery.component for delivery in facts.values()))
    artifact = GENERATED_MODULE_PATH.read_text(encoding="utf-8")

    assert reachable == set(schemas)
    for component in sorted(reachable):
        assert f"class {module.class_name(component)}(" in artifact, component


# --- the lens, not the gate -------------------------------------------------


def test_every_generated_field_is_optional():
    """The description marks fields required that GitHub's own examples omit, so
    a required field anywhere in the artifact is a delivery waiting to be lost."""
    models = [
        value
        for value in vars(generated).values()
        if isinstance(value, type)
        and issubclass(value, BaseModel)
        and value.__module__ == generated.__name__
    ]
    assert models

    for model in models:
        required = sorted(
            name for name, field in model.model_fields.items() if field.is_required()
        )
        assert not required, f"{model.__name__} requires {required}"


def test_a_payload_missing_the_fields_the_description_requires_still_validates():
    document = description()
    schemas = document["components"]["schemas"]
    facts = rebuild_module().dispatch_facts(document)
    by_key = {fact.dispatch_key: fact for fact in facts.values()}
    checked = 0

    for entry in examples():
        event_type, action = delivery_of(entry)
        key = dispatch_key(event_type, action)
        fact = by_key.get(key)
        if fact is None:
            continue
        required = set(schemas[fact.component].get("required", []))
        if not required:
            continue
        payload = json.loads(example_payload(entry))
        stripped = {name: value for name, value in payload.items() if name not in required}

        assert REGISTRY[key](**stripped) is not None
        checked += 1

    assert checked, "no published example exercised the description's required fields"


def test_unknown_fields_are_retained():
    """A field GitHub adds is visible in the log before anyone models it."""
    payload = json.loads(example_payload(example_entry("push")))
    payload["a_field_github_has_not_documented"] = {"nested": True}

    event = parse_event("push", None, payload)

    assert event.modelled is True
    assert event.model_dump()["a_field_github_has_not_documented"] == {"nested": True}


def test_a_payload_the_model_cannot_type_is_accepted_as_an_unmodelled_event():
    """A model stricter than the payload must never cost the delivery (ADR 0001)."""
    payload = {"ref": "refs/heads/main", "commits": "not the array the model expects"}

    event = parse_event("push", None, payload)

    assert isinstance(event, UnmodelledEvent)
    assert event.modelled is False
    assert event.payload == payload
    # A shape the models cannot type is a different fact from an event type they
    # do not cover, and the caller is given the difference to log.
    assert event.validation_error is not None
    assert "WebhookPush" in event.validation_error


def test_an_event_type_the_description_does_not_carry_is_an_unmodelled_event():
    payload = {"action": "opened", "sender": {"login": "octocat"}}

    event = parse_event(UNDOCUMENTED_EVENT_TYPE, "opened", payload)

    assert isinstance(event, UnmodelledEvent)
    assert event.modelled is False
    assert event.payload == payload
    # No model was tried, so there is no error to report.
    assert event.validation_error is None


# --- the action is a literal, not a stringly-typed guess --------------------


def test_the_action_is_pinned_to_its_literal_on_each_event_action_model():
    """The post-process step of the rebuild, asserted where a regeneration that
    lost it would fail: the annotation, and the line the artifact carries."""
    module = rebuild_module()
    artifact = GENERATED_MODULE_PATH.read_text(encoding="utf-8")
    pinned = 0

    for delivery in module.dispatch_facts(description()).values():
        action = delivery.action
        if action is None:
            continue
        pinned += 1
        model = REGISTRY[delivery.dispatch_key]

        assert typing.get_args(model.model_fields["action"].annotation) == (
            typing.Literal[action],
            type(None),
        )
        assert f'    action: Literal["{action}"] | None' in artifact
        with pytest.raises(ValidationError):
            model.model_validate({"action": f"not-{action}"})

    assert pinned, "the published deliveries include no event+action model to pin"
    # The delivery with no action has no action field at all, so the pin is
    # targeted rather than applied everywhere.
    assert "action" not in REGISTRY["push"].model_fields


# --- the typing stands alone ------------------------------------------------


def test_the_models_import_nothing_from_the_application():
    """A property of the code, not a seam: the typing has to be usable without
    running the service (spec 0001, user story 38), so the models package may
    import only from inside itself.
    """
    modules = sorted(MODELS_PACKAGE.glob("*.py"))
    assert modules

    offenders: list[tuple[str, str]] = []
    for module in modules:
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported = [node.module or ""]
            else:
                continue
            for name in imported:
                if name.startswith("github_webhooks.") and not name.startswith(
                    "github_webhooks.models"
                ):
                    offenders.append((module.name, name))

    assert offenders == []
