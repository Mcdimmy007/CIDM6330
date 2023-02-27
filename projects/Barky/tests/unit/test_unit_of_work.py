### The first test case "test_uow_can_retrieve_a_bookmark_after_commit" tests if we can add a bookmark to the repository using the SqlAlchemyUnitOfWork and retrieve it back after committing the changeswithin the context of the unit of work.
### The second test case "test_uow_can_rollback_on_error" tests if the changes are rolled back when an error occurs. 

import unittest
from barkylib.domain.models import Bookmark
from barkylib.services.unit_of_work import SqlAlchemyUnitOfWork

class TestSqlAlchemyUnitOfWork(unittest.TestCase):

    def test_uow_can_retrieve_a_bookmark_after_commit(self):
        # Arrange
        uow = SqlAlchemyUnitOfWork()
        bookmark = Bookmark(
            url="https://wtamu.edu",
            title="WTAMU",
            notes="University landing page",
            date_added="2023-02-26T19:25:00Z"
        )

        # Act
        with uow:
            uow.bookmarks.add(bookmark)
            uow.commit()

        with uow:
            retrieved_bookmark = uow.bookmarks.get(bookmark.id)

        # Assert
        self.assertEqual(retrieved_bookmark, bookmark)

    def test_uow_can_rollback_on_error(self):
        # Arrange
        uow = SqlAlchemyUnitOfWork()
        bookmark = Bookmark(
            url="https://www.wtamu.edu",
            title="WTAMU",
            notes="A University Website",
            date_added="2023-02-26T19:25:00Z"
        )

        # Act
        with uow:
            uow.bookmarks.add(bookmark)
            uow.commit()

            # Introduce an error here
            raise ValueError("Simulating an error")

        # Assert
        with uow:
            retrieved_bookmark = uow.bookmarks.get(bookmark.id)
        self.assertIsNone(retrieved_bookmark)


if __name__ == '__main__':
    unittest.main()


