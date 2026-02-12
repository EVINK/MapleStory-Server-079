"""
ElementalEffectiveness - Converted from Java source
Original: server/life/ElementalEffectiveness.java
Package: server.life
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class ElementalEffectiveness(Enum):
    """Enum ElementalEffectiveness"""

    正常 = 0
    免疫 = 1
    增强 = 2
    虚弱 = 3
    NEUTRAL = 4

    def getByNumber(self, num: int) -> Any:
        # switch (num):
            # case 1:
                return ElementalEffectiveness.免疫
            # case 2:
                return ElementalEffectiveness.增强
            # case 3:
                return ElementalEffectiveness.虚弱
            # case 4:
                return ElementalEffectiveness.NEUTRAL
            # default:
                raise ValueError("Unkown effectiveness: " + num)

