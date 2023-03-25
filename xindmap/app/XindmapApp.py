import logging

import customtkinter as ctk

import xindmap.command
import xindmap.config
import xindmap.controller
import xindmap.input
import xindmap.plugin
import xindmap.state
import xindmap.widget


class XindmapApp:
    """Xindmap application root object.

    It contains all the models, controller, executor and widget composing the
    application.
    It ensures their lifecycle during the application lifetime.
    It also ensures the registration of the callbacks to the events.
    """
    # callback *****************************************************************
    def __callback_setup(self):
        self.__command_call_queue.register_callbacks(
            xindmap.command.CommandCallQueueEvent.call_enqueued,
            self.__command_executor.on_command_call_queue_call_enqueued,
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.input_poped,
            self.__command_controller.on_input_stack_input_poped,
            self.__input_stack_viewer.on_input_stack_input_poped,
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.input_pushed,
            self.__command_controller.on_input_stack_input_pushed,
            self.__input_stack_viewer.on_input_stack_input_pushed,
        )
        self.__input_stack.register_callbacks(
            xindmap.input.InputStackEvent.stack_cleared,
            self.__command_controller.on_input_stack_stack_cleared,
            self.__input_stack_viewer.on_input_stack_stack_cleared,
        )
        self.__state_holder.register_callbacks(
            xindmap.state.StateHolderEvent.state_set,
            self.__command_controller.on_state_holder_state_set,
        )

        self.__main_window.bind_all("<Key>", self.__input_controller.on_key)
        self.__main_window.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """Callback ìnvoked upon modification of the main window size or
        position.

        Places the widgets if the size of the main window changed.

        Args:
            event: The even for which the callback is invoked.
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
        plugins = self.__plugin_importer.import_plugins_from_module(plugin_name)

        for plugin in plugins:
            for command_name, command in plugin.commands():
                self.__command_register.register_command(command_name, command)

        logging.info(f'imported plugin "{plugin_name}"')

    # constructor **************************************************************
    def __init__(self, init_file_path):
        """Instantiates this xindmap app.

        Instantiates all the models, controllers, executors and widgets 
        independently.
        """
        # data *******************************************************
        self.__init_file_path = init_file_path

        self.__previous_height = None
        self.__previous_width = None

        # model ******************************************************
        self.__plugin_importer = xindmap.plugin.PluginImporter()

        self.__command_api = xindmap.command.CommandApi()
        self.__command_mapping_tree = xindmap.command.CommandMappingTree()
        self.__command_call_queue = xindmap.command.CommandCallQueue()
        self.__command_register = xindmap.command.CommandRegister()
        self.__input_stack = xindmap.input.InputStack()
        self.__state_holder = xindmap.state.StateHolder()

        # controller / executor **************************************
        self.__command_executor = xindmap.command.CommandExecutor(
            self.__command_api, self.__command_register
        )

        self.__command_controller = xindmap.controller.CommandController(
            self.__command_call_queue,
            self.__command_mapping_tree,
            xindmap.input.Input(xindmap.input.InputType.default, ":"),
            self.__input_stack,
        )
        self.__input_controller = xindmap.controller.InputController(self.__input_stack)

        # widget *****************************************************
        self.__main_window = ctk.CTk()
        self.__input_stack_viewer = xindmap.widget.InputStackViewer(self.__main_window)

    # initialize ***************************************************************
    def init(self):
        """Initializes this application by setupping callbacks, registering the
        commands and reading the initialization file.

        This method should be called before starting the application via the 
        [`Xindmap.start`][xindmap.app.XindmapApp.XindmapApp.start] method.
        """
        self.__callback_setup()

        self.__command_register.register_command("import", self.__command_import)

        self.__read_init_file()

        self.__state_holder.set_state(xindmap.state.State.command)

    def __read_init_file(self):
        if self.__init_file_path is None:
            return

        with self.__init_file_path.open("r") as init_file:
            for line in init_file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                line_split = line.split()

                command_call = xindmap.command.CommandCall(
                    line_split[0], line_split[1:]
                )
                self.__command_call_queue.enqueue(command_call)

    # start ********************************************************************
    def start(self):
        """Starts this application.

        Without initialization this application first via the
        [`Xindmap.init`][xindmap.app.XindmapApp.XindmapApp.init] method, the
        application will not behave as intented.
        """
        self.__main_window.mainloop()

    # widget *******************************************************************
    def __place_widget(self):
        self.__input_stack_viewer.place(
            anchor=ctk.NW,
            relwidth=0.95,
            height=20,
            relx=0.025,
            y=self.__main_window.winfo_height() - 30,
        )
