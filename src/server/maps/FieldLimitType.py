"""
FieldLimitType - Converted from Java source
Original: server/maps/FieldLimitType.java
Package: server.maps
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class FieldLimitType(Enum):
    """Enum FieldLimitType"""

    Jump = (1)
    MovementSkills = (2)
    SummoningBag = (4)
    MysticDoor = (8)
    ChannelSwitch = (16)
    RegularExpLoss = (32)
    VipRock = (64)
    Minigames = (128)
    NoClue1 = (256)
    Mount = (512)
    PotionUse = (1024)
    Event = (8192)
    Pet = (32768)
    Event2 = (65536)
    DropDown = (131072)

    def __init__(self, i):
        self._i = i

    def getValue(self) -> int:
        return self.i

    def check(self, fieldlimit: int) -> bool:
        return (fieldlimit & self.i) == self.i

