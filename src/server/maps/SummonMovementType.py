"""
SummonMovementType - 从Java源文件转换而来
对应Java源文件: server/maps/SummonMovementType.java
包路径: server.maps
"""

from enum import Enum, IntEnum


class SummonMovementType(Enum):
    """枚举类 SummonMovementType - 从Java枚举转换"""

    不会移动 = (0)
    飞行跟随 = (1)
    WALK_STATIONARY = (2)
    跟随并且随机移动打怪 = (3)
    CIRCLE_STATIONARY = (4)

    def __init__(self, val):
        """初始化枚举值"""
        self._val = val

    def getValue(self) -> int:
        """方法 getValue"""
        return 0

