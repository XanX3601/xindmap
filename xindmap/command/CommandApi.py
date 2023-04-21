class CommandApi:
    """Api for the commands to interact with the application.

    Attributes:
        __input_mapping_tree: 
            An
            [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree]
            used to register mapping.
    """
    # constructor **************************************************************
    def __init__(self, input_mapping_tree):
        """Instantiates this api.

        Args:
            input_mapping_tree:
                An
                [input mapping tree][xindmap.input.InputMappingTree.InputMappingTree].
        """
        self.__input_mapping_tree = input_mapping_tree

    # mapping ******************************************************************
    def map(self, inputs, mapped_inputs):
        """Maps a list of [inputs][xindmap.input.Input.Input] to another one.

        Args:
            inputs: A list of [inputs][xindmap.input.Input.Input].
            mapped_inputs: A list of [inputs][xindmap.input.Input.Input].
        """
        self.__input_mapping_tree.add_mapping(inputs, mapped_inputs)
