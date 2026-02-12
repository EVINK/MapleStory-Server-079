"""
ItemFlag - Converted from Java source
Original: client/inventory/ItemFlag.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class ItemFlag(Enum):
    """Enum ItemFlag"""

    LOCK = (1)
    SPIKES = (2)
    COLD = (4)
    UNTRADEABLE = (8)
    KARMA_EQ = (16)
    KARMA_USE = (2)

    def __init__(self, i):
        self._i = i

    def getValue(self) -> int:
        return self.i

    def check(self, flag: int) -> bool:
        return (flag & self.i) == self.i

