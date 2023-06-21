from .Theme import Theme

theme_name_to_theme = {
    "dracula": Theme(
        arc_dimensions=(15, 15),
        arc_width=3,
        background_color="#282a36",
        bar_height=10,
        check_colors=["#f8f8f2"],
        colors=[
            "#8be9fd",
            "#50fa7b",
            "#ffc86c",
            "#ff79c6",
            "#bd93f9",
            "#ff5555",
            "#f1fa8c",
        ],
        cursor_color="#44475a",
        cursor_width=2,
        foreground_color="#f8f8f2",
        node_dimensions=(20, 3),
        node_margins=(30, 5),
        title_paddings=(0, 10, 10, 0)
    )
}
