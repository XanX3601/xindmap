from .NodeParsingError import NodeParsingError
from .Data import Data

class Node:
    """A single node from a map mind.

    Attributes:
        id: node's identifier, used to compute its hash value.
        parent: node's parent which should also be a node or None if no parent.
        children: list of node's children.
    """
    def __init__(
        self,
        id,
        parent=None,
        data=None
    ):
        """Instantiates self node.

        Args:
            id: node's identifier.
            parent: node's parent. None by default.
            data: node's data. if None then use the default data. None by default
        """
        self.id = id
        self.parent = parent
        self.children = []
        self.data = Data() if data is None else data

    def __hash__(self):
        """Computes node's hash value from its identifier.

        Returns:
            node's hash value.
        """
        return hash(self.id)

    def __eq__(self, other_node):
        """Tests wether self is equal to other_node.

        self equals other_node if:
            - other node is an instance of class Node
            - self and other_node have equal data.
        """
        if not isinstance(other_node, Node):
            return False

        return self.data == other_node.data

    def __str__(self):
        """Computes and returns a string representation of node.

        Returns:
            A string representation of node.
        """
        return 'Node {} ({})'.format(self.id, self.data)

    def __repr__(self):
        """Computes and returns a small string representation of node.

        Returns:
            A small string representation of node.
        """
        return 'Node {}'.format(self.id)

