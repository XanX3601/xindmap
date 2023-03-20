import collections

import xindmap.event

from .CommandCallQueueEvent import CommandCallQueueEvent


class CommandCallQueue(xindmap.event.EventSource):
    # command ******************************************************************
    def enqueue(self, command_call):
        self.__queue.appendleft(command_call)

        event = xindmap.event.Event(
            CommandCallQueueEvent.call_enqueued, call=command_call
        )
        self._dispatch_event(event)

    def dequeue(self):
        command_call = self.__queue.pop()

        event = xindmap.event.Event(
            CommandCallQueueEvent.call_dequeued, call=command_call
        )
        self._dispatch_event(event)

    # constructor **************************************************************
    def __init__(self):
        super().__init__(CommandCallQueueEvent)

        self.__queue = collections.deque()
