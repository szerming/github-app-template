"""The dispatch registry, and the one call a delivery enters through.

The published description carries no ``discriminator`` and keys payloads by
event+action, so this mapping is ours (ADR 0002) -- emitted by the same command
that emits the models, into :mod:`github_webhooks.models.generated`, so the two
cannot drift. Nothing here is hand-maintained.
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .events import Event, UnmodelledEvent
from .generated import DISPATCH

REGISTRY: dict[str, type[Event]] = DISPATCH


def dispatch_key(event_type: str, action: str | None) -> str:
    """The registry key for a delivery: its event header plus its action."""
    return f"{event_type}.{action}" if action else event_type


def parse_event(event_type: str, action: str | None, payload: Any) -> Event:
    """Turn a delivery into its typed event, or the Unmodelled Event fallback.

    The single front door (spec 0001): the handler uses it to produce the log
    record, and whatever comes next will use it instead.

    Both fallback paths are the lens rather than a gate (ADR 0001) -- a refused
    delivery is a lost one -- so neither a key with no model, nor a payload that is
    not a JSON object, nor a payload a model cannot type ever raises. A payload a
    model did try to type carries the error it raised, so the caller can log a
    shape the models cannot type differently from an event type they do not cover
    (spec 0001, user stories 26 and 32).
    """
    model = REGISTRY.get(dispatch_key(event_type, action))
    if model is None or not isinstance(payload, dict):
        return UnmodelledEvent(payload=payload)
    try:
        return model(**payload)
    except ValidationError as error:
        return UnmodelledEvent(payload=payload, validation_error=str(error))
