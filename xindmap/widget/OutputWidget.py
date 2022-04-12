import kivy.uix.widget as kwidget
import kivy.properties as kproperties

class OutputWidget(kwidget.Widget):
    """the widget used to display output messages

    Attributes:
        output_label: label used to display text
    """
    output_label = kproperties.ObjectProperty()

    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

    def info(self, text):
        """outputs an info message
        """
        self.output_label.text = text

    def error(self, text):
        """outputs an error message
        """
        self.output_label.text = '[color=#FF0000]{}[/color]'.format(text)

