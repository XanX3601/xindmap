import enum

class State(enum.Enum):
    """available states
    """
    command = enum.auto()
    insert = enum.auto()
