import collections
import xindmap.event

from .InputStackEvent import InputStackEvent


class InputStack(xindmap.event.EventSource):
    # constructor **************************************************************
    def __init__(self):
        super().__init__(InputStackEvent)

        self.__stack = collections.deque()

    # modification *************************************************************
    def clear(self):
        self.__stack.clear()

        event = xindmap.event.Event(InputStackEvent.stack_cleared)
        self._dispatch_event(event)

    def pop(self):
        input = self.__stack.pop()

        event = xindmap.event.Event(InputStackEvent.input_poped, input=input)
        self._dispatch_event(event)

        return input

    def push(self, input):
        self.__stack.append(input)

        event = xindmap.event.Event(InputStackEvent.input_pushed, input=input)
        self._dispatch_event(event)

    # size *********************************************************************
    def __len__(self):
        return len(self.__stack)
