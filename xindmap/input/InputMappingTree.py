class InputMappingNode:
    """A node from an
    [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree].

    A node is an object that can have other nodes as children.
    Children of a node are linked to it by an
    [input][xindmap.input.Input.Input].

    A list of inputs can be saved in a node to be retrieved later.

    Attributes:
        __children:
            A dictionnary mapping an [input][xindmap.input.Input.Input] to a 
            child of this node.
        inputs: A list of inputs saved in this node or [`None`][].
    """
    # child ********************************************************************
    def add_child(self, input):
        """Adds a child to this node linked by a given
        [input][xindmap.input.Input.Input].

        If a child is already linked to this node by the same
        [input][xindmap.input.Input.Input], it is replaced by the new child.

        Args:
            input:
                The [input][xindmap.input.Input.Input] linking this node to its
                new child.

        Returns:
            The new child.
        """
        if not input.type in self.__children:
            self.__children[input.type] = {}

        if not input.value in self.__children[input.type]:
            self.__children[input.type][input.value] = InputMappingNode()

        return self.__children[input.type][input.value]

    def get_child(self, input):
        """Gets the child linked to this node by the given
        [input][xindmap.input.Input.Input].

        Args:
            input:
                The [input][xindmap.input.Input.Input] linking this node to the
                desired child.

        Returns:
            The child node linked to this one by the given
            [input][xindmap.input.Input.Input] or [`None`][] if no such node 
            exists.
        """
        if input.type not in self.__children:
            return None

        return self.__children[input.type].get(input.value, None)

    def has_child(self):
        """Returns [`True`][] if this node has at least one child, [`False`][]
        otherwise.
        """
        return bool(self.__children)

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this node.
        """
        self.inputs = None
        self.__children = {}


class InputMappingTree:
    """An input mapping tree links
    [input mapping node][xindmap.input.InputMappingTree.InputMappingNode]
    by [inputs][xindmap.input.Input.Input] and offers methods to navigate
    between them.

    As [nodes][xindmap.input.InputMappingTree.InputMappingNode] can contain a
    list of inputs, the mapping tree is an easy way to store mapping from a list
    of [inputs][xindmap.input.Input.Input] to another that can be explored
    [input][xindmap.input.Input.Input] by [input][xindmap.input.Input.Input].

    The mapping tree stores the structure of the tree, starting by its root and
    keeps a cursor on the current node (which is the root at first) that can
    changes by moving around the tree.

    Attributes:
        __root:
            The first [node][xindmap.input.InputMappingTree.InputMappingNode] of
            the tree.
        __current_node:
            The [node][xindmap.input.InputMappingTree.InputMappingNode] on which
            the cursor is currently on.
    """
    # command ******************************************************************
    @property
    def inputs(self):
        """Returns the list of inputs stored in the current
        [node][xindmap.input.InputMappingTree.InputMappingNode].
        """
        return self.__current_node.inputs

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this mapping tree with an only, empty
        [node][xindmap.input.InputMappingTree.InputMappingNode] as its root.
        """
        self.__root = InputMappingNode()

        self.__current_node = self.__root

    # mapping ******************************************************************
    def add_mapping(self, inputs, mapped_inputs):
        """Adds a mapping from a list of [inputs][xindmap.input.Input.Input] to
        another one.

        Args:
            inputs: A list of [inputs][xindmap.input.Input.Input].
            mapped_inputs: A list of [inputs][xindmap.input.Input.Input].
        """
        current_node = self.__root

        for input in inputs:
            current_node = current_node.add_child(input)

        current_node.inputs = mapped_inputs

    # move *********************************************************************
    def can_move(self):
        """Returns [`True`][] if the current
        [node][xindmap.input.InputMappingTree.InputMappingNode] has at least one
        child, [`False`][] otherwise.
        """
        return self.__current_node.has_child()

    def is_on_root(self):
        """Returns [`True`][] if the current
        [node][xindmap.input.InputMappingTree.InputMappingNode] is the root of
        this tree, [`False`][] otherwise.
        """
        return self.__current_node == self.__root

    def move_to_child(self, input):
        """Attemps to move the current node to its child linked to it by a given
        [input][xindmap.input.Input.Input].

        Args:
            input:
                The [input][xindmap.input.Input.Input] linking the current
                [node][xindmap.input.InputMappingTree.InputMappingNode] to the
                desired child.

        Returns:
            [`True`][] if the current
            [node][xindmap.input.InputMappingTree.InputMappingNode] has changed,
            [`False`][] otherwise.
        """
        child = self.__current_node.get_child(input)

        if child is None:
            return False

        self.__current_node = child
        return True

    def move_to_root(self):
        """Moves the current
        [node][xindmap.input.InputMappingTree.InputMappingNode] to the root of
        this tree.

        Returns:
            [`True`][]
        """
        self.__current_node = self.__root

        return True
