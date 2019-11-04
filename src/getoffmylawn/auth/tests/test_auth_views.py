"""Tests for auth views."""

from freezegun import freeze_time
from getoffmylawn.scripts.populate import USER_ONE_ID
from webtest import TestApp

import copy
import jwt

# JWT encoded:
# {'sub': 'aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee1', 'iat': 1546300800}
USER_ONE_JWT = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhYWFhYWFh"
    "YS1iYmJiLTRjY2MtYWFhYS1lZWVlZWVlZWVlZTEiLCJpYXQiOjE1NDYzM"
    "DA4MDB9.OygJRuk6rNakGz3VUr6aul5Lq-2lB5IP7BTWY1RLDV6d3CEeJ"
    "zKQFGZVGp-J-3oFpChArB6JB-McYR9lMtQ4PA"
)


# JWT encoded:
# {'sub': 'aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee2', 'iat': 1546300800}
USER_TWO_JWT = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhYWFhYWFh"
    "YS1iYmJiLTRjY2MtYWFhYS1lZWVlZWVlZWVlZTIiLCJpYXQiOjE1NDYzM"
    "DA4MDB9.titp0HgVtkMEnbU_mE-OnNbjha3hFzzIvmyp3iDbuyoXtvstU"
    "JmtyOYWZXg9IUFdKafQ3gadkSEgvA7PKAWuyA"
)


@freeze_time("2019-01-01")
def test_login(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/users."""
    res = testapp.post_json(
        "/api/users/login",
        {"user": {"username": "one", "password": "secret"}},
        status=200,
    )

    response = copy.deepcopy(res.json)
    response["user"]["token"] = jwt.decode(
        res.json["user"]["token"], "secret", algorithms=["HS512"]
    )
    assert response == {
        "user": {
            "token": {"sub": USER_ONE_ID, "iat": 1546300800},
            "username": "one",
        }
    }


def test_login_failed(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/users with bad credentials."""
    testapp.post_json(
        "/api/users/login",
        {"user": {"username": "one", "password": "noidea"}},
        status=422,
    )


@freeze_time("2019-01-01")
def test_get_current_user(testapp: TestApp, democontent: None) -> None:
    """Test POST /api/user."""
    res = testapp.get(
        "/api/user", headers={"Authorization": f"Token {USER_ONE_JWT}"}, status=200
    )

    response = copy.deepcopy(res.json)
    response["user"]["token"] = jwt.decode(
        res.json["user"]["token"], "secret", algorithms=["HS512"]
    )
    assert response == {
        "user": {
            "token": {"sub": USER_ONE_ID, "iat": 1546300800},
            "username": "one",
        }
    }


@freeze_time("2019-01-01")
def test_invalid_token(testapp: TestApp) -> None:
    """Test GET /api/user with invalid token, because user one is not in db."""
    testapp.get(
        "/api/user", headers={"Authorization": f"Token {USER_ONE_JWT}"}, status=401
    )
