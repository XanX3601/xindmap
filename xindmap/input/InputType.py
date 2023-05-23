import enum


class InputType(enum.Enum):
    """Types of [input][xindmap.input.Input.Input]."""

    backspace = enum.auto()
    """Equivalent of a backspace key.
    """
    default = enum.auto()
    """Default.
    """
    enter = enum.auto()
    """Validate / enter key.
    """
    escape = enum.auto()
    """Escape key.
    """
