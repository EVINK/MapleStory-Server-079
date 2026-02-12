"""
JumpDownMovement - Converted from Java source
Original: server/movement/JumpDownMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class JumpDownMovement(AbstractLifeMovement):
    """
    Class JumpDownMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.pixelsPerSecond = None
        self.offset = None
        self.unk = 0
        self.fh = 0
        super(type, position, duration, newstate)


    def getPixelsPerSecond(self) -> Any:
        return self.pixelsPerSecond

    def setPixelsPerSecond(self, wobble: Any) -> None:
        self.pixelsPerSecond = wobble

    def getOffset(self) -> Any:
        return self.offset

    def setOffset(self, wobble: Any) -> None:
        self.offset = wobble

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
        lew.writePos(self.getPosition())
        lew.writePos(self.pixelsPerSecond)
        lew.writeShort(self.unk)
        lew.writeShort(self.fh)
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

