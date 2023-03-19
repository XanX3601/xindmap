import enum


class CommandCallQueueEvent(enum.Enum):
    call_enqueued = enum.auto()
    call_dequeued = enum.auto()
