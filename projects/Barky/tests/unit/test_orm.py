# pylint: disable=import-error
import unittest

from datetime import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from src.barkylib.adapters import orm
from src.barkylib.domain.models import Bookmark


class TestModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.metadata = MetaData(bind=self.engine)

    def test_start_mappers(self):
        orm.start_mappers()

        # I created a simple bookmark here:
        bookmark = Bookmark(
            title="Test Bookmark",
            url="https://www.example.com",
            notes="This is a test bookmark",
            date_added=datetime.now(),
            date_edited=datetime.now()
        )

        self.session.add(bookmark)
        self.session.commit()

        retrieved_bookmark = self.session.query(
            Bookmark).filter_by(title="Test Bookmark").first()

        
        self.assertEqual(bookmark, retrieved_bookmark)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()


if __name__ == '__main__':
    unittest.main()
