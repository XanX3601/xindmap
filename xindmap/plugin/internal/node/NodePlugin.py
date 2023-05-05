import xindmap.plugin

class NodePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [
            ("add_node", self.command_add_node)
        ]

    def command_add_node(self, api):
        node = api.add_node()

        if node == api.root_node():
            api.select_node(node)
            api.center_view(node)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
