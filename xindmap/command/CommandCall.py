class CommandCall:
    # constructor **************************************************************
    def __init__(self, command_name, args):
        self.__command_name = command_name
        self.__args = args

    # property *****************************************************************
    @property
    def args(self):
        return self.__args

    @property
    def command_name(self):
        return self.__command_name

    # string *******************************************************************
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<command_call {self.__command_name} args={self.__args}>"
