"""
MapleMapObjectType - Converted from Java source
Original: server/maps/MapleMapObjectType.java
Package: server.maps
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleMapObjectType(Enum):
    """Enum MapleMapObjectType"""

    NPC = 0
    MONSTER = 1
    ITEM = 2
    PLAYER = 3
    DOOR = 4
    SUMMON = 5
    SHOP = 6
    MIST = 7
    REACTOR = 8
    LOVE = 9
    HIRED_MERCHANT = 10

