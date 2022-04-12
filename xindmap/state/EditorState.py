import kivy.event as kevent
import kivy.logger as klogger
import kivy.properties as kproperties

from .State import State

class EditorState(kevent.EventDispatcher):
    """represents the current state of the editor

    Attributes:
        state: the current state of the editor
            command by default
    """
    state = kproperties.ObjectProperty(State.command)

    def __init__(self):
        """instantites this editor state
        """
        super().__init__()

    def on_state(self, _, state):
        """callback raised upon changing the editor state

        Args:
            _: same as self
                ignored
            state: the new state of the editor
        """
        print(state, type(state))

        klogger.Logger.info(
            '[editor state] editor state changed to {}'.format(state.name)
        )

