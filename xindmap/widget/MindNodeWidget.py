import kivy.properties as kproperties
import kivy.uix.widget as kwidget

class MindNodeWidget(kwidget.Widget):
    """widget used to display a mind node
    """
    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)
