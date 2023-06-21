import xindmap.config
import xindmap.plugin


class ThemePlugin(xindmap.plugin.Plugin):
    # command ******************************************************************
    def commands(self):
        return [("theme", self.command_theme)]

    def command_theme(self, theme_name, api):
        from .built_in_themes import theme_name_to_theme

        if theme_name not in theme_name_to_theme:
            raise ValueError(f"unknown theme {theme_name}")

        theme = theme_name_to_theme[theme_name]

        self.__apply_theme(theme)

    # constructor **************************************************************
    def __init__(self):
        super().__init__()

    # theme ********************************************************************
    def __apply_theme(self, theme):
        config = xindmap.config.Config()
        Variables = xindmap.config.Variables

        # arc
        #   colors
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_arc_colors,
            theme.arc_colors,
        )
        #   dimensions
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_width,
            theme.arc_dimensions[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_height,
            theme.arc_dimensions[1],
        )
        #   paddings
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_top,
            theme.arc_paddings[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_bottom,
            theme.arc_paddings[1],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_left,
            theme.arc_paddings[2],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_padding_right,
            theme.arc_paddings[3],
        )
        #   width
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_arc_width,
            theme.arc_width,
        )

        # background
        #   color
        config.set(Variables.mind_map_viewer_background_color, theme.background_color)

        # bar
        #   height
        config.set(Variables.input_stack_viewer_height_px, theme.bar_height)
        config.set(Variables.state_viewer_height_px, theme.bar_height)
        #   input background color
        config.set(Variables.input_stack_viewer_background_color, theme.bar_input_background_color)
        #   state background color
        config.set(Variables.state_viewer_background_color, theme.bar_state_background_color)

        # check
        #   colors
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_check_colors,
            theme.check_colors,
        )
        #   width
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_check_width,
            theme.check_width,
        )

        # circle
        #   colors
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_colors,
            theme.circle_colors,
        )
        #   paddings
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_top,
            theme.circle_paddings[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_bottom,
            theme.circle_paddings[1],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_left,
            theme.circle_paddings[2],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_right,
            theme.circle_paddings[3],
        )

        # colors

        # cursor
        #   color
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_color,
            theme.cursor_color,
        )
        #   paddings
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_top,
            theme.cursor_paddings[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_bottom,
            theme.cursor_paddings[1],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_left,
            theme.cursor_paddings[2],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_padding_right,
            theme.cursor_paddings[3],
        )
        #   radius
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_radius,
            theme.cursor_radius,
        )
        #   width
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_selector_width,
            theme.cursor_width,
        )

        # edge
        #   colors
        config.set(Variables.mind_map_viewer_edge_drawing_colors, theme.edge_colors)

        # font

        # foreground
        #   color

        # node
        #   colors
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_body_colors, theme.node_colors
        )
        #   margins
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_margin_right,
            theme.node_margins[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_margin_bottom,
            theme.node_margins[1],
        )
        #   paddings
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_padding_top,
            theme.node_paddings[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_padding_bottom,
            theme.node_paddings[1],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_padding_left,
            theme.node_paddings[2],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_padding_right,
            theme.node_paddings[3],
        )

        # title
        #   color
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_color, theme.title_color
        )
        #   font
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_font, theme.title_font
        )
        # paddings
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_top,
            theme.title_paddings[0],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_bottom,
            theme.title_paddings[1],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_left,
            theme.title_paddings[2],
        )
        config.set(
            Variables.mind_map_viewer_mind_node_drawing_title_padding_right,
            theme.title_paddings[3],
        )
