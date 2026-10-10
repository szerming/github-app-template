"""The harness: the real service, started the way the operator starts it.

Nothing here imports the application's internals. The tests assert only what the
outside shows -- HTTP status codes and the lines the process logs -- so they
survive any refactor of the handler.
"""

from __future__ import annotations

import hashlib
import hmac
import http.client
import json
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Any, Iterator

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
START_SCRIPT = REPO_ROOT / "scripts" / "start.sh"

# GitHub's own published signature vector, so the service under test is started
# with the secret that vector pins.
WEBHOOK_SECRET = "It's a Secret to Everybody"

SIGNATURE_HEADER = "X-Hub-Signature-256"
LEGACY_SIGNATURE_HEADER = "X-Hub-Signature"
DELIVERY_ID_HEADER = "X-GitHub-Delivery"
EVENT_TYPE_HEADER = "X-GitHub-Event"
JSON_CONTENT_TYPE = "application/json"

READY_DEADLINE_SECONDS = 20.0


def sign(secret: str, body: bytes) -> str:
    """The signature GitHub computes: an HMAC-SHA256 hex digest, ``sha256=`` prefixed."""
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class Service:
    """A handle on the running process: post to it, read back what it logged."""

    def __init__(
        self,
        process: subprocess.Popen[bytes],
        log_path: Path,
        host: str,
        port: int,
    ) -> None:
        self.process = process
        self.log_path = log_path
        self.host = host
        self.port = port

    # --- HTTP ---------------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        body: bytes = b"",
        headers: dict[str, str] | None = None,
    ) -> tuple[int, Any]:
        """Write the request by hand.

        ``http.client`` encodes header values as latin-1, which is what makes the
        non-ASCII signature-header case reachable at all -- ``httpx`` refuses it.
        """
        connection = http.client.HTTPConnection(self.host, self.port, timeout=10)
        try:
            connection.putrequest(method, path)
            for name, value in (headers or {}).items():
                connection.putheader(name, value)
            connection.putheader("Content-Length", str(len(body)))
            connection.endheaders(body)
            response = connection.getresponse()
            raw = response.read()
            try:
                payload: Any = json.loads(raw) if raw else None
            except ValueError:
                payload = raw.decode("utf-8", "replace")
            return response.status, payload
        finally:
            connection.close()

    def deliver(
        self,
        body: bytes,
        *,
        secret: str = WEBHOOK_SECRET,
        signature: bool = True,
        content_type: str | None = JSON_CONTENT_TYPE,
        event_type: str | None = "push",
        delivery_id: str | None = "delivery-1",
    ) -> tuple[int, Any]:
        headers: dict[str, str] = {}
        if content_type is not None:
            headers["Content-Type"] = content_type
        if event_type is not None:
            headers[EVENT_TYPE_HEADER] = event_type
        if delivery_id is not None:
            headers[DELIVERY_ID_HEADER] = delivery_id
        if signature:
            headers[SIGNATURE_HEADER] = sign(secret, body)
        return self.request("POST", "/", body, headers)

    # --- log ----------------------------------------------------------------

    def log_lines(self) -> list[str]:
        return self.log_path.read_text(encoding="utf-8", errors="replace").splitlines()

    def records(self, level: str) -> list[dict[str, Any]]:
        """The service's own JSON records at ``level``, in the order written."""
        found: list[dict[str, Any]] = []
        for line in self.log_lines():
            head, separator, rest = line.partition(": ")
            if not separator or head != level:
                continue
            try:
                value = json.loads(rest)
            except ValueError:
                continue
            if isinstance(value, dict):
                found.append(value)
        return found

    def accepted(self) -> list[dict[str, Any]]:
        return self.records("INFO")

    def refused(self) -> list[dict[str, Any]]:
        return self.records("WARNING")

    def accepted_for(self, delivery_id: str) -> list[dict[str, Any]]:
        return [r for r in self.accepted() if r.get("delivery_id") == delivery_id]

    # --- lifecycle ----------------------------------------------------------

    @property
    def alive(self) -> bool:
        return self.process.poll() is None

    def wait_until_ready(self) -> None:
        """Poll the health endpoint; the socket being open is not the app serving."""
        deadline = time.monotonic() + READY_DEADLINE_SECONDS
        while time.monotonic() < deadline:
            if not self.alive:
                raise RuntimeError("service exited before it was ready:\n" + self.tail())
            try:
                status, _ = self.request("GET", "/health")
            except OSError:
                time.sleep(0.05)
                continue
            if status == 200:
                return
            time.sleep(0.05)
        raise RuntimeError("service did not become ready:\n" + self.tail())

    def tail(self, lines: int = 40) -> str:
        return "\n".join(self.log_lines()[-lines:])


@pytest.fixture(scope="module")
def service(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Service]:
    """The service, as a real process on a free port, started through the script."""
    port = free_port()
    log_path = tmp_path_factory.mktemp("service") / "service.log"
    environment = dict(os.environ)
    environment.update(
        {
            "WEBHOOK_SECRET": WEBHOOK_SECRET,
            "HOST": "127.0.0.1",
            "PORT": str(port),
            "LOG_LEVEL": "INFO",
        }
    )

    with open(log_path, "wb") as sink:
        process = subprocess.Popen(
            ["bash", str(START_SCRIPT)],
            cwd=str(REPO_ROOT),
            env=environment,
            stdout=sink,
            stderr=subprocess.STDOUT,
        )
        handle = Service(process, log_path, "127.0.0.1", port)
        try:
            handle.wait_until_ready()
            yield handle
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
