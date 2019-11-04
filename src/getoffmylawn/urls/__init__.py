"""URLs."""

from pyramid.config import Configurator


def includeme(config: Configurator) -> None:
    """Pyramid knob."""
    config.add_route("urls", "/api/urls")
    config.add_route("url", "/api/urls/{slug}")
