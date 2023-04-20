"""Xindmap event module

# `xindmap.event`

[Events][xindmap.event.Event.Event] are the main communication support for the
components to communicate and react to each other activities.
[Events][xindmap.event.Event.Event] are dispatched by
[event source][xindmap.event.EventSource.EventSource].
Callbacks can be registered to be called upon an event dispatching.

## Module exported content

- [`xindmap.event.Event.Event`][]
- [`xindmap.event.EventAttributeError.EventAttributeError`][]
- [`xindmap.event.EventSource.EventSource`][]
- [`xindmap.event.EventSourceError.EventSourceError`][]
- [`xindmap.event.EventTypeError.EventTypeError`][]
"""

from .Event import Event
from .EventAttributeError import EventAttributeError
from .EventSource import EventSource
from .EventSourceError import EventSourceError
from .EventTypeError import EventTypeError
