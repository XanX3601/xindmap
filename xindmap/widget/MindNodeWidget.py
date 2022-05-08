import kivy.properties as kproperties
import kivy.uix.widget as kwidget

class MindNodeWidget(kwidget.Widget):
    """widget used to display a mind node

    Attributes:
        full_height: the height of this widget taking into account the full 
            height of its children
        label: a label used to display the text of the mind node
        mind_node: the mind node displayed
        mind_node_widget_children: the list of mind node widget that display the
            children of the mind node
        mind_node_widget_parent: the mind node widget that display the parent of
            the mind node
    """
    full_height = kproperties.NumericProperty()
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

    def compute_full_height(self):
        """computes the full height of this widget
        """
        self.full_height = sum(
            [child.full_height for child in self.mind_node_widget_children]
        ) + 40 * (len(self.mind_node_widget_children) - 1)

    def compute_mind_node_widget_children_center_y(self):
        """computes the center y of all the children of this widget
        """
        current_point = self.center_y - self.full_height / 2
        for child in self.mind_node_widget_children:
            current_point += child.full_height / 2
            child.center_y = current_point
            current_point += child.full_height / 2
            current_point += 40

    def compute_width(self):
        """computes the width of this widget
        """
        self.width = self.label.width
    
    def compute_x(self):
        """computes the x of this widget
        """
        if self.mind_node_widget_parent is not None:
            self.x = self.mind_node_widget_parent.x\
                    + self.mind_node_widget_parent.width\
                    + 20

    def on_full_height(self, _, __):
        """callback raised upon changing the full height of this widget

        Args:
            _: ignored
                equal self
            __: ignored
                equal full_height
        """
        self.compute_mind_node_widget_children_center_y()

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

    def on_mind_node_widget_child_full_height(
        self,
        mind_node_widget_child,
        full_height
    ):
        """callback raised upon changing the full height of a child of this
        widget
        
        Args:
            mind_node_widget_child: the child
            full_height: the new full height of the child
        """
        self.compute_full_height()

    def on_mind_node_widget_children(self, _, __):
        """callback raised upon modifying the list of child of this widget

        Args:
            _: ignored
                equal to self
            __: ignored
                equal to mind_node_widget_children
        """
        self.compute_full_height()

        for child in self.mind_node_widget_children:
            child.bind(full_height=self.on_mind_node_widget_child_full_height)

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

