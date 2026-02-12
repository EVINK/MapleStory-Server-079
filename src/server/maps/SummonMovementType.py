"""
SummonMovementType - Converted from Java source
Original: server/maps/SummonMovementType.java
Package: server.maps
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class SummonMovementType(Enum):
    """Enum SummonMovementType"""

    不会移动 = (0)
    飞行跟随 = (1)
    WALK_STATIONARY = (2)
    跟随并且随机移动打怪 = (3)
    CIRCLE_STATIONARY = (4)

    def __init__(self, val):
        self._val = val

    def getValue(self) -> int:
        return self.val

