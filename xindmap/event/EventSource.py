from .EventDispatcher import EventDispatcher


class EventSource:
    # callback *****************************************************************
    def register_callbacks(self, event_type, *callbacks):
        event_dispatcher = EventDispatcher()

        for callback in callbacks:
            event_dispatcher.register_callback(self, event_type, callback)

    # constructor **************************************************************
    def __init__(self, event_types):
        event_dispatcher = EventDispatcher()
        event_dispatcher.register_event_source(self, event_types)

    # dispatch *****************************************************************
    def _dispatch_event(self, event):
        event_dispatcher = EventDispatcher()
        event_dispatcher.dispatch_event(self, event)
