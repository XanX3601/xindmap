import enum

from .Variable import Variable
from .VariableTypes import VariableTypes


class Variables(enum.Enum):
    command_controller_mapping_delay_s = Variable(VariableTypes.float, 1)

    # property *****************************************************************
    @property
    def type(self):
        return self.value.type

    @property
    def default(self):
        return self.value.default
