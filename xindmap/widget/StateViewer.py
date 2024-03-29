import customtkinter as ctk
import logging
import xindmap.config
import xindmap.state


class StateViewer(ctk.CTkFrame, xindmap.config.Configurable):
    # callback *****************************************************************
    def on_state_holder_state_set(self, state_holder, event):
        logging.debug(f"state viewer {id(self)}: on_state_holder_state_set(event={event})")

        self.__update_label_text(event.state)

    # config callback **********************************************************
    def on_config_variable_state_viewer_height_px_set(self, value):
        self.__label.configure(height=value)

    # constructor **************************************************************
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        xindmap.config.Configurable.__init__(
            self, [xindmap.config.Variables.state_viewer_height_px]
        )

        self.__label_text = ctk.StringVar(value="hello")
        self.__label = ctk.CTkLabel(
            self,
            textvariable=self.__label_text,
            bg_color="blue",
            height=xindmap.config.Variables.state_viewer_height_px.default,
        )

        self.__label.pack(fill=ctk.BOTH, expand=True)

    # text *********************************************************************
    __state_to_text = {
        xindmap.state.State.command: "-- COMMAND --",
        xindmap.state.State.edit: "-- EDIT --",
        xindmap.state.State.none: "-- ... --",
    }

    def __update_label_text(self, state):
        self.__label_text.set(StateViewer.__state_to_text[state])
