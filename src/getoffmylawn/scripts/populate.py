"""Populate db with demo content.

It's good practice to use strange characters in demo/test content to
verify support for non-ascii inputs.
"""

from datetime import datetime
from getoffmylawn.auth.models import User
from getoffmylawn.urls.models import Url
from pyramid.paster import bootstrap
from pyramid.paster import setup_logging
from sqlalchemy.orm.session import Session

import argparse
import structlog
import sys
import transaction
import typing as t

logger = structlog.getLogger("populate")

USER_ONE_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee1"
USER_TWO_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee2"
USER_JOHNJACOB_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee3"
URL_FOO_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee1"
URL_BAR_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee2"
URL_JOHNJACOB_ID = "aaaaaaaa-bbbb-4ccc-aaaa-eeeeeeeeeee3"

# "secret", hashed
SECRET = "$argon2i$v=19$m=512,t=2,p=2$mRMCwLg3Rgih1JqTUooxxg$/bBw6iXly9rfryTkaoPX/Q"


def add_users(db: Session) -> None:
    """Add demo users to db."""

    one = User(
        id=USER_ONE_ID, username="one", password_hash=SECRET
    )
    db.add(one)
    logger.info("User added", username=one.username)

    two = User(
        id=USER_TWO_ID, username="two", password_hash=SECRET
    )
    db.add(two)
    logger.info("User added", username=two.username)

    # # Postman tests expect this user to be present
    # johnjacob = User(
    #     id=USER_JOHNJACOB_ID,
    #     username="johnjacob",
    #     password_hash=SECRET,
    # )
    # db.add(johnjacob)
    # johnjacob.follows.append(one)
    # logger.info("User added", username=johnjacob.username)

    db.flush()


def add_urls(db: Session) -> None:
    """Add demo urls to db."""

    foo = Url(
        id=URL_FOO_ID,
        slug="foo",
        title="Foö",
        description="Foö desc",
        href="https://glicksoftware.com",
        author=User.by_username("one", db=db),
        created=datetime(2019, 1, 1, 1, 1, 1),
        updated=datetime(2019, 2, 2, 2, 2, 2),
    )

    db.add(foo)
    logger.info("Url added", slug=foo.slug)

    # bar = Article(
    #     id=ARTICLE_BAR_ID,
    #     slug="bar",
    #     title="Bär",
    #     description="Bär desc",
    #     body="Bär body",
    #     author=User.by_username("one", db=db),
    #     created=datetime(2019, 3, 3, 3, 3, 3),
    #     updated=datetime(2019, 4, 4, 4, 4, 4),
    # )
    # db.add(bar)
    # logger.info("Article added", slug=bar.slug)

    # # Postman tests require this user to have at least one article
    # johnjacob = Article(
    #     id=ARTICLE_JOHNJACOB_ID,
    #     slug="i-am-johnjacob",
    #     title="I am John Jacob",
    #     description="johnjacob desc",
    #     body="johnjacob body",
    #     author=User.by_username("johnjacob", db=db),
    #     created=datetime(2019, 5, 5, 5, 5, 5),
    #     updated=datetime(2019, 6, 6, 6, 6, 6),
    # )
    # db.add(johnjacob)
    # logger.info("Article added", slug=johnjacob.slug)

    db.flush()


def main(argv: t.List[str] = sys.argv) -> None:
    """Run the script."""

    parser = argparse.ArgumentParser(
        usage="python -m getoffmylawn.scripts.populate"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="etc/development.ini",
        metavar="<config>",
        help="Pyramid application configuration file.",
    )

    env = bootstrap(parser.parse_args().config)
    setup_logging(parser.parse_args().config)

    with transaction.manager:
        add_users(env["request"].db)
        add_urls(env["request"].db)

    logger.info("populate script finished")
    env["closer"]()


if __name__ == "__main__":
    main()
