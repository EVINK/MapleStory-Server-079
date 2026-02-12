"""
AbsoluteLifeMovement - Converted from Java source
Original: server/movement/AbsoluteLifeMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class AbsoluteLifeMovement(AbstractLifeMovement):
    """
    Class AbsoluteLifeMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.pixelsPerSecond = None
        self.offset = None
        self.unk = 0
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

    def serialize(self, lew: Any) -> None:
        lew.write(self.getType())
        lew.writePos(self.getPosition())
        lew.writePos(self.pixelsPerSecond)
        lew.writeShort(self.unk)
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

