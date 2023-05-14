from .MindNodeDrawing import MindNodeDrawing

class RootNodeDrawing(MindNodeDrawing):
    # constructor **************************************************************
    def __init__(self, canvas):
        super().__init__(canvas)

    # size *********************************************************************
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        center_y = self.center_y

        y = center_y - height // 2
        self._y = y

        self._height = height
        super()._place_components()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        center_x = self.center_x

        x = center_x - width // 2
        self._x = x

        self._width = width
        super()._place_components()
