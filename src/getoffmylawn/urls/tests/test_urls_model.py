"""Tests for the Url model."""

from getoffmylawn.auth.models import User
from getoffmylawn.openapi import json_renderer
from getoffmylawn.scripts.populate import URL_FOO_ID
from getoffmylawn.urls.models import Url
from pyramid.testing import DummyRequest
from sqlalchemy.orm.session import Session

import json


def test_by_shortcuts(db: Session, democontent: None) -> None:
    """Test that by_* shortcuts work."""
    assert Url.by_slug("foo", db) == Url.by_id(URL_FOO_ID, db)


def test_json_renderer(db: Session, democontent: None) -> None:
    """Test that Url is correctly rendered for an OpenAPI JSON response."""
    user = User.by_username("two", db=db)
    url = Url.by_slug("foo", db=db)

    request = DummyRequest()
    request.user = user

    renderer = json_renderer()
    output = renderer(None)(url, {"request": request})

    assert json.loads(output) == {
        "createdAt": "2019-01-01T01:01:01.000Z",
        "description": "Foö desc",
        "href": "https://glicksoftware.com",
        "slug": "foo",
        "title": "Foö",
        "updatedAt": "2019-02-02T02:02:02.000Z",
    }
