import xindmap.event

from .State import State
from .StateHolderEvent import StateHolderEvent


class StateHolder(xindmap.event.EventSource):
    """The state holder stores the current [state][xindmap.state.State.State] of
    the application.

    # Events

    The state holder is an
    [event source][xindmap.event.EventSource.EventSource].
    It dispatches [events][xindmap.event.Event.Event] of types enumed in
    [`StateHolderEvent`][xindmap.state.StateHolderEvent.StateHolderEvent] class.

    ### state set

    **Type**:
        [`StateHolderEvent.state_set`][xindmap.state.StateHolderEvent.StateHolderEvent.state_set]

    Args:
        state: The new [state][xindmap.state.State.State].

    Attributes:
        __state:
            The current [state][xindmap.state.State.State] stored in this
            holder.
    """
    # constructor **************************************************************
    def __init__(self):
        """Instantiates this state holder.
        """
        super().__init__(StateHolderEvent)

        self.__state = State.none

    # state ********************************************************************
    def set_state(self, state):
        """Sets the [state][xindmap.state.State.State] stored in this state
        holder.

        Dispathes the event
        [state set][xindmap.state.StateHolder.StateHolder--state-set].

        Args:
            state: The new [state][xindmap.state.State.State].
        """
        self.__state = state

        event = xindmap.event.Event(StateHolderEvent.state_set, state=state)
        self._dispatch_event(event)
