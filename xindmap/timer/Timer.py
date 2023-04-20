import tkinter as tk

import singleton_decorator


@singleton_decorator.singleton
class Timer:
    """The timer is a singleton object, meaning it is unique at runtime used
    to delay call to functions.

    It is built upon the `after` method common to all widgets from
    [`tkinter`][].

    Attributes:
        __widget:
            A [`tkinter`][] widget used to access methods from the library.
    """
    # constructor **************************************************************
    def __init__(self):
        """Instantiates this timer.
        """
        self.__widget = tk.Widget(None, None)

    # timer ********************************************************************
    def cancel_delay(self, delay_id):
        """Cancels the planned call to a function.

        Args:
            delay_id:
                The id to the planned call that has been returned once it was
                planned using the [`delay`][xindmap.timer.Timer.Timer.delay]
                method.
        """
        self.__widget.after_cancel(delay_id)

    def delay(self, function, args, delay_ms):
        """Delays the call to a function.

        Args:
            function: The function to call.
            args: The arguments to pass to the function upon its invokation.
            delay_ms: The delay, in milliseconds, before calling the function.

        Returns:
            delay_id:
                An id identifying the planned call to the function, usefull to
                cancel the call using the
                [`cancel_delay`][xindmap.timer.Timer.Timer.cancel_delay] method.
        """
        return self.__widget.after(delay_ms, lambda: function(*args))
