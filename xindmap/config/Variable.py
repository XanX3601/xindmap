import collections

from .VariableTypes import VariableTypes

Variable = collections.namedtuple("Variable", ["type", "default"])
"""A variable exposed or shared between components declared in the
[variable list][xindmap.config.Variables.Variables] that can be set through the
[config][xindmap.config.Config.Config].

Attributes:
    type:
        The [type][xindmap.config.VariableTypes.VariableTypes] of the variable.
    default: The default value of the variable.
"""
