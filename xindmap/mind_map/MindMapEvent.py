import enum


class MindMapEvent(enum.Enum):
    cleared = enum.auto()
    node_added = enum.auto()
    node_deleted = enum.auto()
    node_selected = enum.auto()
    node_status_set = enum.auto()
    node_text_set = enum.auto()
    node_unselected = enum.auto()
