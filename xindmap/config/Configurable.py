import inspect
import logging
import re

from .Config import Config
from .Variables import Variables


class Configurable:
    """A configurable is an object using the
    [config][xindmap.config.Config.Config] to expose part of its settings 
    through statically declared [variables][xindmap.config.Variable.Variable] in
    the [variable list][xindmap.config.Variables.Variables].

    Upon instantiation, the configurable declares the
    [variables][xindmap.config.Variable] it wishes to use among the
    [variable list][xindmap.config.Variables.Variables].
    Upon changes on one of these through the
    [config][xindmap.config.Config.Config], the configurable is alerted through
    callbacks.

    The callbacks are expected to be methods of the configurable named
    `on_config_variable_{variable_name}_set` where `{variable_name}` is replaced
    by the name of the [variable][xindmap.config.Variable.Variable] as found in
    the [variable list][xindmap.config.Variables.Variables].
    If the configurable does not implement such a method, a warning logged is
    used to identify the missing method.

    Attributes:
        __callback_regex:
            Compiled regex used to identify the callbacks among the methods of
            the configurable.
        __variable_name_to_callback:
            Dictionnary mapping a variable name to callback called when the
            variable value is set by through the
            [config][xindmap.config.Config.Config].
    """
    # callback *****************************************************************
    __callback_regex = re.compile("on_config_variable_(.*)_set")
    """Compiled regex used to identify callbacks among the methods of a
    configurable.
    """

    def __on_config_variable_set(self, config, event):
        """Callback to be called upon setting a variable value through the
        [config][xindmap.config.Config.Config].

        It calls the callback for the variable that have been set.

        Args:
            config: The [config][xindmap.config.Config.Config].
            event: The event for which this callback is called.
        """
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
        """Instantiates this configurable.

        Builds the mapping from variable name to the corresponding callbacks.

        Args:
            config_variables:
                Iterable containing the
                [variables][xindmap.config.Variables.Variables] from the
                [variable list][xindmap.config.Variables.Variables] on which
                this configurable can be configured.
        """
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
