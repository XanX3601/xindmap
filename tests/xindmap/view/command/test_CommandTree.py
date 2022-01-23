import xindmap.view.command as command

def test_add_path():
    # CONSIDERING
    # a command tree 
    tree = command.CommandTree()

    # a path of command inputs
    command_inputs = [
        command.CommandInput(command.CommandInputType.DEFAULT, ':'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'h'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'e'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'l'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'l'),
        command.CommandInput(command.CommandInputType.DEFAULT, 'o'),
        command.CommandInput(command.CommandInputType.ENTER),
    ]

    # a command
    hello_command = command.Command('hello', 'hello command')

    # WHEN
    # adding the considered path to the tree
    tree.add_path(hello_command, command_inputs)

    # THEN
    # by following the path from the root of the tree will lead us to the
    # command
    tree.root()
    for command_input in command_inputs:
        assert tree.input(command_input)

    assert tree.current_command() == hello_command

