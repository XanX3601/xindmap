import enum

from .Variable import Variable
from .VariableTypes import VariableTypes


class Variables(enum.Enum):
    """Statically declared list of all variables that can be set through the
    [config][xindmap.config.Config.Config].
    """
    command_controller_mapping_delay_s = Variable(VariableTypes.float, 1)
    """The delay (in seconds) used by
    [command controller][xindmap.controller.CommandController.CommandController]
    when having to decide wether accepting a mapping or wait for the user to
    finish the mapping.
    """
    input_stack_input_pushed_event_priority = Variable(VariableTypes.int, 20)
    """The priority to which [event][xindmap.event.Event.Event]
    [input pushed][xindmap.input.InputStack.InputStack--input-pushed]
    is dispatched.
    """
    input_stack_viewer_height_px = Variable(VariableTypes.int, 20)
    """The height (in pixel) of 
    [input stack viewer][xindmap.widget.InputStackViewer.InputStackViewer].
    """
    mind_map_viewer_node_height = Variable(VariableTypes.int, 20)
    mind_map_viewer_node_min_width = Variable(VariableTypes.int, 10)
    mind_map_viewer_node_padding_x = Variable(VariableTypes.int, 5)
    mind_map_viewer_node_padding_y = Variable(VariableTypes.int, 5)

    # property *****************************************************************
    @property
    def type(self):
        """Returns the type of the underlying
        [variable][xindmap.config.Variable.Variable].
        """
        return self.value.type

    @property
    def default(self):
        """Returns the default value of the underlying
        [variable][xindmap.config.Variable.Variable].
        """
        return self.value.default
