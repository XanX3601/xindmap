import enum


class State(enum.Enum):
    """States of xindmap application.
    """
    command = enum.auto()
    """The application is waiting for the user to enter commands.
    """
    none = enum.auto()
    """The application is in no particular state.
    """
