import enum


class StateHolderEvent(enum.Enum):
    """Event types dispatched by
    [`StateHolder`][xindmap.state.StateHolder.StateHolder] class.
    """
    state_set = enum.auto()
    """The [state][xindmap.state.State.State] stored in the holder has changed.
    """
