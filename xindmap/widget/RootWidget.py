import kivy.properties as kproperties
import kivy.uix.widget as kwidget

class RootWidget(kwidget.Widget):
    """the root widget of the app

    Attributes:
        input_widget: the input widget
        mindmap_canvas_widget: the mindmap canvas widget
    """
    input_widget = kproperties.ObjectProperty()
    mind_map_widget = kproperties.ObjectProperty()

    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)
