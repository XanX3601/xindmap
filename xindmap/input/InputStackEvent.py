import enum


class InputStackEvent(enum.Enum):
    input_poped = enum.auto()
    input_pushed = enum.auto()
    stack_cleared = enum.auto()
