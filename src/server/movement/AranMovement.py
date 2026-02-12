"""
AranMovement - Converted from Java source
Original: server/movement/AranMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class AranMovement(AbstractLifeMovement):
    """
    Class AranMovement
    Extends: AbstractLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int):
        super(type, position, duration, newstate)


    def serialize(self, lew: Any) -> None:
        lew.write(self.getType())
        lew.write(self.getNewstate())
        lew.writeShort(self.getDuration())

