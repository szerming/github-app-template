"""Configuration, read from the environment under explicit variable names."""

from __future__ import annotations

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The service's configuration.

    Every field carries an explicit ``validation_alias``: a bare
    ``host``/``port``/``secret`` field would silently pick up an unrelated
    machine-wide variable such as ``PORT``.
    """

    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    webhook_secret: str = Field(validation_alias="WEBHOOK_SECRET")
    host: str = Field(default="127.0.0.1", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")


def load_settings() -> Settings:
    """Build the settings, refusing to start without a usable secret.

    A misconfigured deployment has to fail at startup, naming the variable it is
    missing, rather than accept whatever arrives. An empty secret counts as
    absent: it would make every signature forgeable, so nothing would tell a
    delivery from a forgery.
    """
    try:
        settings = Settings()
    except ValidationError as exc:
        missing = [str(error["loc"][0]) for error in exc.errors() if error["type"] == "missing"]
        if missing:
            raise SystemExit(
                "refusing to start: missing required environment variable(s): " + ", ".join(missing)
            ) from exc
        raise
    if not settings.webhook_secret:
        raise SystemExit(
            "refusing to start: WEBHOOK_SECRET is set but empty, so no delivery "
            "could be told from a forgery"
        )
    return settings
