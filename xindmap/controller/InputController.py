import logging

import xindmap.input


class InputController:
    # callback *****************************************************************
    def on_key(self, event):
        logging.debug(f"input controller {id(self)}: on_key(event={event})")

        input = None

        if event.keycode == 22:
            input = xindmap.input.Input(xindmap.input.InputType.backspace)
        elif event.keycode == 36:
            input = xindmap.input.Input(xindmap.input.InputType.enter)
        elif event.keycode == 50:
            input = None
        else:
            input = xindmap.input.Input(xindmap.input.InputType.default, event.char)

        if input is not None:
            self.input_stack.push(input)

    # constructor **************************************************************
    def __init__(self, input_stack):
        self.input_stack = input_stack
