from .CommandRegisterError import CommandRegisterError
from .CommandRegistrationError import CommandRegistrationError


class CommandRegister:
    """A register containing commands under a unique name.

    Attributes:
        __command_name_to_command: Dictionnary mapping command name to command.
    """

    # command ******************************************************************
    def __getitem__(self, command_name):
        """Gets a command from its name.

        Args:
            command_name: The name of the command.

        Returns:
            The command mapped to the given name.

        Raises:
            CommandRegisterError: If no command exists in this register under
                the given name.
        """
        if command_name not in self.__command_name_to_command:
            raise CommandRegisterError(
                f"no command registered under name {command_name}"
            )

        return self.__command_name_to_command[command_name]

    @property
    def command_names(self):
        """Returns all registered command names."""
        return self.__command_name_to_command.keys()

    def register_command(self, name, command):
        """Registers a command.

        Args:
            name: The name under which register the command.
            command: The comamnd to register.

        Raises:
            CommandRegistrationError: If a command is already registered under
                the same name.
        """
        if name in self.__command_name_to_command:
            raise CommandRegistrationError(f'command name "{name}" alreagy registered')

        self.__command_name_to_command[name] = command

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this register."""
        self.__command_name_to_command = {}
