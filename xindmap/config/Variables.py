import enum

import customtkinter as ctk

from .Variable import Variable
from .VariableTypes import VariableTypes


class Variables(enum.Enum):
    """Statically declared list of all variables that can be set through the
    [config][xindmap.config.Config.Config].
    """

    command_controller_mapping_delay_s = Variable(VariableTypes.float, 1)
    """The delay (in seconds) used by
    [command controller][xindmap.controller.CommandController.CommandController]
    when having to decide wether accepting a mapping or wait for the user to
    finish the mapping.
    """
    input_stack_input_pushed_event_priority = Variable(VariableTypes.int, 20)
    """The priority to which [event][xindmap.event.Event.Event]
    [input pushed][xindmap.input.InputStack.InputStack--input-pushed]
    is dispatched.
    """
    input_stack_viewer_background_color = Variable(VariableTypes.color, "#f00")
    input_stack_viewer_height_px = Variable(VariableTypes.float, 20)
    """The height (in pixel) of 
    [input stack viewer][xindmap.widget.InputStackViewer.InputStackViewer].
    """
    mind_map_viewer_background_color = Variable(VariableTypes.color, "#000")
    mind_map_viewer_edge_drawing_colors = Variable(
        VariableTypes.color_list, ["#f00", "#0f0", "#00f"]
    )
    mind_map_viewer_edge_drawing_inner_point_padding_width_percentage = Variable(
        VariableTypes.float, 0.2
    )
    mind_map_viewer_edge_drawing_line_width = Variable(VariableTypes.float, 3)
    mind_map_viewer_mind_node_drawing_body_colors = Variable(
        VariableTypes.color_list, ["#f00", "#0f0", "#00f"]
    )
    mind_map_viewer_mind_node_drawing_body_height = Variable(VariableTypes.int, 2)
    mind_map_viewer_mind_node_drawing_body_min_width = Variable(VariableTypes.int, 30)
    mind_map_viewer_mind_node_drawing_description_background_color = Variable(
        VariableTypes.color, "#f00"
    )
    mind_map_viewer_mind_node_drawing_description_margin_top = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_description_max_width = Variable(
        VariableTypes.int, 100
    )
    mind_map_viewer_mind_node_drawing_description_padding_bottom = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_description_padding_left = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_description_padding_right = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_description_padding_top = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_margin_bottom = Variable(VariableTypes.int, 10)
    mind_map_viewer_mind_node_drawing_margin_right = Variable(VariableTypes.int, 50)
    mind_map_viewer_mind_node_drawing_padding_bottom = Variable(VariableTypes.int, 5)
    mind_map_viewer_mind_node_drawing_padding_left = Variable(VariableTypes.int, 5)
    mind_map_viewer_mind_node_drawing_padding_right = Variable(VariableTypes.int, 5)
    mind_map_viewer_mind_node_drawing_padding_top = Variable(VariableTypes.int, 5)
    mind_map_viewer_mind_node_drawing_selector_color = Variable(
        VariableTypes.color, "#fff"
    )
    mind_map_viewer_mind_node_drawing_selector_padding_bottom = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_selector_padding_left = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_selector_padding_right = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_selector_padding_top = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_selector_radius = Variable(VariableTypes.int, 10)
    mind_map_viewer_mind_node_drawing_selector_width = Variable(VariableTypes.int, 1)
    mind_map_viewer_mind_node_drawing_status_arc_colors = Variable(
        VariableTypes.color_list, ["#f00", "#0f0", "#00f"]
    )
    mind_map_viewer_mind_node_drawing_status_arc_width = Variable(VariableTypes.int, 3)
    mind_map_viewer_mind_node_drawing_status_check_colors = Variable(
        VariableTypes.color_list, ["#f00", "#0f0", "#00f"]
    )
    mind_map_viewer_mind_node_drawing_status_check_width = Variable(
        VariableTypes.int, 1
    )
    mind_map_viewer_mind_node_drawing_status_height = Variable(VariableTypes.int, 20)
    mind_map_viewer_mind_node_drawing_status_inner_circle_colors = Variable(
        VariableTypes.color_list, ["#f00", "#0f0", "#00f"]
    )
    mind_map_viewer_mind_node_drawing_status_inner_circle_padding_bottom = Variable(
        VariableTypes.int, 3
    )
    mind_map_viewer_mind_node_drawing_status_inner_circle_padding_left = Variable(
        VariableTypes.int, 3
    )
    mind_map_viewer_mind_node_drawing_status_inner_circle_padding_right = Variable(
        VariableTypes.int, 3
    )
    mind_map_viewer_mind_node_drawing_status_inner_circle_padding_top = Variable(
        VariableTypes.int, 3
    )
    mind_map_viewer_mind_node_drawing_status_padding_bottom = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_status_padding_left = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_status_padding_right = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_status_padding_top = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_status_width = Variable(VariableTypes.int, 20)
    mind_map_viewer_mind_node_drawing_title_padding_bottom = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_title_padding_left = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_title_padding_right = Variable(
        VariableTypes.int, 5
    )
    mind_map_viewer_mind_node_drawing_title_color = Variable(
        VariableTypes.color, "#fff"
    )
    mind_map_viewer_mind_node_drawing_title_padding_top = Variable(VariableTypes.int, 5)
    mind_map_viewer_mind_node_drawing_title_font = Variable(
        VariableTypes.font, "TkDefaultFont"
    )
    state_viewer_background_color = Variable(VariableTypes.color, "#f00")
    state_viewer_height_px = Variable(VariableTypes.int, 20)
    xindmap_app_main_window_height_px = Variable(VariableTypes.int, 600)
    xindmap_app_main_window_width_px = Variable(VariableTypes.int, 800)

    # property *****************************************************************
    @property
    def type(self):
        """Returns the type of the underlying
        [variable][xindmap.config.Variable.Variable].
        """
        return self.value.type

    @property
    def default(self):
        """Returns the default value of the underlying
        [variable][xindmap.config.Variable.Variable].
        """
        return self.value.default
