import enum
import logging

import xindmap.command
import xindmap.config
import xindmap.input
import xindmap.state
import xindmap.timer


class CommandControllerState(enum.Enum):
    free_typing = enum.auto()
    mapping = enum.auto()


class CommandController(xindmap.config.Configurable):
    # callback *****************************************************************
    def on_input_stack_stack_cleared(self, input_stack, event):
        logging.debug(
            f"command controller {id(self)}: on_input_stack_stack_cleared(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        self.__set_state(CommandControllerState.mapping)

    def on_input_stack_input_poped(self, input_stack, event):
        logging.debug(
            f"command controller {id(self)}: on_input_stack_input_poped(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        if len(input_stack) == 0:
            self.__set_state(CommandControllerState.mapping)

    def on_input_stack_input_pushed(self, input_stack, event):
        logging.debug(
            f"command controller {id(self)}: on_input_stack_input_pushed(event={event})"
        )

        # if this controller is not active then do nothing
        if not self.__is_active:
            return

        # if input is the first of the input stack and it is equal to free typing
        # input then, set the state to free typing
        if (
            self.__command_mapping_tree.is_on_root()
            and event.input == self.__free_typing_input
        ):
            self.__set_state(CommandControllerState.free_typing)
        else:
            self.__state_to_input_process[self.__state](event.input)

    def on_state_holder_state_set(self, state_holder, event):
        logging.debug(
            f"command controller {id(self)}: on_state_holder_state_set(event={event})"
        )

        self.__is_active = event.state == xindmap.state.State.command

        if self.__is_active:
            self.__set_state(CommandControllerState.mapping)

    # config callback **********************************************************
    def on_config_variable_command_controller_mapping_delay_s_set(self, value):
        pass

    # constructor **************************************************************
    def __init__(
        self, command_call_queue, command_mapping_tree, free_typing_input, input_stack
    ):
        super().__init__((xindmap.config.Variables.command_controller_mapping_delay_s,))

        self.__command_call_queue = command_call_queue
        self.__command_mapping_tree = command_mapping_tree
        self.__free_typing_input = free_typing_input
        self.__input_stack = input_stack

        self.__is_active = False

        self.__mapping_timer_id = None
        self.__mapping_delay_s = (
            xindmap.config.Variables.command_controller_mapping_delay_s.default
        )

        print(self.__mapping_delay_s)

        self.__free_typing_content = ""

        self.__state_to_input_process = {
            CommandControllerState.free_typing: self.__free_typing_input_process,
            CommandControllerState.mapping: self.__mapping_input_process,
        }

        self.__set_state(CommandControllerState.mapping)

    # input ********************************************************************
    def __free_typing_input_process(self, input):
        if input.type == xindmap.input.InputType.default:
            self.__free_typing_content += input.value

        elif input.type == xindmap.input.InputType.enter:
            free_typing_content_split = self.__free_typing_content.split()

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

    def __mapping_input_inputs(self, inputs):
        self.__input_stack.clear()

        for i in inputs:
            self.__input_stack.push(i)

    def __mapping_input_process(self, input):
        # try to move in the mapping tree
        has_moved = self.__command_mapping_tree.move_to_child(input)

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
        if self.__command_mapping_tree.inputs is not None:
            inputs = self.__command_mapping_tree.inputs

            if self.__command_mapping_tree.can_move():
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
        if state == CommandControllerState.mapping:
            self.__command_mapping_tree.move_to_root()
        elif state == CommandControllerState.free_typing:
            self.__free_typing_content = ""

        self.__state = state
