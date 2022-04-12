import kivy.logger as klogger
import kivy.properties as kproperties
import kivy.uix.widget as kwidget

from .MindNodeWidget import MindNodeWidget

class MindMapWidget(kwidget.Widget):
    """widget used to display a mind map

    Attributes:
        current_mind_node_widget: the mind node widget that display the current
            node of the mind map
        mind_node_to_mind_node_widget: a dictionnary linking a mind node to the
            mind node widget that is used to display it
        scatter: the scatter widget in which are displayed the mind node widgets
    """
    scatter = kproperties.ObjectProperty()

    def __init__(self, **kwargs):
        """instantiates this widget

        Args:
            kwargs: dictionnary of args
        """
        super().__init__(**kwargs)

        self.current_mind_node_widget = None
        self.mind_node_to_mind_node_widget = {}

    def add_mind_node_widget(self, mind_node):
        """adds a mind node widget that displays a given mind node

        Args:
            mind_node: the mind node to display using a new mind node widget
        """
        # retrive the mind node widget that displays the mind node parent
        mind_node_widget_parent = self.mind_node_to_mind_node_widget.get(
            mind_node.parent, None
        )

        # create the new mind node widget
        mind_node_widget = MindNodeWidget(mind_node, mind_node_widget_parent)

        # add the new mind node widget to its parent's children
        if mind_node_widget_parent is not None:
            mind_node_widget_parent.mind_node_widget_children.append(
                mind_node_widget
            )
        
        # store the new mind node widget
        self.mind_node_to_mind_node_widget[mind_node] = mind_node_widget

        # display the new mind node widget
        self.scatter.add_widget(mind_node_widget)

    def center_on_current_mind_node_widget(self):
        """centers this widget on the current mind node widget
        """
        if self.current_mind_node_widget is not None:
            futur_center_x, futur_center_y = self.scatter.to_parent(
                *self.current_mind_node_widget.center
            )

            delta_x = self.center_x - futur_center_x
            delta_y = self.center_y - futur_center_y

            self.scatter.x += delta_x
            self.scatter.y += delta_y
        
    def init(self, mind_map):
        """initializes this widget

        Args:
            mind_map: the mind map
        """
        self._mind_map = mind_map
        self._mind_map.bind(current_node=self.on_mind_map_current_node)

    def on_mind_map_current_node(self, mind_map, current_node):
        """callback raised upon changing the current node of the mind map

        Args:
            mind_map: the mind map
            current_node: the new current node
        """
        if current_node not in self.mind_node_to_mind_node_widget:
            self.add_mind_node_widget(current_node)

        self.current_mind_node_widget = self.mind_node_to_mind_node_widget[current_node]


