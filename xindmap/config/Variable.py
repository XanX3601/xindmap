import collections

from .VariableTypes import VariableTypes

Variable = collections.namedtuple("Variable", ["type", "default"])
