import collections
import logging
import queue

import customtkinter as ctk
import sortedcontainers

import xindmap.config
import xindmap.mind_map

from .Direction import Direction
from .EdgeDrawing import EdgeDrawing
from .Hitbox import Hitbox
from .MindMapViewerError import MindMapViewerError
from .MindNodeDrawing import MindNodeDrawing


class MindMapViewer(ctk.CTkFrame, xindmap.config.Configurable):
    # callback *****************************************************************
    def on_mind_map_cleared(self, _, event):
        logging.debug(f"mind map viewer {id(self)}: on_mind_map_cleared(event={event})")

        self.__node_id_to_child_ids = {}
        self.__node_id_to_child_id_to_edge_drawing = {}
        self.__node_id_to_drawing = {}
        self.__node_id_to_hitbox = {}
        self.__node_id_to_parent_id = {}
        self.__node_id_to_direction = {}

        self.__root_id = None
        self.__root_direction_to_hitbox = {}
        self.__root_direction_to_child_ids = {}

        self.__canvas.delete(ctk.ALL)

    def on_mind_map_node_added(self, mind_map, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_added(event={event})"
        )

        node_id = event.node_id
        parent_id = mind_map.node_parent_id(node_id)

        drawing = MindNodeDrawing(self.__canvas)

        if self.__root_id is None:
            self.__root_id = node_id

            self.__root_direction_to_hitbox = {
                Direction.left: Hitbox(),
                Direction.right: Hitbox(),
            }

            self.__root_direction_to_child_ids = {
                Direction.left: sortedcontainers.SortedList(),
                Direction.right: sortedcontainers.SortedList(),
            }

            self.__node_id_to_child_ids[node_id] = sortedcontainers.SortedList()
            self.__node_id_to_child_id_to_edge_drawing[node_id] = {}
            self.__node_id_to_drawing[node_id] = drawing
            self.__node_id_to_parent_id[node_id] = None
            self.__node_id_to_direction[node_id] = None

            self.__compute_hitbox_width(node_id)

        else:
            # basic stuff for the new node
            self.__node_id_to_child_ids[node_id] = sortedcontainers.SortedList()
            self.__node_id_to_child_id_to_edge_drawing[node_id] = {}
            self.__node_id_to_drawing[node_id] = drawing
            self.__node_id_to_hitbox[node_id] = Hitbox()

            # handle the relation to its parent
            self.__node_id_to_parent_id[node_id] = parent_id
            self.__node_id_to_child_ids[parent_id].add(node_id)
            self.__node_id_to_child_id_to_edge_drawing[parent_id][
                node_id
            ] = EdgeDrawing(self.__canvas)

            # handle the direction of the new node
            # if parent is root then there is extra step
            if parent_id == self.__root_id:
                if len(self.__root_direction_to_child_ids[Direction.right]) < 3:
                    direction = Direction.right
                elif len(self.__root_direction_to_child_ids[Direction.right]) == len(
                    self.__root_direction_to_child_ids[Direction.left]
                ):
                    direction = Direction.right
                else:
                    direction = Direction.left

                self.__root_direction_to_child_ids[direction].add(node_id)
            else:
                direction = self.__node_id_to_direction[parent_id]

            self.__node_id_to_direction[node_id] = direction

            # handle the body color of the new node
            # if parent is root then pick new color else, pick parent's color
            if parent_id == self.__root_id:
                config = xindmap.config.Config()

                body_colors = config.get(
                    xindmap.config.Variables.mind_map_viewer_mind_node_drawing_body_colors
                )

                root_childs_ids = self.__node_id_to_child_ids[self.__root_id]

                body_color = body_colors[len(root_childs_ids) % len(body_colors)]

                drawing.body_color = body_color
            else:
                parent_drawing = self.__node_id_to_drawing[parent_id]

                body_color = parent_drawing.body_color

                drawing.body_color = body_color

            # copy the body color
            self.__node_id_to_child_id_to_edge_drawing[parent_id][
                node_id
            ].color = body_color

            # compute the x of the hitbox from the parent
            self.__compute_hitbox_width(node_id)
            self.__compute_children_hitbox_x(
                parent_id,
                direction=self.__node_id_to_direction[node_id],
                update_drawing_coords=False,
            )

        # compute the y of the hitbox from the new node
        self.__compute_hitbox_height(node_id)
        self.__compute_hitbox_y_from_root(self.__node_id_to_direction[node_id])

    def on_mind_map_node_deleted(self, _, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_deleted(event={event})"
        )

        # TODO: refactor

        node_id = event.node_id

        parent_id = self.__node_id_to_parent_id[node_id]

        del self.__node_id_to_child_ids[node_id]
        del self.__node_id_to_drawing[node_id]
        del self.__node_id_to_child_id_to_edge_drawing[node_id]
        del self.__node_id_to_hitbox[node_id]
        del self.__node_id_to_parent_id[node_id]

        if node_id == self.__root_id:
            self.__root_id = None

        if parent_id is not None:
            self.__node_id_to_child_ids[parent_id].remove(node_id)

            del self.__node_id_to_child_id_to_edge_drawing[parent_id][node_id]

            self.__compute_hitbox_height(parent_id)
            self.__compute_hitbox_y_from_root(self.__node_id_to_direction[parent_id])

    def on_mind_map_node_selected(self, _, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_selected(event={event})"
        )

        node_id = event.node_id
        previous_node_id = event.previous_node_id

        self.__node_id_to_drawing[node_id].is_selected = True

        if previous_node_id is not None:
            self.__node_id_to_drawing[previous_node_id].is_selected = False

    def on_mind_map_node_statuts_set(self, _, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_status_set(event={event})"
        )

        node_id = event.node_id
        status = event.status

        drawing = self.__node_id_to_drawing[node_id]
        parent_id = self.__node_id_to_parent_id[node_id]

        previous_height = drawing.height
        previous_width = drawing.width

        drawing.status = status

        self.__compute_completion(node_id)

        if parent_id is not None:
            parent_drawing = self.__node_id_to_drawing[parent_id]

            parent_previous_height = parent_drawing.height
            parent_previous_width = parent_drawing.width

            self.__compute_completion(parent_id)

            will_need_to_compute_height = (
                previous_height != drawing.height
                or parent_previous_height != parent_drawing.height
            )
            has_computed_width_or_height = False

            if parent_previous_width != parent_drawing.width:
                self.__compute_hitbox_width(parent_id)
                self.__compute_hitbox_width(node_id)

                self.__compute_children_hitbox_x(
                    parent_id,
                    update_drawing_coords=not will_need_to_compute_height,
                    direction=self.__node_id_to_direction[node_id],
                )

                has_computed_width_or_height = True

            elif previous_width != drawing.width:
                self.__compute_hitbox_width(node_id)

                self.__compute_children_hitbox_x(
                    node_id, update_drawing_coords=not will_need_to_compute_height
                )

                has_computed_width_or_height = True

            if previous_height != drawing.height:
                self.__compute_hitbox_height(node_id)
                self.__compute_hitbox_y_from_root(self.__node_id_to_direction[node_id])
                has_computed_width_or_height = True

            elif parent_previous_height != parent_drawing.height:
                self.__compute_hitbox_height(parent_id)
                self.__compute_hitbox_y_from_root(self.__node_id_to_direction[node_id])
                has_computed_width_or_height = True

            if not has_computed_width_or_height:
                self.__compute_drawing_coords(node_id)
                self.__compute_drawing_coords(parent_id)

        else:
            will_need_to_compute_height = previous_height != drawing.height
            has_computed_width_or_height = False

            if previous_width != drawing.width:
                self.__compute_hitbox_width(node_id)

                self.__compute_children_hitbox_x(
                    node_id, update_drawing_coords=not will_need_to_compute_height
                )

                has_computed_width_or_height = True

            if will_need_to_compute_height:
                self.__compute_hitbox_height(node_id)
                self.__compute_hitbox_y_from_root(self.__node_id_to_direction[node_id])
                has_computed_width_or_height = True

            if not has_computed_width_or_height:
                self.__compute_drawing_coords(node_id)

    def on_mind_map_node_text_set(self, mind_map, event):
        logging.debug(
            f"mind map viewer {id(self)}: on_mind_map_node_title_set(event={event})"
        )

        node_id = event.node_id

        title = mind_map.node_title(node_id)

        drawing = self.__node_id_to_drawing[node_id]

        previous_width = drawing.width
        previous_height = drawing.height

        drawing.title = title

        if previous_width != drawing.width:
            self.__compute_hitbox_width(node_id)

        if previous_width != drawing.width or previous_height != drawing.height:
            parent_id = self.__node_id_to_parent_id[node_id]

            if parent_id is not None:
                self.__compute_children_hitbox_x(
                    parent_id,
                    direction=self.__node_id_to_direction[node_id],
                    update_drawing_coords=False,
                )
            else:
                self.__compute_children_hitbox_x(node_id, update_drawing_coords=False)

            self.__compute_hitbox_height(node_id)
            self.__compute_hitbox_y_from_root(self.__node_id_to_direction[node_id])
        else:
            self.__compute_drawing_coords(node_id)

        # TODO: refactor

    # config callback **********************************************************
    def on_config_variable_mind_map_viewer_edge_drawing_inner_point_padding_width_percentage_set(
        self, _
    ):
        for (
            child_id_to_edge_drawing
        ) in self.__node_id_to_child_id_to_edge_drawing.values():
            for edge_drawing in child_id_to_edge_drawing.values():
                edge_drawing.update_components()

    def on_config_variable_mind_map_viewer_edge_drawing_line_width_set(self, value):
        for (
            child_id_to_edge_drawing
        ) in self.__node_id_to_child_id_to_edge_drawing.values():
            for edge_drawing in child_id_to_edge_drawing.values():
                edge_drawing.set_line_width(value)

    def on_config_variable_mind_map_viewer_mind_node_drawing_body_height_set(self, _):
        if self.__root_id is not None:
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_body_min_width_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id,
                direction=None,
                update_drawing_coords=True,
                update_drawing_size=True,
                update_hitbox_width=True,
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_margin_bottom_set(self, _):
        if self.__root_id is not None:
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_margin_right_set(self, _):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(self.__root_id)

    def on_config_variable_mind_map_viewer_mind_node_drawing_padding_bottom_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_padding_left_set(self, _):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_padding_right_set(self, _):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_padding_top_set(self, _):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_padding_bottom_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_size()
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_padding_left_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_size()
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_padding_right_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_size()
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_padding_top_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_size()
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_selector_radius_set(
        self, _
    ):
        if self.__root_id is not None:
            for drawing in self.__node_id_to_drawing.values():
                drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_height_set(self, _):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_inner_circle_padding_bottom_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_inner_circle_padding_left_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_inner_circle_padding_right_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_inner_circle_padding_top_set(
        self, _
    ):
        for drawing in self.__node_id_to_drawing.values():
            drawing.update_components()

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_padding_bottom_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_padding_left_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_padding_right_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_padding_top_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_status_width_set(self, _):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_title_padding_bottom_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    def on_config_variable_mind_map_viewer_mind_node_drawing_title_padding_left_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_title_padding_right_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_children_hitbox_x(
                self.__root_id, update_drawing_size=True, update_hitbox_width=True
            )

    def on_config_variable_mind_map_viewer_mind_node_drawing_title_padding_top_set(
        self, _
    ):
        if self.__root_id is not None:
            self.__compute_all_hitboxes_height()
            self.__compute_hitbox_y_from_root(Direction.left)
            self.__compute_hitbox_y_from_root(Direction.right)

    # constructor **************************************************************
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)

        Variables = xindmap.config.Variables

        xindmap.config.Configurable.__init__(
            self,
            (
                Variables.mind_map_viewer_edge_drawing_inner_point_padding_width_percentage,
                Variables.mind_map_viewer_edge_drawing_line_width,
                Variables.mind_map_viewer_mind_node_drawing_body_height,
                Variables.mind_map_viewer_mind_node_drawing_body_min_width,
                Variables.mind_map_viewer_mind_node_drawing_margin_bottom,
                Variables.mind_map_viewer_mind_node_drawing_margin_right,
                Variables.mind_map_viewer_mind_node_drawing_padding_bottom,
                Variables.mind_map_viewer_mind_node_drawing_padding_left,
                Variables.mind_map_viewer_mind_node_drawing_padding_right,
                Variables.mind_map_viewer_mind_node_drawing_padding_top,
                Variables.mind_map_viewer_mind_node_drawing_selector_padding_bottom,
                Variables.mind_map_viewer_mind_node_drawing_selector_padding_left,
                Variables.mind_map_viewer_mind_node_drawing_selector_padding_right,
                Variables.mind_map_viewer_mind_node_drawing_selector_padding_top,
                Variables.mind_map_viewer_mind_node_drawing_selector_radius,
                Variables.mind_map_viewer_mind_node_drawing_status_height,
                Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_bottom,
                Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_left,
                Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_right,
                Variables.mind_map_viewer_mind_node_drawing_status_inner_circle_padding_top,
                Variables.mind_map_viewer_mind_node_drawing_status_padding_bottom,
                Variables.mind_map_viewer_mind_node_drawing_status_padding_left,
                Variables.mind_map_viewer_mind_node_drawing_status_padding_right,
                Variables.mind_map_viewer_mind_node_drawing_status_padding_top,
                Variables.mind_map_viewer_mind_node_drawing_status_width,
                Variables.mind_map_viewer_mind_node_drawing_title_padding_bottom,
                Variables.mind_map_viewer_mind_node_drawing_title_padding_left,
                Variables.mind_map_viewer_mind_node_drawing_title_padding_right,
                Variables.mind_map_viewer_mind_node_drawing_title_padding_top,
            ),
        )

        self.__canvas = ctk.CTkCanvas()

        self.__node_id_to_child_ids = {}
        self.__node_id_to_child_id_to_edge_drawing = {}
        self.__node_id_to_drawing = {}
        self.__node_id_to_hitbox = {}
        self.__node_id_to_parent_id = {}
        self.__node_id_to_direction = {}

        self.__root_id = None
        self.__root_direction_to_hitbox = {}
        self.__root_direction_to_child_ids = {}

        self.__canvas.pack(fill=ctk.BOTH, expand=True)

    # direction ****************************************************************
    def node_direction(self, node_id):
        direction = self.__node_id_to_direction.get(node_id, None)

        if direction is not None:
            direction = direction.name

        return direction if direction else ""

    # node computation *********************************************************
    def __compute_all_hitboxes_height(self):
        config = xindmap.config.Config()

        drawing_margin_bottom = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_margin_bottom
        )

        child_ids = self.__node_id_to_child_ids[self.__root_id]

        priority_queue = queue.PriorityQueue()
        for child_id in child_ids:
            priority_queue.put((0, child_id))

        node_ids_seen = set()

        while not priority_queue.empty():
            priority, node_id = priority_queue.get()

            child_ids = self.__node_id_to_child_ids[node_id]

            if not child_ids:
                drawing = self.__node_id_to_drawing[node_id]
                hitbox = self.__node_id_to_hitbox[node_id]

                drawing.update_size()

                hitbox.height = drawing.height

            elif node_id not in node_ids_seen:
                node_ids_seen.add(node_id)

                for child_id in child_ids:
                    priority_queue.put((priority - 1, child_id))

            else:
                drawing = self.__node_id_to_drawing[node_id]
                hitbox = self.__node_id_to_hitbox[node_id]

                drawing.update_size()

                height = max(
                    drawing.height,
                    sum(
                        self.__node_id_to_hitbox[child_id].height
                        for child_id in child_ids
                    )
                    + drawing_margin_bottom * (len(child_ids) - 1),
                )

                hitbox.height = height

            parent_id = self.__node_id_to_parent_id[node_id]

            if parent_id == self.__root_id:
                continue

            parent_child_ids = self.__node_id_to_child_ids[parent_id]
            node_index = parent_child_ids.index(node_id)
            if node_index == len(parent_child_ids) - 1:
                priority_queue.put((priority + 1, parent_id))

        drawing = self.__node_id_to_drawing[self.__root_id]

        for direction in Direction:
            child_ids = self.__root_direction_to_child_ids[direction]
            hitbox = self.__root_direction_to_hitbox[direction]

            height = max(
                drawing.height,
                sum(self.__node_id_to_hitbox[child_id].height for child_id in child_ids)
                + drawing_margin_bottom * (len(child_ids) - 1),
            )

            hitbox.height = height

    def __compute_children_hitbox_x(
        self,
        node_id,
        direction=None,
        update_drawing_coords=True,
        update_drawing_size=False,
        update_hitbox_width=False,
    ):
        # config variable
        config = xindmap.config.Config()

        drawing_margin_right = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_margin_right
        )

        # retrieve child ids and have specific treatment for root
        child_ids = self.__node_id_to_child_ids[node_id]
        if node_id == self.__root_id and direction is not None:
            child_ids = self.__root_direction_to_child_ids[direction]

        queue = collections.deque(child_ids)

        while queue:
            node_id = queue.pop()

            child_ids = self.__node_id_to_child_ids[node_id]
            drawing = self.__node_id_to_drawing[node_id]
            direction = self.__node_id_to_direction[node_id]
            hitbox = self.__node_id_to_hitbox[node_id]

            parent_id = self.__node_id_to_parent_id[node_id]

            if parent_id == self.__root_id:
                parent_hitbox = self.__root_direction_to_hitbox[direction]
            else:
                parent_hitbox = self.__node_id_to_hitbox[parent_id]

            if direction == Direction.left:
                hitbox.x2 = parent_hitbox.x1 - drawing_margin_right
            else:
                hitbox.x1 = parent_hitbox.x2 + drawing_margin_right

            if update_drawing_size:
                drawing.update_size()

            if update_hitbox_width:
                self.__compute_hitbox_width(node_id)

            if update_drawing_coords:
                self.__compute_drawing_coords(node_id)

            queue.extendleft(child_ids)

    def __compute_completion(self, node_id):
        child_ids = self.__node_id_to_child_ids[node_id]
        drawing = self.__node_id_to_drawing[node_id]

        child_completed_count = 0
        child_to_complete_count = 0

        for child_id in child_ids:
            child_completion = self.__node_id_to_drawing[child_id].completion

            if child_completion is not None:
                child_to_complete_count += 1
                if child_completion == 1:
                    child_completed_count += 1

        if child_to_complete_count > 0:
            completion = (
                child_completed_count / child_to_complete_count
                if child_completed_count < child_to_complete_count
                else 1
            )
        elif drawing.status == xindmap.mind_map.MindNodeStatus.none:
            completion = None
        elif (
            drawing.status == xindmap.mind_map.MindNodeStatus.to_do
            or drawing.status == xindmap.mind_map.MindNodeStatus.in_progress
        ):
            completion = 0
        else:
            completion = 1

        drawing.completion = completion

    def __compute_drawing_coords(self, node_id):
        drawing = self.__node_id_to_drawing[node_id]

        # ensure that the root hitbox stays at the same place
        # this work because this method is called first for the root and later
        # for other nodes.
        if node_id == self.__root_id:
            self.__root_direction_to_hitbox[Direction.right].center_x = 0
            self.__root_direction_to_hitbox[Direction.right].center_y = 0

            self.__root_direction_to_hitbox[Direction.left].center_x = 0
            self.__root_direction_to_hitbox[Direction.left].center_y = 0

            drawing.x1 = self.__root_direction_to_hitbox[Direction.right].x1
            drawing.center_y = self.__root_direction_to_hitbox[Direction.left].center_y
            drawing.update_components()

            return

        hitbox = self.__node_id_to_hitbox[node_id]
        parent_id = self.__node_id_to_parent_id[node_id]

        drawing.center_y = hitbox.center_y
        drawing.x1 = hitbox.x1

        drawing.update_components()

        if parent_id is not None:
            direction = self.__node_id_to_direction[node_id]
            parent_drawing = self.__node_id_to_drawing[parent_id]

            edge_drawing = self.__node_id_to_child_id_to_edge_drawing[parent_id][
                node_id
            ]

            if direction == Direction.right:
                edge_drawing.x1 = parent_drawing.anchor_x2
                edge_drawing.y1 = parent_drawing.anchor_y
                edge_drawing.x2 = drawing.anchor_x1
                edge_drawing.y2 = drawing.anchor_y
            else:
                edge_drawing.x1 = drawing.anchor_x2
                edge_drawing.y1 = drawing.anchor_y
                edge_drawing.x2 = parent_drawing.anchor_x1
                edge_drawing.y2 = parent_drawing.anchor_y

            edge_drawing.update_components()

    def __compute_hitbox_height(self, node_id):
        config = xindmap.config.Config()

        drawing_margin_bottom = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_margin_bottom
        )

        # keep the direction of the node to limit the computation required later
        direction = self.__node_id_to_direction[node_id]
        parent_id = self.__node_id_to_parent_id[node_id]

        # compute height from node till root
        while parent_id is not None:
            child_ids = self.__node_id_to_child_ids[node_id]
            drawing = self.__node_id_to_drawing[node_id]
            hitbox = self.__node_id_to_hitbox[node_id]
            parent_id = self.__node_id_to_parent_id[node_id]

            height = max(
                drawing.height,
                sum(self.__node_id_to_hitbox[child_id].height for child_id in child_ids)
                + drawing_margin_bottom * (len(child_ids) - 1),
            )

            hitbox.height = height

            node_id = parent_id
            parent_id = self.__node_id_to_parent_id[node_id]

        # compute height for root on the minimum direction possible
        drawing = self.__node_id_to_drawing[self.__root_id]

        directions = tuple(Direction) if direction is None else (direction,)
        for direction in directions:
            child_ids = self.__root_direction_to_child_ids[direction]
            hitbox = self.__root_direction_to_hitbox[direction]

            height = max(
                sum(self.__node_id_to_hitbox[child_id].height for child_id in child_ids)
                + drawing_margin_bottom * (len(child_ids) - 1),
                drawing.height,
            )

            hitbox.height = height

    def __compute_hitbox_width(self, node_id):
        drawing = self.__node_id_to_drawing[node_id]

        if node_id == self.__root_id:
            self.__root_direction_to_hitbox[Direction.left].width = drawing.width
            self.__root_direction_to_hitbox[Direction.right].width = drawing.width
        else:
            self.__node_id_to_hitbox[node_id].width = drawing.width

    def __compute_hitbox_y_from_root(self, direction, update_drawing_coords=True):
        if direction is None:
            return

        config = xindmap.config.Config()

        drawing_margin_bottom = config.get(
            xindmap.config.Variables.mind_map_viewer_mind_node_drawing_margin_bottom
        )

        if update_drawing_coords:
            self.__compute_drawing_coords(self.__root_id)

        child_ids = self.__root_direction_to_child_ids[direction]
        hitbox = self.__root_direction_to_hitbox[direction]

        y = hitbox.y1
        for child_id in child_ids:
            child_hitbox = self.__node_id_to_hitbox[child_id]

            child_hitbox.y1 = y

            if update_drawing_coords:
                self.__compute_drawing_coords(child_id)

            y += child_hitbox.height + drawing_margin_bottom

        queue = collections.deque()
        queue.extendleft(child_ids)

        while queue:
            node_id = queue.pop()

            child_ids = self.__node_id_to_child_ids[node_id]
            hitbox = self.__node_id_to_hitbox[node_id]

            y = hitbox.y1
            for child_id in child_ids:
                child_hitbox = self.__node_id_to_hitbox[child_id]

                child_hitbox.y1 = y

                if update_drawing_coords:
                    self.__compute_drawing_coords(child_id)

                y += child_hitbox.height + drawing_margin_bottom

            queue.extendleft(child_ids)

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
