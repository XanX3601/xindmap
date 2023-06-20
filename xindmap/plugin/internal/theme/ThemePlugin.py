import xindmap.plugin

class ThemePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return []

    def command_theme(self, theme_name, api):
        pass

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
