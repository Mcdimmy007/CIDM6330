from __future__ import annotations

import abc
from abc import ABC

from barkylib import config
from barkylib.adapters import repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class AbstractUnitOfWork(ABC):
    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for product in self.products.seen:
            while product.events:
                yield product.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

# In the "SqlAlchemyUnitofWork" class takes a "Session" object
class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: Session):
        self.session = session
        self.products = repository.SqlAlchemyRepository(session)

# This enter method returns the object itself
    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        return self

# The exit method calls the parent class exit without passing any argument
    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

# This creates a session factory and returns the session object
def create_session():
    engine = create_engine(
        config.get_sqlite_file_url(),
        isolation_level="REPEATABLE READ",
    )
    session_factory = sessionmaker(bind=engine)
    return session_factory()
