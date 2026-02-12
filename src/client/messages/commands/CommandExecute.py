"""
CommandExecute - Converted from Java source
Original: client/messages/commands/CommandExecute.java
Package: client.messages.commands
"""

from enum import Enum, IntEnum
from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes


class CommandExecute(ABC):
    """
    Class CommandExecute
    """


    def getType(self) -> Any:
        return ServerConstants.CommandType.NORMAL

    @staticmethod
    def getType() -> Any:
        return ServerConstants.CommandType.TRADE


# Inner class from Java (originally nested)
class TradeExecute(CommandExecute, ABC):
    """
    Class TradeExecute
    Extends: CommandExecute
    """


    def getType(self) -> Any:
        return ServerConstants.CommandType.TRADE


# Inner class from Java (originally nested)
class ReturnValue(Enum):
    """Enum ReturnValue"""

    DONT_LOG = 0
    LOG = 1

