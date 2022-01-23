class CommandNode:
    """A command node.

    Attributes:
        command:
            the command holded by this node. None if this node does not hold a
            command.
    """
    def __init__(self, command=None):
        """Instantiates this command node.

        Args:
            command:
                the command holded by this node. None if this node does not hold
                a command. None by default.
        """
        self.command = command
        self.__neighbors = {}

    def __setitem__(self, command_input, neighbor):
        """Sets command input as link between this command node and the given
        neighbor.

        Args:
            command_input:
                command input linking this node to the given neighbor.
            neighbor:
                the neighbor linked to this node by the given command input.
        """
        self.__neighbors[command_input] = neighbor

    def __getitem__(self, command_input):
        """Gets the neighbor linked to this node by the given command input or
        None if such a neighbor does not exist.

        Args:
            command_input:
                the command input linking this node to the desired neighbor.

        Returns:
            The neighbor linked to this node by the given command input or None
            if such a neighbor does not exist.
        """
        return self.__neighbors.get(command_input, None)

    def __contains__(self, command_input):
        """Tests wether it exists a neighbor linked to this node by the given
        command input.

        Args:
            command_input:
                the command input that may link this node to one of its
                neighbor.

        Returns:
            True if there is a neighbor linked to this node by the given command
            input, false otherwise.
        """
        return command_input in self.__neighbors

