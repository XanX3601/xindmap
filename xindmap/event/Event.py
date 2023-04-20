from .EventAttributeError import EventAttributeError


class Event:
    """An event is something that occurs and is dispatched by an
    [event source][xindmap.event.EventSource.EventSource].

    An event has two primary attribute but upon instantiation, the event can be
    asigned any number of other attributes.

    Attributes:
        __attribute_name_to_value:
            Dictionnary mapping the name of attributes dynamically given to the
            event upon instantiating it.
        __source: The [event source][xindmap.event.EventSource.EventSource]
        __type:
            The [type][xindmap.event.EventSource.EventSource--event-type] of the
            event.
    """
    # attribute ****************************************************************
    def __getattr__(self, attribute_name):
        """Gets an attribute that is not statically declared.

        Args:
            attribute_name: The name of the attribute to get

        Returns:
            The value of the attribute.

        Raises:
            EventAttributeError: If the attribute does not exist.
        """
        if attribute_name not in self.__attribute_name_to_value:
            raise EventAttributeError(
                f"attribute {attribute_name} not found for event {self}"
            )

        return self.__attribute_name_to_value[attribute_name]

    # constructor **************************************************************
    def __init__(self, type, **kwargs):
        """Instantiates this event.

        Args:
            type:
                The [type][xindmap.event.EventSource.EventSource--event-type] of
                the event.
            kwargs: All other attributes dynamically given to this event.
        """
        self.__type = type
        self.__attribute_name_to_value = kwargs

    # string *******************************************************************
    def __repr__(self):
        """Same as [`__str__`][xindmap.event.Event.Event.__str__].
        """
        return str(self)

    def __str__(self):
        """Returns a string representation of this event.
        """
        return f"event {repr(self.__type)} {self.__attribute_name_to_value}"

    # type *********************************************************************
    @property
    def type(self):
        """Returns the [type][xindmap.event.EventSource.EventSource--event-type]
        of this event.
        """
        return self.__type
