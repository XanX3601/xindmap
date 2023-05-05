import xindmap.plugin

class ViewPlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [
            ("center_view", self.command_center_view)
        ]

    def command_center_view(self, api):
        api.center_view(api.current_node())

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
