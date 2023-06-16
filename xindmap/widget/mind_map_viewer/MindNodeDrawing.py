import itertools

import customtkinter as ctk

import xindmap.config
import xindmap.mind_map
import xindmap.widget.tools

from .Hitbox import Hitbox


class MindNodeDrawing:
    # body *********************************************************************
    def __update_body_components_coords(self):
        # body rectangle
        x1 = self.__body_hitbox.x1
        y1 = self.__body_hitbox.y1
        x2 = self.__body_hitbox.x2
        y2 = self.__body_hitbox.y2

        self.__body_rectangle_hitbox.coords(x1, y1, x2, y2)
        if self.__body_rectangle_hitbox != self.__body_rectangle_current_hitbox:
            self.__body_rectangle_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(self.__body_rectangle_id, x1, y1, x2, y2)

    def __update_body_hitbox_coords(self):
        self.__body_hitbox.x1 = self.__hitbox.x1
        self.__body_hitbox.y2 = self.__hitbox.y2

    def __update_body_hitbox_size(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        body_height = config.get(
            Variables.mind_map_viewer_mind_node_drawing_body_height
        )

        min_width = config.get(
            Variables.mind_map_viewer_mind_node_drawing_body_min_width
        )

        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_left
        )
        padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_right
        )

        height = body_height
        width = (
            padding_left
            + max(min_width, self.__status_hitbox.width + self.__title_hitbox.width)
            + padding_right
        )

        self.__body_hitbox.width = width
        self.__body_hitbox.height = height

    @property
    def body_color(self):
        return self.__canvas.itemcget(self.__body_rectangle_id, "fill")

    @body_color.setter
    def body_color(self, color):
        self.__canvas.itemconfigure(self.__body_rectangle_id, fill=color, outline=color)

    # constructor **************************************************************
    __id_counter = itertools.count()

    def __init__(self, canvas, body_color="#fff"):
        self.__id = next(MindNodeDrawing.__id_counter)

        self.__canvas = canvas

        self.__is_selected = False

        self.__completion = None
        self.__status = xindmap.mind_map.MindNodeStatus.none

        self.__body_hitbox = Hitbox()
        self.__hitbox = Hitbox()
        self.__selector_hitbox = Hitbox()
        self.__status_hitbox = Hitbox()
        self.__title_hitbox = Hitbox()

        # components
        drawing_tag = f"mind_node_drawing_{self.__id}"

        self.__body_rectangle_id = self.__canvas.create_rectangle(
            0,
            0,
            0,
            0,
            fill=body_color,
            outline=body_color,
            tags=(drawing_tag, "mind_node_drawing_body_rectangle"),
        )
        self.__body_rectangle_current_hitbox = Hitbox()
        self.__body_rectangle_hitbox = Hitbox()

        self.__selector_polygon_id = self.__canvas.create_polygon(
            0,
            0,
            0,
            0,
            fill="",
            outline="white",
            smooth=True,
            state=ctk.HIDDEN,
            tags=(drawing_tag, "mind_node_drawing_selector_polygon"),
        )
        self.__selector_polygon_current_hitbox = Hitbox()
        self.__selector_polygon_hitbox = Hitbox()

        self.__status_arc_id = self.__canvas.create_arc(
            0,
            0,
            0,
            0,
            outline="orange",
            start=90,
            state=ctk.HIDDEN,
            style=ctk.ARC,
            tags=(drawing_tag, "mind_node_drawing_status_arc"),
            width=3,
        )
        self.__status_arc_current_hitbox = Hitbox()
        self.__status_arc_hitbox = Hitbox()

        self.__status_check_id = self.__canvas.create_line(
            0,
            0,
            0,
            0,
            state=ctk.HIDDEN,
            tags=(drawing_tag, "mind_node_drawing_status_check"),
        )
        self.__status_check_current_hitbox = Hitbox()
        self.__status_check_hitbox = Hitbox()

        self.__status_inner_circle_id = self.__canvas.create_oval(
            0,
            0,
            0,
            0,
            state=ctk.HIDDEN,
            tags=(drawing_tag, "mind_node_drawing_status_inner_circle"),
        )
        self.__status_inner_circle_current_hitbox = Hitbox()
        self.__status_inner_circle_hitbox = Hitbox()

        self.__title_text_id = self.__canvas.create_text(
            0, 0, anchor=ctk.NW, tags=(drawing_tag, "mind_node_drawing_title_text")
        )
        self.__title_text_current_hitbox = Hitbox()
        self.__title_text_hitbox = Hitbox()

        # handle canvas zindex

        # order is
        # - selector polygon
        # - body rectangle
        # - title text
        # - status inner circle
        # - status arc
        # - status check

        self.__canvas.lower(
            "mind_node_drawing_status_arc", "mind_node_drawing_status_check"
        )
        self.__canvas.lower(
            "mind_node_drawing_status_inner_circle", "mind_node_drawing_status_arc"
        )
        self.__canvas.lower(
            "mind_node_drawing_title_text", "mind_node_drawing_status_inner_circle"
        )
        self.__canvas.lower(
            "mind_node_drawing_body_rectangle", "mind_node_drawing_title_text"
        )
        self.__canvas.lower(
            "mind_node_drawing_selector_polygon", "mind_node_drawing_body_rectangle"
        )

        self.__update_status_hitbox_size()
        self.__update_title_hitbox_size()
        self.__update_body_hitbox_size()
        self.__update_hitbox_size()
        self.__update_selector_hitbox_size()

    def __del__(self):
        self.__canvas.delete(f"mind_node_drawing_{self.__id}")

    # coordinate ***************************************************************
    @property
    def anchor_x1(self):
        return self.__body_hitbox.x1

    @property
    def anchor_x2(self):
        return self.__body_hitbox.x2

    @property
    def anchor_y(self):
        return self.__body_hitbox.center_y

    @property
    def center_x(self):
        return self.__hitbox.center_x

    @center_x.setter
    def center_x(self, center_x):
        self.__hitbox.center_x = center_x

    @property
    def center_y(self):
        return self.__hitbox.center_y

    @center_y.setter
    def center_y(self, center_y):
        self.__hitbox.center_y = center_y

    @property
    def x1(self):
        return self.__hitbox.x1

    @x1.setter
    def x1(self, x1):
        self.__hitbox.x1 = x1

    @property
    def y1(self):
        return self.__hitbox.y1

    @y1.setter
    def y1(self, y1):
        self.__hitbox.y1 = y1

    # hitbox *******************************************************************
    def __update_hitbox_size(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_bottom
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_top
        )

        # padding left and right are in the body hitbox width
        height = (
            padding_top
            + max(self.__status_hitbox.height, self.__title_hitbox.height)
            + self.__body_hitbox.height
            + padding_bottom
        )
        width = self.__body_hitbox.width

        self.__hitbox.width = width
        self.__hitbox.height = height

    # selector *****************************************************************
    def __update_selector_components_coords(self):
        config = xindmap.config.Config()

        radius = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_selector_radius
        )

        # selector polygon
        x1 = self.__selector_hitbox.x1
        y1 = self.__selector_hitbox.y1
        x2 = self.__selector_hitbox.x2
        y2 = self.__selector_hitbox.y2

        self.__selector_polygon_hitbox.coords(x1, y1, x2, y2)
        if self.__selector_polygon_hitbox != self.__selector_polygon_current_hitbox:
            self.__selector_polygon_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(
                self.__selector_polygon_id,
                *xindmap.widget.tools.compute_round_rectangle_points(
                    x1, y1, x2, y2, radius
                ),
            )

    def __update_selector_hitbox_coords(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_left
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_top
        )

        self.__selector_hitbox.x1 = self.__hitbox.x1 - padding_left
        self.__selector_hitbox.y1 = self.__hitbox.y1 - padding_top

    def __update_selector_hitbox_size(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_bottom
        )
        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_left
        )
        padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_right
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_top
        )

        height = self.__hitbox.height + padding_top + padding_bottom
        width = self.__hitbox.width + padding_left + padding_right

        self.__selector_hitbox.height = height
        self.__selector_hitbox.width = width

    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, is_selected):
        if is_selected != self.__is_selected:
            self.__is_selected = is_selected

            state = ctk.NORMAL if is_selected else ctk.HIDDEN

            self.__canvas.itemconfigure(self.__selector_polygon_id, state=state)

    # size *********************************************************************
    @property
    def height(self):
        return self.__hitbox.height

    @property
    def width(self):
        return self.__hitbox.width

    # status *******************************************************************
    def __update_status_components_coords(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_bottom
        )
        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_left
        )
        padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_right
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_top
        )

        inner_padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_bottom
        )
        inner_padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_left
        )
        inner_padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_right
        )
        inner_padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_top
        )

        # status arc
        x1 = self.__status_hitbox.x1 + padding_left
        y1 = self.__status_hitbox.y1 + padding_top
        x2 = self.__status_hitbox.x2 - padding_right
        y2 = self.__status_hitbox.y2 - padding_bottom

        self.__status_arc_hitbox.coords(x1, y1, x2, y2)
        if self.__status_arc_hitbox != self.__status_arc_current_hitbox:
            self.__status_arc_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(self.__status_arc_id, x1, y1, x2, y2)

        # status check
        x1 = self.__status_hitbox.x1 + padding_left + inner_padding_left
        y1 = self.__status_hitbox.y1 + padding_top + inner_padding_top
        x2 = self.__status_hitbox.x2 - padding_left - inner_padding_left
        y2 = self.__status_hitbox.y2 - padding_bottom - inner_padding_bottom

        self.__status_check_hitbox.coords(x1, y1, x2, y2)
        if self.__status_check_hitbox != self.__status_check_current_hitbox:
            self.__status_check_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(
                self.__status_check_id,
                x1 + self.__status_check_current_hitbox.width * 0.17,
                y1 + self.__status_check_current_hitbox.height * 0.55,
                x1 + self.__status_check_current_hitbox.width * 0.37,
                y1 + self.__status_check_current_hitbox.height * 0.74,
                x1 + self.__status_check_current_hitbox.width * 0.81,
                y1 + self.__status_check_current_hitbox.height * 0.29,
            )

        # status inner circle
        x1 = self.__status_hitbox.x1 + padding_left + inner_padding_left
        y1 = self.__status_hitbox.y1 + padding_top + inner_padding_top
        x2 = self.__status_hitbox.x2 - padding_right - inner_padding_right
        y2 = self.__status_hitbox.y2 - padding_bottom - inner_padding_bottom

        self.__status_inner_circle_hitbox.coords(x1, y1, x2, y2)
        if (
            self.__status_inner_circle_hitbox
            != self.__status_inner_circle_current_hitbox
        ):
            self.__status_inner_circle_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(self.__status_inner_circle_id, x1, y1, x2, y2)

    def __update_status_hitbox_coords(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_left
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_padding_top
        )

        self.__status_hitbox.x1 = self.__hitbox.x1 + padding_left
        self.__status_hitbox.y1 = self.__hitbox.y1 + padding_top

    def __update_status_hitbox_size(self):
        if self.__completion is None:
            self.__status_hitbox.width = 0
            self.__status_hitbox.height = 0
        else:
            config = xindmap.config.Config()
            Variables = xindmap.config.Variables

            padding_bottom = config.get(
                Variables.mind_map_viewer_mind_node_drawing_status_padding_bottom
            )
            padding_left = config.get(
                Variables.mind_map_viewer_mind_node_drawing_status_padding_left
            )
            padding_right = config.get(
                Variables.mind_map_viewer_mind_node_drawing_status_padding_right
            )
            padding_top = config.get(
                Variables.mind_map_viewer_mind_node_drawing_status_padding_top
            )

            height = config.get(
                Variables.mind_map_viewer_mind_node_drawing_status_height
            )
            width = config.get(Variables.mind_map_viewer_mind_node_drawing_status_width)

            height = padding_top + height + padding_bottom
            width = padding_left + width + padding_right

            self.__status_hitbox.width = width
            self.__status_hitbox.height = height

    @property
    def completion(self):
        return self.__completion

    @completion.setter
    def completion(self, completion):
        self.__completion = completion

        previous_status_hitbox_height = self.__status_hitbox.height
        previous_status_hitbox_width = self.__status_hitbox.width

        self.__update_status_hitbox_size()

        if (
            previous_status_hitbox_height != self.__status_hitbox.height
            or previous_status_hitbox_width != self.__status_hitbox.width
        ):
            self.__update_body_hitbox_size()
            self.__update_hitbox_size()
            self.__update_selector_hitbox_size()

        if completion is None:
            self.__canvas.itemconfigure(self.__status_arc_id, state=ctk.HIDDEN)
        else:
            self.__canvas.itemconfigure(
                self.__status_arc_id, extent=completion * 359, state=ctk.NORMAL
            )

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

        if status == xindmap.mind_map.MindNodeStatus.done:
            self.__canvas.itemconfigure(self.__status_check_id, state=ctk.NORMAL)
            self.__canvas.itemconfigure(
                self.__status_inner_circle_id,
                state=ctk.NORMAL,
                fill="orange",
                outline="orange",
            )
        elif status == xindmap.mind_map.MindNodeStatus.in_progress:
            self.__canvas.itemconfigure(self.__status_check_id, state=ctk.HIDDEN)
            self.__canvas.itemconfigure(
                self.__status_inner_circle_id,
                state=ctk.NORMAL,
                fill="orange",
                outline="orange",
            )
        elif status == xindmap.mind_map.MindNodeStatus.none:
            self.__canvas.itemconfigure(self.__status_check_id, state=ctk.HIDDEN)
            self.__canvas.itemconfigure(self.__status_inner_circle_id, state=ctk.HIDDEN)
        elif status == xindmap.mind_map.MindNodeStatus.to_do:
            self.__canvas.itemconfigure(self.__status_check_id, state=ctk.HIDDEN)
            self.__canvas.itemconfigure(
                self.__status_inner_circle_id,
                state=ctk.NORMAL,
                fill="",
                outline="orange",
            )

    # title ********************************************************************
    def __update_title_components_coords(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_bottom
        )
        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_left
        )
        padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_right
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_top
        )

        # title text
        x1 = self.__title_hitbox.x1 + padding_left
        y1 = self.__title_hitbox.y1 + padding_top
        x2 = self.__title_hitbox.x2 - padding_right
        y2 = self.__title_hitbox.y2 - padding_bottom

        self.__title_text_hitbox.coords(x1, y1, x2, y2)
        if self.__title_text_hitbox != self.__title_text_current_hitbox:
            self.__title_text_current_hitbox.coords(x1, y1, x2, y2)

            self.__canvas.coords(self.__title_text_id, x1, y1)

    def __update_title_hitbox_coords(self):
        self.__title_hitbox.x1 = self.__status_hitbox.x2
        self.__title_hitbox.y2 = self.__body_hitbox.y1

    def __update_title_hitbox_size(self):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        padding_bottom = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_bottom
        )
        padding_left = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_left
        )
        padding_right = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_right
        )
        padding_top = config.get(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_top
        )

        text_bbox = self.__canvas.bbox(self.__title_text_id)

        text_height = text_bbox[3] - text_bbox[1]
        text_width = text_bbox[2] - text_bbox[0]

        height = padding_top + text_height + padding_bottom
        width = padding_left + text_width + padding_right

        self.__title_hitbox.width = width
        self.__title_hitbox.height = height

    @property
    def title(self):
        return self.__canvas.itemcget(self.__title_text_id, "text")

    @title.setter
    def title(self, title):
        self.__canvas.itemconfigure(self.__title_text_id, text=title)

        previous_title_hitbox_height = self.__title_hitbox.height
        previous_title_hitbox_width = self.__title_hitbox.width

        self.__update_title_hitbox_size()

        if (
            previous_title_hitbox_height != self.__title_hitbox.height
            or previous_title_hitbox_width != self.__title_hitbox.width
        ):
            self.__update_body_hitbox_size()
            self.__update_hitbox_size()
            self.__update_selector_hitbox_size()

    # update *******************************************************************
    def update_size(self):
        self.__update_status_hitbox_size()
        self.__update_title_hitbox_size()
        self.__update_body_hitbox_size()
        self.__update_hitbox_size()
        self.__update_selector_hitbox_size()

    def update_components(self):
        self.__update_selector_hitbox_coords()

        # body before status because status is placed according to body
        # status before title because title placed according to status and body
        self.__update_body_hitbox_coords()
        self.__update_status_hitbox_coords()
        self.__update_title_hitbox_coords()

        # order does not matter because they are placed according to their
        # hitbox
        self.__update_body_components_coords()
        self.__update_selector_components_coords()
        self.__update_status_components_coords()
        self.__update_title_components_coords()
