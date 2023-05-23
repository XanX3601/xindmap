import xindmap.config
import xindmap.event

class CommandApi:
    """Api for the commands to interact with the application.

    Attributes:
        __input_mapping_tree: 
            An
            [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree]
            used to register mapping.
    """
    # config *******************************************************************
    def get_config(self, variable):
        config = xindmap.config.Config()
        return config.get(variable)

    def set_config(self, variable, value, wait=False):
        config = xindmap.config.Config()
        config.set(variable, value)
        if wait:
            self.__wait()

    # constructor **************************************************************
    def __init__(self, input_mapping_tree, mind_map, mind_map_viewer, state_holder):
        """Instantiates this api.

        Args:
            input_mapping_tree:
                An
                [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree].
        """
        self.__input_mapping_tree = input_mapping_tree
        self.__mind_map = mind_map
        self.__mind_map_viewer = mind_map_viewer
        self.__state_holder = state_holder

    # mapping ******************************************************************
    def map(self, inputs, mapped_inputs):
        """Maps a list of [inputs][xindmap.input.Input.Input] to another one.

        Args:
            inputs: A list of [inputs][xindmap.input.Input.Input].
            mapped_inputs: A list of [inputs][xindmap.input.Input.Input].
        """
        self.__input_mapping_tree.add_mapping(inputs, mapped_inputs)

    # mind map *****************************************************************
    def populate_from_dict(self, node_dict, wait=False):
        self.__mind_map.populate_from_dict(node_dict)
        if wait:
            self.__wait()
            
    def to_dict(self):
        return self.__mind_map.to_dict()

    # node *********************************************************************
    def add_node(self, parent_id=None, wait=False):
        node_id = self.__mind_map.node_add(parent_id)
        if wait:
            self.__wait()
        return node_id

    def children_node(self, parent_id=None):
        return self.__mind_map.node_child_ids(parent_id)

    def current_node(self):
        return self.__mind_map.current_node_id

    def delete_node(self, node_id=None, wait=False):
        self.__mind_map.node_delete(node_id)
        if wait:
            self.__wait()

    def parent_node(self, node_id=None):
        return self.__mind_map.node_parent_id(node_id)

    def root_node(self):
        return self.__mind_map.root_node_id

    def select_node(self, node_id, wait=False):
        self.__mind_map.node_select(node_id)
        if wait:
            self.__wait()

    # state ********************************************************************
    def set_state(self, state, wait=False):
        self.__state_holder.set_state(state)
        if wait:
            self.__wait()

    # view *********************************************************************
    def center_view(self, node_id, wait=False):
        self.__mind_map_viewer.view_center_on_node(node_id)
        if wait:
            self.__wait()

    # wait *********************************************************************
    def __wait(self):
        xindmap.event.wait_for_event_dispatching()

