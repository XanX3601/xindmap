import xindmap.plugin


class NodePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [
            ("add_node", self.command_add_node),
            ("delete_node", self.command_delete_node),
        ]

    def command_add_node(self, api):
        node = api.add_node(wait=True)

        if node == api.root_node():
            api.select_node(node)
            api.center_view(node)

    def command_delete_node(self, api):
        parent = api.parent_node()
        api.delete_node()

        if parent is not None:
            api.select_node(parent)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
