"""
MapleQuestActionType - Converted from Java source
Original: server/quest/MapleQuestActionType.java
Package: server.quest
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleQuestActionType(Enum):
    """Enum MapleQuestActionType"""

    UNDEFINED = (-1)
    exp = (0)
    item = (1)
    nextQuest = (2)
    money = (3)
    quest = (4)
    skill = (5)
    pop = (6)
    buffItemID = (7)
    infoNumber = (8)
    yes = (9)
    no = (10)
    sp = (11)

    def __init__(self, type):
        self._type = type

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
            return MapleQuestActionType.UNDEFINED

