"""The dispatch registry, and the one call a delivery enters through.

The published description carries no ``discriminator`` and keys payloads by
event+action, so this mapping is ours (ADR 0002). It is empty here: this slice
types nothing, so every delivery is an Unmodelled Event. A later slice emits the
table from the same script that emits the models, so the two cannot drift.
"""

from __future__ import annotations

from typing import Any

from .events import Event, UnmodelledEvent

REGISTRY: dict[str, type[Event]] = {}


def dispatch_key(event_type: str, action: str | None) -> str:
    """The registry key for a delivery: its event header plus its action."""
    return f"{event_type}.{action}" if action else event_type


def parse_event(event_type: str, action: str | None, payload: Any) -> Event:
    """Turn a delivery into its typed event, or the Unmodelled Event fallback.

    The single front door (spec 0001): the handler uses it to produce the log
    record, and whatever comes next will use it instead.
    """
    model = REGISTRY.get(dispatch_key(event_type, action))
    if model is None or not isinstance(payload, dict):
        return UnmodelledEvent(payload=payload)
    return model(**payload)
