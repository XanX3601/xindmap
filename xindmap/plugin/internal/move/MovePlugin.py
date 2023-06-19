import sortedcontainers

import xindmap.mind_map
import xindmap.plugin


class MovePlugin(xindmap.plugin.Plugin):
    # callback *****************************************************************
    def on_mind_map_node_added(self, api, node):
        parent = api.parent_node(node)

        root = api.root_node()

        if node == root:
            self.__root_to_direction_to_children = {
                "left": sortedcontainers.SortedList(),
                "right": sortedcontainers.SortedList(),
            }
            self.__root_to_direction_to_last_index = {
                direction: 0 for direction in self.__root_to_direction_to_children
            }

        else:
            self.__node_to_children[node] = sortedcontainers.SortedList()
            self.__node_to_last_index[node] = 0

            if parent is not None:
                if parent == root:
                    direction = api.direction_node(node)
                    self.__root_to_direction_to_children[direction].add(node)
                else:
                    self.__node_to_children[parent].add(node)

    # command ******************************************************************
    def commands(self):
        return [
            ("move_down", self.command_move_down),
            ("move_left", self.command_move_left),
            ("move_right", self.command_move_right),
            ("move_up", self.command_move_up),
        ]

    def command_move_down(self, api):
        node = api.current_node()
        root = api.root_node()

        if node == root:
            return

        parent = api.parent_node(node)

        if parent == root:
            direction = api.direction_node(node)
            siblings = self.__root_to_direction_to_children[direction]
        else:
            siblings = self.__node_to_children[parent]

        node_index = siblings.index(node)

        if node_index < len(siblings) - 1:
            next_node = siblings[node_index + 1]
        else:
            grand_parent = api.parent_node(parent)

            if grand_parent == root:
                direction = api.direction_node(parent)
                parent_siblings = self.__root_to_direction_to_children[direction]
            else:
                parent_siblings = self.__node_to_children[grand_parent]

            parent_index = parent_siblings.index(parent)

            next_node = None
            while next_node is None:
                parent_index += 1

                if parent_index == len(parent_siblings):
                    return

                parent = parent_siblings[parent_index]
                siblings = self.__node_to_children[parent]

                if siblings:
                    next_node = siblings[0]

        api.select_node(next_node)

    def command_move_left(self, api):
        node = api.current_node()
        direction = api.direction_node(node)

        if direction == "":
            children = self.__root_to_direction_to_children["left"]

            if not children:
                return

            next_node = children[self.__root_to_direction_to_last_index["left"]]
        elif direction == "left":
            children = self.__node_to_children[node]

            if not children:
                return

            next_node = children[self.__node_to_last_index[node]]
        else:
            parent = api.parent_node(node)
            root = api.root_node()

            if parent == root:
                siblings = self.__root_to_direction_to_children[direction]
                node_index = siblings.index(node)
                self.__root_to_direction_to_last_index[direction] = node_index
            else:
                siblings = self.__node_to_children[parent]
                node_index = siblings.index(node)
                self.__node_to_last_index[parent] = node_index

            next_node = parent

        api.select_node(next_node)

    def command_move_right(self, api):
        node = api.current_node()
        direction = api.direction_node(node)

        if direction == "":
            children = self.__root_to_direction_to_children["right"]

            if not children:
                return

            next_node = children[self.__root_to_direction_to_last_index["right"]]
        elif direction == "left":
            parent = api.parent_node(node)
            root = api.root_node()

            if parent == root:
                siblings = self.__root_to_direction_to_children[direction]
                node_index = siblings.index(node)
                self.__root_to_direction_to_last_index[direction] = node_index
            else:
                siblings = self.__node_to_children[parent]
                node_index = siblings.index(node)
                self.__node_to_last_index[parent] = node_index

            next_node = parent
        else:
            children = self.__node_to_children[node]

            if not children:
                return

            next_node = children[self.__node_to_last_index[node]]

        api.select_node(next_node)

    def command_move_up(self, api):
        node = api.current_node()
        root = api.root_node()

        if node == root:
            return

        parent = api.parent_node(node)

        if parent == root:
            direction = api.direction_node(node)
            siblings = self.__root_to_direction_to_children[direction]
        else:
            siblings = self.__node_to_children[parent]

        node_index = siblings.index(node)

        if node_index > 0:
            next_node = siblings[node_index - 1]
        else:
            grand_parent = api.parent_node(parent)

            if grand_parent == root:
                direction = api.direction_node(parent)
                parent_siblings = self.__root_to_direction_to_children[direction]
            else:
                parent_siblings = self.__node_to_children[grand_parent]

            parent_index = parent_siblings.index(parent)

            next_node = None
            while next_node is None:
                parent_index -= 1

                if parent_index == -1:
                    return

                parent = parent_siblings[parent_index]
                siblings = self.__node_to_children[parent]

                if siblings:
                    next_node = siblings[-1]

        api.select_node(next_node)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()

        self.__node_to_children = {}
        self.__node_to_last_index = {}

        self.__root_to_direction_to_children = {}
        self.__root_to_direction_to_last_index = {}

    # initialization ***********************************************************
    def init(self, api):
        api.register_callback(
            xindmap.mind_map.MindMapEvent.node_added, self.on_mind_map_node_added
        )
