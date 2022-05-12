import itertools
import kivy.event as kevent
import kivy.properties as kproperties
import xindmap.logging as xlogging

from .State import State

class EditorState(kevent.EventDispatcher):
    """represents the current state of the editor

    Attributes:
        state: the current state of the editor
            command by default
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    state = kproperties.ObjectProperty(State.command)

    # dunder *******************************************************************
    def __init__(self):
        """instantites this editor state
        """
        super().__init__()

        self.__id = next(EditorState.__id_counter)

        xlogging.info('{}: instantiated', self)

    # callback *****************************************************************
    def on_state(self, _, state):
        """callback raised upon changing the editor state

        Args:
            _: same as self
                ignored
            state: the new state of the editor
        """
        xlogging.info('{}: on state', self)

