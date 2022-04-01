class CommandNode:
    """a node in the command tree

    Attributes:
        children: a dictionnary linking input to children of this node
        command: the command holded by this node
        parent: the parent of this node
    """
    def __init__(self, parent=None):
        """instantiates this node

        Args:
            parent: the parent of this node
                None by default
        """
        self.parent = parent

        self.children = {}
        self.command = None

