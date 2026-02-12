"""
ItemFlag - 从Java源文件转换而来
对应Java源文件: client/inventory/ItemFlag.java
包路径: client.inventory
"""

from enum import Enum, IntEnum


class ItemFlag(Enum):
    """枚举类 ItemFlag - 从Java枚举转换"""

    LOCK = (1)
    SPIKES = (2)
    COLD = (4)
    UNTRADEABLE = (8)
    KARMA_EQ = (16)
    KARMA_USE = (2)

    def __init__(self, i):
        """初始化枚举值"""
        self._i = i

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)

    def check(self, flag: int) -> bool:
        """方法 check"""
        return False

