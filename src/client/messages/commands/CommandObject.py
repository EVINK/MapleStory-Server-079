"""
CommandObject - Converted from Java source
Original: client/messages/commands/CommandObject.java
Package: client.messages.commands
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes


class CommandObject:
    """
    Class CommandObject
    """

    def __init__(self, com: str, c: Any, gmLevel: int):
        self.command = None
        self.gmLevelReq = None
        self.exe = None
        self.command = com
        self.exe = c
        self.gmLevelReq = gmLevel


    def execute(self, c: Any, splitted: list) -> int:
        return self.exe.execute(c, splitted)

    def getType(self) -> Any:
        return self.exe.getType()

    def getReqGMLevel(self) -> int:
        return self.gmLevelReq

