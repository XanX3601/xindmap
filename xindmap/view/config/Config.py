import xindmap.view.command as xcommand

class Config:
    """A command for the Xindmap app.

    Attributes:
        command_tree: the command tree.
    """
    def __init__(self):
        self.command_tree = xcommand.CommandTree()
