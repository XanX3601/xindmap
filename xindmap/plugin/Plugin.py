class Plugin:
    """Interface describing the behaviour of a plugin."""

    # command ******************************************************************
    def commands(self):
        """Returns a list of couple formed of a command name and the command
        itself.
        """
        return []

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this plugin."""
        pass
