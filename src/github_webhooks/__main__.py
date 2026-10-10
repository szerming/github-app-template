"""Start the service: ``python -m github_webhooks`` (wrapped by scripts/start.sh)."""

from __future__ import annotations

import uvicorn

from .app import app


def main() -> None:
    settings = app.state.settings
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
        # The service's own log record per delivery is the output; uvicorn's
        # access log would only add noise to it.
        access_log=False,
    )


if __name__ == "__main__":
    main()
