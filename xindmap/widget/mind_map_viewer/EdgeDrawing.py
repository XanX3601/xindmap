import itertools

import customtkinter as ctk

import xindmap.config


class EdgeDrawing:
    # component ****************************************************************
    def set_line_width(self, width):
        self.__canvas.itemconfigure(self.__line_id, width=width)

    # constructor **************************************************************
    __id_counter = itertools.count()

    def __init__(self, canvas):
        self.__id = next(EdgeDrawing.__id_counter)

        self.__canvas = canvas

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        # components
        drawing_tag = f"edge_drawing_{self.__id}"

        config = xindmap.config.Config()

        line_width = config.get(
            xindmap.config.Variables.mind_map_viewer_edge_drawing_line_width
        )

        self.__line_id = self.__canvas.create_line(
            0,
            0,
            0,
            0,
            smooth=True,
            tags=(drawing_tag, "edge_drawing_line"),
            width=line_width,
        )

    def __del__(self):
        self.__canvas.delete(f"edge_drawing_{self.__id}")

    # update *******************************************************************
    def update_components(self):
        config = xindmap.config.Config()

        padding_width_percentage = config.get(
            xindmap.config.Variables.mind_map_viewer_edge_drawing_inner_point_padding_width_percentage
        )

        width = self.x2 - self.x1
        padding = width * padding_width_percentage

        self.__canvas.coords(
            self.__line_id,
            self.x1,
            self.y1,
            self.x1 + padding,
            self.y1,
            self.x2 - padding,
            self.y2,
            self.x2,
            self.y2,
        )
