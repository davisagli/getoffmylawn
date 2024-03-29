"""Package initializer."""

from pyramid.config import Configurator
from pyramid.router import Router
from pyramid_heroku import expandvars_dict

import structlog
import typing as t

logger = structlog.getLogger("init")


def configure_logging() -> None:
    """Configure structlog logging.

    Whenever structlog is imported it only creates a proxy. Calling this
    method turns the proxy into an actual logger.
    """
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.format_exc_info,
            structlog.processors.KeyValueRenderer(
                key_order=("level", "logger", "event"), sort_keys=True
            ),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def configure(config: Configurator) -> None:
    """Configure Pyramid to serve the getoffmylawn API."""

    # Configure DB
    config.include("pyramid_deferred_sqla")
    config.sqlalchemy_engine(pool_size=5, max_overflow=1, pool_timeout=5)

    # Configure pyramid_openapi3 integration
    config.include(".openapi")

    # Configure authentication & authorization
    config.include(".auth")

    # Find and configure all decorated objects
    config.scan(
        ignore=[
            "getoffmylawn.conftest",
            "getoffmylawn.auth.tests",
            "getoffmylawn.scripts.tests",
            "getoffmylawn.tests",
            "getoffmylawn.urls",
            "getoffmylawn.urls.tests",
        ]
    )

    # Configure content
    config.commit()
    config.include(".urls")
    config.scan("getoffmylawn.urls", ignore=["getoffmylawn.urls.tests"])


def main(global_config: t.Dict[str, str], **settings: str) -> Router:
    """Return a Pyramid WSGI application."""

    # Support for turning off alembic DB checks in certain scripts
    if global_config.get("SKIP_CHECK_DB_MIGRATED"):
        settings["SKIP_CHECK_DB_MIGRATED"] = global_config["SKIP_CHECK_DB_MIGRATED"]

    # Expand environment variables in .ini files
    settings = expandvars_dict(settings)

    # Configure Pyramid
    config = Configurator(
        settings=settings, root_factory="getoffmylawn.auth.RootFactory"
    )
    configure(config)

    # Up, Up and Away!
    return config.make_wsgi_app()
