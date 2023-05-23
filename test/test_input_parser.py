import xindmap.input


def test_parse_single_input():
    string_to_expected_input = {
        "a": xindmap.input.Input(xindmap.input.InputType.default, "a"),
        "aa": None,
        "<CR>": xindmap.input.Input(xindmap.input.InputType.enter),
        "<BS>": xindmap.input.Input(xindmap.input.InputType.backspace),
    }

    for string, expected_input in string_to_expected_input.items():
        input = xindmap.input.InputParser.parse_input(string)
        assert input == expected_input


def test_parse_inputs():
    string_to_expected_inputs = {
        "a<CR>b<>": [
            xindmap.input.Input(xindmap.input.InputType.default, "a"),
            xindmap.input.Input(xindmap.input.InputType.enter),
            xindmap.input.Input(xindmap.input.InputType.default, "b"),
            xindmap.input.Input(xindmap.input.InputType.default, "<"),
            xindmap.input.Input(xindmap.input.InputType.default, ">"),
        ],
        "abc<CR><CR>b<>": [
            xindmap.input.Input(xindmap.input.InputType.default, "a"),
            xindmap.input.Input(xindmap.input.InputType.default, "b"),
            xindmap.input.Input(xindmap.input.InputType.default, "c"),
            xindmap.input.Input(xindmap.input.InputType.enter),
            xindmap.input.Input(xindmap.input.InputType.enter),
            xindmap.input.Input(xindmap.input.InputType.default, "b"),
            xindmap.input.Input(xindmap.input.InputType.default, "<"),
            xindmap.input.Input(xindmap.input.InputType.default, ">"),
        ],
        "import test<CR>:test<CR>": [
            xindmap.input.Input(xindmap.input.InputType.default, "i"),
            xindmap.input.Input(xindmap.input.InputType.default, "m"),
            xindmap.input.Input(xindmap.input.InputType.default, "p"),
            xindmap.input.Input(xindmap.input.InputType.default, "o"),
            xindmap.input.Input(xindmap.input.InputType.default, "r"),
            xindmap.input.Input(xindmap.input.InputType.default, "t"),
            xindmap.input.Input(xindmap.input.InputType.default, " "),
            xindmap.input.Input(xindmap.input.InputType.default, "t"),
            xindmap.input.Input(xindmap.input.InputType.default, "e"),
            xindmap.input.Input(xindmap.input.InputType.default, "s"),
            xindmap.input.Input(xindmap.input.InputType.default, "t"),
            xindmap.input.Input(xindmap.input.InputType.enter),
            xindmap.input.Input(xindmap.input.InputType.default, ":"),
            xindmap.input.Input(xindmap.input.InputType.default, "t"),
            xindmap.input.Input(xindmap.input.InputType.default, "e"),
            xindmap.input.Input(xindmap.input.InputType.default, "s"),
            xindmap.input.Input(xindmap.input.InputType.default, "t"),
            xindmap.input.Input(xindmap.input.InputType.enter),
        ],
    }

    for string, expected_inputs in string_to_expected_inputs.items():
        inputs = xindmap.input.InputParser.parse_inputs(string)
        assert inputs == expected_inputs


def test_stringify_input():
    input_to_expected_string = [
        (xindmap.input.Input(xindmap.input.InputType.default, "a"), "a"),
        (xindmap.input.Input(xindmap.input.InputType.enter), "<CR>"),
        (xindmap.input.Input(xindmap.input.InputType.backspace), "<BS>"),
    ]

    for input, expeted_string in input_to_expected_string:
        input_as_str = xindmap.input.InputParser.stringify_input(input)
        assert input_as_str == expeted_string
