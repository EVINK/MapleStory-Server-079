"""
AuctionState - Converted from Java source
Original: server/custom/auction/AuctionState.java
Package: server.custom.auction
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class AuctionState(Enum):
    """Enum AuctionState"""

    下架 = (0)
    上架 = (1)
    已售 = (2)

    def __init__(self, state):
        self._state = state

    def getState(self) -> int:
        return self.state

    def getState(self, state: int) -> Any:
        for as in values():
            if as.state == state:
                return as
        return None

