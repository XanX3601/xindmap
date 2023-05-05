import logging

import xindmap.input
import xindmap.plugin


class MappingPlugin(xindmap.plugin.Plugin):
    """A [plugin][xindmap.plugin.Plugin.Plugin] exposing commands to map
    [input][xindmap.input.Input.Input] sequence to other
    [input][xindmap.input.Input.Input] sequence.
    """

    # command ******************************************************************
    def commands(self):
        """Returns the list of commands exposed by this mapping plugin."""
        return [
            ("map", self.command_mapping)
        ]

    def command_mapping(self, inputs_as_string, mapped_inputs_as_string, api):
        """Maps a list of inputs to another list of inputs
        """
        inputs = xindmap.input.InputParser.parse_inputs(inputs_as_string)
        mapped_inputs = xindmap.input.InputParser.parse_inputs(mapped_inputs_as_string)

        api.map(inputs, mapped_inputs)

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this plugin"""
        super().__init__()
