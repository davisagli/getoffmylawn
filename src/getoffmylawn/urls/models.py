"""Url model."""

from __future__ import annotations
from datetime import datetime
from pyramid.request import Request
from pyramid_deferred_sqla import Base
from pyramid_deferred_sqla import Model
from pyramid_deferred_sqla import model_config
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

import typing as t

__all__ = ["Url"]


@model_config(Base)
class Url(Model):
    """A single URL."""

    __tablename__ = "urls"

    def __json__(
        self, request: Request
    ) -> t.Dict[str, t.Union[int, bool, str, t.List[str]]]:
        """JSON renderer support."""
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "href": self.href,
            "createdAt": self.created,
            "updatedAt": self.updated,
        }

    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    author = relationship(
        "User", backref=backref("urls", order_by="desc(Url.created)")
    )

    slug = Column(String, nullable=False, unique=True)
    title = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=False)
    href = Column(Unicode, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def by_slug(cls: t.Type[Url], slug: str, db: Session) -> t.Optional[Url]:
        """Get Url by slug."""
        q = db.query(cls)
        q = q.filter(cls.slug == slug)
        return q.one_or_none()

    @classmethod
    def by_id(cls: t.Type[Url], uuid: str, db: Session) -> t.Optional[Url]:
        """Get Url by id."""
        q = db.query(cls)
        q = q.filter(cls.id == uuid)
        return q.one_or_none()
