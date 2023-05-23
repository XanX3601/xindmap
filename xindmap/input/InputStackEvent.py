import enum


class InputStackEvent(enum.Enum):
    """Event types dispatched by
    [`InputStack`][xindmap.input.InputStack.InputStack] class.
    """

    input_poped = enum.auto()
    """An [input][xindmap.input.Input.Input] has been poped out of the stack."""
    input_pushed = enum.auto()
    """An [input][xindmap.input.Input.Input] has been pushed in the stack."""
    stack_cleared = enum.auto()
    """The stack has been cleared of all its
    [inputs][xindmap.input.Input.Input].
    """
