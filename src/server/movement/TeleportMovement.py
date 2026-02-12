"""
TeleportMovement - Converted from Java source
Original: server/movement/TeleportMovement.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class TeleportMovement(AbsoluteLifeMovement):
    """
    Class TeleportMovement
    Extends: AbsoluteLifeMovement
    """

    def __init__(self, type: int, position: Any, duration: int, newstate: int, newfh: int):
        super(type, position, duration, newstate)


    def serialize(self, lew: Any) -> None:
        lew.write(self.getType())
        lew.writeShort(self.getPosition().x)
        lew.writeShort(self.getPosition().y)
        lew.writeShort(self.getPixelsPerSecond().x)
        lew.writeShort(self.getPixelsPerSecond().y)
        lew.write(self.getNewstate())

