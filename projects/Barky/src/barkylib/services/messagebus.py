from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Dict, List, Type, Union

from barkylib.domain import commands, events

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]

## The MessageBus class now has a queue_commands and a queue_events method that are used to handle the commands and events returned
## by the unit of works 'collect_new_commands' and collect_new_events' method respectively.
class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    ## The handle method has been updated to only process one message at a time, since messages are now handled through
    ## the 'queue_commands and 'queue_events'
    
    def handle(self, message: Message):
        if isinstance(message, events.Event):
            self.handle_event(message)
        elif isinstance(message, commands.Command):
            self.handle_command(message)
        else:
            raise Exception(f"{message} was not an Event or Command")

    def handle_event(self, event: events.Event):
        handlers = self.event_handlers[type(event)]
        for handler in handlers:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue_commands(self.uow.collect_new_commands())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue_events(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
 #
    def queue_commands(self, commands: List[commands.Command]):
        for command in commands:
            self.handle(command)

    def queue_events(self, events: List[events.Event]):
        for event in events:
            self.handle(event)
