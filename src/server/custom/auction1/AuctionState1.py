"""
AuctionState1 - Converted from Java source
Original: server/custom/auction1/AuctionState1.java
Package: server.custom.auction1
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class AuctionState1(Enum):
    """Enum AuctionState1"""

    下架 = (0)
    上架 = (1)
    已售 = (2)

    def __init__(self, state1):
        self._state1 = state1

    def getState1(self) -> int:
        return self.state1

    def getState1(self, state1: int) -> Any:
        for as in values():
            if as.state1 == state1:
                return as
        return None

