"""The wire contract of ticket #1, asserted against a real running process."""

from __future__ import annotations

import hashlib
import hmac
import json

from conftest import (
    DELIVERY_ID_HEADER,
    EVENT_TYPE_HEADER,
    JSON_CONTENT_TYPE,
    LEGACY_SIGNATURE_HEADER,
    SIGNATURE_HEADER,
    WEBHOOK_SECRET,
    Service,
    sign,
)

# GitHub's published validation vector. The digest is quoted from GitHub's own
# documentation, so the test pins the algorithm rather than agreeing with itself.
PUBLISHED_BODY = b"Hello, World!"
PUBLISHED_DIGEST = "757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"


def issue_payload(number: int = 7) -> bytes:
    return json.dumps(
        {
            "action": "opened",
            "sender": {"login": "octocat"},
            "repository": {"full_name": "octo/hello-world"},
            "issue": {"number": number},
        }
    ).encode("utf-8")


def push_payload() -> bytes:
    """A push carries no action at all: the payload is complete as it stands."""
    return json.dumps(
        {
            "ref": "refs/heads/main",
            "sender": {"login": "octocat"},
            "repository": {"full_name": "octo/hello-world"},
        }
    ).encode("utf-8")


# --- readiness --------------------------------------------------------------


def test_health_endpoint_reports_readiness(service: Service) -> None:
    status, _ = service.request("GET", "/health")
    assert status == 200


# --- acceptance -------------------------------------------------------------


def test_published_signature_vector_is_recomputed_and_accepted(service: Service) -> None:
    """Signing the documented body with the documented secret must reproduce the
    documented digest -- and the service itself must accept that delivery."""
    assert sign(WEBHOOK_SECRET, PUBLISHED_BODY) == "sha256=" + PUBLISHED_DIGEST

    status, _ = service.request(
        "POST",
        "/",
        PUBLISHED_BODY,
        {
            SIGNATURE_HEADER: sign(WEBHOOK_SECRET, PUBLISHED_BODY),
            "Content-Type": JSON_CONTENT_TYPE,
        },
    )
    assert status == 202


def test_a_signed_delivery_is_answered_202_naming_the_delivery(service: Service) -> None:
    status, ack = service.deliver(
        issue_payload(), event_type="issues", delivery_id="ack-1"
    )

    assert status == 202
    assert ack["delivery_id"] == "ack-1"
    assert ack["event_type"] == "issues"
    assert ack["action"] == "opened"
    # Nothing is typed yet, and that is the permanent fallback, not a stub.
    assert ack["modelled"] is False
    # No timestamp: a response a test can assert exactly.
    assert "timestamp" not in ack


def test_the_acknowledgement_omits_the_action_when_there_is_none(service: Service) -> None:
    status, ack = service.deliver(push_payload(), event_type="push", delivery_id="ack-2")

    assert status == 202
    assert ack["modelled"] is False
    assert "action" not in ack


# --- refusal ----------------------------------------------------------------


def test_no_signature_header_is_refused(service: Service) -> None:
    status, _ = service.deliver(
        issue_payload(), signature=False, delivery_id="refuse-missing"
    )
    assert status == 401


def test_a_wrong_secret_is_refused(service: Service) -> None:
    status, _ = service.deliver(
        issue_payload(), secret="not-the-secret", delivery_id="refuse-wrong-secret"
    )
    assert status == 401


def test_a_signature_valid_for_other_bytes_is_refused(service: Service) -> None:
    status, _ = service.request(
        "POST",
        "/",
        issue_payload(number=7),
        {
            SIGNATURE_HEADER: sign(WEBHOOK_SECRET, issue_payload(number=8)),
            "Content-Type": JSON_CONTENT_TYPE,
            DELIVERY_ID_HEADER: "refuse-other-bytes",
        },
    )
    assert status == 401


