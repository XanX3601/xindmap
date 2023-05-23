import xindmap.event

from .EditableHolderEvent import EditableHolderEvent


class EditableHolder(xindmap.event.EventSource):
    # constructor **************************************************************
    def __init__(self):
        super().__init__(EditableHolderEvent)

        self.__editable = None

    # editable *****************************************************************
    def set_editable(self, editable):
        self.__editable = editable

        event = xindmap.event.Event(EditableHolderEvent.editable_set, editable=editable)
        self._dispatch_event(event)
