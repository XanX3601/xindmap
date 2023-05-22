import customtkinter as ctk
import logging
import queue
import sortedcontainers
import xindmap.config

from .EdgeDrawing import EdgeDrawing
from .MindMapViewerError import MindMapViewerError
from .MindNodeDrawing import MindNodeDrawing
from .RootNodeDrawing import RootNodeDrawing


class MindMapViewer(ctk.CTkFrame, xindmap.config.Configurable):
    # callback *****************************************************************
    def on_mind_map_cleared(self, mind_map, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_cleared(event={event})"
        )

        self.__node_id_to_edge_drawings = {}
        self.__node_id_to_child_ids = {}
        self.__node_id_to_drawing = {}
        self.__node_id_to_parent_id = {}
        self.__root_id = None

        self.__canvas.delete("all")

    def on_mind_map_node_added(self, mind_map, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_added(event={event})"
        )

        node_id = event.node_id
        parent_id = mind_map.node_parent_id(node_id)

        if self.__root_id is None:
            self.__root_id = node_id

        if node_id == self.__root_id:
            node_drawing = RootNodeDrawing(self.__canvas)
        else:
            node_drawing = MindNodeDrawing(self.__canvas)

        self.__node_id_to_child_ids[node_id] = sortedcontainers.SortedList()
        self.__node_id_to_drawing[node_id] = node_drawing
        self.__node_id_to_edge_drawings[node_id] = {}
        self.__node_id_to_parent_id[node_id] = parent_id

        if parent_id is not None:
            self.__node_id_to_child_ids[parent_id].add(node_id)

            edge_drawing = EdgeDrawing(self.__canvas)
            self.__node_id_to_edge_drawings[parent_id][node_id] = edge_drawing

        self.__node_drawing_compute_height_and_y(node_id)
        self.__node_drawing_compute_width_and_x(node_id)

    def on_mind_map_node_deleted(self, mind_map, event):
        def on_mind_map_node_deleted_recursivity(node_id):
            child_ids = list(self.__node_id_to_child_ids[node_id])
            for child_id in child_ids:
                on_mind_map_node_deleted_recursivity(child_id)
            del self.__node_id_to_child_ids[node_id]

            for edge_drawing in self.__node_id_to_edge_drawings[node_id].values():
                edge_drawing.clear()
            del self.__node_id_to_edge_drawings[node_id]

            self.__node_id_to_drawing[node_id].clear()
            del self.__node_id_to_drawing[node_id]

            parent_id = self.__node_id_to_parent_id.get(node_id, None)
            if parent_id is not None:
                self.__node_id_to_child_ids[parent_id].remove(node_id)
                self.__node_id_to_edge_drawings[parent_id][node_id].clear()
                del self.__node_id_to_edge_drawings[parent_id][node_id]

            if node_id == self.__root_id:
                self.__root_id = None

        logging.debug(f"mind map viewer {id(self)}: on_mind_map_node_deleted(event={event})")

        node_id = event.node_id
        parent_id = self.__node_id_to_parent_id.get(node_id, None)

        on_mind_map_node_deleted_recursivity(node_id)

        if parent_id is not None:
            self.__node_drawing_compute_height_and_y(parent_id)
            self.__node_drawing_compute_width_and_x(parent_id)

    def on_mind_map_node_selected(self, mind_map, event):
        logging.debug(f"mind map viewer {id(self)}: on_mind_map_node_selected(event={event})")

        previous_node_id = event.previous_node_id
        node_id = event.node_id

        if previous_node_id in self.__node_id_to_drawing:
            node_drawing = self.__node_id_to_drawing[previous_node_id]
            node_drawing.is_selected = False

        if node_id in self.__node_id_to_drawing:
            node_drawing = self.__node_id_to_drawing[node_id]
            node_drawing.is_selected = True

    def on_mind_map_node_title_set(self, mind_map, event):
        logging.debug(f"mind map viewer {id(self)}: on_mind_map_node_title_set(event={event})")

        node_id = event.node_id
        title = event.title

        if node_id in self.__node_id_to_drawing:
            node_drawing = self.__node_id_to_drawing[node_id]
            node_drawing.title = title

            self.__node_drawing_compute_width_and_x(node_id)

    # config callback **********************************************************
    def on_config_variable_mind_map_viewer_node_height_set(self, value):
        if self.__root_id is not None:
            self.__node_drawing_compute_height_and_y(self.__root_id)

    def on_config_variable_mind_map_viewer_node_margin_x_set(self, value):
        if self.__root_id is not None:
            self.__node_drawing_compute_width_and_x(self.__root_id)

    def on_config_variable_mind_map_viewer_node_margin_y_set(self, value):
        if self.__root_id is not None:
            self.__node_drawing_compute_height_and_y(self.__root_id)

    def on_config_variable_mind_map_viewer_node_padding_y_set(self, value):
        if self.__root_id is not None:
            self.__node_drawing_compute_height_and_y(self.__root_id)

    # constructor **************************************************************
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
        xindmap.config.Configurable.__init__(
            self,
            (
                xindmap.config.Variables.mind_map_viewer_node_height,
                xindmap.config.Variables.mind_map_viewer_node_margin_x,
                xindmap.config.Variables.mind_map_viewer_node_margin_y,
                xindmap.config.Variables.mind_map_viewer_node_padding_y,
            ),
        )

        self.__node_id_to_edge_drawings = {}
        self.__node_id_to_child_ids = {}
        self.__node_id_to_drawing = {}
        self.__node_id_to_parent_id = {}
        self.__root_id = None

        self.__canvas = ctk.CTkCanvas()

        self.__canvas.pack(fill=ctk.BOTH, expand=True)

    # edge drawing *************************************************************
    def __edge_drawing_compute_from_and_to(self, node_id):
        node_drawing = self.__node_id_to_drawing[node_id]
        for child_id in self.__node_id_to_child_ids[node_id]:
            child_drawing = self.__node_id_to_drawing[child_id]
            edge_drawing = self.__node_id_to_edge_drawings[node_id][child_id]

            from_x = node_drawing.x + node_drawing.width
            from_y = node_drawing.center_y
            to_x = child_drawing.x
            to_y = child_drawing.center_y

            edge_drawing.set_coords(from_x, from_y, to_x, to_y)

    # node drawing *************************************************************
    def __node_drawing_compute_height_and_y(self, node_id):
        priority_queue = queue.PriorityQueue()
        priority_queue_items = set()
        node_ids_met = set()

        first_item = (0, node_id)
        priority_queue.put(first_item)
        priority_queue_items.add(first_item)

        config = xindmap.config.Config()

        while not priority_queue.empty():
            current_item = priority_queue.get()
            priority_queue_items.remove(current_item)

            priority, node_id = current_item

            node_child_ids = self.__node_id_to_child_ids[node_id]
            node_drawing = self.__node_id_to_drawing[node_id]
            node_parent_id = self.__node_id_to_parent_id[node_id]

            if not node_child_ids:
                height = config.get(
                    xindmap.config.Variables.mind_map_viewer_node_height
                ) + config.get(xindmap.config.Variables.mind_map_viewer_node_padding_y)

                node_drawing.height = height
                
                if node_parent_id is not None:
                    item = (priority + 1, node_parent_id)
                    if item not in priority_queue_items:
                        priority_queue.put(item)
                        priority_queue_items.add(item)
            elif priority <= 0 and node_id not in node_ids_met:
                for child_id in node_child_ids:
                    item = (priority - 1, child_id)
                    if item not in priority_queue_items:
                        priority_queue_items.add(item)
                        priority_queue.put(item)
                node_ids_met.add(node_id)
            else:
                height = sum(
                    self.__node_id_to_drawing[child_id].height
                    for child_id in node_child_ids
                )
                height += config.get(xindmap.config.Variables.mind_map_viewer_node_margin_y) * (len(node_child_ids) - 1)

                node_drawing.height = height

                if node_parent_id is not None:
                    item = (priority + 1, node_parent_id)
                    if item not in priority_queue_items:
                        priority_queue_items.add(item)
                        priority_queue.put(item)

        first_item = (0, self.__root_id)
        priority_queue.put(first_item)

        while not priority_queue.empty():
            current_item = priority_queue.get()

            priority, node_id = current_item

            node_child_ids = self.__node_id_to_child_ids[node_id]
            node_drawing = self.__node_id_to_drawing[node_id]
            
            y = node_drawing.y
            for child_id in node_child_ids:
                child_drawing = self.__node_id_to_drawing[child_id]
                child_drawing.y = y
                y += child_drawing.height + config.get(xindmap.config.Variables.mind_map_viewer_node_margin_y)

                item = (priority + 1, child_id)
                priority_queue.put(item)

            self.__edge_drawing_compute_from_and_to(node_id)

    def __node_drawing_compute_width_and_x(self, node_id):
        priority_queue = queue.PriorityQueue()

        first_item = (0, node_id)
        priority_queue.put(first_item)

        config = xindmap.config.Config()

        while not priority_queue.empty():
            current_item = priority_queue.get()

            priority, node_id = current_item

            node_child_ids = self.__node_id_to_child_ids[node_id]
            node_drawing = self.__node_id_to_drawing[node_id]
            node_parent_id = self.__node_id_to_parent_id[node_id]

            min_width = config.get(xindmap.config.Variables.mind_map_viewer_node_min_width) + config.get(xindmap.config.Variables.mind_map_viewer_node_padding_x)
            title_width = node_drawing.title_width()
            width = title_width + config.get(xindmap.config.Variables.mind_map_viewer_node_padding_x)
            width = max(min_width, width)

            node_drawing.width = width

            if node_parent_id is not None:
                parent_drawing = self.__node_id_to_drawing[node_parent_id]

                x = parent_drawing.x + parent_drawing.width + config.get(xindmap.config.Variables.mind_map_viewer_node_margin_x)
                node_drawing.x = x

                node_index = self.__node_id_to_child_ids[node_parent_id].index(node_id)
                if node_index == len(self.__node_id_to_child_ids[node_parent_id]) - 1:
                    self.__edge_drawing_compute_from_and_to(node_parent_id)

            for child_id in node_child_ids:
                item = (priority + 1, child_id)
                priority_queue.put(item)

    # view *********************************************************************
    def view_center_on_node(self, node_id):
        if node_id not in self.__node_id_to_drawing:
            raise MindMapViewerError(f"unknown node id {node_id}")

        node_drawing = self.__node_id_to_drawing[node_id]
        x = int(node_drawing.center_x)
        y = int(node_drawing.center_y)

        center_x = self.__canvas.winfo_width() // 2
        center_y = self.__canvas.winfo_height() // 2

        top_left_x = int(self.__canvas.canvasx(0))
        top_left_y = int(self.__canvas.canvasy(0))

        x -= top_left_x
        y -= top_left_y

        self.__canvas.scan_mark(x, y)
        self.__canvas.scan_dragto(center_x, center_y, 1)

