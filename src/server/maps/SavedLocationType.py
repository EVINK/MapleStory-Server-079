"""
SavedLocationType - 从Java源文件转换而来
对应Java源文件: server/maps/SavedLocationType.java
包路径: server.maps
"""

from enum import Enum, IntEnum


class SavedLocationType(Enum):
    """枚举类 SavedLocationType - 从Java枚举转换"""

    FREE_MARKET = (0)
    MULUNG_TC = (1)
    WORLDTOUR = (2)
    FLORINA = (3)
    FISHING = (4)
    RICHIE = (5)
    DONGDONGCHIANG = (6)
    EVENT = (7)
    AMORIA = (8)
    CHRISTMAS = (9)
    MONSTER_CARNIVAL = (10)
    PVP = (11)
    HOTEL = (12)
    PACH = (13)
    Pachinko_port = (14)
    DOJO = (15)
    CYGNUSINTRO = (16)
    ENGLISH = (17)
    SLEEP = (18)
    ARIANT = (19)
    ARIANT_PQ = (20)
    WEDDING = (21)

    def __init__(self, index):
        """初始化枚举值"""
        self._index = index

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)

    def fromString(self, Str: str) -> Any:
        """方法 fromString"""
        raise NotImplementedError("方法 fromString 尚未实现")

