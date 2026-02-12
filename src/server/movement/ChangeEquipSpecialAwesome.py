"""
ChangeEquipSpecialAwesome - Converted from Java source
Original: server/movement/ChangeEquipSpecialAwesome.java
Package: server.movement
"""

from typing import Optional, Any

# Internal module imports
# from tools.data.output.LittleEndianWriter import *  # TODO: import specific classes


class ChangeEquipSpecialAwesome(LifeMovementFragment):
    """
    Class ChangeEquipSpecialAwesome
    Implements: LifeMovementFragment
    """

    def __init__(self, wui: int):
        self.wui = 0
        self.wui = wui


    def serialize(self, lew: Any) -> None:
        lew.write(10)
        lew.write(self.wui)

    def getPosition(self) -> Any:
        return Point(0, 0)

