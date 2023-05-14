import enum
import logging
import shlex

import xindmap.command
import xindmap.config
import xindmap.input
import xindmap.state
import xindmap.timer


class CommandControllerState(enum.Enum):
    """Internal state of
    [command controller][xindmap.controller.CommandController.CommandController].
    """
    free_typing = enum.auto()
    """Free typing mode.
    """
    mapping = enum.auto()
    """Mapping mode.
    """


class CommandController(xindmap.config.Configurable):
    """The command controller controlles the application whenever it is in the
    [`State.command`][xindmap.state.State.State.command] state.

    It watches [inputs][xindmap.input.Input.Input] in an
    [input stack][xindmap.input.InputStack.InputStack] and creates
    [command calls][xindmap.command.CommandCall.CommandCall].

    # State

    This controller works differently according to the the content of the 
    [input stack][xindmap.input.InputStack.InputStack] it deals with.

    ## free typing mode

    In this mode, the controller will create a
    [command call][xindmap.command.CommandCall.CommandCall] whenever a
    [input][xindmap.input.Input.Input] of type
    [`InputType.enter`][xindmap.input.InputType.InputType.enter] is
    [pushed][xindmap.input.InputStack.InputStack--input-pushed] in
    the [stack][xindmap.input.InputStack.InputStack].
    It then creates a [command call][xindmap.command.CommandCall.CommandCall]
    based on the [stack][xindmap.input.InputStack.InputStack] content.

    To enter this mode, the first [input][xindmap.input.Input.Input] in the 
    [stack][xindmap.input.InputStack.InputStack] must equal the
    `free_typing_input` passed upon instantiating this controller.

    ## mapping mode

    In this mode, the controller uses [inputs][xindmap.input.Input.Input] pushed
    in the [stack][xindmap.input.InputStack.InputStack] to explore the
    [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree] passed
    upon instatiating this controller.
    If it finds a mapping, it adds the mapped inputs to the
    [stack][xindmap.input.InputStack.InputStack].

    # Configurable

    The command controller is
    [configurable][xindmap.config.Configurable.Configurable].

    ### [`command_controller_mapping_delay_s`][xindmap.config.Variables.Variables.command_controller_mapping_delay_s]

    Configs the time, in seconds, for which the controller delay the approval
    of a input mapping when another input mapping starts with the same
    [inputs][xindmap.input.Input.Input].

    Attributes:
        __command_call_queue:
            The
            [command call queue][xindmap.command.CommandCallQueue.CommandCallQueue]
            in which enqueue the
            [command calls][xindmap.command.CommandCall.CommandCall] this
            controller creates.
        __free_typing_content:
            Buffer used to stored a text representation of the inputs in the
            [stack][xindmap.input.InputStack.InputStack] later use as a command
            name.
        __free_typing_input:
            The input that, if find as the first
            [input][xindmap.input.Input.Input] of the
            [stack][xindmap.input.InputStack.InputStack] changes the state of
            this controller to [free typing](#free-typing-mode)
        __input_mapping_tree:
            The
            [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree]
            in which find the mapping of inputs while this controller is in
            [mapping](#mapping-mode) mode.
        __input_stack:
            The [input stack][xindmap.input.InputStack.InputStack] this
            controller deals with.
        __is_active:
            Indicates wether this controller is active or not, depending on the
            [state][xindmap.state.State.State] of the application.
        __mapping_timer_id:
            Used to store the timer id returned by the
            [timer][xindmap.timer.Timer] to cancel the delay before approving a
            mapping of inputs if it can lead to another mapping.
        __mapping_delay_s:
            The length of the delay before approving a mapping of inputs if it
            can lead to another mapping in the
            [mapping tree][xindmap.input.InputMappingTree.InputMappingTree].
        __state_to_input_process:
            Dictionnary mapping a
            [state][xindmap.controller.CommandController.CommandControllerState]
            to a method used to process an [input][xindmap.input.Input.Input].
    """
    # callback *****************************************************************
    def on_input_stack_stack_cleared(self, input_stack, event):
        """Callback to be called upon
        [stack cleared][xindmap.input.InputStack.InputStack--stack-cleared]
        event dispatched by the
        [input stack][xindmap.input.InputStack.InputStack].

        If this controller is active, sets its state to
        [mapping][xindmap.controller.CommandController.CommandController--mapping-mode].

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the event.
            event: The event for which this callback is called.
        """
        logging.debug(
            f"command controller {id(self)}: on_input_stack_stack_cleared(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        self.__set_state(CommandControllerState.mapping)

    def on_input_stack_input_poped(self, input_stack, event):
        """Callback to be called upon
        [input poped][xindmap.input.InputStack.InputStack--input-poped] event
        dispatched by the [input stack][xindmap.input.InputStack.InputStack].

        If this controller is active and the
        [input stack][xindmap.input.InputStack.InputStack] is empty, sets this
        controller state to
        [mapping][xindmap.controller.CommandController.CommandController--mapping-mode].

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the event.
            event: The event for which this callback is called.
        """
        logging.debug(
            f"command controller {id(self)}: on_input_stack_input_poped(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        if len(input_stack) == 0:
            self.__set_state(CommandControllerState.mapping)

    def on_input_stack_input_pushed(self, input_stack, event):
        """Callback to be called upon
        [input pushed][xindmap.input.InputStack.InputStack--input-pushed] event
        dispatched by the [input stack][xindmap.input.InputStack.InputStack].

        Sets the
        [state][xindmap.controller.CommandController.CommandControllerState] of
        this controller to
        [free typing][xindmap.controller.CommandController.CommandController--free-typing-mode]
        if the
        [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree] is
        on its root and the [input][xindmap.input.Input.Input] that has been
        pushed in the [stack][xindmap.input.InputStack.InputStack] equals
        `self.__free_typing_input`.

        Processes the [input][xindmap.input.Input.Input] that has been pushed
        in the [stack][xindmap.input.InputStack.InputStack] with the process
        methods depending on this controller
        [state][xindmap.controller.CommandController.CommandControllerState].

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the event.
            event: the event for which this call back is called for.
        """
        logging.debug(
            f"command controller {id(self)}: on_input_stack_input_pushed(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        # if input is the first of the input stack and it is equal to free typing
        # input then, set the state to free typing
        if (
            self.__input_mapping_tree.is_on_root()
            and self.__state != CommandControllerState.free_typing
            and event.input == self.__free_typing_input
        ):
            self.__set_state(CommandControllerState.free_typing)
        else:
            self.__state_to_input_process[self.__state](event.input)

    def on_state_holder_state_set(self, state_holder, event):
        """Callback to be called upon
        [state set][xindmap.state.StateHolder.StateHolder--state-set] event
        dispatched by the [state holder][xindmap.state.StateHolder.StateHolder].

        Sets wether this controller is active or not depending on the
        application state.

        Args:
            state_holder:
                The [state holder][xindmap.state.StateHolder.StateHolder] that
                dispatched the event.
            event: The event this callback is called for.
        """
        logging.debug(
            f"command controller {id(self)}: on_state_holder_state_set(event={event})"
        )

        self.__is_active = event.state == xindmap.state.State.command

        if self.__is_active:
            self.__set_state(CommandControllerState.mapping)

    # config callback **********************************************************
    def on_config_variable_command_controller_mapping_delay_s_set(self, value):
        """Config callback called whenever
        [`command_controller_mapping_delay_s`][xindmap.config.Variables.Variables.command_controller_mapping_delay_s].
        config variable value is set.

        Args:
            value: The new value of the variable
        """
        self.__mapping_delay_s = value

    # constructor **************************************************************
    def __init__(
        self, command_call_queue, input_mapping_tree, free_typing_input, input_stack
    ):
        """Instantiates this controller.

        Args:
            command_call_queue:
                The
                [command call queue][xindmap.command.CommandCallQueue.CommandCallQueue]
                in which enqueue the
                [command calls][xindmap.command.CommandCall.CommandCall] this
                controller creates.
            input_mapping_tree:
                The
                [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree]
                containing the mapping of inputs this controller must use.
            free_typing_input:
                The [input][xindmap.input.Input.Input] toggling the
                [free typing mode][xindmap.controller.CommandController.CommandController--free-typing-mode]
                of this controller.
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] this
                controller deals with.
        """
        super().__init__((xindmap.config.Variables.command_controller_mapping_delay_s,))

        self.__command_call_queue = command_call_queue
        self.__input_mapping_tree = input_mapping_tree
        self.__free_typing_input = free_typing_input
        self.__input_stack = input_stack

        self.__is_active = False

        self.__mapping_timer_id = None
        self.__mapping_delay_s = (
            xindmap.config.Variables.command_controller_mapping_delay_s.default
        )

        self.__free_typing_content = ""

        self.__state_to_input_process = {
            CommandControllerState.free_typing: self.__free_typing_input_process,
            CommandControllerState.mapping: self.__mapping_input_process,
        }

        self.__set_state(CommandControllerState.mapping)

    # input ********************************************************************
    def __free_typing_input_process(self, input):
        """Processes an input as if this controller is on
        [free typing mode][xindmap.controller.CommandController.CommandController--free-typing-mode].

        Args:
            input: the input to process
        """
        if input.type == xindmap.input.InputType.default:
            self.__free_typing_content += input.value

        elif input.type == xindmap.input.InputType.enter:
            free_typing_content_split = shlex.split(self.__free_typing_content)

            if free_typing_content_split:
                command_name = free_typing_content_split[0]
                args = free_typing_content_split[1:]

                command_call = xindmap.command.CommandCall(command_name, args)
                self.__command_call_queue.enqueue(command_call)

            self.__input_stack.clear()

        elif input.type == xindmap.input.InputType.backspace:
            self.__free_typing_content = self.__free_typing_content[:-1]

            # since free typing is always triggered by a first input, the input
            # stack always has at least two elements
            self.__input_stack.pop()
            self.__input_stack.pop()

        elif input.type == xindmap.input.InputType.escape:
            self.__input_stack.clear()

    def __mapping_input_inputs(self, inputs):
        """Pushes the given inputs in the
        [input stack][xindmap.input.InputStack.InputStack].

        It is called upon approving a mapping of inputs.

        Args:
            inputs: Iterable containing the inputs to be pushed.
        """
        self.__input_stack.clear()

        for i in inputs:
            self.__input_stack.push(i)

    def __mapping_input_process(self, input):
        """Processed an input as if this controller is on
        [mapping mode][xindmap.controller.CommandController.CommandController--mapping-mode].

        Args:
            input: the input to process
        """
        # try to move in the mapping tree
        has_moved = self.__input_mapping_tree.move_to_child(input)

        # if it did not move, forget the mapping and reset everything
        if not has_moved:
            self.__input_stack.clear()
            return

        # if move and there was a delay, cancel it
        if self.__mapping_timer_id is not None:
            timer = xindmap.timer.Timer()
            timer.cancel_delay(self.__mapping_timer_id)

            self.__mapping_timer_id = None

        # if there is inputs on the current mapping node, inputs them directly
        # if the node is a leaf or delay the inputs
        if self.__input_mapping_tree.inputs is not None:
            inputs = self.__input_mapping_tree.inputs

            if self.__input_mapping_tree.can_move():
                timer = xindmap.timer.Timer()
                self.__mapping_timer_id = timer.delay(
                    self.__mapping_input_inputs,
                    (inputs,),
                    int(self.__mapping_delay_s * 1000),
                )
            else:
                self.__mapping_input_inputs(inputs)

    # state ********************************************************************
    def __set_state(self, state):
        """Sets this controller state.

        Args:
            state:
                The new
                [state][xindmap.controller.CommandController.CommandControllerState].
        """
        if state == CommandControllerState.mapping:
            self.__input_mapping_tree.move_to_root()
        elif state == CommandControllerState.free_typing:
            self.__free_typing_content = ""

        self.__state = state
