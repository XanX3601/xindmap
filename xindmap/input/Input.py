class Input:
    # constructor **************************************************************
    def __init__(self, type, value=None):
        self.__type = type
        self.__value = value

    # input ********************************************************************
    def __eq__(self, other_input):
        if not isinstance(other_input, Input):
            return False

        return self.__type == other_input.__type and self.__value == other_input.__value

    # property *****************************************************************
    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    # string *******************************************************************
    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<input {self.type.name} value={self.value}>"
