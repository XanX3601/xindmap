import kivy.properties as kproperties
import kivy.uix.widget as kwidget

class MindNodeWidget(kwidget.Widget):
    """widget used to display a mind node

    Attributes:
        label: a label used to display the text of the mind node
        mind_node: the mind node displayed
        mind_node_widget_children: the list of mind node widget that display the
            children of the mind node
        mind_node_widget_parent: the mind node widget that display the parent of
            the mind node
    """
    label = kproperties.ObjectProperty()
    mind_node_widget_children = kproperties.ListProperty()
    mind_node_widget_parent = kproperties.ObjectProperty()

    def __init__(self, mind_node, mind_node_widget_parent, **kwargs):
        """instantiates this widget

        Args:
            mind_node: the mind node to display
            mind_node_widget_parent: the mind node widget that display the 
                parent of the mind node
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

        self.mind_node = mind_node
        self.mind_node.bind(text=self.on_mind_node_text)

    def on_mind_node_text(self, mind_node, text):
        """callback raised upon changing the text of the mind node

        Args:
            mind_node: the mind node
            text: the new text of the mind node
        """
        self.label.text = text
