import inspect
import kivy.app as kapp
import kivy.logger as klogger
import xindmap.input as xinput

class CommandController:
    """command controller
    """
    def __init__(self):
        """instantiates this controller
        """
        pass

    def execute(self, command):
        """executes a command

        Args:
            command: the command to execute
        """
        klogger.Logger.info(
            '[command controller] command {} submitted'.format(command)
        )

        if command in self._commands:
            self._commands[command]()

    def init(self, mind_map, mind_map_widget, command_tree):
        """initializes this controller

        Args:
            mind_map: the mind map
            mind_map_widget: the mind map widget
            command_tree: the command tree
        """
        self._mind_map = mind_map
        self._mind_map_widget = mind_map_widget
        self._commands = {}
        self._command_tree = command_tree

        for method_name, method in inspect.getmembers(self, inspect.ismethod):
            if method_name.startswith('command'):
                command_name = method_name.removeprefix('command_')

                self._commands[command_name] = method

                inputs = [
                    xinput.Input(xinput.InputType.default, c) for c in command_name
                ]
                inputs.insert(0, xinput.Input(xinput.InputType.default, ':'))
                inputs.append(xinput.Input(xinput.InputType.enter))

                self._command_tree.add_command(command_name, inputs)

    def command_add_node(self):
        """adds a node in the mind map
        """
        self._mind_map.add_node()
        klogger.Logger.info('[command controller] command add_node done')

    def command_quit(self):
        """quits the application
        """
        kapp.App.get_running_app().stop()

