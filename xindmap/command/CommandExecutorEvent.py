import enum


class CommandExecutorEvent(enum.Enum):
    after_command_execution = enum.auto()
    before_command_execution = enum.auto()
