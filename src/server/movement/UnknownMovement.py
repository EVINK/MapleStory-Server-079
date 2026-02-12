"""
UnknownMovement - Converted from Java source
Original: server/movement/UnknownMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class UnknownMovement(AbstractLifeMovement):
    """
    Class UnknownMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.pixelsPerSecond = None
        self.unk = 0
        self.fh = 0
        super(type, position, duration, newstate)


    def getPixelsPerSecond(self) -> Any:
        return self.pixelsPerSecond

    def setPixelsPerSecond(self, wobble: Any) -> None:
        self.pixelsPerSecond = wobble

    def getUnk(self) -> int:
        return self.unk

    def setUnk(self, unk: int) -> None:
        self.unk = unk

    def getFH(self) -> int:
        return self.fh

    def setFH(self, fh: int) -> None:
        self.fh = fh

    def serialize(self, lew: Any) -> None:
        lew.write(self.getType())
        lew.writeShort(self.unk)
        lew.writeShort(self.getPosition().x)
        lew.writeShort(self.getPosition().y)
        lew.writeShort(self.pixelsPerSecond.x)
        lew.writeShort(self.pixelsPerSecond.y)
        lew.writeShort(self.fh)
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

