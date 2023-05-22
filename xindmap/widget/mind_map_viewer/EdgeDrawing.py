class EdgeDrawing:
    # coords *******************************************************************
    @property
    def from_x(self):
        return self.__from_x

    @from_x.setter
    def from_x(self, from_x):
        self.__from_x = from_x
        self.__place_components()

    @property
    def from_y(self):
        return self.__from_y

    @from_y.setter
    def from_y(self, from_y):
        self.__from_y = from_y
        self.__place_components()

    def set_coords(self, from_x, from_y, to_x, to_y):
        self.__from_x = from_x
        self.__from_y = from_y
        self.__to_x = to_x
        self.__to_y = to_y
        self.__place_components()

    @property
    def to_x(self):
        return self.__to_x

    @to_x.setter
    def to_x(self, to_x):
        self.__to_x = to_x
        self.__place_components()

    @property
    def to_y(self):
        return self.__to_y

    @to_y.setter
    def to_y(self, to_y):
        self.__to_y = to_y
        self.__place_components()

    # constructor **************************************************************
    def __init__(self, canvas):
        self.__canvas = canvas

        self.__from_x = 0
        self.__from_y = 0
        self.__to_x = 0
        self.__to_y = 0

        self.__line_id = self.__canvas.create_line(self.__from_x, self.__from_y, self.__to_x, self.__to_y)

    # draw *********************************************************************
    def clear(self):
        self.__canvas.delete(self.__line_id)

    def __place_components(self):
        self.__canvas.coords(self.__line_id, self.__from_x, self.__from_y, self.__to_x, self.__to_y)
