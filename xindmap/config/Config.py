import inspect

import singleton_decorator

import xindmap.event

from .ConfigError import ConfigError
from .Variables import Variables
from .VariableTypes import VariableTypes


@singleton_decorator.singleton
class Config(xindmap.event.EventSource):
    # constructor **************************************************************
    def __init__(self):
        super().__init__(Variables)

        self.__variable_name_to_value = {}
        for variable in Variables:
            self.__variable_name_to_value[variable.name] = variable

        functions = inspect.getmembers(self, inspect.isfunction)
        function_name_to_function = {
            function_name: function for function_name, function in functions
        }

        self.__variable_type_to_check_function = {}
        for type in VariableTypes:
            check_function_name = f"_Config__variable_type_{type.name}_check"
            function = function_name_to_function[check_function_name]

            self.__variable_type_to_check_function[type] = function

    # type *********************************************************************
    @staticmethod
    def __variable_type_int_check(value):
        return isinstance(value, int)

    @staticmethod
    def __variable_type_float_check(value):
        return isinstance(value, float) or isinstance(value, int)

    @staticmethod
    def __variable_type_string_check(value):
        return isinstance(value, str)

    # variable *****************************************************************
    def set(self, variable, value):
        if not self.__variable_type_to_check_function[variable.type](value):
            raise ConfigError(
                f"value {value} for variable {variable} is not of type {variable.type}"
            )

        self.__variable_name_to_value[variable.name] = value

        event = xindmap.event.Event(variable, value=value)
        self._dispatch_event(event)
