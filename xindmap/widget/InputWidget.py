import kivy.uix.widget as kwidget
import kivy.properties as kproperties

class InputWidget(kwidget.Widget):
    """the widget used to display the user's inputs

    Attributes:
        input_label: input label
    """
    input_label = kproperties.ObjectProperty()

    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

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
