from .CommandRegisterError import CommandRegisterError
from .CommandRegistrationError import CommandRegistrationError


class CommandRegister:
    # command ******************************************************************
    def __getitem__(self, command_name):
        if command_name not in self.__command_name_to_command:
            raise CommandRegisterError(
                f"no command registered under name {command_name}"
            )

        return self.__command_name_to_command[command_name]

    @property
    def command_names(self):
        return self.__command_name_to_command.keys()

    def register_command(self, name, command):
        if name in self.__command_name_to_command:
            raise CommandRegistrationError(f'command name "{name}" alreagy registered')

        self.__command_name_to_command[name] = command

    # constructor **************************************************************
    def __init__(self):
        self.__command_name_to_command = {}