def test_the_legacy_sha1_header_is_refused_and_logged_distinctly(service: Service) -> None:
    body = issue_payload()
    legacy = "sha1=" + hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha1).hexdigest()

    status, _ = service.request(
        "POST",
        "/",
        body,
        {
            LEGACY_SIGNATURE_HEADER: legacy,
            "Content-Type": JSON_CONTENT_TYPE,
            DELIVERY_ID_HEADER: "refuse-legacy",
        },
    )
    assert status == 401

    forged, _ = service.request(
        "POST",
        "/",
        body,
        {
            SIGNATURE_HEADER: "sha256=" + "0" * 64,
            "Content-Type": JSON_CONTENT_TYPE,
            DELIVERY_ID_HEADER: "refuse-forgery",
        },
    )
    assert forged == 401

    legacy_reasons = {
        record["rejected"]
        for record in service.refused()
        if record.get("delivery_id") == "refuse-legacy"
    }
    forgery_reasons = {
        record["rejected"]
        for record in service.refused()
        if record.get("delivery_id") == "refuse-forgery"
    }
    # A stale webhook configuration must not read as an attack.
    assert legacy_reasons and forgery_reasons
    assert legacy_reasons.isdisjoint(forgery_reasons)


def test_a_signature_header_with_a_non_ascii_byte_is_refused(service: Service) -> None:
    status, _ = service.request(
        "POST",
        "/",
        issue_payload(),
        {
            SIGNATURE_HEADER: "sha256=\xe9",
            "Content-Type": JSON_CONTENT_TYPE,
            DELIVERY_ID_HEADER: "refuse-non-ascii",
        },
    )
    # A refusal, never a 500 raised by the comparison.
    assert status == 401
    assert service.request("GET", "/health")[0] == 200


# --- the delivery's shape ---------------------------------------------------


def test_a_non_json_content_type_is_refused_after_the_signature_check(service: Service) -> None:
    body = b"name=value&other=thing"
    status, _ = service.deliver(
        body, content_type="application/x-www-form-urlencoded", delivery_id="ct-form"
    )

    assert status == 415
    logged = [
        record
        for record in service.refused()
        if record.get("delivery_id") == "ct-form"
    ]
    assert logged
    assert logged[-1]["raw_body"] == body.decode()


def test_an_unsigned_non_json_delivery_is_refused_at_the_signature(service: Service) -> None:
    """The content-type gate sits after the signature check, not in front of it."""
    status, _ = service.deliver(
        b"name=value",
        content_type="application/x-www-form-urlencoded",
        signature=False,
        delivery_id="ct-unsigned",
    )
    assert status == 401


def test_a_body_that_is_not_json_is_accepted_and_logged_raw(service: Service) -> None:
    status, ack = service.deliver(PUBLISHED_BODY, event_type="push", delivery_id="raw-1")

    assert status == 202
    assert ack["modelled"] is False
    records = service.accepted_for("raw-1")
    assert len(records) == 1
    assert records[0]["payload"] == PUBLISHED_BODY.decode()


# --- the log record ---------------------------------------------------------


def test_exactly_one_log_record_per_delivery_carrying_the_payload(service: Service) -> None:
    body = issue_payload(number=42)
    status, _ = service.deliver(body, event_type="issues", delivery_id="log-1")

    assert status == 202
    records = service.accepted_for("log-1")
    assert len(records) == 1

    record = records[0]
    assert record["event_type"] == "issues"
    assert record["action"] == "opened"
    assert record["sender"] == "octocat"
    assert record["repository"] == "octo/hello-world"
    assert record["modelled"] is False
    assert record["payload"] == json.loads(body)


def test_the_log_record_is_one_compact_single_line_of_json(service: Service) -> None:
    service.deliver(issue_payload(number=99), event_type="issues", delivery_id="compact-1")

    lines = [
        line for line in service.log_lines() if '"delivery_id":"compact-1"' in line
    ]
    assert len(lines) == 1

    line = lines[0]
    assert "\n" not in line
    message = line.partition(": ")[2]
    # Compact: no space after a separator, and it round-trips exactly.
    assert json.dumps(json.loads(message), separators=(",", ":"), ensure_ascii=False) == message
