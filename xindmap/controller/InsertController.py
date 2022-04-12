import kivy.logger as klogger

class InsertController:
    """insert controller

    Attributes:
    """
    def __init__(self):
        """instantiates this controller
        """
        pass

    def init(self, mind_map):
        """initializes this controller

        Args:
            mind_map: the mind map
        """
        self._mind_map = mind_map

    def insert(self, text):
        """inserts the given text at the end of the current node text

        Args:
            text: an input
        """
        klogger.Logger.info('[insert controller] insert {}'.format(text))

        if self._mind_map.current_node is not None:
            self._mind_map.current_node.text += text

