"""
MapleMessengerCharacter - Converted from Java source
Original: handling/world/MapleMessengerCharacter.java
Package: handling.world
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes


class MapleMessengerCharacter:
    """
    Class MapleMessengerCharacter
    Implements: Serializable
    """

    def __init__(self, maplechar: Any):
        self.name = ""
        self.id = 0
        self.channel = 0
        self.online = False
        self.name = ""
        self.id = -1
        self.channel = -1
        self.online = False
        self.name = maplechar.getName()
        self.channel = maplechar.getClient().getChannel()
        self.id = maplechar.getId()
        self.online = True

    # Static initializer
    # MapleMessengerCharacter.serialVersionUID = 6215463252132450750


    def getChannel(self) -> int:
        return self.channel

    def isOnline(self) -> bool:
        return self.online

    def setOnline(self, online: bool) -> None:
        self.online = online

    def getName(self) -> str:
        return self.name

    def getId(self) -> int:
        return self.id

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + ((self.name is None) ? 0 : self.name.hashCode())
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        if self.name is None:
            if other.name is not None:
                return False
        elif not self.name == (other.name):
            return False
        return True

