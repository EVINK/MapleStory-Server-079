"""
AttackType - Converted from Java source
Original: handling/channel/handler/AttackType.java
Package: handling.channel.handler
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class AttackType(Enum):
    """Enum AttackType"""

    NON_RANGED = 0
    RANGED = 1
    RANGED_WITH_SHADOWPARTNER = 2
    NON_RANGED_WITH_MIRROR = 3

