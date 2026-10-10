"""Model fidelity: the claims that are about the models rather than the wire.

This is the second of spec 0001's two seams. Asserting these facts through HTTP
would mean computing a signature and scraping a log line per fixture to reach the
same answer, so the models package is exercised directly, through its entry
point, and the published description and example payloads it is checked against
are the vendored ones, so nothing here needs the network.
"""

from __future__ import annotations

import json
import typing

import pytest
from conftest import (
    GENERATED_MODULE_PATH,
    delivery_of,
    description,
    dispatch_key,
    example_manifest,
    example_payload,
    rebuild_module,
    sha256,
)
from pydantic import BaseModel, ValidationError

from github_webhooks.models import REGISTRY, Event, UnmodelledEvent, generated, parse_event

# Shapes the pinned description publishes that no scoped delivery can reach. If
# the scope ever widened to the whole document, these are what would appear.
UNREACHABLE_WITNESSES = (
    "webhook-issues-opened",
    "check-run-with-simple-check-suite",
    "code-of-conduct",
)


def examples() -> list[dict]:
    entries = example_manifest()["examples"]
    assert entries, "no vendored example payloads: the coverage claims below would be vacuous"
    return entries


# --- what the description says a delivery can carry --------------------------


def test_the_vendored_examples_are_the_published_ones():
    """An edited fixture would change what the models are said to cover."""
    for entry in examples():
        assert sha256(example_payload(entry)) == entry["sha256"], entry["path"]


def test_every_published_example_is_typed_by_the_model_it_dispatches_to():
    for entry in examples():
        event_type, action = delivery_of(entry)
        key = dispatch_key(event_type, action)
        model = REGISTRY[key]

        event = parse_event(event_type, action, json.loads(example_payload(entry)))

        assert isinstance(event, model), f"{entry['path']} -> {type(event).__name__}, wanted {model.__name__}"
        assert event.modelled is True


def test_every_key_the_description_publishes_for_the_scoped_deliveries_has_an_entry():
    """The table is emitted beside the models, so a dropped key fails the build
    rather than being hand-maintained back into a file nobody regenerates."""
    module = rebuild_module()
    stem = module.model_stem(description())

    assert set(stem) == set(module.SCOPE)
    for facts in stem.values():
        assert facts["dispatch_key"] in REGISTRY, facts["dispatch_key"]
        assert issubclass(REGISTRY[facts["dispatch_key"]], Event)


def test_the_artifact_carries_only_the_shapes_the_scoped_deliveries_reach():
    module = rebuild_module()
    document = description()
    schemas = document["components"]["schemas"]
    stem = module.model_stem(document)
    reachable = module.schema_closure(document, (facts["component"] for facts in stem.values()))
    artifact = GENERATED_MODULE_PATH.read_text(encoding="utf-8")

    # Every shape a scoped delivery can reach is in the artifact ...
    for component in sorted(reachable):
        assert f"class {module.class_name(component)}(" in artifact, component

    # ... and a shape it cannot reach is not, though the description publishes it.
    for component in UNREACHABLE_WITNESSES:
        assert component in schemas
        assert component not in reachable
        assert f"class {module.class_name(component)}(" not in artifact, component


# --- the lens, not the gate --------------------------------------------------


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
    stem = rebuild_module().model_stem(document)
    by_key = {entry["webhook_key"]: entry for entry in examples()}

    for facts in stem.values():
        required = set(document["components"]["schemas"][facts["component"]].get("required", []))
        assert required, f"the description requires nothing for {facts['webhook_key']}"
        payload = json.loads(example_payload(by_key[facts["webhook_key"]]))
        stripped = {name: value for name, value in payload.items() if name not in required}

        assert REGISTRY[facts["dispatch_key"]](**stripped) is not None


def test_unknown_fields_are_retained():
    """A field GitHub adds is visible in the log before anyone models it."""
    entry = next(entry for entry in examples() if entry["webhook_key"] == "push")
    payload = json.loads(example_payload(entry))
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


def test_an_event_type_outside_the_scope_is_an_unmodelled_event():
    payload = {"action": "opened", "sender": {"login": "octocat"}}

    event = parse_event("issues", "opened", payload)

    assert isinstance(event, UnmodelledEvent)
    assert event.modelled is False
    assert event.payload == payload


# --- the action is a literal, not a stringly-typed guess ---------------------


def test_the_action_is_pinned_to_its_literal_on_each_event_action_model():
    """The post-process step of the rebuild, asserted where a regeneration that
    lost it would fail: the annotation, and the line the artifact carries."""
    module = rebuild_module()
    artifact = GENERATED_MODULE_PATH.read_text(encoding="utf-8")
    pinned = 0

    for facts in module.model_stem(description()).values():
        action = facts["action"]
        if action is None:
            continue
        pinned += 1
        model = REGISTRY[facts["dispatch_key"]]

        assert typing.get_args(model.model_fields["action"].annotation) == (
            typing.Literal[action],
            type(None),
        )
        assert f'    action: Literal["{action}"] | None = None' in artifact
        with pytest.raises(ValidationError):
            model.model_validate({"action": "synchronize"})

    assert pinned, "the scoped deliveries include no event+action model to pin"
    # The delivery with no action has no action field at all, so the pin is
    # targeted rather than applied everywhere.
    assert "action" not in REGISTRY["push"].model_fields
