"""
MapleInventoryType - 从Java源文件转换而来
对应Java源文件: client/inventory/MapleInventoryType.java
包路径: client.inventory
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleInventoryType(Enum):
    """枚举类 MapleInventoryType - 从Java枚举转换"""

    UNDEFINED = (0)
    EQUIP = (1)
    USE = (2)
    SETUP = (3)
    ETC = (4)
    CASH = (5)
    EQUIPPED = (-1)

    def getType(self) -> int:
        """方法 getType"""
        return getattr(self, 'type', 0)

    def getBitfieldEncoding(self) -> int:
        """方法 getBitfieldEncoding"""
        return getattr(self, 'bitfield_encoding', 0)

    def getByType(self, type: int) -> Any:
        """方法 getByType"""
        raise NotImplementedError("方法 getByType 尚未实现")

    def getByWZName(self, name: str) -> Any:
        """方法 getByWZName"""
        raise NotImplementedError("方法 getByWZName 尚未实现")

