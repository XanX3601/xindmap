import re

from .Input import Input
from .InputType import InputType


class InputParser:
    """Collection of methods to parse and convert
    [inputs][xindmap.input.Input.Input].

    This class is not made to be instantiated, only to expose static methods.
    """

    # parse ********************************************************************
    __input_type_to_regex = {
        InputType.backspace: "<BS>",
        InputType.default: ".",
        InputType.enter: "<CR>",
    }

    __input_type_to_compiled_regex = {
        input_type: re.compile(regex)
        for input_type, regex in __input_type_to_regex.items()
    }

    __input_types_but_default = [
        input_type for input_type in InputType if input_type != InputType.default
    ]

    __split_regex = (
        "("
        + "|".join(
            regex
            for input_type, regex in __input_type_to_regex.items()
            if input_type != InputType.default
        )
        + ")"
    )

    __compiled_string_regex = re.compile(__split_regex)

    @classmethod
    def parse_input(cls, input_as_str):
        """Parses a string into a single [input][xindmap.input.Input.Input].

        Args:
            input_as_str: the [string][str] to parse

        Returns:
            input:
                The [input][xindmap.input.Input.Input] once parsed or [`None`][]
                if it could not be parsed.
        """
        for input_type in cls.__input_types_but_default:
            regex = cls.__input_type_to_compiled_regex[input_type]
            if regex.fullmatch(input_as_str):
                return Input(input_type)

        if cls.__input_type_to_compiled_regex[InputType.default].fullmatch(
            input_as_str
        ):
            return Input(InputType.default, input_as_str)

        return None

    @classmethod
    def parse_inputs(cls, inputs_as_str):
        """Parses a string into a list of [inputs][xindmap.input.Input.Input].

        Args:
            inputs_as_str: the [string][str] to parse

        Returns:

        """
        inputs_as_str_split = cls.__compiled_string_regex.split(inputs_as_str)
        assert None not in inputs_as_str_split

        inputs = []
        for input_as_str in inputs_as_str_split:
            input = cls.parse_input(input_as_str)
            if input is None:
                for c in input_as_str:
                    inputs.append(cls.parse_input(c))
            else:
                inputs.append(input)

        return inputs

    # string *******************************************************************
    @classmethod
    def stringify_input(cls, input):
        """Converts an [input][xindmap.input.Input.Input] into a [string][str]
        that is parsable.

        Args:
            input: The [input][xindmap.input.Input.Input] to convert

        Returns:
            input_as_str:
                The [input][xindmap.input.Input.Input] as a [string][str]
        """
        if input.type != InputType.default:
            return cls.__input_type_to_regex[input.type]
        return input.value
