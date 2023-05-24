import inspect
import re

import singleton_decorator

import xindmap.event

from .ConfigError import ConfigError
from .Variables import Variables
from .VariableTypes import VariableTypes


@singleton_decorator.singleton
class Config(xindmap.event.EventSource):
    """A singleton config holding current values of
    [variables][xindmap.config.Variable.Variable] from
    [`Variables`][xindmap.config.Variables.Variables] class.

    As it is a singleton, the config is a unique object during the runtime of
    the application.
    It can be accessed using the constructor of the class:

    ```python
    import xindmap.config

    config_a = xindmap.config.Config()
    config_b = xindmap.config.Config()

    assert(id(config_a) == id(config_b))
    ```

    The value of each variable can be set freely but the new value must respect
    the type of the variable.

    The config is an [event source][xindmap.event.EventSource.EventSource].
    It dispatches event of typed enumed in
    [`Variables`][xindmap.config.Variables.Variables] class.
    It dispatches one event type for each available variable.

    Is is not recommended to register callback to this config.
    The recommended way is for classes to derive the
    [`Configurable`][xindmap.config.Configurable.Configurable] class if they
    need to be synchronized with a variable value.

    It is ensure for the variable values to comply with the variable type.

    Attributes:
        __variable_name_to_value:
            Dictionnary mapping a variable name to its current value
        __variable_type_to_check_function:
            Dictionnary mapping a
            [variable type][xindmap.config.VariableTypes.VariableTypes]
            to a method checking if a value complies with the type.
    """

    # constructor **************************************************************
    def __init__(self):
        """Instantiates this config."""
        super().__init__(Variables)

        self.__variable_name_to_value = {}
        for variable in Variables:
            self.__variable_name_to_value[variable.name] = variable.default

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
    def __variable_type_color_check(value):
        return isinstance(value, str) and re.fullmatch(
            r"#[\dabcdef]{6}|#[\dabcdef]{3}", value
        )

    @staticmethod
    def __variable_type_int_check(value):
        """Checks if a value complies with type
        [`VariableTypes.int`][xindmap.config.VariableTypes.VariableTypes.int].

        Args:
            value: The value to check

        Returns:
            [`True`][] if the value complies, [`False`][] otherwise.
        """
        return isinstance(value, int)

    @staticmethod
    def __variable_type_float_check(value):
        """Checks if a value complies with type
        [`VariableTypes.float`][xindmap.config.VariableTypes.VariableTypes.float].

        Args:
            value: The value to check

        Returns:
            [`True`][] if the value complies, [`False`][] otherwise.
        """
        return isinstance(value, float) or isinstance(value, int)

    @staticmethod
    def __variable_type_string_check(value):
        """Checks if a value complies with type
        [`VariableTypes.string`][xindmap.config.VariableTypes.VariableTypes.string].

        Args:
            value: The value to check

        Returns:
            [`True`][] if the value complies, [`False`][] otherwise.
        """
        return isinstance(value, str)

    # variable *****************************************************************
    def get(self, variable):
        return self.__variable_name_to_value[variable.name]

    def set(self, variable, value):
        """Sets the value of a variable.

        Raises an error if the value does not comply with the variable type.

        Args:
            variable:
                The [variable][xindmap.config.Variable.Variable] from the
                [variable list][xindmap.config.Variables.Variables].
            value: The value to be set.

        Raises:
            ConfigError: If the value does not comply with the variable type.
        """
        if not self.__variable_type_to_check_function[variable.type](value):
            raise ConfigError(
                f"value {value} for variable {variable} is not of type {variable.type}"
            )

        self.__variable_name_to_value[variable.name] = value

        event = xindmap.event.Event(variable, value=value)
        self._dispatch_event(event)
