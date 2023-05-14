import enum

class MindMapEvent(enum.Enum):
    node_added = enum.auto()
    node_selected = enum.auto()
    node_title_set = enum.auto()
