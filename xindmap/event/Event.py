from .EventAttributeError import EventAttributeError


class Event:
    # attribute ****************************************************************
    def __getattr__(self, attribute_name):
        if attribute_name not in self.__attribute_name_to_value:
            raise EventAttributeError(
                f"attribute {attribute_name} not found for event {self}"
            )

        return self.__attribute_name_to_value[attribute_name]

    # constructor **************************************************************
    def __init__(self, type, **kwargs):
        self.__type = type
        self.__attribute_name_to_value = kwargs

    # string *******************************************************************
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"event {repr(self.__type)} {self.__attribute_name_to_value}"

    # type *********************************************************************
    @property
    def type(self):
        return self.__type
