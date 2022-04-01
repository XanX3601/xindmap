import enum

class InputType(enum.Enum):
    """type of input
    """
    default = enum.auto()
    backspace = enum.auto()
    enter = enum.auto()
    escape = enum.auto()
