import inspect
import logging
import re

from .Config import Config
from .Variables import Variables


class Configurable:
    # callback *****************************************************************
    __callback_regex = re.compile("on_config_variable_(.*)_set")

    def __on_config_variable_set(self, config, event):
        variable = event.type

        if variable.name not in self.__variable_name_to_callback:
            logging.warning(
                f"configurable {id(self)}: callback not implemented for config variable {variable.name} for object {str(self)} ({type(self)})"
            )
            return

        callback = self.__variable_name_to_callback[variable.name]
        callback(event.value)

    # constructor **************************************************************
    def __init__(self, config_variables):
        config = Config()

        for variable in config_variables:
            config.register_callbacks(variable, self.__on_config_variable_set)

        self.__variable_name_to_callback = {}
        methods = inspect.getmembers(self, inspect.ismethod)
        for method_name, method in methods:
            result = Configurable.__callback_regex.search(method_name)

            if result is None:
                continue

            variable_name = result.groups()[0]
            self.__variable_name_to_callback[variable_name] = method
