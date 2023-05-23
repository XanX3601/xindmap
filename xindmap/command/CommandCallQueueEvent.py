import enum


class CommandCallQueueEvent(enum.Enum):
    """Event types dispatched by
    [`CommandCallQueue`][xindmap.command.CommandCallQueue.CommandCallQueue]
    class.
    """

    call_dequeued = enum.auto()
    """A call has been dequeued from the command call queue."""
    call_enqueued = enum.auto()
    """A call has been enqueued to the command call queue."""
