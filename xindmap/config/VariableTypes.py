import enum


class VariableTypes(enum.Enum):
    """The list of available types for
    [variables][xindmap.config.Variable.Variable].
    """

    int = enum.auto()
    """Integer.
    """
    float = enum.auto()
    """Floating number (including integer ones).
    """
    string = enum.auto()
    """String.
    """
