"""
MapleEventType - Converted from Java source
Original: server/events/MapleEventType.java
Package: server.events
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleEventType(Enum):
    """Enum MapleEventType"""

    打椰子比赛 = ("椰子比赛", new int[])
    打瓶盖比赛 = ("打瓶盖", new int[])
    向高地 = ("向高地", new int[])
    上楼上楼 = ("上楼~上楼~", new int[])
    快速0X猜题 = ("快速OX猜题", new int[])
    雪球赛 = ("雪球赛", new int[])

    def getByString(self, splitted: str) -> Any:
        for t in values():
            if t.command.lower() == splitted.lower():
                return t
        return None

