"""Xindmpa input module.

# `xindmap.input`

When users interact with the application, it should be convert in way for every
component of the application to understand.
That way, if the user input device changes, only the conversion function must be
redo.
This module exposes classes that describe user inputs.

## Module exported content

- [`xindmap.input.Input.Input`][]
- [`xindmap.input.InputMappingTree.InputMappingTree`][]
- [`xindmap.input.InputStack.InputStack`][]
- [`xindmap.input.InputStackEvent.InputStackEvent`][]
- [`xindmap.input.InputType.InputType`][]
"""

from .Input import Input
from .InputMappingTree import InputMappingTree
from .InputStack import InputStack
from .InputStackEvent import InputStackEvent
from .InputType import InputType
