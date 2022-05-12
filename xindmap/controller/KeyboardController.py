import itertools
import kivy.core.window as kwindow
import xindmap.input as xinput
import xindmap.logging as xlogging

class KeyboardController:
    """keyboard controller

    Attributes:
        keyboard: the controlled keyboard
    """
    # static *******************************************************************
    __id_counter = itertools.count()

    # dunder *******************************************************************
    def __init__(self):
        """instantiates this controller
        """
        self.__id = next(KeyboardController.__id_counter)

        self.keyboard = kwindow.Window.request_keyboard(
            self.on_keyboard_closed,
            None
        )
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_textinput=self.on_textinput)

        xlogging.info('{}: instantiated', self)

    def __str__(self):
        """computes a string representation of this controller

        Returns:
            a string representation of this controller
        """
        return 'keyboard controller {}'.format(self.__id)

    # init *********************************************************************
    def init(self, input_controller):
        """initializes this controller

        Args:
            input_controller: the input controller
        """
        self._input_controller = input_controller

        xlogging.info('{}: initialized', self)

    # callback *****************************************************************
    def on_key_down(self, keyboard, keycode, text, modifiers):
        """callback raised when a key is pressed down on the keyboard

        Args:
            keyboard: the keyboard on which the key has been pressed
            keycode: the code of the key that has been pressed
            text: the text corresponding to the key that has been pressed
            modifiers: list of modifiers key that have been pressed alongside 
                the key
        """
        xlogging.debug('{}: on key down', self)

        keycode, keyname = keycode

        if keycode == self.keyboard.keycodes['backspace']:
            input = xinput.Input(xinput.InputType.backspace)
            self._input_controller.input(input)

        elif keycode == self.keyboard.keycodes['enter']:
            input = xinput.Input(xinput.InputType.enter)
            self._input_controller.input(input)

        elif keycode == self.keyboard.keycodes['escape']:
            input = xinput.Input(xinput.InputType.escape)
            self._input_controller.input(input)

        return True

    def on_textinput(self, keyboard, text):
        """callback raised when text is entered through the keyboard

        Args:
            keyboard: the keyboard on which text has been entered
            text: the text that has been entered
        """
        xlogging.debug('{}: on text input', self)

        input = xinput.Input(xinput.InputType.default, text)

        self._input_controller.input(input)

    def on_keyboard_closed(self):
        """callback raised when keyboard is closed

        Args:
            keyboard: the keyboard
        """
        xlogging.critical('{}: on keyboard closed', self)
