import ast
import inspect

import customtkinter as ctk

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
    variable_name_to_variable = {
        "test": xindmap.config.Variables.mind_map_viewer_mind_node_drawing_title_color
    }

    @classmethod
    def parse_color_value(cls, value):
        return str(value)

    @classmethod
    def parse_color_list_value(cls, value):
        return ast.literal_eval(value)

    @classmethod
    def parse_int_value(cls, value):
        return int(value)

    @classmethod
    def parse_float_value(cls, value):
        return float(value)

    @classmethod
    def parse_font_value(cls, value):
        value = value.split("-")

        if not value:
            raise ValueError(f"cannot parse {value} into a valid font value")

        font = str(value[0])
        size = int(value[1]) if len(value) >= 2 else None
        weight = str(value[2]) if len(value) >= 3 else None
        slant = str(value[3]) if len(value) >= 4 else "roman"
        underline = (
            True if len(value) >= 5 and value[4].lower() in {"true", "t"} else False
        )
        overstrike = (
            True if len(value) >= 6 and value[5].lower() in {"true", "t"} else False
        )

        font = ctk.CTkFont(
            font,
            size=size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike,
        )

        return font

    @classmethod
    def parse_string_value(cls, value):
        return str(value)
