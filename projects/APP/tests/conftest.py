# pylint: disable=redefined-outer-name
import os
import time
from pathlib import Path

import pytest
from sqlalchemy.exc import OperationalError
import redis
import requests
from allocation import config
from allocation.adapters.orm import mapper_registry, start_mappers
from sqlalchemy import create_engine
from sqlalchemy.sql import delete, insert, select, text
from sqlalchemy.orm import sessionmaker, clear_mappers

from allocation import config
from allocation.entrypoints.flask_app import create_app
from allocation.domain.model import Batch
from allocation.adapters.orm import mapper_registry, start_mappers, batches


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def file_sqlite_db():
    engine = create_engine(config.get_sqlite_filedb_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(file_sqlite_db):
    # setup
    start_mappers()
    # what is "yield?"
    # Python Generators: https://realpython.com/introduction-to-python-generators/
    yield sessionmaker(bind=file_sqlite_db)()
    # teardown
    clear_mappers()
    file_sqlite_db.dispose()


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(config.get_api_url())


@retry(stop=stop_after_delay(10))
def wait_for_redis_to_come_up():
    r = redis.Redis(**config.get_redis_host_and_port())
    return r.ping()


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri(), isolation_level="SERIALIZABLE")
    wait_for_postgres_to_come_up(engine)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(session_factory):
    return session_factory

@pytest.fixture
def test_client(flask_api):
    return flask_api.test_client()

@pytest.fixture
def flask_api(session):
    app = create_app()
    app.config.update({"TESTING": True})
    return app