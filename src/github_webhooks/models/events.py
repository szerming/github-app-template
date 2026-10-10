"""The typed shapes a delivery can take."""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict


class Event(BaseModel):
    """Base for every typed delivery payload.

    Models describe what GitHub sends, not what it promises (ADR 0001): unknown
    fields are kept, and nothing here can refuse a delivery.
    """

    model_config = ConfigDict(extra="allow")

    modelled: ClassVar[bool] = True


class UnmodelledEvent(Event):
    """A delivery whose event type has no dedicated model.

    The permanent fallback, not a stub: it is what happens to any event type the
    models do not cover, for the life of the service. It carries the raw payload
    so that a newly introduced GitHub event is visible rather than refused.
    """

    modelled: ClassVar[bool] = False

    payload: Any = None
