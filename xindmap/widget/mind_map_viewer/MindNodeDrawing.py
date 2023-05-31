import customtkinter as ctk

import xindmap.config
import xindmap.mind_map
import xindmap.widget.tools


class MindNodeDrawing(xindmap.config.Configurable):
    # config callback **********************************************************
    def on_config_variable_mind_map_viewer_mind_node_drawing_body_height_set(
        self, value
    ):
        self._place_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_radius_set(
        self, value
    ):
        self._place_components()

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
        self._place_components()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._place_components()

    # constructor **************************************************************
    def __init__(self, canvas):
        super().__init__(
            [
                xindmap.config.Variables.mind_map_viewer_mind_node_drawing_body_height,
                xindmap.config.Variables.mind_map_viewer_mind_node_drawing_selector_radius,
            ]
        )

        self.__canvas = canvas

        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0

        self._is_selected = False
        self._status = xindmap.mind_map.MindNodeStatus.none

        config = xindmap.config.Config()

        self._body_id = self.__canvas.create_rectangle(
            0, 0, 0, 0, outline="", fill="pink", tags="mind_node_drawing_body_id"
        )
        self._description_body_id = self.__canvas.create_rectangle(
            0,
            0,
            0,
            0,
            fill="green",
            state=ctk.HIDDEN,
            outline="",
            tags="mind_node_drawing_description_body",
        )
        self._description_id = self.__canvas.create_text(
            0,
            0,
            text="",
            anchor=ctk.NW,
            state=ctk.HIDDEN,
            width=config.get(
                xindmap.config.Variables.mind_map_viewer_mind_node_drawing_description_width
            ),
            tags="mind_node_drawing_description",
        )
        self._selector_id = self.__canvas.create_polygon(
            0,
            0,
            0,
            0,
            state=ctk.HIDDEN,
            fill="",
            outline="white",
            smooth=True,
            tags="mind_node_drawing_selector",
        )
        self._title_id = self.__canvas.create_text(
            0, 0, text="", anchor=ctk.S, tags="mind_node_drawing_title"
        )

        self.__canvas.tag_raise(
            "mind_node_drawing_description_body", "mind_node_drawing_body_id"
        )
        self.__canvas.tag_raise(
            "mind_node_drawing_description_body", "mind_node_drawing_title"
        )
        self.__canvas.tag_raise(
            "mind_node_drawing_description", "mind_node_drawing_description_body"
        )
        self.__canvas.tag_raise(
            "mind_node_drawing_selector", "mind_node_drawing_description"
        )

        self._place_components()

    # description **************************************************************
    @property
    def description(self):
        return self.__canvas.itemcget(self._description_id, "text")

    @description.setter
    def description(self, description):
        self.__canvas.itemconfigure(self._description_id, text=description)

    # draw *********************************************************************
    def clear(self):
        self.__canvas.delete(self._title_id, self._description_id, self._body_id)

    def _place_components(self):
        config = xindmap.config.Config()

        x = self._x
        y = self._y
        width = self._width
        height = self._height

        center_x = self.center_x
        center_y = self.center_y

        body_height = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_body_height
        )
        body_half_height = body_height / 2

        description_bbox = self.__canvas.bbox(self._description_id)
        title_bbox = self.__canvas.bbox(self._title_id)

        self.__canvas.coords(
            self._body_id,
            x,
            center_y - body_half_height,
            x + width,
            center_y + body_half_height,
        )
        self.__canvas.coords(self._title_id, center_x, center_y - body_half_height)
        self.__canvas.coords(self._description_id, x, y + height)
        if (
            description_bbox is not None
            and abs(description_bbox[0] - description_bbox[2]) > 5
        ):
            self.__canvas.coords(self._description_body_id, *description_bbox)

        if title_bbox is not None:
            self.__canvas.coords(
                self._selector_id,
                xindmap.widget.tools.compute_round_rectangle_points(
                    *title_bbox,
                    radius=config.get(
                        xindmap.config.Variables.mind_map_viewer_mind_node_drawing_selector_radius
                    )
                ),
            )

    # select *******************************************************************
    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, is_selected):
        self.__is_selected = is_selected

        if is_selected:
            self.__canvas.itemconfigure(self._description_id, state=ctk.NORMAL)
            self.__canvas.itemconfigure(self._description_body_id, state=ctk.NORMAL)
            self.__canvas.itemconfigure(self._selector_id, state=ctk.NORMAL)
            self._place_components()
        else:
            self.__canvas.itemconfigure(self._description_id, state=ctk.HIDDEN)
            self.__canvas.itemconfigure(self._description_body_id, state=ctk.HIDDEN)
            self.__canvas.itemconfigure(self._selector_id, state=ctk.HIDDEN)

    # size *********************************************************************
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self._place_components()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self._place_components()

    # status *******************************************************************
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    # title ********************************************************************
    @property
    def title(self):
        return self.__canvas.itemcget(self._title_id, "text")

    @title.setter
    def title(self, title):
        self.__canvas.itemconfigure(self._title_id, text=title)

    def title_width(self):
        x1, _, x2, _ = self.__canvas.bbox(self._title_id)
        return abs(x1 - x2)
