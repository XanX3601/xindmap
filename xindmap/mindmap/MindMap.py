import itertools
import kivy.event as kevent
import kivy.properties as kproperties
import xindmap.logging as xlogging

from .MindNode import MindNode

class MindMap(kevent.EventDispatcher):
    """a mind map

    Attributes:
        current_node: a node in this map that is currently selected
        root_node: the root of the map
            None if this map does not have a root
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    current_node = kproperties.ObjectProperty()
    root_node = kproperties.ObjectProperty()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this map
        """
        super().__init__()

        self.__id = next(MindMap.__id_counter)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this mind map

        Returns:
            a string representation of this mind map
        """
        return 'mind map {}'.format(self.__id)

    # node *********************************************************************
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

        xlogging.info('{}: node {} added', self, self.current_node)

        return node

    # current node *************************************************************
    def child(self):
        """moves the current node to its first child

        if the current node does not have any children, do nothing
        """
        if self.current_node.children:
            self.current_node = self.current_node.children[0]

            xlogging.info(
                '{}: current node changed to {} by going to first child',
                self,
                self.current_node
            )

    def parent(self):
        """moves the current node to its parent

        if the current not does not have any parent, do nothing
        """
        if self.current_node.parent is not None:
            self.current_node = self.current_node.parent

            xlogging.info(
                '{}: current node changed to {} by going to parent',
                self,
                self.current_node
            )

