"""Models related to auth."""

from __future__ import annotations
from pyramid.request import Request
from pyramid_deferred_sqla import Base
from pyramid_deferred_sqla import Model
from pyramid_deferred_sqla import model_config
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm.session import Session

import typing as t

__all__ = ["User"]


@model_config(Base)
class User(Model):
    """A logged-in user."""

    __tablename__ = "users"

    def __json__(self, request: Request) -> t.Dict[str, str]:
        """JSON renderer support."""
        return {
            "username": self.username,
            "token": request.create_jwt_token(str(self.id)),
        }

    username = Column(String, nullable=False, unique=True)

    @classmethod
    def by_id(cls: t.Type[User], uuid: str, db: Session) -> t.Optional[User]:
        """Get User by id."""
        q = db.query(cls)
        q = q.filter(cls.id == uuid)
        return q.one_or_none()

    @classmethod
    def by_username(cls: t.Type[User], username: str, db: Session) -> t.Optional[User]:
        """Get User by username."""
        q = db.query(cls)
        q = q.filter(cls.username == username)
        return q.one_or_none()
