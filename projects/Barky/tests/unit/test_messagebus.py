# pylint: disable=trailing-whitespace
import logging
import pytest

from barkylib.adapters import repository
from barkylib.domain import commands, events, models
from barkylib.services import handlers 
from barkylib.services import  messagebus, unit_of_work

logger = logging.getLogger(__name__)


@pytest.fixture
def sqlite_uow():
    sqlite_uow = unit_of_work.SqlAlchemyUnitOfWork()
    yield sqlite_uow
    sqlite_uow.rollback()


@pytest.fixture
def sqlite_session_factory():
    yield unit_of_work.SqlAlchemySessionFactory()
    

def test_message_bus(sqlite_uow: Generator[SqlAlchemyUnitOfWork, None, None], sqlite_session_factory: Generator[Any, None, None]):
    # Creating and adding a bookmark
    bookmark_id = models.Bookmark.next_id()
    bookmark = models.Bookmark(bookmark_id, "Test Bookmark", "https://www.test.com", "Test Description")
    with sqlite_session_factory() as session:
        repo = memory_repository.MemoryBookmarkRepository(session)
        repo.add(bookmark)
        sqlite_uow.commit()

    # Create a command to update the bookmark
    update_command = commands.UpdateBookmarkCommand(
        bookmark_id=bookmark.id,
        title="Updated Test Bookmark",
        url="https://www.updated-test.com",
        description="Updated Test Description",
    )

    # Create a message bus with the necessary handlers
    event_handlers = {
        events.BookmarkUpdated: [handlers.EmailNotificationHandler],
    }
    command_handlers = {
        commands.UpdateBookmarkCommand: handlers.UpdateBookmarkHandler(sqlite_uow),
    }
    message_bus = messagebus.MessageBus(sqlite_uow, event_handlers, command_handlers)

    # Handle the command and check if the bookmark was updated
    message_bus.handle(update_command)

    with sqlite_session_factory() as session:
        repo = memory_repository.MemoryBookmarkRepository(session)
        updated_bookmark = repo.get(bookmark.id)
        assert updated_bookmark.title == "Updated Test Bookmark"
        assert updated_bookmark.url == "https://www.updated-test.com"
        assert updated_bookmark.description == "Updated Test Description"

