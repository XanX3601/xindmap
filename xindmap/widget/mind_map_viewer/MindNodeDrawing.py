import customtkinter as ctk

class MindNodeDrawing:
    # coords *******************************************************************
    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.truc()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.truc()

    # constructor **************************************************************
    def __init__(self, canvas):
        self.__canvas = canvas

        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0

        self._is_selected = False

        self._body_id = self.__canvas.create_rectangle(
            self._x, self._y, self._x + self._width, self._y + self._height
        )
        self._title_id = self.__canvas.create_text(self._x, self._y, text="hello is this centered ?", anchor=ctk.CENTER)

    def truc(self):
        self.__canvas.coords(self._body_id, self._x, self._y, self._x+self._width, self._y+self._height)
        self.__canvas.coords(self._title_id, self.center_x, self.center_y)

    # select *******************************************************************
    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, is_selected):
        self.__is_selected = is_selected

        if is_selected:
            self.__canvas.itemconfigure(self._body_id, fill="red")
        else:
            self.__canvas.itemconfigure(self._body_id, fill="")

    # size *********************************************************************
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self.truc()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self.truc()

    # title ********************************************************************
    @property
    def title(self):
        return self.__canvas.itemcget(self._title_id, "text")
