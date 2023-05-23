import itertools

from .VariableTypes import VariableTypes

class Variable:
    # compare ******************************************************************
    def __eq__(self, variable):
        if not isinstance(variable, Variable):
            return False

        return self.__id == variable.__id

    # constructor **************************************************************
    def __init__(self, type, default):
        self.__id = next(Variable.__id_counter)

        self.type = type
        self.default = default

    # id ***********************************************************************
    __id_counter = itertools.count()
