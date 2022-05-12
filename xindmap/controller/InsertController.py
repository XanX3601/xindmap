import itertools
import xindmap.logging as xlogging

class InsertController:
    """insert controller
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this controller
        """
        self.__id = next(InsertController.__id_counter)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this controller

        Returns:
            a string representation of this controller
        """
        return 'insert controller {}'.format(self.__id)

    # init *********************************************************************
    def init(self, mind_map):
        """initializes this controller

        Args:
            mind_map: the mind map
        """
        self._mind_map = mind_map

        xlogging.info('{}: initialized', self)

    # insert *******************************************************************
    def insert(self, text):
        """inserts the given text at the end of the current node text

        Args:
            text: an input
        """
        xlogging.info('{}: insert {}', self, text)

        if self._mind_map.current_node is not None:
            self._mind_map.current_node.text += text

