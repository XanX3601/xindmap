import xindmap.editable
import xindmap.event

from .MindMapEvent import MindMapEvent
from .MindMapError import MindMapError
from .MindNode import MindNode


class MindMap(xindmap.event.EventSource, xindmap.editable.Editable):
    # constructor **************************************************************
    def __init__(self):
        xindmap.event.EventSource.__init__(self, MindMapEvent)
        xindmap.editable.Editable.__init__(self)

        self.__node_id_to_node = {}
        self.__root = None
        self.__current_node_id = None

    # current ******************************************************************
    @property
    def current_node_id(self):
        return self.__current_node_id

    # edit *********************************************************************
    def add_text(self, text):
        if self.__current_node_id is None:
            return

        text = text.replace("\n", "")

        node = self.__node_id_to_node[self.__current_node_id]
        node.title += text

        event = xindmap.event.Event(MindMapEvent.node_title_set, node_id=node.id, title=node.title)
        self._dispatch_event(event)

    def remove_last_char(self):
        if self.__current_node_id is None:
            return

        node = self.__node_id_to_node[self.__current_node_id]
        node.title = node.title[:-1]

        event = xindmap.event.Event(MindMapEvent.node_title_set, node_id=node.id, title=node.title)
        self._dispatch_event(event)


    # node *********************************************************************
    def node_add(self, parent_id=None):
        if parent_id is None:
            parent_id = self.__current_node_id

        if self.__root is None:
            node = MindNode(None)
            self.__root = node
        elif parent_id in self.__node_id_to_node:
            node = MindNode(self.__node_id_to_node[parent_id])
            parent = self.__node_id_to_node[parent_id]
            parent.add_child(node)
        else:
            raise MindMapError(f"unknown node id {parent_id}")

        self.__node_id_to_node[node.id] = node

        event = xindmap.event.Event(MindMapEvent.node_added, node_id=node.id)
        self._dispatch_event(event)

        return node.id

    def node_child_ids(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.child_ids()

    def node_id_exists(self, node_id):
        return node_id in self.__node_id_to_node

    def node_parent_id(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.parent.id if node.parent is not None else None

    def node_select(self, node_id):
        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")
        previous_node_id = self.__current_node_id
        self.__current_node_id = node_id

        event = xindmap.event.Event(
            MindMapEvent.node_selected,
            previous_node_id=previous_node_id,
            node_id=node_id,
        )
        self._dispatch_event(event)

    def node_title(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.title

    # root *********************************************************************
    @property
    def root_node_id(self):
        return self.__root.id if self.__root is not None else None

    # size *********************************************************************
    def __len__(self):
        return len(self.__node_id_to_node)
