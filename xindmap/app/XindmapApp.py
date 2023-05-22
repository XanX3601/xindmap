import logging
import json
import pathlib
import shlex

import customtkinter as ctk

import xindmap.command
import xindmap.config
import xindmap.controller
import xindmap.editable
import xindmap.input
import xindmap.mind_map
import xindmap.plugin
import xindmap.state
import xindmap.widget


class XindmapApp:
    """Core / root object of the Xindmap application.

    This object, considered to be unique during the lifetime of the application
    holds the other objects, setup their interaction and contain logic bricks
    that are necessary for plugins to work (see [`xindmap.plugin`][]).

    # `XindmapApp`

    This object is the core of Xindmap during its lifetime.
    It holds the different part of the application, setups their interaction
    and ensure their lifecycle along the application lifetime.

    The application is built upon a Model View Controller (MVC) architecture.

    ## Model

    Models contain logics, functions and data used by the application.
    Here are presented the models of the application:

    ### Command api

    The command api is an instance of
    [`CommandApi`][xindmap.command.CommandApi.CommandApi] class.
    It is given to commands upon invoking them so they can interact with the
    application through the established interface.

    ### Command call queue

    The command call queue is an instance of
    [`CommandCallQueue`][xindmap.command.CommandCallQueue.CommandCallQueue]
    class.
    All [command calls][xindmap.command.CommandCall.CommandCall] transist
    through this queue to be treater by the
    [command executor](#command-executor).

    ### Command register

    The command register is an instance of
    [`CommandRegister`][xindmap.command.CommandRegister.CommandRegister] class.
    It registers all commands available to the user.

    ### Input mapping tree

    The input mapping tree is an instance of
    [`InputMappingTree`][xindmap.input.InputMappingTree.InputMappingTree] class.
    It stores mapping from list of inputs to list of inputs.
    Its final purpose is for the user to create their custom mapping to simulate
    long serie of interaction via a few inputs.

    ### Input stack

    The input stack is an instance of
    [`InputStack`][xindmap.input.InputStack.InputStack] class.
    All [inputs][xindmap.input.Input.Input] passed through this queue
    to be later treated by the (`input controller`)[#input-controller].

    ### Plugin importer

    The plugin importer is an instance of
    [`PluginImporter`][xindmap.plugin.PluginImporter.PluginImporter] class.
    It is used to import plugins from python module which are classes derived
    from [`xindmap.plugin.Plugin.Plugin`] class.
    The plug importer instantiates plugins dynamically during runtime.

    ### State holder

    The state holder is an instance of
    [`StateHolder`][xindmap.state.StateHolder.StateHolder] class.
    It contains the current state of the application.

    ## Controller

    Controllers are the interface between the [view](#view) and the
    [models](#model).
    Controllers could be included in this application but it is more suitable to
    have them as sperate entities to ensure code modularity and not have a super
    objects.

    ### Command controller

    The command controller is an instance of
    [`xindmap.controller.CommandController.CommandController`] class.
    It controls the creation of
    [command calls][xindmap.command.CommandCall.CommandCall] from
    [inputs][xindmap.input.Input.Input] when the application is on
    [command][xindmap.state.State.State.command] state.

    ### Command executor

    The command executor is an instance of
    [`CommandExecutor`][xindmap.command.CommandExecutor.CommandExecutor] class.
    It handles the [command calls][xindmap.command.CommandCall.CommandCall]
    placed in the [command call queue](#command-call-queue) and executes the
    corresponding commands.

    ### Input controller

    The input controller is an instance of
    [`InputController`][xindmap.controller.InputController.InputController] class.
    It transforms user interaction into [inputs][xindmap.input.Input.Input].

    ## Widget

    Widgets are part of the graphic interface.

    ### Main window

    The main window is an instance of
    [`customtkinter.CTk`](https://github.com/TomSchimansky/CustomTkinter/wiki/CTk-(tkinter.Tk)).
    It is the parent of all widgets.

    ### Input stack viewer

    The input stack viewer is an instance of
    [`InputStackViewer`][xindmap.widget.InputStackViewer.InputStackViewer]
    class.
    It displays the content of the [input stack](#input-stack).

    ## Event

    [models](#model), [controllers](#controller) and [widgets](#widget)
    communicate through events.
    Xindmap implements its own event system on top of the main loop of
    [`tkinter`][] to have better named and control over the events.

    ### Event source

    - [command call queue](#command-call-queue)
        - [call enqueued][xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent.call_enqueued]:
          dispatched when a
          [command call][xindmap.command.CommandCall.CommandCall] is added to
          the queue.
        - [call dequeued][xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent.call_dequeued]:
          dispatched when a
          [command call][xindmap.command.CommandCall.CommandCall] is removed
          from the queue.
    - [input stack](#input-stack)
        - [input poped][xindmap.input.InputStackEvent.InputStackEvent.input_poped]:
          dispatched when an [input][xindmap.input.Input.Input] is removed from
          the stack.
        - [input pushed][xindmap.input.InputStackEvent.InputStackEvent.input_pushed]:
          dispatched when an [input][xindmap.input.Input.Input] is added to the
          stack.
        - [stack cleared][xindmap.input.InputStackEvent.InputStackEvent.stack_cleared]:
          dispatched when the stack is cleared.
    - [main window](#main-window)
        - configure: dispatched upon reconfiguration of the window (size, position,
          ...).
        - key: dispatched when the user press a key on the keyboard.
    - [state holder](#state-holder)
        - [state set][xindmap.state.StateHolderEvent.StateHolderEvent.state_set]:
          dispatched when the state of the application is set to a new value.

    ### Event schema

    ```mermaid
    flowchart LR
        command_call_queue(["command call queue"])
        call_dequeued{{"call dequeued"}}
        call_enqueued{{"call enqueued"}}

        command_controller(["command controller"])

        command_executor(["command executor"])

        main_window(["main window"])
        configure{{"configure"}}
        key{{"key"}}

        input_controller(["input controller"])

        input_stack(["input stack"])
        input_poped{{"input poped"}}
        input_pushed{{"input pushed"}}
        stack_cleared{{"stack cleared"}}

        input_stack_viewer(["input stack viewer"])

        state_holder(["state holder"])
        state_set{{"state set"}}

        xindmap_app(["xindmap app"])

        command_call_queue --> call_dequeued

        command_call_queue --> call_enqueued
        call_enqueued --> command_executor

        main_window --> configure
        configure --> xindmap_app

        main_window --> key
        key --> input_controller

        input_stack --> input_poped
        input_poped --> command_controller
        input_poped --> input_stack_viewer

        input_stack --> input_pushed
        input_pushed --> command_controller
        input_pushed --> input_stack_viewer

        input_stack --> stack_cleared
        stack_cleared --> command_controller
        stack_cleared --> input_stack_viewer

        state_holder --> state_set
        state_set --> command_controller
    ```

    ## Config

    Xindmap centralizes the configuration of its component in a singleton object
    from the [`Config`][xindmap.config.Config.Config] class.
    The goal of the config is for component to expose some variables to
    configure them or share variable among them.
    Components that derives from
    [`Configurable`][xindmap.config.Configurable.Configurable] class can be 
    configured on [`variables`][xindmap.config.Variables.Variables] they
    declared during their instantiation.
    Upon modifying variables through the
    [`config`][xindmap.config.Config.Config], the corresponding callbacks will
    be called and components will have the opportunity to process the new value.

    The [`config`][xindmap.config.Config.Config] is only mention here because it
    is part of the way the application works but it will be detailed in the
    documentation of the concerned components.

    Attributes:
        __command_api: [command api](#command-api)
        __command_call_queue: [command call queue](#command-call-queue)
        __command_controller: [command controller](#command-controller)
        __command_executor: [command executor](#command-executor)
        __command_register: [command register](#command-register)
        __init_file_path:
            Path to the application initialization file to read before starting
            it.
            It is specified upon instantiating this object.
            It is expected to be derived from [`pathlib.Path`][] class.
        __input_controller: [input controller](#input-controller)
        __input_mapping_tree: [input mapping tree](#input-mapping-tree)
        __input_stack: [input stack](#input-stack)
        __input_stack_viewer: [input stack viewer](#input-stack-viewer)
        __main_window: [main window](#main-window)
        __plugin_importer: [plugin importer](#plugin-importer)
        __previous_height:
            Holds the last observed main window height.
            Used to prevent replacing widgets upon any configuration event from
            the main window.
        __previous_width:
            Holds the last observed main window width.
            Used to prevent replacing widgets upon any configuration event from
            the main window.
        __state_hoder: [state holder](#state-holder)
    """
    # callback *****************************************************************
    def __callback_setup(self):
        """Registers callbacks from the attributes of this application for their
        expected event source.

        Upon starting the application, some callbacks should have already been
        registered at their expected sources.
        If not, the application will not respond to any user interaction.

        This method is called upon initializing this application using the
        [`init`][xindmap.app.XindmapApp.XindmapApp.init] method.
        """
        self.__command_call_queue.register_callbacks(
            xindmap.command.CommandCallQueueEvent.call_enqueued,
            self.__command_executor.on_command_call_queue_call_enqueued,
        )
        self.__editable_holder.register_callbacks(
            xindmap.editable.EditableHolderEvent.editable_set,
            self.__edit_controller.on_editable_holder_editable_set
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.input_poped,
            self.__command_controller.on_input_stack_input_poped,
            self.__input_stack_viewer.on_input_stack_input_poped,
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.input_pushed,
            self.__command_controller.on_input_stack_input_pushed,
            self.__edit_controller.on_input_stack_input_pushed,
            self.__input_stack_viewer.on_input_stack_input_pushed,
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.stack_cleared,
            self.__command_controller.on_input_stack_stack_cleared,
            self.__input_stack_viewer.on_input_stack_stack_cleared,
        )
        self.__mind_map.register_callbacks(
            xindmap.mind_map.MindMapEvent.cleared,
            self.__mind_map_viewer.on_mind_map_cleared
        )
        self.__mind_map.register_callbacks(
            xindmap.mind_map.MindMapEvent.node_added,
            self.__mind_map_viewer.on_mind_map_node_added
        )
        self.__mind_map.register_callbacks(
            xindmap.mind_map.MindMapEvent.node_deleted,
            self.__mind_map_viewer.on_mind_map_node_deleted
        )
        self.__mind_map.register_callbacks(
            xindmap.mind_map.MindMapEvent.node_selected,
            self.__mind_map_viewer.on_mind_map_node_selected
        )
        self.__mind_map.register_callbacks(
            xindmap.mind_map.MindMapEvent.node_title_set,
            self.__mind_map_viewer.on_mind_map_node_title_set
        )
        self.__state_holder.register_callbacks(
            xindmap.state.StateHolderEvent.state_set,
            self.__command_controller.on_state_holder_state_set,
            self.__edit_controller.on_state_holder_state_set,
            self.__state_viewer.on_state_holder_state_set,
        )

        self.__main_window.bind("<Configure>", self.on_configure)
        self.__main_window.bind_all("<Key>", self.__input_controller.on_key)

    def on_configure(self, event):
        """Callback to be called upon configuration changes from the main window
        of the application.

        It replaces widgets if the size of the main window has changed.

        Args:
            event:
                Event for which this callback is called.
                It is only used for logging as the size of the main window is
                direcly queried at the window.
        """
        logging.debug(f"xindmap app {id(self)}: on_configure(event={event})")

        height = self.__main_window.winfo_height()
        width = self.__main_window.winfo_width()

        if self.__previous_height != height or self.__previous_width != width:
            self.__previous_width = width
            self.__previous_height = height

            self.__place_widget()

    # command ******************************************************************
    def __command_import(self, plugin_name, api):
        """Imports a plugin and registers its commands.

        This is one of the few command that is available by default.

        Args:
            plugin_name: The plugin to import identified by its module name.
            api:
                Command api used to interact with the application.
                It is not used here because `self` already has full access to
                the application and can interact directly with it.
        """
        plugins = self.__plugin_importer.import_plugins_from_module(plugin_name)

        for plugin in plugins:
            for command_name, command in plugin.commands():
                self.__command_register.register_command(command_name, command)

        logging.info(f'imported plugin "{plugin_name}"')

    def __command_load(self, file_path, api):
        self.__mind_map.clear()

        file_path = pathlib.Path(file_path)
        if not file_path.is_file():
            raise ValueError(f"not a file \"{file_path}\"")

        with file_path.open("r") as file:
            node_dict = json.load(file)
        
        api.populate_from_dict(node_dict, True)
        api.select_node(self.__mind_map.root_node_id)
        api.center_view(self.__mind_map.root_node_id)

        self.__last_file_path = file_path

    def __command_quit(self, api):
        self.__main_window.quit()
        exit(0)

    def __command_save(self, file_path=None, api=None):
        if file_path is None:
            file_path = self.__last_file_path

        if file_path is None:
            raise ValueError(f"can not save as no file was given")

        file_path = pathlib.Path(file_path)
        root_dict = api.to_dict()

        with file_path.open("w") as file:
            json.dump(root_dict, file, indent=2)

    # constructor **************************************************************
    def __init__(self, init_file_path):
        """Instantiates the application.

        Instantiates data model, controller and widgets in the correct order
        so that dependencies are respected.
        Does not setup the application further.
        Setup steps are done during initialization in
        [`init`][xindmap.app.XindmapApp.XindmapApp.init] method to make code
        clearer.

        Args:
            init_file_path:
                Path to the initialization file read during the initialization
                of the application.
                It is expected to be an instance of [`pathlib.Path`][] class.
        """
        # data *******************************************************
        self.__init_file_path = init_file_path

        self.__previous_height = None
        self.__previous_width = None

        self.__last_file_path = None

        # model ******************************************************
        self.__plugin_importer = xindmap.plugin.PluginImporter()

        self.__command_call_queue = xindmap.command.CommandCallQueue()
        self.__command_register = xindmap.command.CommandRegister()
        self.__editable_holder = xindmap.editable.EditableHolder()
        self.__input_mapping_tree = xindmap.input.InputMappingTree()
        self.__input_stack = xindmap.input.InputStack()
        self.__mind_map = xindmap.mind_map.MindMap()
        self.__state_holder = xindmap.state.StateHolder()

        # controller ************************************************
        self.__command_controller = xindmap.controller.CommandController(
            self.__command_call_queue,
            self.__input_mapping_tree,
            xindmap.input.Input(xindmap.input.InputType.default, ":"),
            self.__input_stack,
        )
        self.__edit_controller = xindmap.controller.EditController(self.__state_holder)
        self.__input_controller = xindmap.controller.InputController(self.__input_stack)

        # widget *****************************************************
        self.__main_window = ctk.CTk()
        self.__mind_map_viewer = xindmap.widget.MindMapViewer(self.__main_window)
        self.__input_stack_viewer = xindmap.widget.InputStackViewer(self.__main_window)
        self.__state_viewer = xindmap.widget.StateViewer(self.__main_window)

        # api ********************************************************
        self.__command_api = xindmap.command.CommandApi(
            self.__input_mapping_tree,
            self.__mind_map,
            self.__mind_map_viewer,
            self.__state_holder
        )

        # executor ***************************************************
        self.__command_executor = xindmap.command.CommandExecutor(
            self.__command_api, self.__command_register
        )

    # initialize ***************************************************************
    def init(self):
        """Initializes this application.

        Setups callbacks between attributes.

        Registers default commands.

        Read the initialization file.

        Sets the default state of the application.
        """
        self.__callback_setup()

        self.__command_register.register_command("import", self.__command_import)
        self.__command_register.register_command("quit", self.__command_quit)
        self.__command_register.register_command("q", self.__command_quit)
        self.__command_register.register_command("load", self.__command_load)
        self.__command_register.register_command("save", self.__command_save)

        self.__read_init_file()

        self.__editable_holder.set_editable(self.__mind_map)
        self.__state_holder.set_state(xindmap.state.State.command)

    def __read_init_file(self):
        """Reads the initialization file and enqueues command call read.

        The initialization file is expected to be filled with
        [command calls][xindmap.command.CommandCall.CommandCall] on each line.
        The initialization file is read line by line.
        Each line is assumed to contain one of these:

        - Command call:

          A space separated list of words starting by the command name followed
          by arguments.

        - Comment:

          A free typing line starting by `#`.

        Lines can contains any amount of spaces or tabs at start or end of the
        line without any consequences.
        """
        if self.__init_file_path is None:
            return

        with self.__init_file_path.open("r") as init_file:
            for line in init_file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                line_split = shlex.split(line)

                command_call = xindmap.command.CommandCall(
                    line_split[0], line_split[1:]
                )
                self.__command_call_queue.enqueue(command_call)

    # start ********************************************************************
    def start(self):
        """Starts this application by starting [`tkinter`][] main loop.
        """
        self.__main_window.mainloop()

    # widget *******************************************************************
    def __place_widget(self):
        """Places widgets inside the main window.

        It is not mandatory for widgets to use the `place` method to set their
        position in the main window, the name of the method was chose
        arbitrarly.
        """
        self.__input_stack_viewer.place(
            anchor=ctk.NW,
            relwidth=0.825,
            relx=0.15,
            y=self.__main_window.winfo_height() - 30,
        )
        self.__mind_map_viewer.place(
            anchor=ctk.NW,
            relwidth=1,
            relheight=1,
            x=0,
            y=0
        )
        self.__state_viewer.place(
            anchor=ctk.NW,
            relwidth=.10,
            relx=0.025,
            y=self.__main_window.winfo_height() - 30,
        )
