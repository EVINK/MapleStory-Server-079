"""
PartyOperation - Converted from Java source
Original: handling/world/PartyOperation.java
Package: handling.world
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class PartyOperation(Enum):
    """Enum PartyOperation"""

    JOIN = 0
    LEAVE = 1
    EXPEL = 2
    DISBAND = 3
    SILENT_UPDATE = 4
    LOG_ONOFF = 5
    CHANGE_LEADER = 6
    CHANGE_LEADER_DC = 7

