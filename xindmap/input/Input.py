class Input:
    """Represents an input by the user.

    Attributes:
        __type: The [type][xindmap.input.InputType.InputType] of the input.
        __value: The value of the input.
    """
    # constructor **************************************************************
    def __init__(self, type, value=None):
        """Instantiates this input

        Args:
            type: The [type][xindmap.input.InputType.InputType] of this input.
            value: The value of this input, [`None`][] by default.
        """
        self.__type = type
        self.__value = value

    # input ********************************************************************
    def __eq__(self, other_input):
        """Tests wether this input equals another.

        This input equals another one if it the other
        [is an instance][isinstance] of [`Input`][xindmap.input.Input.Input]
        class and they share the same
        [type][xindmap.event.EventSource.EventSource--event-type] and value.

        Args:
            other_input: The object to which compare this input.

        Returns:
            [`True`][] if this input equals `other_input`, [`False`][]
            otherwise.
        """
        if not isinstance(other_input, Input):
            return False

        return self.__type == other_input.__type and self.__value == other_input.__value

    # property *****************************************************************
    @property
    def type(self):
        """Returns the type of this input
        """
        return self.__type

    @property
    def value(self):
        """Returns the value of this input
        """
        return self.__value

    # string *******************************************************************
    def __repr__(self):
        """Same as [`__str__`][xindmap.input.Input.Input.__str__].
        """
        return str(self)

    def __str__(self):
        """Returns a string representation of this input.
        """
        return f"<input {self.type.name} value={self.value}>"
