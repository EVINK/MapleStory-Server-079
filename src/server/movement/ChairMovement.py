"""
ChairMovement - Converted from Java source
Original: server/movement/ChairMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class ChairMovement(AbstractLifeMovement):
    """
    Class ChairMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        self.unk = 0
        super(type, position, duration, newstate)


    def getUnk(self) -> int:
        return self.unk

    def setUnk(self, unk: int) -> None:
        self.unk = unk

    def serialize(self, lew: Any) -> None:
        lew.write(self.getType())
        lew.writeShort(self.getPosition().x)
        lew.writeShort(self.getPosition().y)
        lew.writeShort(self.unk)
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

