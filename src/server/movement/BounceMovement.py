"""
BounceMovement - Converted from Java source
Original: server/movement/BounceMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class BounceMovement(AbstractLifeMovement):
    """
    Class BounceMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.unk = 0
        self.fh = 0
        super(type, position, duration, newstate)


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
        lew.writeShort(self.getUnk())
        lew.writeShort(self.getFH())
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

