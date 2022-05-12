import itertools
import kivy.event as kevent
import kivy.properties as kproperties
import xindmap.logging as xlogging

class MindNode(kevent.EventDispatcher):
    """a mind node

    Attributes:
        children: a list containing the children of this node
        parent: the node parent of this node or None it if does not have one
        text: the text contained in the node
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    children = kproperties.ListProperty()
    parent = kproperties.ObjectProperty()
    text = kproperties.ObjectProperty()

    # dunder *******************************************************************
    def __init__(self, parent, text=''):
        """instantiates this node

        Args:
            text: the text of the node
        """
        super().__init__()

        self.__id = next(MindNode.__id_counter)

        self.parent = parent
        self.text = text

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this mind node

        Returns:
            a string representation of this node
        """
        return 'mind node {}'.format(self.__id)
