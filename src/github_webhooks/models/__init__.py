"""Typed payload models and the dispatch that selects one.

Nothing in this package may import the application: the typing has to be usable
without running the service (spec 0001).
"""

from __future__ import annotations

from .events import Event, UnmodelledEvent
from .registry import REGISTRY, dispatch_key, parse_event

__all__ = ["Event", "REGISTRY", "UnmodelledEvent", "dispatch_key", "parse_event"]
