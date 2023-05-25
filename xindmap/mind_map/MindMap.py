import collections

import xindmap.editable
import xindmap.event

from .MindMapError import MindMapError
from .MindMapEvent import MindMapEvent
from .MindNode import MindNode
from .MindNodeStatus import MindNodeStatus


class MindMap(xindmap.event.EventSource, xindmap.editable.Editable):
    # clear ********************************************************************
    def clear(self):
        self.__node_id_to_node = {}
        self.__root = None
        self.__current_node_id = None

        event = xindmap.event.Event(MindMapEvent.cleared)
        self._dispatch_event(event)

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

    # dict *********************************************************************
    def populate_from_dict(self, node_dict, parent_id=None):
        def from_dict_recursivity(node_dict, parent_id=None):
            node_id = self.node_add(parent_id)

            if "text" in node_dict:
                self.node_set_text(node_dict["text"], node_id)

            if "status" in node_dict:
                self.node_set_status(MindNodeStatus[node_dict["status"]], node_id)

            if "childs" in node_dict:
                for child_dict in node_dict["childs"]:
                    from_dict_recursivity(child_dict, node_id)

        if parent_id is None:
            parent_id = self.__current_node_id

        if parent_id is None and self.__root is not None:
            raise MindMapError(
                f"can not populate from dict with no parent id if mind map is not empty"
            )

        from_dict_recursivity(node_dict, parent_id)

    def to_dict(self):
        def to_dict_recursivity(node_id):
            node = self.__node_id_to_node[node_id]

            node_dict = {"text": node.text, "status": node.status.name, "childs": []}

            for child_id in node.child_ids():
                node_dict["childs"].append(to_dict_recursivity(child_id))

            return node_dict

        return to_dict_recursivity(self.root_node_id)

    # edit *********************************************************************
    def add_text(self, text):
        if self.__current_node_id is None:
            return

        node = self.__node_id_to_node[self.__current_node_id]

        node.add_text(text)

        event = xindmap.event.Event(
            MindMapEvent.node_text_set, node_id=node.id, text=node.text
        )
        self._dispatch_event(event)

    def remove_last_char(self):
        if self.__current_node_id is None:
            return

        node = self.__node_id_to_node[self.__current_node_id]
        node.text = node.text[:-1]

        event = xindmap.event.Event(
            MindMapEvent.node_text_set, node_id=node.id, text=node.text
        )
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

    def node_delete(self, node_id=None):
        def node_delete_recursivity(node_id):
            node = self.__node_id_to_node[node_id]

            for child_id in node.child_ids():
                node_delete_recursivity(child_id)

            if node.parent is not None:
                node.parent.remove_child(node)

            del self.__node_id_to_node[node.id]

            if node == self.__root:
                self.__root = None
            if node_id == self.__current_node_id:
                self.node_unselect()

            event = xindmap.event.Event(MindMapEvent.node_deleted, node_id=node_id)
            self._dispatch_event(event)

        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node if {node_id}")

        node_delete_recursivity(node_id)

    def node_description(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]
        
        return node.description

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

    def node_set_status(self, status, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]
        node.status = status

        event = xindmap.event.Event(
            MindMapEvent.node_status_set, node_id=node_id, status=status
        )
        self._dispatch_event(event)

    def node_set_text(self, text, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]
        node.text = text

        event = xindmap.event.Event(
            MindMapEvent.node_text_set, node_id=node_id, text=text
        )
        self._dispatch_event(event)

    def node_status(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.status

    def node_text(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.text

    def node_title(self, node_id=None):
        if node_id is None:
            node_id = self.__current_node_id

        if node_id not in self.__node_id_to_node:
            raise MindMapError(f"unknown node id {node_id}")

        node = self.__node_id_to_node[node_id]

        return node.title

    def node_unselect(self):
        previous_node_id = self.__current_node_id
        self.__current_node_id = None

        event = xindmap.event.Event(
            MindMapEvent.node_unselected, previous_node_id=previous_node_id
        )
        self._dispatch_event(event)

    # root *********************************************************************
    @property
    def root_node_id(self):
        return self.__root.id if self.__root is not None else None

    # size *********************************************************************
    def __len__(self):
        return len(self.__node_id_to_node)
