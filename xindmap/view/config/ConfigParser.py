import re

import xindmap.view.command as xcommand

from .Config import Config
from .ConfigParserException import ConfigParserException

class ConfigParser:
    """Hold and update a default config.

    Holds a default config that is updated when parsing config files or settings
    value.

    Attributes:
        config: the config.
        command_input_handler: the command input handler used by this parser.
    """
    def __init__(self, command_dict):
        """Instantiates self config parser.

        Args:
            command_dict:
                a dictionnary associating command name to command.
        """
        self.config = Config()
        self.__command_dict = command_dict

        self.command_input_handler = xcommand.CommandInputHandler()

        self.__line_starts_to_method = {
            'map': self.map
        }
        self.__map_regex = re.compile('map [^ ]* [^ ]*')

    def __build_command_tree(self):
        """Builds the command tree in the config based on the command dict.

        This method is called upon instantiating this config parser.
        It is called once to build the command tree in its default state.
        """
        for command in self.__command_dict.values():
            command_path_as_str = ':{}<CR>'.format(command.name)
            self.config.command_tree.add_path(
                self.command_input_handler.string_to_command_inputs(command_path_as_str),
                command
            )

    def parse_config_file(self, file_path):
        """Parses a config file to update the internal config.

        Args:
            file_path: the path to the config file to parse.
        """
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                if line[-1] == '\n':
                    line = line[:-1]

                line_split = line.split()

                if len(line_split) >= 0:
                    line_start = line_split[0]

                    if line_start in self.__line_starts_to_method:
                        self.__line_starts_to_method[line_start](line)

    def map(self, line):
        """Maps a keyboard pattern to a command.

        The line is expected to follow the pattern:

            map [^ ]* [^ ]*

        Args:
            line: the line to parse.

        Raises:
            ConfigParserException:
                raised when an error occurs while parsing the line.
        """
        if not self.__map_regex.fullmatch(line):
            raise ConfigParserException(
                'line "{}" does not match excpected pattern "map [^ ]* [^ ]*"'
            )

        _, path, command_name = line.split()

        if command_name not in self.__command_dict:
            raise ConfigParserException(
                'unknown command "{}"'.format(command_name)
            )

        self.config.command_tree.add_path(
            self.command_input_handler.string_to_command_inputs(path),
            self.__command_dict[command_name]
        )

