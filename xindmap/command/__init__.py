"""Xindmap command module.

# `xindmap.command`

Commands are the way user interacts with the application.
The commands can pretty much do anything and are only limited by the possibility
of the api they are given to interact with the application.
Command are invoke through
[command calls][xindmap.command.CommandCall.CommandCall] which will be
processed by the
[executor][xindmap.command.CommandExecutor.CommandExecutor].

## Module exported content

- [`xindmap.command.CommandApi.CommandApi`][]
- [`xindmap.command.CommandCall.CommandCall`][]
- [`xindmap.command.CommandCallQueue.CommandCallQueue`][]
- [`xindmap.command.CommandCallQueueEvent.CommandCallQueueEvent`][]
- [`xindmap.command.CommandExecutor.CommandExecutor`][]
- [`xindmap.command.CommandRegister.CommandRegister`][]
- [`xindmap.command.CommandRegistrationError.CommandRegistrationError`][]
"""

from .CommandApi import CommandApi
from .CommandCall import CommandCall
from .CommandCallQueue import CommandCallQueue
from .CommandCallQueueEvent import CommandCallQueueEvent
from .CommandExecutor import CommandExecutor
from .CommandRegister import CommandRegister
from .CommandRegistrationError import CommandRegistrationError
