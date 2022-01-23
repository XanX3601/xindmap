import xindmap.view.command as xcommand

class XindmapCommandDict(dict):
    """A dictionnary holding the commands available in the Xindmap app.
    """
    def __init__(self):
        """Instantiates this xindmap command dict.
        """
        super().__init__()

        self['move_up'] = xcommand.Command('move_up', 'move up')

