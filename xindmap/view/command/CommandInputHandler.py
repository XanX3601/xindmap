import re

from .CommandInput import CommandInput
from .CommandInputType import CommandInputType

class CommandInputHandler:
    """A command input handler.
    """
    def __init__(self):
        """Instantiates this command input handler.
        """
        self.__regexes = {
            CommandInputType.ENTER: re.compile('<CR>'),
            CommandInputType.DEFAULT: re.compile('.+')
        }

        # build split regex
        split_regex = [type for type in CommandInputType if type != CommandInputType.DEFAULT]
        split_regex = '|'.join(self.__regexes[type].pattern for type in split_regex)
        split_regex = '({})'.format(split_regex)
        split_regex = re.compile(split_regex)

        self.__split_regex = split_regex

    def string_to_command_inputs(self, string):
        """Converts a string to a list of command input.

        Args:
            string: the string to convert.

        Returns:
            A list of command input.
        """
        split_string = self.__split_regex.split(string)
        command_inputs = []

        for element in split_string:
            if self.__regexes[CommandInputType.ENTER].fullmatch(element):
                command_inputs.append(CommandInput(CommandInputType.ENTER))

            elif self.__regexes[CommandInputType.DEFAULT].fullmatch(element):
                command_inputs += [
                    CommandInput(CommandInputType.DEFAULT, c) for c in element
                ]

        return command_inputs


        

