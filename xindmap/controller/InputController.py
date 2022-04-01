import collections
import kivy.event as kevent
import kivy.logger as klogger
import kivy.properties as kproperties
import xindmap.input as xinput

class InputController(kevent.EventDispatcher):
    """input controller

    Attributes:
        inputs: the current input sequence
        inputs_text: the concatenation of string representation of the inputs in
            the inputs sequence
    """
    inputs_text = kproperties.StringProperty()

    def __init__(self):
        """instantiates this controller
        """
        super().__init__()

        self.inputs = collections.deque()
        self.inputs_result = collections.deque()

    def init(self, command_controller, command_tree, input_widget):
        """initializes this controller
        
        Args:
            command_controller: the command controller
            command_tree: the command tree
            input_widget: the input widget
        """
        self._command_controller = command_controller
        self._command_tree = command_tree
        self._input_widget = input_widget

    def input(self, input):
        """inputs to this controller

        Args:
            input: an input
        """
        def clear(self):
            self.inputs.clear()
            self.inputs_text = ''
            self.inputs_result.clear()

            self._command_tree.root()

        klogger.Logger.debug(
            '[input controller] input type {} value {}'.format(input.type.name, input.value)
        )

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

    def on_inputs_text(self, _, text):
        """callback raised when the property inputs_text is changed

        Args:
            _: this controller
                ignored
            text: the new value of inputs_text
        """
        self._input_widget.text = text

