import collections

import xindmap.event

from .CommandCallQueueError import CommandCallQueueError
from .CommandCallQueueEvent import CommandCallQueueEvent


class CommandCallQueue(xindmap.event.EventSource):
    """A queue of [command calls][xindmap.command.CommandCall.CommandCall].

    This is a buffer to store
    [command calls][xindmap.command.CommandCall.CommandCall].

    As it is a queue, the command call queue only exposes two actions:

    - enqueue a command call
    - dequeue the oldest command call in the queue

    # Events

    The command call queue is an
    [event source][xindmap.event.EventSource.EventSource].
    It dispatches event of types enumed in
    [`CommandCallQueueEvent`][xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent]
    class.

    ### call enqueued

    **Type**:
        [`CommandCallQueueEvent.call_enqueued`][xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent.call_enqueued]

    Args:
        call:
            The [command call][xindmap.command.CommandCall.CommandCall] that has 
            been enqueued.

    ### call dequeued

    **Type**: [`CommandCallQueueEvent.call_dequeued`][xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent.call_dequeued]

    Args:
        call:
            The [command call][xindmap.command.CommandCall.CommandCall] that has
            been dequeued.

    Attributes:
        __queue:
            The underlying container in which the
            [command calls][xindmap.command.CommandCall.CommandCall] are stored.
    """
    # command ******************************************************************
    def dequeue(self):
        """Dequeues a [command call][xindmap.command.CommandCall.CommandCall]
        from this queue.

        Dispatches the event
        [call dequeued][xindmap.command.CommandCallQueue.CommandCallQueue--call-dequeued].

        Raises an error if this queue is empty.

        Raises:
            CommandCallQueueError: If this queue is empty.
        """
        if not self.__queue:
            raise CommandCallQueueError("can not dequeue from an empty queue")

        command_call = self.__queue.pop()

        event = xindmap.event.Event(
            CommandCallQueueEvent.call_dequeued, call=command_call
        )
        self._dispatch_event(event)

    def enqueue(self, command_call):
        """Enqueues a [command call][xindmap.command.CommandCall.CommandCall] in
        this queue.

        Dispatches the event
        [call enqueued][xindmap.command.CommandCallQueue.CommandCallQueue--call-enqueued].

        Args:
            command_call:
                The [command call][xindmap.command.CommandCall.CommandCall] to
                enqueue.
        """
        self.__queue.appendleft(command_call)

        event = xindmap.event.Event(
            CommandCallQueueEvent.call_enqueued, call=command_call
        )
        self._dispatch_event(event)

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this queue.
        """
        super().__init__(CommandCallQueueEvent)

        self.__queue = collections.deque()
