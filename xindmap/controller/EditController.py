import logging
import xindmap.input
import xindmap.state

class EditController:
    # callback *****************************************************************
    def on_editable_holder_editable_set(self, editable_holder, event):
        logging.debug(f"edit controller {id(self)}: on_editable_holder_editable_set(event={event})")

        self.__editable = event.editable

    def on_input_stack_input_pushed(self, input_stack, event):
        logging.debug(f"edit controller {id(self)}: on_input_stack_input_pushed(event={event})")

        if not self.__is_active:
            return

        input = event.input
        text = xindmap.input.InputParser.textify_input(input)

        input_stack.clear()

        if input.type == xindmap.input.InputType.escape:
            self.__state_holder.set_state(xindmap.state.State.command)
        if input.type == xindmap.input.InputType.backspace and self.__editable is not None:
            self.__editable.remove_last_char()
        elif self.__editable is not None:
            self.__editable.add_text(text)

    def on_state_holder_state_set(self, state_hoder, event):
        logging.debug(f"edit controller {id(self)}: on_state_holder_state_set(event={event})")

        self.__is_active = event.state == xindmap.state.State.edit

    # constructor **************************************************************
    def __init__(self, state_holder):
        self.__state_holder = state_holder

        self.__is_active = False
        self.__editable = None

