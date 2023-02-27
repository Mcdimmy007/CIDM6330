# pylint: disable=import-error
from unittest.mock import Mock

from barkylib.services import handlers, messagebus, unit_of_work
from barkylib.bootstrap import bootstrap


def test_bootstrap_starts_orm_and_returns_messagebus_instance():
    start_mappers = Mock()
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    dependencies = {"uow": uow}

    injected_event_handlers = {
        event_type: [
            handler for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: handler
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    messagebus_instance = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    result = bootstrap(start_orm=True, uow=uow)

    start_mappers.assert_called_once()
    assert isinstance(result, messagebus.MessageBus)
    assert result.uow == uow
    assert result.event_handlers == injected_event_handlers
    assert result.command_handlers == injected_command_handlers


