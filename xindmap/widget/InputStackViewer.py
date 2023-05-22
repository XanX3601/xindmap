import collections
import logging

import customtkinter as ctk

import xindmap.config
import xindmap.input


class InputStackViewer(ctk.CTkFrame, xindmap.config.Configurable):
    """Widget displaying the content of an
    [input stack][xindmap.input.InputStack.InputStack].

    Attributes:
        __input_text_queue:
            Queue holding the converted [inputs][xindmap.input.Input.Input].
        __label_text: A `customtkinter.StringVar` holding the text to display.
        __label: A `customtkinter.CTkLabel` displaying the text.
    """

    # callback *****************************************************************
    def on_input_stack_stack_cleared(self, input_stack, event):
        """Callback to be called upon
        [stack cleared][xindmap.input.InputStack.InputStack--stack-cleared]
        event dispatched by an
        [input stack][xindmap.input.InputStack.InputStack].

        It clears the displayed text.

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the event.
            event:
                The
                [stack cleared][xindmap.input.InputStack.InputStack--stack-cleared]
                event for which this callback is called.
        """
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_stack_cleared(event={event})"
        )

        self.__input_text_queue.clear()
        self.__update_label_text()

    def on_input_stack_input_poped(self, input_stack, event):
        """Callback to be called upon
        [input poped][xindmap.input.InputStack.InputStack--input-poped] event
        dispatched by an [input stack][xindmap.input.InputStack.InputStack].

        It removes the last input placed in the internal queue.

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the event.
            event:
                The
                [input poped][xindmap.input.InputStack.InputStack--input-poped]
                event for which this callback is called.
        """
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_input_poped(event={event})"
        )

        self.__input_text_queue.pop()
        self.__update_label_text()

    def on_input_stack_input_pushed(self, input_stack, event):
        """Callback to be called upon
        [input pushed][xindmap.input.InputStack.InputStack--input-pushed] event
        dispatched by an [input stack][xindmap.input.InputStack.InputStack].

        It transforms the pushed [input][xindmap.input.Input.Input] into a text
        representation and places it in the internal queue.

        Args:
            input_stack:
                The [input stack][xindmap.input.InputStack.InputStack] that
                dispatched the evnet.
            event:
                The
                [input pushed][xindmap.input.InputStack.InputStack--input-pushed]
                event for which this callback is called.
        """
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_input_pushed(event={event})"
        )

        self.__input_text_queue.append(
            xindmap.input.InputParser.stringify_input(event.input)
        )
        self.__update_label_text()

    # config callback **********************************************************
    def on_config_variable_input_stack_viewer_height_px_set(self, value):
        """Config callback called whenerver
        [`input_stack_viewer_height_px`][xindmap.config.Variables.Variables.input_stack_viewer_height_px]
        config variable is set.
        """
        self.__label.configure(height=value)

    # constructor **************************************************************
    def __init__(self, parent):
        """Instantiates this input stack viewer.

        Args:
            parent: The widget holding this input stack viewer.
        """
        ctk.CTkFrame.__init__(self, parent)
        xindmap.config.Configurable.__init__(
            self, (xindmap.config.Variables.input_stack_viewer_height_px,)
        )

        self.__input_text_queue = collections.deque()

        self.__label_text = ctk.StringVar(value="")
        self.__label = ctk.CTkLabel(
            self,
            textvariable=self.__label_text,
            height=xindmap.config.Variables.input_stack_viewer_height_px.default,
            bg_color="red"
        )

        self.__label.pack(fill=ctk.BOTH, expand=True)

    # text *********************************************************************
    def __update_label_text(self):
        """Updates the displayed text based on the content of the internal
        queue.
        """
        self.__label_text.set("".join(self.__input_text_queue))
