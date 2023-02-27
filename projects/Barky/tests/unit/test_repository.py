# pylint: disable=missing-module-docstring
from sqlalchemy import create_engine
from src.barkylib.domain.models import Bookmark
from src.barkylib.adapters.orm import AbstractRepository, SqlAlchemyRepository


def test_sqlalchemy_repository():
    
    rep = SqlAlchemyRepository()

    
    bookmark = Bookmark(title="Test Bookmark", url="https://testbookmark.com")
    rep.add_one(bookmark)

    
    result = rep.get("Test Bookmark")

    
    assert result.title == "Test Bookmark"
    assert result.url == "https://testbookmark.com"


class SqlAlchemyRepository(AbstractRepository):
    """
    Uses guidance from the basic SQLAlchemy 2.0 tutorial:
    https://docs.sqlalchemy.org/en/20/tutorial/index.html
    """

    def __init__(self, url=None) -> None:
        super().__init__()

        self.engine = None

        
        if url != None:
            self.engine = create_engine(url)
        else:
            
            self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        # ensure tables are there
        Base.metadata.create_all(self.engine)

        # obtain session
        # the session is used for all transactions
        self.Session = sessionmaker(bind=self.engine)

    def add_one(self, bookmark: Bookmark) -> int:
        with self.Session() as session:
            session.add(bookmark)
            session.commit()

    def _get(self, title) -> Bookmark:
        with self.Session() as session:
            return session.query(Bookmark).filter_by(title=title).first()

    def add_many(self, bookmarks: list[Bookmark]) -> int:
        with self.Session() as session:
            session.add_all(bookmarks)
            session.commit()

    def delete_one(self, bookmark) -> int:
        pass

    def delete_many(self, bookmarks) -> int:
        pass

    def update(self, bookmark) -> int:
        pass

    def update_many(self, bookmarks) -> int:
        pass

    def find_first(self, query) -> Bookmark:
        pass

    def find_all(self, query) -> list[Bookmark]:
        pass




