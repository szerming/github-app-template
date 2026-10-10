"""The delivery endpoint, the health endpoint, and the log record per delivery."""

from __future__ import annotations

import json
import sys
from typing import Any

from fastapi import FastAPI, Request, Response
from loguru import logger
from pydantic import BaseModel

from . import signing
from .models import parse_event
from .settings import Settings, load_settings

DELIVERY_ID_HEADER = "X-GitHub-Delivery"
EVENT_TYPE_HEADER = "X-GitHub-Event"

# What a refusal is logged as: the reasons have to be distinguishable, so that a
# stale webhook configuration does not read as an attack.
REJECTED_LEGACY_SHA1 = "legacy-sha1-signature"
REJECTED_INVALID_SIGNATURE = "invalid-signature"
REJECTED_NON_JSON_CONTENT_TYPE = "non-json-content-type"


class Acknowledgement(BaseModel):
    """The JSON document returned for an accepted delivery.

    No timestamp: it is the one field that would make a response
    non-deterministic.
    """

    delivery_id: str
    event_type: str
    action: str | None = None
    modelled: bool


def _compact(value: Any) -> str:
    """Compact single-line JSON, so one record is one greppable line."""
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False, default=str)


def _log_refusal(rejected: str, **fields: Any) -> None:
    logger.warning("{}", _compact({"rejected": rejected, **fields}))


def _log_delivery(record: dict[str, Any]) -> None:
    logger.info("{}", _compact(record))


def _configure_logging(settings: Settings) -> None:
    logger.remove()
    logger.add(sys.stderr, level=settings.log_level.upper(), format="{level}: {message}")


def _raw_text(body: bytes) -> str:
    return body.decode("utf-8", errors="replace")


def _parse_json(body: bytes) -> dict[str, Any] | None:
    """Parse best-effort. An unparseable body is a delivery that concerns nothing."""
    try:
        value = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _nested(payload: dict[str, Any] | None, *path: str) -> Any:
    current: Any = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _is_json_content_type(content_type: str) -> bool:
    return content_type.split(";", 1)[0].strip().lower() == "application/json"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings if settings is not None else load_settings()
    _configure_logging(settings)

    app = FastAPI(title="GitHub webhook ingress")
    app.state.settings = settings

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/",
        status_code=202,
        response_model=Acknowledgement,
        response_model_exclude_none=True,
    )
    async def receive_delivery(request: Request) -> Acknowledgement | Response:
        # Take the request as bytes: the check is over exactly these, which is
        # what makes tampering the thing that is detected.
        body = await request.body()
        delivery_id = request.headers.get(DELIVERY_ID_HEADER.lower(), "")
        event_type = request.headers.get(EVENT_TYPE_HEADER.lower(), "")

        signature = request.headers.get(signing.SIGNATURE_HEADER.lower())
        legacy = request.headers.get(signing.LEGACY_SIGNATURE_HEADER.lower())
        if not signing.signature_is_valid(settings.webhook_secret, body, signature):
            # Keyed on the sha256 header being absent, not merely on the legacy
            # one being present: otherwise a forgery that also sends a sha1
            # header wears the benign label and a real attack reads as a stale
            # configuration.
            if signing.is_legacy_signature(legacy) and signature is None:
                _log_refusal(
                    REJECTED_LEGACY_SHA1,
                    delivery_id=delivery_id,
                    reason=(
                        "the deprecated sha1 signature scheme is not accepted; "
                        "reconfigure the webhook to sha256"
                    ),
                )
            else:
                _log_refusal(
                    REJECTED_INVALID_SIGNATURE,
                    delivery_id=delivery_id,
                    reason="signature missing or not verified",
                )
            return Response(status_code=401)

        content_type = request.headers.get("content-type", "")
        if not _is_json_content_type(content_type):
            _log_refusal(
                REJECTED_NON_JSON_CONTENT_TYPE,
                delivery_id=delivery_id,
                content_type=content_type,
                raw_body=_raw_text(body),
            )
            return Response(status_code=415)

        payload = _parse_json(body)
        action = payload.get("action") if isinstance(payload, dict) else None
        event = parse_event(event_type, action, payload)

        record: dict[str, Any] = {
            "delivery_id": delivery_id,
            "event_type": event_type,
        }
        if action is not None:
            record["action"] = action
        record["sender"] = _nested(payload, "sender", "login")
        record["repository"] = _nested(payload, "repository", "full_name")
        record["modelled"] = event.modelled
        # The payload is the product of V1: written even though nothing consumes
        # it yet. A body that is not JSON is logged raw rather than dropped.
        record["payload"] = payload if payload is not None else _raw_text(body)
        _log_delivery(record)

        return Acknowledgement(
            delivery_id=delivery_id,
            event_type=event_type,
            action=action,
            modelled=event.modelled,
        )

    return app


app = create_app()
