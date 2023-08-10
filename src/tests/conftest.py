import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from sqlalchemy.engine import create_engine

from app import config, main, models
from app.database import get_session

from . import utils

postgresql_proc = factories.postgresql_proc(
    host="localhost",
    user="code-challenge",
    port="5432",
    password="password",
)

pg_fixture = factories.postgresql("postgresql_proc", db_name="code-challenge_dev")


@pytest.fixture(scope="function")
def fastapi_client(session):
    return TestClient(main.app)


@pytest.fixture(scope="function")
def session(pg_fixture):
    sqlalchemy_uri = (
        f"postgresql://{pg_fixture.info.user}:{pg_fixture.info.password}@"
        f"{pg_fixture.info.host}:{pg_fixture.info.port}"
        f"/{pg_fixture.info.dbname}"
    )
    config.settings.db_uri = sqlalchemy_uri
    engine = create_engine(config.settings.db_uri, echo=False)
    models.Base.metadata.create_all(engine)

    Session = get_session()
    session = Session()
    utils.test_item(session)
    yield session
    session.commit()

    models.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_settings(pg_fixture):
    config.settings.db_uri = (
        f"postgresql://{pg_fixture.info.user}:{pg_fixture.info.password}@"
        f"{pg_fixture.info.host}:{pg_fixture.info.port}"
        f"/{pg_fixture.info.dbname}"
    )
