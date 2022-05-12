import itertools
import xindmap.logging as xlogging

from .CommandNode import CommandNode

class CommandTree:
    """a command tree

    Attributes:
        root_node: the root of the tree
        current_node: the current node
            the root node by default
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this command tree
        """
        self.__id = next(CommandTree.__id_counter)

        self.root_node = CommandNode()
        self.current_node = self.root_node

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this tree

        Returns:
            a string representation of this tree
        """
        return 'command tree {}'.format(self.__id)

    # command ******************************************************************
    def add_command(self, command, inputs):
        """adds a command to this tree

        Args:
            command: the command to be added
            inputs: the list of inputs that lead from the root of the tree to
                the command
        """
        current_node = self.root_node

        for input in inputs:
            if input not in current_node.children:
                current_node.children[input] = CommandNode(current_node)

            current_node = current_node.children[input]

        current_node.command = command

        xlogging.info(
            '{}: command {} added with inputs {}',
            self,
            command,
            inputs
        )

    @property
    def command(self):
        """gets the command holded by the current node

        Returns:
            the command of the current node
        """
        return self.current_node.command

    # move in the tree *********************************************************
    def next_node(self, input):
        """moves on to a child of the current node linked to it by the given
        input
        if it cannot move to a child, do nothing

        Args:
            input: the input to use
        
        Returns:
            True if the current node has changed, False otherwise
        """
        if input not in self.current_node.children:
            return False

        self.current_node = self.current_node.children[input]

        xlogging.info(
            '{}: current node changed for {} with input {}',
            self,
            self.current_node,
            input
        )

        return True

    def previous_node(self):
        """moves on to the parent of the current node
        if the current node does not have a parent, do nothing

        Returns:
            True if the current node has changed, False otherwise
        """
        if self.current_node.parent is None:
            return False

        self.current_node = self.current_node.parent

        xlogging.info(
            '{}: current node changed for its parent {}',
            self,
            self.current_node
        )
        
        return True

    def root(self):
        """returns to the top of the tree
        """
        self.current_node = self.root_node

        xlogging.info(
            '{}: current node changed for root {}',
            self,
            self.current_node
        )
