"""HTTP operations for auth."""

from getoffmylawn.auth.models import User
from mypy_extensions import TypedDict
from pyramid.httpexceptions import exception_response
from pyramid.request import Request
from pyramid.view import view_config

# Python representation of openapi.yaml's UserResponse schema
UserResponse = TypedDict("UserResponse", {"user": User})


@view_config(
    route_name="user",
    renderer="json",
    request_method="GET",
    openapi=True,
    permission="authenticated",
)
def current_user(request: Request) -> UserResponse:
    """Get currently logged in user."""
    return {"user": request.user}


@view_config(
    route_name="users.login", renderer="json", request_method="POST", openapi=True
)
def login(request: Request) -> UserResponse:
    """User logs in."""
    body = request.openapi_validated.body

    user = User.by_username(body.user.username, db=request.db)
    if user and user.verify_password(body.user.password):
        return {"user": user}

    raise exception_response(
        422, json_body={"errors": {"username or password": ["is invalid"]}}
    )
