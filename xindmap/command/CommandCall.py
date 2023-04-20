class CommandCall:
    """Call to a command for it to be executed later on.

    Attributes:
        __command_name: The name of the command.
        __args:
            List of arguments to be passed on to the command upon its execution.
    """
    # constructor **************************************************************
    def __init__(self, command_name, args):
        """Instantiates this command call.

        Args:
            command_name: The name of the command.
            args:
                List of arguments to be passed on to the commands upon its
                execution.
        """
        self.__command_name = command_name
        self.__args = args

    # property *****************************************************************
    @property
    def args(self):
        """Returns the arguments to be passed on to the command upon its
        execution.
        """
        return self.__args

    @property
    def command_name(self):
        """Returns the name of the command.
        """
        return self.__command_name

    # string *******************************************************************
    def __repr__(self):
        """Same as [`__str__`][xindmap.command.CommandCall.CommandCall.__str__].
        """
        return str(self)

    def __str__(self):
        """Returns a string representation of this command call.
        """
        return f"<command_call {self.__command_name} args={self.__args}>"
