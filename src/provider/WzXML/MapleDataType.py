"""
MapleDataType - Converted from Java source
Original: provider/WzXML/MapleDataType.java
Package: provider.WzXML
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleDataType(Enum):
    """Enum MapleDataType"""

    NONE = 0
    IMG_0x00 = 1
    SHORT = 2
    INT = 3
    FLOAT = 4
    DOUBLE = 5
    STRING = 6
    EXTENDED = 7
    PROPERTY = 8
    CANVAS = 9
    VECTOR = 10
    CONVEX = 11
    SOUND = 12
    UOL = 13
    UNKNOWN_TYPE = 14
    UNKNOWN_EXTENDED_TYPE = 15

