import logging
import xindmap.event

from .CommandExecutorEvent import CommandExecutorEvent
from .CommandRegisterError import CommandRegisterError


class CommandExecutor(xindmap.event.EventSource):
    # callback *****************************************************************
    def on_command_call_queue_call_enqueued(self, command_call_queue, event):
        logging.debug(
            f"command executor {id(self)}: on_command_queue_command_enqueued(event={event})"
        )

        command_call = event.call

        try:
            command = self.__command_register[command_call.command_name]
        except CommandRegisterError as error:
            logging.warning(f'command "{command_call.command_name}" not found')
            return

        try:
            command(*command_call.args, api=self.__command_api)
        except Exception as error:
            logging.warning(f"command bugged, what to do ?")
            logging.warning(error)

        command_call_queue.dequeue()

    # constructor **************************************************************
    def __init__(self, command_api, command_register):
        super().__init__(CommandExecutorEvent)

        self.__command_api = command_api
        self.__command_register = command_register
