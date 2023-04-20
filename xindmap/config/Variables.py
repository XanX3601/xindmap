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
