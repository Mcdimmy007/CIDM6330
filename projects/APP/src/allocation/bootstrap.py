import inspect
from typing import Callable

from allocation.adapters import orm, redis_eventpublisher
from allocation.adapters.notifications import AbstractNotifications, EmailNotifications
from allocation.service_layer import handlers, messagebus, unit_of_work
from allocation.service_layer.handlers import Command, Event

"""The Container Class is introduced to hold all the dependencies of the system"""

class Container:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, dependency):
        self.dependencies[dependency.__name__] = dependency

    def get_dependency(self, name):
        return self.dependencies[name]


def bootstrap(
    start_orm: bool = True,
    container: Container = None,
) -> messagebus.MessageBus:
    if container is None:
        container = Container()
    container.add_dependency(unit_of_work.AbstractUnitOfWork)
    container.add_dependency(unit_of_work.SqlAlchemyUnitOfWork)
    container.add_dependency(orm.AbstractRepository)
    container.add_dependency(orm.SqlAlchemyRepository)
    container.add_dependency(AbstractNotifications)
    container.add_dependency(EmailNotifications)
    container.add_dependency(redis_eventpublisher.publish)

    if start_orm:
        orm.start_mappers()

    injected_event_handlers = {
        event_type: [
            container.get_dependency(handler) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: container.get_dependency(handler)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=container.get_dependency(unit_of_work.AbstractUnitOfWork)(),
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

"""The inject_dependencies method is modified to retrieve the dependencies from the container instead of a dictionary of dependencies."""
def inject_dependencies(handler, container):
    params = inspect.signature(handler).parameters
    deps = {
        name: container.get_dependency(name) for name in params
    }
    return lambda message: handler(message, **deps)
