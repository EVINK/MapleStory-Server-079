"""
MapleInventoryType - Converted from Java source
Original: client/inventory/MapleInventoryType.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleInventoryType(Enum):
    """Enum MapleInventoryType"""

    UNDEFINED = (0)
    EQUIP = (1)
    USE = (2)
    SETUP = (3)
    ETC = (4)
    CASH = (5)
    EQUIPPED = (-1)

    def getType(self) -> int:
        return self.type

    def getBitfieldEncoding(self) -> int:
        return (short)(2 << self.type)

    def getByType(self, type: int) -> Any:
        for l in values():
            if l.getType() == type:
            return l
        return None

    def getByWZName(self, name: str) -> Any:
        # switch (name):
            # case "Install":
            return SETUP
            # case "Consume":
            return USE
            # case "Etc":
            return ETC
            # case "Cash":
            return CASH
            # case "Pet":
            return CASH
        return UNDEFINED

