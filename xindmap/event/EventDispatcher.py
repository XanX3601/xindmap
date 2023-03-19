import collections
import singleton_decorator

from .EventSourceError import EventSourceError
from .EventTypeError import EventTypeError


@singleton_decorator.singleton
class EventDispatcher:
    # callback *****************************************************************
    def register_callback(self, event_source, event_type, callback):
        # prevent unregistered event source **************************
        if event_source not in self.__event_source_to_event_type_to_callbacks:
            raise EventSourceError(f"event source not registered")

        # prevent unknown event type *********************************
        if (
            event_type
            not in self.__event_source_to_event_type_to_callbacks[event_source]
        ):
            raise EventTypeError("event type not dispatched by event source")

        # add callback if it is not added yet ************************
        if (
            callback
            not in self.__event_source_to_event_type_to_callbacks[event_source][
                event_type
            ]
        ):
            self.__event_source_to_event_type_to_callbacks[event_source][
                event_type
            ].append(callback)

    # constructor **************************************************************
    def __init__(self):
        self.__event_queue = collections.deque()
        self.__event_source_to_event_type_to_callbacks = {}
        self.__is_dispatching = False

    # dispatch *****************************************************************
    def dispatch_event(self, event_source, event):
        # prevent unregistered event source **************************
        if event_source not in self.__event_source_to_event_type_to_callbacks:
            raise EventSourceError(f"event source not registered")

        # prevent unknown event type *********************************
        if (
            event.type
            not in self.__event_source_to_event_type_to_callbacks[event_source]
        ):
            raise EventTypeError("event type not dispatched by event source")

        # add event to queue *****************************************
        self.__event_queue.appendleft((event_source, event))

        # dispatch event *********************************************
        if not self.__is_dispatching:
            self.__is_dispatching = True

            self.__dispatch_event_queue()

    def __dispatch_event_queue(self):
        while self.__event_queue:
            event_source, event = self.__event_queue.pop()

            for callback in self.__event_source_to_event_type_to_callbacks[
                event_source
            ][event.type]:
                callback(event_source, event)

        self.__is_dispatching = False

    # source *******************************************************************
    def register_event_source(self, event_source, event_types):
        self.__event_source_to_event_type_to_callbacks[event_source] = {
            event_type: [] for event_type in event_types
        }
