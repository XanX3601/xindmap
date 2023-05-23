import dataclasses
import itertools
import queue
import threading
import typing

import singleton_decorator

from .EventSourceError import EventSourceError
from .EventTypeError import EventTypeError

dispatching_condition = threading.Condition()
dispatching_lock = threading.Lock()


def wait_for_event_dispatching():
    dispatching_lock.acquire()
    dispatching_lock.release()


@dataclasses.dataclass(order=True)
class EventQueueItem:
    """Dataclass used to store events in a [priority queue][queue.PriorityQueue]
    used by the
    [event dispatcher][xindmap.event.EventDispatcher.EventDispatcher].

    Attributes:
        priority:
            The level of priority (the lower the value, the higher the
            priority).
        item_id:
            The identifier of the item.
            It is initialized automaticaly.
        event_source:
            The [source][xindmap.event.EventSource.EventSource] of the store
            [event][xindmap.event.Event.Event]
        event: The stored [event][xindmap.event.Event.Event].
    """

    priority: int
    item_id: int = dataclasses.field(
        default_factory=itertools.count().__next__, init=False
    )
    event_source: typing.Any = dataclasses.field(compare=False)
    event: typing.Any = dataclasses.field(compare=False)


@singleton_decorator.singleton
class EventDispatcher:
    """The event dispatcher centralizes the dispatching of
    [events][xindmap.event.Event.Event] to ensure they are dispatched one at a
    time even if dispatching an [event][xindmap.event.Event.Event] leads to
    dispatching another one.

    This is a singleton and is therefore unique during runtime.

    This class should not be called upon and is only made to be used by
    [event sources][xindmap.event.EventSource.EventSource] as a way to register
    [callbacks][xindmap.event.EventSource.EventSource--callback] and dispatch
    their events in the same place.

    This dispatcher was designed to work on top of [`tkinter`][] main loop and
    was therefore designed for a single thread environment.
    It may work in a multi thread environment but no protection is being added
    to ensure that race condition are properly handled.

    Attributes:
        __event_queue:
            Queue used as buffer for [events][xindmap.event.Event.Event] to
            dispatch to make sure they are dispatched in the right order.
        __event_source_to_event_type_to_callbacks:
            A dictionnary mapping an
            [event source][xindmap.event.EventSource.EventSource] to the
            [event types][xindmap.event.EventSource.EventSource--event-type]
            it produces to
            [callbacks][xindmap.event.EventSource.EventSource--callback]
            registered to each ones.
        __is_dispatching:
            [`True`][] if [events][xindmap.event.Event.Event] are being
            dispatched, [`False`][] otherwise.
    """

    # callback *****************************************************************
    def register_callback(self, event_source, event_type, callback):
        """Registers a
        [callback][xindmap.event.EventSource.EventSource--callback] to an
        [event type][xindmap.event.EventSource.EventSource--event-type]
        produced by a given
        [event source][xindmap.event.EventSource.EventSource].

        Registering a
        [callback][xindmap.event.EventSource.EventSource--callback] means that
        it will be called whenever the
        [event source][xindmap.event.EventSource.EventSource] dispatches an
        [event][xindmap.event.Event.Event] of a given
        [type][xindmap.event.EventSource.EventSource--event-type].

        Args:
            event_source:
                The [event source][xindmap.event.EventSource.EventSource]
                producing [events][xindmap.event.Event.Event] of the given
                [type][xindmap.event.EventSource.EventSource--event-type] to
                which register the
                [callback][xindmap.event.EventSource.EventSource--callback].
            event_type:
                The
                [event type][xindmap.event.EventSource.EventSource--event-type]
                to which register the
                [callback][xindmap.event.EventSource.EventSource--callback].
            callback:
                The [callback][xindmap.event.EventSource.EventSource--callback]
                to register.

        Raises:
            EventSourceError: If the
                [event source][xindmap.event.EventSource.EventSource] is unknown
                to this dispatcher.
            EventTypeError: If the
                [event source][xindmap.event.EventSource.EventSource] does not
                dispatch [event][xindmap.event.Event.Event] of the given
                [type][xindmap.event.EventSource.EventSource--event-type].
        """
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
        """Instantiates this dispatcher.

        As it is a singleton, this method is called once during runtime.
        """
        self.__event_queue = queue.PriorityQueue()
        self.__event_source_to_event_type_to_callbacks = {}
        self.__is_dispatching = False
        self.__dispatching_priority = None

    # dispatch *****************************************************************
    def dispatch_event(self, event_source, event, priority):
        """Dispatches an [event][xindmap.event.Event.Event].

        It adds the [event][xindmap.event.Event.Event] to the internal event
        queue and starts to dispatch them using the internal
        [dispatch method][xindmap.event.EventDispatcher.EventDispatcher.__dispatch_event_queue].
        if is not already dispatching the queue.

        [events][xindmap.event.Event.Event] can be dispatched with different
        priority.
        It is represented by an integer value.
        The lower the value, the higher the priority.

        Args:
            event_source:
                The [source][xindmap.event.EventSource.EventSource] of the
                [event][xindmap.event.Event.Event].
            event:
                The [event][xindmap.event.Event.Event] to dispatch.
            priority:
                The priority value of the [event][xindmap.event.Event.Event].
                The lower it is, the higher the priority.

        Raises:
            EventSourceError: If the
                [event source][xindmap.event.EventSource.EventSource] is unknown
                to this dispatcher.
            EventTypeError: If the
                [event source][xindmap.event.EventSource.EventSource] does not
                dispatch [events][xindmap.event.Event.Event] of this
                [type][xindmap.event.EventSource.EventSource--event-type].
        """
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
        self.__event_queue.put(EventQueueItem(priority, event_source, event))

        # dispatch event *********************************************
        if not self.__is_dispatching:
            self.__dispatch_event_queue()

    def __dispatch_event_queue(self):
        """Internal method in charge of dispatching events stored in the
        internal event queue.

        It calls every
        [callbacks][xindmap.event.EventSource.EventSource--callback] in their
        registration order linked to [events][xindmap.event.Event.Event] stored
        in the internal event queue till it is empty.
        """
        with dispatching_lock:
            self.__is_dispatching = True

            while not self.__event_queue.empty():
                queue_item = self.__event_queue.get()
                priority = queue_item.priority
                event_source, event = queue_item.event_source, queue_item.event

                self.__dispatching_priority = priority

                for callback in self.__event_source_to_event_type_to_callbacks[
                    event_source
                ][event.type]:
                    callback(event_source, event)

            self.__is_dispatching = False

    def is_dispatching(self):
        return self.__is_dispatching

    # source *******************************************************************
    def register_event_source(self, event_source, event_types):
        """Registers an [event source][xindmap.event.EventSource.EventSource]
        making it known to this dispatcher.

        Without this registration step, the
        [event source][xindmap.event.EventSource.EventSource] can not dispatch
        events using
        [`dispatch_event`][xindmap.event.EventDispatcher.EventDispatcher.dispatch_event].

        Args:
            event_source:
                The [event source][xindmap.event.EventSource.EventSource] to
                register.
            event_types:
                Iterable containing
                [event types][xindmap.event.EventSource.EventSource--event-type]
                the [event source][xindmap.event.EventSource.EventSource] can
                dispatch.
        """
        self.__event_source_to_event_type_to_callbacks[event_source] = {
            event_type: [] for event_type in event_types
        }
