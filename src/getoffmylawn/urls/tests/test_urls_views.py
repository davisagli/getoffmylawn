"""Tests for Url related views."""

from getoffmylawn.auth.tests.test_auth_views import USER_ONE_JWT
from getoffmylawn.auth.tests.test_auth_views import USER_TWO_JWT
from getoffmylawn.urls.models import Url
from sqlalchemy.orm.session import Session
from webtest import TestApp


def test_GET_url(testapp: TestApp, democontent: None) -> None:
    """Test GET /api/urls/{slug}."""
    res = testapp.get("/api/urls/foo", status=200)

    assert res.json == {
        "createdAt": "2019-01-01T01:01:01.000Z",
        "description": "Foö desc",
        "href": "https://glicksoftware.com",
        "slug": "foo",
        "title": "Foö",
        "updatedAt": "2019-02-02T02:02:02.000Z",
    }


def test_POST_url(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/urls."""
    res = testapp.post_json(
        "/api/urls",
        {"title": "A title", "description": "A description", "href": "https://test",},
        headers={"Authorization": f"Token {USER_TWO_JWT}"},
        status=201,
    )

    assert res.json["title"] == "A title"
    assert res.json["description"] == "A description"
    assert res.json["href"] == "https://test"
    assert res.json["slug"] == "a-title"


def test_PUT_url(testapp: TestApp, democontent: None) -> None:
    """Test PUT /api/urls/{slug}."""
    res = testapp.put_json(
        "/api/urls/foo",
        {
            "title": "New title",
            "description": "New description",
            "href": "https://new",
        },
        headers={"Authorization": f"Token {USER_ONE_JWT}"},
        status=200,
    )

    assert res.json == {
        "createdAt": "2019-01-01T01:01:01.000Z",
        "description": "New description",
        "href": "https://new",
        "slug": "foo",
        "title": "New title",
        "updatedAt": "2019-02-02T02:02:02.000Z",
    }


def test_DELETE_url(testapp: TestApp, db: Session, democontent: None) -> None:
    """Test DELETE /api/urls/{slug}."""
    assert Url.by_slug("foo", db=db) is not None
    testapp.delete(
        "/api/urls/foo", headers={"Authorization": f"Token {USER_ONE_JWT}"}, status=200,
    )

    assert Url.by_slug("foo", db=db) is None
