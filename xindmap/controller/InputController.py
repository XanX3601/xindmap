import logging

import xindmap.input


class InputController:
    """The input controller converts user interaction into
    [inputs][xindmap.input.Input.Input].

    Attributes:
        input_stack:
            The [input stack][xindmap.input.InputStack.InputStack] in which push
            the [input][xindmap.input.Input.Input] created by this controller
    """
    # callback *****************************************************************
    def on_key(self, event):
        """Callback to be called whenever the user press on the keyboard.

        Args:
            event: The event this callback is called for.
        """
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
        """Instantiates this input controller.

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] in which
                push the [input][xindmap.input.Input.Input] created by this 
                controller.
        """
        self.input_stack = input_stack
