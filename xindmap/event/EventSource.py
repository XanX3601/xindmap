from .EventDispatcher import EventDispatcher


class EventSource:
    """Class to be derived from if a class wants to dispatch
    [events][xindmap.event.Event.Event].

    An event source is an object producing [events][xindmap.event.Event.Event]
    of fixed [types][xindmap.event.EventSource.EventSource--event-type] to which
    callbacks can be registered to.
    They are then called when an [event][xindmap.event.Event.Event] is produced.

    ## Callback

    Callbacks are function like object that can be invoked and that take two
    arguments: 

    - the source of the event
    - the [event][xindmap.event.Event.Event]

    ## Event type

    Each event must have a type which can be any hashable object.

    During design, it was thought that event type could be members of
    [enum][`enum.Enum`] so that they are declared as variable in the code rather
    than [strings][str] that must be listed in a documentation.
    """
    # callback *****************************************************************
    def register_callbacks(self, event_type, *callbacks):
        """Registers
        [callbacks][xindmap.event.EventSource.EventSource--callback] on
        [events][xindmap.event.Event.Event] of given
        [type][xindmap.event.EventSource.EventSource--event-type].

        Args:
            event_type:
                The [type][xindmap.event.EventSource.EventSource--event-type] of
                [event][xindmap.event.Event.Event] for which the registered 
                [callback][xindmap.event.EventSource.EventSource--callback]
                must be called.
            callbacks:
                All callbacks to register
        """
        event_dispatcher = EventDispatcher()

        for callback in callbacks:
            event_dispatcher.register_callback(self, event_type, callback)

    # constructor **************************************************************
    def __init__(self, event_types):
        """Instantiates this event source.

        Args:
            event_types:
                Iterator to all
                [types][xindmap.event.EventSource.EventSource--event-type] this
                event source produces.
        """
        event_dispatcher = EventDispatcher()
        event_dispatcher.register_event_source(self, event_types)

    # dispatch *****************************************************************
    def _dispatch_event(self, event):
        """Dispatches an [event][xindmap.event.Event.Event] to registered 
        [callbacks][xindmap.event.EventSource.EventSource--callback].

        Args:
            event: The [event][xindmap.event.Event.Event] to dispatch.
        """
        event_dispatcher = EventDispatcher()
        event_dispatcher.dispatch_event(self, event)
