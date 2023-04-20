import collections

import xindmap.event

from .InputStackEvent import InputStackEvent


class InputStack(xindmap.event.EventSource):
    """A stack containing [inputs][xindmap.input.Input.Input].

    # Events

    The input stack is an [event source][xindmap.event.EventSource.EventSource].
    It dispatches event of types enumed in
    [`InputStackEvent`][xindmap.input.InputStackEvent.InputStackEvent] class.

    ### input poped

    **Type**:
        [`InputStackEvent.input_poped`][xindmap.input.InputStackEvent.InputStackEvent.input_poped]

    Args:
        input: The [input][xindmap.input.Input.Input] that has been poped.

    ### input pushed

    **Type**:
        [`InputStackEvent.input_pushed`][xindmap.input.InputStackEvent.InputStackEvent.input_pushed]

    Args:
        input: The [input][xindmap.input.Input.Input] that has been pushed.
    
    ### stack cleared

    **Type**:
        [`InputStackEvent.stack_cleared`][xindmap.input.InputStackEvent.InputStackEvent.stack_cleared]

    Attributes:
        __stack:
            The underlying [`deque`][collections.deque] containing the
            [inputs][xindmap.input.Input.Input].
    """
    # constructor **************************************************************
    def __init__(self):
        """Instantiates this stack.
        """
        super().__init__(InputStackEvent)

        self.__stack = collections.deque()

    # modification *************************************************************
    def clear(self):
        """Clears this stack of all its contained
        [inputs][xindmap.input.Input.Input].

        Dispatches the event
        [stack cleared][xindmap.input.InputStack.InputStack--stack-cleared].
        """
        self.__stack.clear()

        event = xindmap.event.Event(InputStackEvent.stack_cleared)
        self._dispatch_event(event)

    def pop(self):
        """Pops the latest [input][xindmap.input.Input.Input] pushed in this
        stack.

        Dispatches the event
        [input poped][xindmap.input.InputStack.InputStack--input-poped].

        Returns:
            The poped [input][xindmap.input.Input.Input].
        """
        input = self.__stack.pop()

        event = xindmap.event.Event(InputStackEvent.input_poped, input=input)
        self._dispatch_event(event)

        return input

    def push(self, input):
        """Pushes an [input][xindmap.input.Input.Input] in this stack.

        Dispatches the event
        [input pushed][xindmap.input.InputStack.InputStack--input-pushed].

        Args:
            input: The [input][xindmap.input.Input.Input] to push.
        """
        self.__stack.append(input)

        event = xindmap.event.Event(InputStackEvent.input_pushed, input=input)
        self._dispatch_event(event)

    # size *********************************************************************
    def __len__(self):
        """Returns the number of [inputs][xindmap.input.Input.Input] in this
        stack.
        """
        return len(self.__stack)
