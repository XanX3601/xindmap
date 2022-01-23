import xindmap.view.command as command

def test_string_to_command_inputs():
    # CONSIDERING
    # a command input handler
    # a giant string containing all the possible command input types
    input_handler = command.CommandInputHandler()

    string = ':hello<CR>'

    # WHEN
    # split
    command_inputs = input_handler.string_to_command_inputs(string)

    # THEN
    # the returned list of command inputs must match the content of the string
    expected_command_inputs = [
        command.CommandInput(command.CommandInputType.DEFAULT, ':'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'h'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'e'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'l'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'l'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'o'),
        command.CommandInput(command.CommandInputType.ENTER),
    ]

    assert command_inputs == expected_command_inputs
