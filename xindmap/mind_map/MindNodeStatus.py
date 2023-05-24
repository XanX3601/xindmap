import enum


class MindNodeStatus(enum.Enum):
    done = enum.auto()
    in_progress = enum.auto()
    none = enum.auto()
    to_do = enum.auto()
