import sortedcontainers

import xindmap.mind_map
import xindmap.plugin


class MovePlugin(xindmap.plugin.Plugin):
    # callback *****************************************************************
    def on_mind_map_node_added(self, api, node):
        direction = api.direction_node(node)
        parent = api.parent_node(node)

        if parent is None:
            deep_level = 0
        else:
            deep_level = self.__node_to_deep_level[parent] + 1

        self.__node_to_deep_level[node] = deep_level
        self.__node_to_last_index[node] = 0

        if deep_level not in self.__deep_level_to_direction_to_nodes:
            self.__deep_level_to_direction_to_nodes[deep_level] = {}
        if direction not in self.__deep_level_to_direction_to_nodes[deep_level]:
            self.__deep_level_to_direction_to_nodes[deep_level][
                direction
            ] = sortedcontainers.SortedList()

        self.__deep_level_to_direction_to_nodes[deep_level][direction].add(node)

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
        if node is None:
            return

        deep_level = self.__node_to_deep_level[node]
        direction = api.direction_node(node)

        nodes = self.__deep_level_to_direction_to_nodes[deep_level][direction]

        node_index = nodes.index(node)

        if node_index < len(nodes) - 1:
            next_node = nodes[node_index + 1]

            api.select_node(next_node)

    def command_move_left(self, api):
        node = api.current_node()
        root = api.root_node()

        if node == root:
            children = api.children_node(root)
            children = [
                child for child in children if api.direction_node(child) == "left"
            ]

            if not children:
                return

            next_node = children[self.__root_last_left_index]
        elif api.direction_node(node) == "left":
            children = api.children_node(node)

            next_node = children[self.__node_to_last_index[node]]
        else:
            parent = api.parent_node(node)
            siblings = api.children_node(parent)

            if parent == root:
                siblings = [
                    sibling
                    for sibling in siblings
                    if api.direction_node(sibling) == "right"
                ]
                self.__root_last_right_index = siblings.index(node)
            else:
                self.__node_to_last_index[parent] = siblings.index(node)

            next_node = parent

        api.select_node(next_node)

    def command_move_right(self, api):
        node = api.current_node()
        root = api.root_node()

        if node == root:
            children = api.children_node(root)
            children = [
                child for child in children if api.direction_node(child) == "right"
            ]

            if not children:
                return

            next_node = children[self.__root_last_right_index]
        elif api.direction_node(node) == "right":
            children = api.children_node(node)

            next_node = children[self.__node_to_last_index[node]]
        else:
            parent = api.parent_node(node)
            siblings = api.children_node(parent)

            if parent == root:
                siblings = [
                    sibling
                    for sibling in siblings
                    if api.direction_node(sibling) == "left"
                ]
                self.__root_last_left_index = siblings.index(node)
            else:
                self.__node_to_last_index[parent] = siblings.index(node)

            next_node = parent

        api.select_node(next_node)

    def command_move_up(self, api):
        node = api.current_node()
        if node is None:
            return

        deep_level = self.__node_to_deep_level[node]
        direction = api.direction_node(node)

        nodes = self.__deep_level_to_direction_to_nodes[deep_level][direction]

        node_index = nodes.index(node)

        if node_index > 0:
            next_node = nodes[node_index - 1]

            api.select_node(next_node)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()

        self.__deep_level_to_direction_to_nodes = {}
        self.__node_to_deep_level = {}
        self.__node_to_last_index = {}

        self.__root_last_left_index = 0
        self.__root_last_right_index = 0

    # initialization ***********************************************************
    def init(self, api):
        api.register_callback(
            xindmap.mind_map.MindMapEvent.node_added, self.on_mind_map_node_added
        )
