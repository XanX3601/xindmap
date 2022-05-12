import itertools
import kivy.uix.widget as kwidget
import kivy.properties as kproperties
import xindmap.logging as xlogging

class InputWidget(kwidget.Widget):
    """the widget used to display the user's inputs

    Attributes:
        input_label: input label
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    input_label = kproperties.ObjectProperty()

    # dunder *******************************************************************
    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

        self.__id = next(InputWidget.__id_counter)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this widget

        Returns:
            a string representation of this widget
        """
        return 'input widget {}'.format(self.__id)

    # text *********************************************************************
    @property
    def text(self):
        """gets the displayed text

        Returns:
            the displayed text
        """
        return self.input_label.text

    @text.setter
    def text(self, text):
        """sets the displayed text

        Args:
            text: the text to display
        """
        self.input_label.text = text
