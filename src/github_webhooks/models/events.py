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
    """A delivery whose payload no model typed.

    The permanent fallback, not a stub: it is what happens to any event type the
    models do not cover, and to a payload they cover but cannot type, for the life
    of the service. It carries the raw payload so that a newly introduced GitHub
    event, or a field whose shape changed, is visible rather than refused.
    """

    modelled: ClassVar[bool] = False

    payload: Any = None

    # Why the fallback was taken, when there was something to try: the validation
    # error a model raised. ``None`` means no model covers this delivery's key,
    # which is a different fact -- a shape the models cannot type rather than an
    # event type they do not cover -- and the log has to tell them apart.
    validation_error: str | None = None
