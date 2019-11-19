"""HTTP operations on Url resource."""

from getoffmylawn.openapi import object_or_404
from getoffmylawn.urls.models import Url
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.view import view_config
from slugify import slugify


@view_config(route_name="url", renderer="json", request_method="GET", openapi=True)
def url(request: Request) -> Url:
    """Get an URL."""
    url = object_or_404(
        Url.by_slug(request.openapi_validated.parameters["path"]["slug"], db=request.db)
    )
    return url


@view_config(route_name="urls", renderer="json", request_method="POST", openapi=True)
def create(request: Request) -> Url:
    """Get an URL."""
    body = request.openapi_validated.body
    url = Url(
        title=body.title,
        description=body.description,
        href=body.href,
        slug=getattr(body, "slug", None) or slugify(body.title),
        author=request.user,
    )
    request.db.add(url)
    request.db.flush()
    request.response.status_code = 201
    return url


@view_config(route_name="url", renderer="json", request_method="PUT", openapi=True)
def update(request: Request) -> Url:
    """Update an URL."""
    body = request.openapi_validated.body
    url = object_or_404(
        Url.by_slug(request.openapi_validated.parameters["path"]["slug"], db=request.db)
    )

    if getattr(body, "title", None):
        url.title = body.title
    if getattr(body, "description", None):
        url.description = body.description
    if getattr(body, "href", None):
        url.href = body.href

    return url


@view_config(route_name="url", renderer="json", request_method="DELETE", openapi=True)
def delete(request: Request) -> None:
    """Delete an URL."""
    url = object_or_404(
        Url.by_slug(request.openapi_validated.parameters["path"]["slug"], db=request.db)
    )
    request.db.delete(url)
    return None


@view_config(route_name="redirect")
def redirect(request: Request) -> None:
    """Redirect to target."""
    slug = request.matchdict["slug"]
    url = object_or_404(Url.by_slug(slug, db=request.db))
    raise HTTPFound(url.href)
