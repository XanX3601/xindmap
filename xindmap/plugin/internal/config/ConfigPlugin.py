import inspect

import xindmap.config
import xindmap.plugin


class ConfigPlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [("set", self.command_set)]

    def command_set(self, variable_name, variable_value=None, api=None):
        variable = ConfigPlugin.variable_name_to_variable.get(variable_name, None)
        if variable is not None:
            if variable_value is None:
                variable_value = variable.default

            variable_value = self.variable_type_to_parser[variable.type](variable_value)
            api.set_config(variable, variable_value)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()

        methods = inspect.getmembers(self, inspect.ismethod)
        method_name_to_method = {method_name: method for method_name, method in methods}

        self.variable_type_to_parser = {}
        for type in xindmap.config.VariableTypes:
            parser_name = f"parse_{type.name}_value"
            method = method_name_to_method[parser_name]

            self.variable_type_to_parser[type] = method

    # variable *****************************************************************
    variable_name_to_variable = {}

    @classmethod
    def parse_int_value(cls, value):
        return int(value)

    @classmethod
    def parse_float_value(cls, value):
        return float(value)

    @classmethod
    def parse_string_value(cls, value):
        return str(value)
