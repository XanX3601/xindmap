from .CommandNode import CommandNode

class CommandTree:
    """a command tree

    Attributes:
        root_node: the root of the tree
        current_node: the current node
            the root node by default
    """
    def __init__(self):
        """instantiates this command tree
        """
        self.root_node = CommandNode()
        self.current_node = self.root_node

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

    @property
    def command(self):
        """gets the command holded by the current node

        Returns:
            the command of the current node
        """
        return self.current_node.command

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
        
        return True

    def root(self):
        """returns to the top of the tree
        """
        self.current_node = self.root_node
