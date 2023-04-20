import enum


class State(enum.Enum):
    """States of xindmap application.
    """
    command = enum.auto()
    """The application is waiting for the user to enter commands.
    """
    input = enum.auto()
    """The application is letting a user free type inside a text.
    """
    none = enum.auto()
    """The application is in no particular state.
    """
