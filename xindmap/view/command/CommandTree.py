from .CommandNode import CommandNode

class CommandTree:
    """A command tree.
    """
    def __init__(self):
        """Instantiates this command tree.
        """
        self.__root_node = CommandNode()
        self.__current_node = self.__root_node

    def add_path(self, command, command_inputs):
        """Adds a path from the root to the given command composed of each
        command input in the list.

        If the path of command inputs already led to a command, replaces it.

        Args:
            command: a command.
            command_inputs: a list of command input.
        """
        current_node = self.__root_node

        for command_input in command_inputs:
            if command_input not in current_node:
                current_node[command_input] = CommandNode()

            current_node = current_node[command_input]

        current_node.command = command

    def current_command(self):
        """Returns the command holded by the current node or None if the current
        node does not hold a command.

        Returns:
            The command holded by the current node or None if it does not hold
            any.
        """
        return self.__current_node.command

    def input(self, command_input):
        """Changes the current node for its neighbor linked to it by the given
        command input.

        Does not change the current node if no neighbor is linked to it by the
        command input.

        Args:
            command_input: a command input.

        Returns:
            True if the current node has changed, false otherwise.
        """
        result = command_input in self.__current_node

        if result:
            self.__current_node = self.__current_node[command_input]

        return result

    def root(self):
        """Changes the current node to the root of the tree.
        """
        self.__current_node = self.__root_node
