import logging
import queue
import threading

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

        command_execution_item = (command_call.command_name, command_call.args)
        self.__command_execution_queue.put(command_execution_item)

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

        self.__command_execution_queue = queue.Queue()
        self.__command_execution_thread_running = True
        self.__command_execution_thread = threading.Thread(
            target=self.__command_execution_thread_target
        )
        self.__command_execution_thread.start()

    # thread *******************************************************************
    def __command_execution_thread_target(self):
        while self.__command_execution_thread_running:
            print("waiting for command")
            command_name, args = self.__command_execution_queue.get()
            print(command_name)

            if command_name is None:
                print("I am supposed to stop")
                self.__command_execution_thread_running = False
                continue

            try:
                command = self.__command_register[command_name]
            except CommandRegisterError as error:
                logging.warning(f'command "{command_name}" not found')
                continue

            try:
                command(*args, api=self.__command_api)
            except Exception as error:
                logging.warning("command bugged, what to do ?")
                logging.warning(error)

            print(self.__command_execution_queue.qsize())

    def stop(self):
        while self.__command_execution_thread.is_alive():
            self.__command_execution_queue.put((None, None))
            print(self.__command_execution_thread.is_alive())
            input()
