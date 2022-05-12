import xindmap.logging as xlogging

from .InputType import InputType

class Input:
    """an input

    Attributes:
        type: type of the input
        value: value of the input
    """
    # dunder *******************************************************************
    def __init__(self, type, value=None):
        """instantiates this input

        Args:
            type: type of the input
            value: value of the input
        """
        self.type = type
        self.value = value

        xlogging.debug('input: instantiated type {} value {}', type, value)

    def __eq__(self, other_input):
        """tests wether this input equals another one

        Args:
            other_input: another input

        Returns:
            True if this input equals the other one, False otherwise
        """
        if not isinstance(other_input, Input):
            return False

        return self.type == other_input.type and self.value == other_input.value

    def __hash__(self):
        """computes the hash value of this input

        Returns:
            the hash value of this input
        """
        return hash((self.type, self.value))

    def __repr__(self):
        """computes a small string reprepsentation of this input

        Returns:
            a small string representation of this input
        """
        return str(self)

    def __str__(self):
        """computes a string representation of this input

        Returns:
            a string represenation of this input
        """
        if self.type == InputType.default:
            return str(self.value)
        elif self.type == InputType.backspace:
            return '<BS>'
        elif self.type == InputType.enter:
            return '<CR>'

