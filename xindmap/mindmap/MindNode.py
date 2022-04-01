import kivy.event as kevent
import kivy.properties as kproperties

class MindNode(kevent.EventDispatcher):
    """a mind node

    Attributes:
        children: a list containing the children of this node
        parent: the node parent of this node or None it if does not have one
        text: the text contained in the node
    """
    children = kproperties.ListProperty()
    parent = kproperties.ObjectProperty()
    text = kproperties.ObjectProperty()

    def __init__(self, parent, text=''):
        """instantiates this node

        Args:
            text: the text of the node
        """
        super().__init__()

        self.parent = parent
        self.text = text
