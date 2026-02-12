"""
MapleQuestRequirementType - Converted from Java source
Original: server/quest/MapleQuestRequirementType.java
Package: server.quest
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleQuestRequirementType(Enum):
    """Enum MapleQuestRequirementType"""

    UNDEFINED = (-1)
    job = (0)
    item = (1)
    quest = (2)
    lvmin = (3)
    lvmax = (4)
    end = (5)
    mob = (6)
    npc = (7)
    fieldEnter = (8)
    interval = (9)
    startscript = (10)
    endscript = (10)
    pet = (11)
    pettamenessmin = (12)
    mbmin = (13)
    questComplete = (14)
    pop = (15)
    skill = (16)
    mbcard = (17)

    def getITEM(self) -> Any:
        return MapleQuestRequirementType.item

    def getType(self) -> int:
        return self.type

    def getByType(self, type: int) -> Any:
        for l in values():
            if l.getType() == type:
                return l
        return None

    def getByWZName(self, name: str) -> Any:
        try:
            return valueOf(name)
        except IllegalArgumentException as ex:
            return MapleQuestRequirementType.UNDEFINED

