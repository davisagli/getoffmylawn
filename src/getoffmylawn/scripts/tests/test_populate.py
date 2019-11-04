"""Test the populate.py script.

Since this script is used a lot in other test suites, we only need very
simple testing here.
"""

from getoffmylawn.auth.models import User
from getoffmylawn.conftest import AppEnvType
from getoffmylawn.scripts.populate import main
from pyramid_deferred_sqla import Base
from sqlalchemy.orm.session import Session
from unittest import mock

import transaction


@mock.patch("getoffmylawn.scripts.populate.argparse")
def test_populate(argparse: mock.MagicMock, app_env: AppEnvType, db: Session) -> None:
    """Test that db is populated with demo content."""

    argparse.ArgumentParser.return_value.parse_args.return_value.config = "etc/test.ini"
    main()
    assert db.query(User).count() == 2

    # manual test teardown is needed because main() does db.commit()
    with transaction.manager:
        engine = app_env["registry"].settings["sqlalchemy.engine"]
        tables = ", ".join(Base.metadata.tables.keys())
        engine.execute("TRUNCATE {} CASCADE".format(tables))
