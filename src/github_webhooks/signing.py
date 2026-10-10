"""Proving a delivery came from GitHub: HMAC-SHA256 over the raw request bytes."""

from __future__ import annotations

import hashlib
import hmac

SIGNATURE_HEADER = "X-Hub-Signature-256"
LEGACY_SIGNATURE_HEADER = "X-Hub-Signature"

_SHA256_PREFIX = "sha256="
_SHA1_PREFIX = "sha1="


def signature_is_valid(secret: str, body: bytes, header: str | None) -> bool:
    """Whether ``header`` is a valid ``sha256=`` signature over ``body``.

    Both sides are encoded to bytes before comparison. A signature header is
    attacker-controlled, ASGI servers decode header bytes as latin-1, and
    ``hmac.compare_digest`` raises on a non-ASCII ``str`` -- which would turn a
    forged delivery into a 500 instead of the 401 the contract promises. An
    unencodable header is simply invalid. Comparison is constant time.
    """
    if not header or not header.startswith(_SHA256_PREFIX):
        return False
    try:
        provided = header.encode("ascii")
    except UnicodeEncodeError:
        return False
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"{_SHA256_PREFIX}{expected}".encode("ascii"), provided)


def is_legacy_signature(header: str | None) -> bool:
    """Whether ``header`` is the deprecated SHA-1 scheme.

    A webhook configured before this service existed still sends
    ``X-Hub-Signature``; refusing it needs its own diagnosis so that a stale
    configuration does not read as an attack.
    """
    return bool(header) and header.startswith(_SHA1_PREFIX)
