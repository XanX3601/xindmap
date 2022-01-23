import itertools

import xindmap.view.command as command

def test_enter_inputs_are_always_equal():
    # CONSIDERING
    # 3 enter inputs
    # 2 of them have the same value
    # 1 of then has a different value
    commands = [
        command.CommandInput(command.CommandInputType.ENTER, None),
        command.CommandInput(command.CommandInputType.ENTER, None),
        command.CommandInput(command.CommandInputType.ENTER, 'hello')
    ]

    # THEN
    # they are all equal
    assert commands[0] == commands[1]
    assert commands[0] == commands[2]
    assert commands[1] == commands[2]

def test_different_type_input_are_never_equal():
    # CONSIDERING
    # an input of each type
    command_inputs = [
        command.CommandInput(command.CommandInputType.ENTER),
        command.CommandInput(command.CommandInputType.DEFAULT, 'h')
    ]

    # THEN
    # None are equal
    for input1, input2 in itertools.combinations(command_inputs, 2):
        assert not input1 == input2

def test_default_inputs_are_equal_if_value_are_equal():
    # CONSIDERING
    # 3 default command inputs
    # 2 of them have the same value
    # 1 of then has a different value
    commands = [
        command.CommandInput(command.CommandInputType.DEFAULT, 'a'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'b'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'b')
    ]

    # THEN
    # the ones with the same value are equal, others are not
    assert not commands[0] == commands[1]
    assert not commands[0] == commands[2]
    assert commands[1] == commands[2]

