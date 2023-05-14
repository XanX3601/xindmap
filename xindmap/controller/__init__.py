"""Xindmap controller module.

# `xindmap.controller`

To avoid having all the logic code centralized in an unique object, the
application make use of controllers.
They are object containing logic bricks from the application.

## Module exported content

- [`xindmap.controller.CommandController.CommandController`][]
- [`xindmap.controller.InputController.InputController`][]
"""

from .CommandController import CommandController
from .EditController import EditController
from .InputController import InputController
