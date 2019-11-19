"""HTTP operations for auth."""

from authomatic.adapters import WebObAdapter
from getoffmylawn.auth.models import User
from mypy_extensions import TypedDict
from pyramid.httpexceptions import exception_response
from pyramid.request import Request
from pyramid.response import Response
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


@view_config(route_name="login")
def login(request: Request) -> Response:
    """User logs in using GitHub."""
    response = Response()
    result = request.authomatic.login(WebObAdapter(request, response), "github")
    if result is None:
        return response
    if result.error:
        return exception_response(401, json_body={"error": result.error.message})

    result.user.update()
    username = result.user.username
    user = User.by_username(username, db=request.db)
    if user is None:
        return exception_response(401, json_body={"error": "Not authorized."})

    return Response(json_body={"token": request.create_jwt_token(str(user.id))})
