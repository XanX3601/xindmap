import singleton_decorator
import tkinter as tk


@singleton_decorator.singleton
class Timer:
    # constructor **************************************************************
    def __init__(self):
        self.__widget = tk.Widget(None, None)

    # timer ********************************************************************
    def cancel_delay(self, delay_id):
        self.__widget.after_cancel(delay_id)

    def delay(self, function, args, delay_ms):
        return self.__widget.after(delay_ms, lambda: function(*args))
