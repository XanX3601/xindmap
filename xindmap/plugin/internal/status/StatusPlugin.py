import xindmap.mind_map
import xindmap.plugin


class StatusPlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [("status", self.command_status)]

    def command_status(self, status, api):
        try:
            status = xindmap.mind_map.MindNodeStatus[status]
            api.set_node_status(status)
        except KeyError:
            raise ValueError(f"unknown status {status}")

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
