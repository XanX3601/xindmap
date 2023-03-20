import collections
import logging

import customtkinter as ctk

import xindmap.input


class InputStackViewer(ctk.CTkFrame):
    # callback *****************************************************************
    def on_input_stack_stack_cleared(self, input_stack, event):
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_stack_cleared(event={event})"
        )

        self.__input_text_queue.clear()
        self.__update_label_text()

    def on_input_stack_input_poped(self, input_stack, event):
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_input_poped(event={event})"
        )

        self.__input_text_queue.pop()
        self.__update_label_text()

    def on_input_stack_input_pushed(self, input_stack, event):
        logging.debug(
            f"input stack viewer {id(self)}: on_input_stack_input_pushed(event={event})"
        )

        self.__input_text_queue.append(self.__input_to_text(event.input))
        self.__update_label_text()

    # constructor **************************************************************
    def __init__(self, parent):
        super().__init__(parent)

        self.__input_text_queue = collections.deque()

        self.__label_text = ctk.StringVar(value="")
        self.__label = ctk.CTkLabel(self, textvariable=self.__label_text)

        self.__label.pack(fill=ctk.BOTH, expand=True)

    # input ********************************************************************
    def __input_to_text(self, input):
        if input.type == xindmap.input.InputType.enter:
            return "<CR>"
        elif input.type == xindmap.input.InputType.backspace:
            return "<BS>"
        elif input.type == xindmap.input.InputType.default:
            return input.value

    # text *********************************************************************
    def __update_label_text(self):
        self.__label_text.set("".join(self.__input_text_queue))
