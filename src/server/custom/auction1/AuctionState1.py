"""
AuctionState1 - 从Java源文件转换而来
对应Java源文件: server/custom/auction1/AuctionState1.java
包路径: server.custom.auction1
"""

from enum import Enum, IntEnum


class AuctionState1(Enum):
    """枚举类 AuctionState1 - 从Java枚举转换"""

    下架 = (0)
    上架 = (1)
    已售 = (2)

    def __init__(self, state1):
        """初始化枚举值"""
        self._state1 = state1

    def getState1(self) -> int:
        """方法 getState1"""
        return getattr(self, 'state1', 0)

    def getState1(self, state1: int) -> Any:
        """方法 getState1"""
        raise NotImplementedError("方法 getState1 尚未实现")

