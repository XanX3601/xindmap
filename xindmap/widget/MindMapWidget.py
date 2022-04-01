import kivy.logger as klogger
import kivy.properties as kproperties
import kivy.uix.widget as kwidget

from .MindNodeWidget import MindNodeWidget

class MindMapWidget(kwidget.Widget):
    """widget used to display a mind map
    """
    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)
        

    def init(self, mind_map):
        """initializes this widget

        Args:
            mind_map: the mind map
        """
        self._mind_map = mind_map
