import logging

from .CommandRegisterError import CommandRegisterError


class CommandExecutor:
    """Executes command from
    [command calls][xindmap.command.CommandCall.CommandCall] found in a
    [command register][xindmap.command.CommandRegister.CommandRegister].

    Attributes:
        __command_api:
            The [command api][xindmap.command.CommandApi.CommandApi] given to
            commands upon their execution.
        __command_register:
            The
            [command register][xindmap.command.CommandRegister.CommandRegister]
            in which find the executable commands.
    """
    # callback *****************************************************************
    def on_command_call_queue_call_enqueued(self, command_call_queue, event):
        """Callback to be called upon
        [call enqueued][xindmap.command.CommandCallQueue.CommandCallQueue--call-enqueued]
        event dispatched by a
        [command call queue][xindmap.command.CommandCallQueue.CommandCallQueue].

        It executes the command as described in the
        [command call][xindmap.command.CommandCall.CommandCall] and then
        dequeues it.

        Args:
            command_call_queue:
                The
                [comamnd call queue][xindmap.command.CommandCallQueue.CommandCallQueue]
                that dispatched the event.
            event:
                The
                [call enqueued][xindmap.command.CommandCallQueue.CommandCallQueue--call-enqueued]
                event for which this callback is called.
        """
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
        """Instantiates this command executor.

        Args:
            command_api:
                the [command api][xindmap.command.CommandApi.CommandApi] to be
                given to the commands upon their execution.
            command_register:
                the
                [command register][xindmap.command.CommandRegister.CommandRegister]
                in which the executable commands can be
                found.
        """
        self.__command_api = command_api
        self.__command_register = command_register

        self.__command_execution_queue()

    # thread *******************************************************************
    def command_execution_thread(self):
        pass
