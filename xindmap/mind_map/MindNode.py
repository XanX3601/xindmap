import itertools

from .MindNodeStatus import MindNodeStatus


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

        self.__text = ""
        self.__title_index = None
        self.status = MindNodeStatus.none

    # id ***********************************************************************
    __id_count = itertools.count()

    @property
    def id(self):
        return self.__id

    # parent *******************************************************************
    @property
    def parent(self):
        return self.__parent

    # text *********************************************************************
    def add_text(self, text):
        self.__text += text

        if self.__title_index is None and "\n" in text:
            self.__title_index = self.__text.index("\n")

    def delete_last_char(self):
        self.__text = self.__text[:-1]

        if self.__title_index is not None and self.__title_index <= len(self.__text):
            self.__title_index = None

    @property
    def description(self):
        return None if self.__title_index is None else self.__text[self.__title_index+1:]

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__title_index = text.index("\n") if "\n" in text else None

        self.__text = text

    @property
    def title(self):
        return self.__text if self.__title_index is None else self.__text[:self.__title_index]
