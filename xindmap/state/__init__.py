""" Xindmap state module.

# `xindmap.state`

The behaviour of the application depends on its current
[state][xindmap.state.State.State].
It is stored in a [state holder][xindmap.state.StateHolder.StateHolder] to have
a wrapper around it able to dispatch [events][xindmap.event.Event.Event].

## Module exported content

- [`xindmap.state.State.State`][]
- [`xindmap.state.StateHolder.StateHolder`][]
- [`xindmap.state.StateHolderEvent.StateHolderEvent`][]
"""

from .State import State
from .StateHolder import StateHolder
from .StateHolderEvent import StateHolderEvent
