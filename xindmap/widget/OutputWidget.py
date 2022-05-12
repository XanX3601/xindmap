import itertools
import kivy.uix.widget as kwidget
import kivy.properties as kproperties
import xindmap.logging as xlogging

class OutputWidget(kwidget.Widget):
    """the widget used to display output messages

    Attributes:
        output_label: label used to display text
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    output_label = kproperties.ObjectProperty()

    # dunder *******************************************************************
    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

        self.__id = next(OutputWidget.__id_counter)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this widget

        Returns:
            a string representation of this widget
        """
        return 'output widget {}'.format(self.__id)

    # output *******************************************************************
    def info(self, text):
        """outputs an info message
        """
        self.output_label.text = text

    def error(self, text):
        """outputs an error message
        """
        self.output_label.text = '[color=#FF0000]{}[/color]'.format(text)

