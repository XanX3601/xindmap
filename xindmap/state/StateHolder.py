import xindmap.event

from .State import State
from .StateHolderEvent import StateHolderEvent


class StateHolder(xindmap.event.EventSource):
    # constructor **************************************************************
    def __init__(self):
        super().__init__(StateHolderEvent)

        self.__state = State.none

    # state ********************************************************************
    def set_state(self, state):
        self.__state = state

        event = xindmap.event.Event(StateHolderEvent.state_set, state=state)
        self._dispatch_event(event)
