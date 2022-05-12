import inspect
import itertools
import kivy.app as kapp
import xindmap.input as xinput
import xindmap.logging as xlogging
import xindmap.state as xstate

class CommandController:
    """command controller
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this controller
        """
        self.__id = next(CommandController.__id_counter)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this controller

        Returns:
            a string representation of this controller
        """
        return 'command controller {}'.format(self.__id)

    # execute ******************************************************************
    def execute(self, command):
        """executes a command

        Args:
            command: the command to execute
        """
        if command in self._commands:
            xlogging.info('{}: execute command {}', self, command)

            self._commands[command]()
        else:
            xlogging.debug('{}: command {} unknown', self, command)

    # init *********************************************************************
    def init(self,
        editor_state,
        command_tree,
        mind_map,
        mind_map_widget,
        output_widget
    ):
        """initializes this controller

        Args:
            editor_state: the stat of the editor
            command_tree: the command tree
            mind_map: the mind map
            mind_map_widget: the mind map widget
            output_widget: the output widget
        """
        self._editor_state = editor_state
        self._commands = {}
        self._command_tree = command_tree
        self._mind_map = mind_map
        self._mind_map_widget = mind_map_widget
        self._output_widget = output_widget

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

        xlogging.info('{}: initialized', self)

    # command ******************************************************************
    def command_add_node(self):
        """adds a node in the mind map
        """
        self._mind_map.add_node()

        xlogging.info('{}: command add_node done', self)

    def command_insert_mode(self):
        """changes the cu
        """
        if self._mind_map.current_node is None:
            self._output_widget.error('no node selected')
        else:
            self._editor_state.state = xstate.State.insert

        xlogging.info('{}: command insert_node done', self)

    def command_quit(self):
        """quits the application
        """
        kapp.App.get_running_app().stop()

    def command_view_center(self):
        """centers the view on the current mind node
        """
        self._mind_map_widget.center_on_current_mind_node_widget()

        xlogging.info('{}: command view_center done', self)

    """
    def command_test(self):
        self._canvas_widget.scatter.center = self._canvas_widget.center

    def command_scale(self):
        self._canvas_widget.scatter.scale *= 1.1

    def command_left(self):
        self._canvas_widget.scatter.x -= 10

    def command_truc(self):
        print(
            'temp center', self._canvas_widget.temp.center
        )
        print('temp pos', self._canvas_widget.pos)
        print('scatter center', self._canvas_widget.scatter.center)
        print('scatter pos', self._canvas_widget.scatter.pos)

        x_center, y_center = self._canvas_widget.center
        x_node, y_node = self._canvas_widget.temp.center
        x_node, y_node = self._canvas_widget.scatter.to_parent(x_node, y_node)

        print(x_center, y_center)
        print(x_node, y_node)

        delta_x = x_center - x_node
        delta_y = y_center - y_node

        print(delta_x, delta_y)

        self._canvas_widget.scatter.x += delta_x
        self._canvas_widget.scatter.y += delta_y
    """
