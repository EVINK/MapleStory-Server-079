"""
MapleGuildResponse - Converted from Java source
Original: handling/world/guild/MapleGuildResponse.java
Package: handling.world.guild
"""

from enum import Enum, IntEnum
from typing import Optional, Any

# Internal module imports
# from handling.MaplePacket import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleGuildResponse(Enum):
    """Enum MapleGuildResponse"""

    NOT_IN_CHANNEL = (42)
    ALREADY_IN_GUILD = (40)
    NOT_IN_GUILD = (45)

    def __init__(self, val):
        self._val = val

    def getValue(self) -> int:
        return self.value

    def getPacket(self) -> Any:
        return MaplePacketCreator.genericGuildMessage(self.value)

