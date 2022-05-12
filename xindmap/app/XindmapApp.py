import itertools
import kivy.app as kapp
import xindmap.controller as xcontroller
import xindmap.command as xcommand
import xindmap.logging as xlogging
import xindmap.mindmap as xmindmap
import xindmap.state as xstate
import xindmap.widget as xwidget

class XindmapApp(kapp.App):
    """the xindmap application class

    Attributes:
        editor_state: the state of the editor
        command_controller: the command controller
        command_tree: the command tree
        input_controller: the input controller
        keyboard_controller: the keyboard controller
        mind_map: the mind map
        root_widget: the root widget
    """
    # id ***********************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this app
        """
        super().__init__()

        self.__id = next(XindmapApp.__id_counter)

        self.editor_state = xstate.EditorState()
        self.command_tree = xcommand.CommandTree()
        self.mind_map = xmindmap.MindMap()

        self.command_controller = xcontroller.CommandController()
        self.input_controller = xcontroller.InputController()
        self.insert_controller = xcontroller.InsertController()
        self.keyboard_controller = xcontroller.KeyboardController()

        self.root_widget = xwidget.RootWidget()

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this app

        Returns:
            a string representation of this app
        """
        return 'xindmap app {}'.format(1)

    # init *********************************************************************
    def init(self):
        """initializes all the members of this application
        """
        self.command_controller.init(
            self.editor_state,
            self.command_tree,
            self.mind_map,
            self.root_widget.mind_map_widget,
            self.root_widget.output_widget
        )
        self.keyboard_controller.init(self.input_controller)
        self.input_controller.init(
            self.editor_state,
            self.command_controller,
            self.command_tree,
            self.root_widget.input_widget,
            self.insert_controller
        )
        self.insert_controller.init(
            self.mind_map
        )
        self.root_widget.mind_map_widget.init(
            self.mind_map
        )

        xlogging.info('{}: initialized', self)

    # build ********************************************************************
    def build(self):
        """builds this application
        """
        return self.root_widget
