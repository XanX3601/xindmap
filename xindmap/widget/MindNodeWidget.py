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

        self.label.bind(width=self.on_label_width)

        self.mind_node = mind_node
        self.mind_node.bind(text=self.on_mind_node_text)

        self.mind_node_widget_parent = mind_node_widget_parent
        if self.mind_node_widget_parent is not None:
            self.mind_node_widget_parent.bind(
                x=self.on_mind_node_widget_parent_x
            )
            self.mind_node_widget_parent.bind(
                width=self.on_mind_node_widget_parent_width
            )

        self.compute_x()
        self.compute_width()

    def compute_width(self):
        """computes the width of this widget
        """
        self.width = self.label.width
    
    def compute_x(self):
        if self.mind_node_widget_parent is not None:
            self.x = self.mind_node_widget_parent.x\
                    + self.mind_node_widget_parent.width\
                    + 20

    def on_label_width(self, label, width):
        """callback raised upon changing the width of the label

        Args:
            label: the label
            width: the new width of the label
        """
        self.compute_width()

    def on_mind_node_text(self, mind_node, text):
        """callback raised upon changing the text of the mind node

        Args:
            mind_node: the mind node
            text: the new text of the mind node
        """
        self.label.text = text

    def on_mind_node_widget_parent_width(self, mind_node_widget_parent, width):
        """callback raised upon changing the width of the mind node widget
        parent

        Args:
            mind_node_widget_parent: the mind node widget parent
            width: the new value of width
        """
        self.compute_x()

    def on_mind_node_widget_parent_x(self, mind_node_widget_parent, x):
        """callback raised upon changing the x of the mind node widget parent

        Args:
            mind_node_widget_parent: the mind node widget parent
            x: the new value of x
        """
        self.compute_x()

