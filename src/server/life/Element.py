"""
Element - Converted from Java source
Original: server/life/Element.java
Package: server.life
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class Element(Enum):
    """Enum Element"""

    NEUTRAL = 0
    PHYSICAL = 1
    FIRE = 2
    ICE = 3
    LIGHTING = 4
    POISON = 5
    HOLY = 6
    DARKNESS = 7

    def getFromChar(self, c: str) -> Any:
        # switch (Character.toUpperCase(c)):
            # case 'F':
                return Element.FIRE
            # case 'I':
                return Element.ICE
            # case 'L':
                return Element.LIGHTING
            # case 'S':
                return Element.POISON
            # case 'H':
                return Element.HOLY
            # case 'P':
                return Element.NEUTRAL
            # default:
                raise ValueError("unknown elemnt char " + c)

