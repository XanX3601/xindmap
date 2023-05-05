import xindmap.plugin


class MovePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [
            ("move_down", self.command_move_down),
            ("move_left", self.command_move_left),
            ("move_right", self.command_move_right),
            ("move_up", self.command_move_up),
        ]

    def command_move_down(self, api):
        current_node = api.current_node()
        if current_node is None:
            return

        parent = api.parent_node(current_node)
        if parent is None:
            return

        siblings = api.children_node(parent)
        siblings.sort()
        current_node_index = siblings.index(current_node)
        if current_node_index >= len(siblings) - 1:
            return

        next_sibling = siblings[current_node_index + 1]
        api.select_node(next_sibling)

    def command_move_left(self, api):
        current_node = api.current_node()
        if current_node is None:
            return

        parent = api.parent_node(current_node)
        if parent is None:
            return

        api.select_node(parent)

    def command_move_right(self, api):
        current_node = api.current_node()
        if current_node is None:
            return

        children = api.children_node(current_node)
        if not children:
            return

        children.sort()
        first_child = children[0]

        api.select_node(first_child)

    def command_move_up(self, api):
        current_node = api.current_node()
        if current_node is None:
            return

        parent = api.parent_node(current_node)
        if parent is None:
            return

        siblings = api.children_node(parent)
        siblings.sort()
        current_node_index = siblings.index(current_node)
        if current_node_index == 0:
            return

        previous_sibling = siblings[current_node_index - 1]
        api.select_node(previous_sibling)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()
