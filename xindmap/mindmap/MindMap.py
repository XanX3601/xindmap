import kivy.event as kevent
import kivy.properties as kproperties

from .MindNode import MindNode

class MindMap(kevent.EventDispatcher):
    """a mind map

    Attributes:
        current_node: a node in this map that is currently selected
        root_node: the root of the map
            None if this map does not have a root
    """
    current_node = kproperties.ObjectProperty()
    root_node = kproperties.ObjectProperty()

    def __init__(self):
        """instantiates this map
        """
        super().__init__()

    def add_node(self):
        """adds a node to this map

        Returns:
            the added node
        """
        if self.root_node is None:
            node = MindNode(None)

            self.root_node = node
            self.current_node = node
        else:
            node = MindNode(self.current_node)

            self.current_node.children.append(node)
            self.current_node = node

        return node

    def child(self):
        """moves the current node to its first child

        if the current node does not have any children, do nothing
        """
        if self.current_node.children:
            self.current_node = self.current_node.children[0]

    def parent(self):
        """moves the current node to its parent

        if the current not does not have any parent, do nothing
        """
        if self.current_node.parent is not None:
            self.current_node = self.current_node.parent




