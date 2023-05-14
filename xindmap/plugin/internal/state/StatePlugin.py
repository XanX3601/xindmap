import xindmap.plugin
import xindmap.state

class StatePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [
            ("edit_mode", self.command_edit_state),
        ]

    def command_edit_state(self, api):
        api.set_state(xindmap.state.State.edit)


    # constructor **************************************************************
    def __init__(self):
        super().__init__()
