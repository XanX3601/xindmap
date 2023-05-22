import itertools

class MindNode:
    # child ********************************************************************
    def add_child(self, mind_node):
        self.__child_id_to_child[mind_node.id] = mind_node

    def child_ids(self):
        return list(self.__child_id_to_child.keys())
    
    def remove_child(self, mind_node):
        del self.__child_id_to_child[mind_node.id]

    # constructor **************************************************************
    def __init__(self, parent):
        self.__id = next(MindNode.__id_count)

        self.__parent = parent
        self.__child_id_to_child = {}

        self.title = ""

    # id ***********************************************************************
    __id_count = itertools.count()

    @property
    def id(self):
        return self.__id

    # parent *******************************************************************
    @property
    def parent(self):
        return self.__parent

