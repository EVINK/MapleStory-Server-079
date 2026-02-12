"""
CharacterIdChannelPair - Converted from Java source
Original: handling/world/CharacterIdChannelPair.java
Package: handling.world
"""

from typing import Optional, Any
import os


class CharacterIdChannelPair(Externalizable):
    """
    Class CharacterIdChannelPair
    Implements: Externalizable, Comparable<CharacterIdChannelPair>
    """

    def __init__(self):
        self.charid = 0
        self.channel = 0
        self.charid = 0
        self.channel = 1


    def getCharacterId(self) -> int:
        return self.charid

    def getChannel(self) -> int:
        return self.channel

    def readExternal(self, in: Any) -> None:
        self.charid = in.readInt()
        self.channel = in.readByte()

    def writeExternal(self, out: Any) -> None:
        out.writeInt(self.charid)
        out.writeByte(self.channel)

    def compareTo(self, o: Any) -> int:
        return self.channel - o.channel

