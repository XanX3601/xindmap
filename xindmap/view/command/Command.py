class Command:
    """A command.

    Attributes:
        name: command's name.
        description: command's description.
    """
    def __init__(self, name, description):
        """Instantiates this command.

        Args:
            name: command's name.
            description: command's description.
        """
        self.name = name
        self.description = description
        
    def __eq__(self, other_command):
        """Tests wether this command equals another one.

        Args:
            other_command: another command.

        Returns:
            True if this command equals the other one, false otherwise.
        """
        if not isinstance(other_command, Command):
            return False

        return self.name == other_command.name
