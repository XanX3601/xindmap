import itertools
import kivy.properties as kproperties
import kivy.uix.widget as kwidget
import xindmap.logging as xlogging

class RootWidget(kwidget.Widget):
    """the root widget of the app

    Attributes:
        input_widget: the input widget
        mindmap_canvas_widget: the mindmap canvas widget
        output_widget: the output widget
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    input_widget = kproperties.ObjectProperty()
    mind_map_widget = kproperties.ObjectProperty()
    output_widget = kproperties.ObjectProperty()

    # dunder *******************************************************************
    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

        self.__id = next(RootWidget.__id_counter)
        print(self.__id)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this widget

        Returns:
            a string representation of this widget
        """
        if hasattr(self, '_RootWidget__id'):
            return 'root widget {}'.format(self.__id)

        return super().__str__()
