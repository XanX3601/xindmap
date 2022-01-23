from .CommandInputType import CommandInputType

class CommandInput:
    """A command input.

    Attributes:
        type: command input's type.
        value: command input's value.
    """
    def __init__(self, type, value=None):
        """Instantiates this command input.

        Args:
            type: command input's type.
            value: command input's value. None by default.
        """
        self.type = type
        self.value = value

        self.__type_value_str = '{}_{}'.format(type, value)

    def __hash__(self):
        """Computes this command input's hash value.

        Returns:
            This command input's hash value.
        """
        return hash(self.__type_value_str)

    def __eq__(self, other_command_input):
        """Tests wether this command input equals another command input.

        Args:
            other_command_input: the other command input.

        Returns:
            true if this command input equals the other one, false otherwise.
        """
        if not isinstance(other_command_input, CommandInput):
            return False

        if self.type == CommandInputType.ENTER:
            return self.type == other_command_input.type

        # DEFAULT
        return self.type == other_command_input.type \
            and self.value == other_command_input.value

    def __str__(self):
        """Returns a string representation of this command input.

        Returns:
            A string representation of this command input.
        """
        return self.__type_value_str

    def __repr__(self):
        """Returns a small string representation of this command input.

        Returns:
            A small string representation of this command input
        """
        return self.__type_value_str

