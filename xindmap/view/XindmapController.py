import kivy.core.window
import kivy.uix.widget
import kivy.properties

class XindmapController(kivy.uix.widget.Widget):
    """The main widget for the Xindmap app.
    """
    command_label = kivy.properties.ObjectProperty()

    def __init__(self, config, **kwargs):
        """Instantiates this controller.

        Args:
            config: the config for the Xindmap app.
            kwargs: all the arguments to pass to the widget constructor
        """
        super().__init__(**kwargs)

        # save config and save shortcut to objects stored in the config
        self.__config = config
        self.__command_tree = config.command_tree

        # keyboard
        self.__keyboard = kivy.core.window.Window.request_keyboard(
            self._on_keyboard_closed, self
        )
        self.__keyboard.bind(
            on_key_down = self._on_key_down,
            on_textinput=self._on_text_input
        )

    def _on_keyboard_closed(self):
        """Callback raised when the keyboard listener is closed.
        """
        pass

    def _on_text_input(self, keyboard, text):
        """Callback raised when text is being entered.

        Args:
            keyboard: the keyboard listener
            keycode: the code of the key
            text: the text corresponding to the key
            modifiers: TODO
        """
        print('text', text, self.modifiers)
        step_has_been_taken = self.__command_tree.step(text)

        if step_has_been_taken:
            self.command_label.text = self.__command_tree.current_path()

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        """Callback raised when a key is pressed.
        """
        print('key', keycode, text, modifiers)
        self.modifiers = modifiers
