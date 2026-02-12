"""
MapleMapObjectType - 从Java源文件转换而来
对应Java源文件: server/maps/MapleMapObjectType.java
包路径: server.maps
"""

from enum import Enum, IntEnum


class MapleMapObjectType(Enum):
    """枚举类 MapleMapObjectType - 从Java枚举转换"""

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

