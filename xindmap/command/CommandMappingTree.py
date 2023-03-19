import xindmap.input


class CommandMappingNode:
    # child ********************************************************************
    def add_child(self, input):
        if not input.type in self.__children:
            self.__children[input.type] = {}

        if not input.value in self.__children[input.type]:
            self.__children[input.type][input.value] = CommandMappingNode()

        return self.__children[input.type][input.value]

    def get_child(self, input):
        if input.type not in self.__children:
            return None

        return self.__children[input.type].get(input.value, None)

    def has_child(self):
        return bool(self.__children)

    # constructor **************************************************************
    def __init__(self):
        self.inputs = None
        self.__children = {}


class CommandMappingTree:
    # command ******************************************************************
    @property
    def inputs(self):
        return self.__current_node.inputs

    # constructor **************************************************************
    def __init__(self):
        self.__root = CommandMappingNode()

        self.__current_node = self.__root

    # mapping ******************************************************************
    def add_mapping(self, inputs, mapped_inputs):
        current_node = self.__root

        for input in inputs:
            current_node = current_node.add_child(input)

        current_node.inputs = mapped_inputs

    # move *********************************************************************
    def can_move(self):
        return self.__current_node.has_child()

    def is_on_root(self):
        return self.__current_node == self.__root

    def move_to_child(self, input):
        child = self.__current_node.get_child(input)

        if child is None:
            return False

        self.__current_node = child
        return True

    def move_to_root(self):
        self.__current_node = self.__root

        return True
