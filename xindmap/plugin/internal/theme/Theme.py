class Theme:
    # constructor **************************************************************
    def __init__(
        self,
        arc_colors=None,
        arc_dimensions=(20, 20),
        arc_paddings=(5, 5, 5, 5),
        arc_width=3,
        background_color="#000",
        bar_height=20,
        check_colors=None,
        check_width=1,
        circle_colors=None,
        circle_paddings=(3, 3, 3, 3),
        colors=["#fff"],
        cursor_color="#fff",
        cursor_paddings=(5, 5, 5, 5),
        cursor_radius=10,
        cursor_width=1,
        edge_colors=None,
        font="TkDefaultFont",
        foreground_color="#fff",
        node_colors=None,
        node_dimensions=(30, 2),
        node_margins=(50, 10),
        node_paddings=(5, 5, 5, 5),
        title_color=None,
        title_font=None,
        title_paddings=(5, 5, 5, 5)
    ):
        self.arc_colors = arc_colors if arc_colors is not None else colors
        self.arc_dimensions = arc_dimensions
        self.arc_paddings = arc_paddings
        self.arc_width = arc_width
        self.background_color = background_color
        self.bar_height = bar_height
        self.check_colors = check_colors if check_colors is not None else colors
        self.check_width = check_width
        self.circle_colors = circle_colors if circle_colors is not None else colors
        self.circle_paddings = circle_paddings
        self.colors = colors
        self.cursor_color = cursor_color
        self.cursor_paddings = cursor_paddings
        self.cursor_radius = cursor_radius
        self.cursor_width = cursor_width
        self.edge_colors = edge_colors if edge_colors is not None else colors
        self.font = font
        self.foreground_color = foreground_color
        self.node_colors = node_colors if node_colors is not None else colors
        self.node_dimensions = node_dimensions
        self.node_margins = node_margins
        self.node_paddings = node_paddings
        self.title_color = title_color if title_color is not None else foreground_color
        self.title_font = title_font if title_font is not None else font
        self.title_paddings = title_paddings

