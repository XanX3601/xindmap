class Hitbox:
    # compare ******************************************************************
    def __eq__(self, other_hitbox):
        if not isinstance(other_hitbox, Hitbox):
            return False

        return (
            self.__x1 == other_hitbox.__x1
            and self.__y1 == other_hitbox.__y1
            and self.__x2 == other_hitbox.__x2
            and self.__y2 == other_hitbox.__y2
        )

    # constructor **************************************************************
    def __init__(self):
        self.__x1 = 0
        self.__y1 = 0
        self.__x2 = 0
        self.__y2 = 0

        self.__height = 0
        self.__width = 0

    # coordinate ***************************************************************
    @property
    def center_x(self):
        return self.__x1 + self.__width / 2

    @center_x.setter
    def center_x(self, center_x):
        if center_x != self.center_x:
            self.x1 = center_x - self.__width / 2

    @property
    def center_y(self):
        return self.__y1 + self.__height / 2

    @center_y.setter
    def center_y(self, center_y):
        if center_y != self.center_y:
            self.y1 = center_y - self.__height / 2

    def coords(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        self.__height = y2 - y1
        self.__width = x2 - x1

    @property
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, x1):
        if x1 != self.__x1:
            self.__x1 = x1
            self.__x2 = x1 + self.__width

    @property
    def x2(self):
        return self.__x2

    @x2.setter
    def x2(self, x2):
        if x2 != self.__x2:
            self.__x2 = x2
            self.__x1 = x2 - self.__width

    @property
    def y1(self):
        return self.__y1

    @y1.setter
    def y1(self, y1):
        if y1 != self.__y1:
            self.__y1 = y1
            self.__y2 = y1 + self.__height

    @property
    def y2(self):
        return self.__y2

    @y2.setter
    def y2(self, y2):
        if y2 != self.__y2:
            self.__y2 = y2
            self.__y1 = y2 - self.__height

    # size *********************************************************************
    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height != self.__height:
            self.__height = height
            self.__y2 = self.__y1 + height

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        if width != self.__width:
            self.__width = width
            self.__x2 = self.__x1 + width

    # string *******************************************************************
    def __str__(self):
        return f"hitbox {self.__width}x{self.__height} ({self.__x1}, {self.__y1}, {self.__x2}, {self.__y2})"
