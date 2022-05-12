import collections
import itertools
import kivy.event as kevent
import kivy.properties as kproperties
import xindmap.input as xinput
import xindmap.logging as xlogging
import xindmap.state as xstate

class InputController(kevent.EventDispatcher):
    """input controller

    Attributes:
        inputs: the current input sequence
        inputs_text: the concatenation of string representation of the inputs in
            the inputs sequence
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # property *****************************************************************
    inputs_text = kproperties.StringProperty()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this controller
        """
        super().__init__()

        self.__id = next(InputController.__id_counter)

        self.inputs = collections.deque()
        self.inputs_result = collections.deque()

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this controller

        Returns:
            a string representation of this controller
        """
        return 'input controller {}'.format(self.__id)

    # init *********************************************************************
    def init(
        self,
        editor_state,
        command_controller,
        command_tree,
        input_widget,
        insert_controller
    ):
        """initializes this controller
        
        Args:
            command_controller: the command controller
            command_tree: the command tree
            input_widget: the input widget
            insert_controller: the insert controller
        """
        self._editor_state = editor_state
        self._command_controller = command_controller
        self._command_tree = command_tree
        self._input_widget = input_widget
        self._insert_controller = insert_controller

        xlogging.info('{}: initialized', self)

    # unput ********************************************************************
    def input(self, input):
        """inputs to this controller dependending on the state of the editor

        Args:
            input: an input
        """
        xlogging.info(
            '{}: input type {} value {}',
            self,
            input.type,
            input.value
        )

        if self._editor_state.state == xstate.State.command:
            self.input_command(input)
        elif self._editor_state.state == xstate.State.insert:
            self.input_insert(input)

    def input_command(self, input):
        """inputs to this controller an input in command mode

        Args:
            input: an input
        """
        def clear(self):
            self.inputs.clear()
            self.inputs_text = ''
            self.inputs_result.clear()

            self._command_tree.root()

        if input.type == xinput.InputType.backspace:
            if self.inputs:
                input = self.inputs.pop()
                self.inputs_text = self.inputs_text.removesuffix(str(input))

                if self.inputs_result.pop():
                    self._command_tree.previous_node()

        elif input.type == xinput.InputType.escape:
            clear(self)

        else:
            self.inputs.append(input)
            self.inputs_text += str(input)

            if not self.inputs_result or self.inputs_result[-1]:
                self.inputs_result.append(
                    self._command_tree.next_node(input)
                )
            else:
                self.inputs_result.append(False)

            if self._command_tree.command is not None:
                self._command_controller.execute(self._command_tree.command)

                clear(self)

    def input_insert(self, input):
        """inputs to this controller an input in insert mode

        Args:
            input: an input
        """
        if input.type == xinput.InputType.default:
            self._insert_controller.insert(input.value)

        elif input.type == xinput.InputType.escape:
            self._editor_state.state = xstate.State.command

    # callback *****************************************************************
    def on_inputs_text(self, _, text):
        """callback raised when the property inputs_text is changed

        Args:
            _: this controller
                ignored
            text: the new value of inputs_text
        """
        xlogging.debug('{}: on inputs text', self)

        self._input_widget.text = text

