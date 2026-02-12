"""
AuctionState - 从Java源文件转换而来
对应Java源文件: server/custom/auction/AuctionState.java
包路径: server.custom.auction
"""

from enum import Enum, IntEnum


class AuctionState(Enum):
    """枚举类 AuctionState - 从Java枚举转换"""

    下架 = (0)
    上架 = (1)
    已售 = (2)

    def __init__(self, state):
        """初始化枚举值"""
        self._state = state

    def getState(self) -> int:
        """方法 getState"""
        return getattr(self, 'state', 0)

    def getState(self, state: int) -> Any:
        """方法 getState"""
        raise NotImplementedError("方法 getState 尚未实现")

