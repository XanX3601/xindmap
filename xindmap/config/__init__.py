"""Xindmap config module.

# `xindmap.config`

Component whishing to expose or share common variable can do so using the 
[config][xindmap.config.Config.Config].
It exposes [variables][xindmap.config.Variable.Variable] to which classes 
derived from [`Configurable`][xindmap.config.Configurable.Configurable] can
subscribe to upon instantiation.
When the value of a variable is changed all
[configurables][xindmap.config.Configurable.Configurable] are warned of the
change and can freely interpret the new value.

[Variables][xindmap.config.Variable.Variable] are declared statically.
They can be accessed through the
[`Variables`][xindmap.config.Variables.Variables] class.

## Module exported content

- [`xindmap.config.Config.Config`][]
- [`xindmap.config.Configurable.Configurable`][]
- [`xindmap.config.Variables.Variables`][]
"""

from .Config import Config
from .Configurable import Configurable
from .Variables import Variables
