import enum


class State(enum.Enum):
    command = enum.auto()
    input = enum.auto()
    none = enum.auto()
