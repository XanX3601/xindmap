import itertools
import xindmap.logging as xlogging

class CommandNode:
    """a node in the command tree

    Attributes:
        children: a dictionnary linking input to children of this node
        command: the command holded by this node
        parent: the parent of this node
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self, parent=None):
        """instantiates this node

        Args:
            parent: the parent of this node
                None by default
        """
        self.__id = next(CommandNode.__id_counter)

        self.parent = parent

        self.children = {}
        self.command = None

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this node

        Returns:
            a string representation of this node
        """
        return 'command node {}'.format(self.__id)

