"""
MapleDataType - 从Java源文件转换而来
对应Java源文件: provider/WzXML/MapleDataType.java
包路径: provider.WzXML
"""

from enum import Enum, IntEnum


class MapleDataType(Enum):
    """枚举类 MapleDataType - 从Java枚举转换"""

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

