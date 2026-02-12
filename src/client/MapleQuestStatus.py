"""
MapleQuestStatus - Converted from Java source
Original: client/MapleQuestStatus.java
Package: client
"""

from typing import Dict
from typing import Iterator
from typing import Optional, Any
import math
import time

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes


class MapleQuestStatus:
    """
    Class MapleQuestStatus
    Implements: Serializable
    """

    def __init__(self, quest: Any, status: int):
        self.quest = None
        self.status = 0
        self.killedMobs = {}
        self.npc = 0
        self.completionTime = 0
        self.forfeited = 0
        self.customData = ""
        self.killedMobs = None
        self.forfeited = 0
        self.quest = quest
        self.setStatus(status)
        self.completionTime = int(time.time() * 1000)
        if status == 1 and not quest.getRelevantMobs() == 0:
            self.registerMobs()

    # Static initializer
    # MapleQuestStatus.serialVersionUID = 91795419934134


    def getQuest(self) -> Any:
        return self.quest

    def getStatus(self) -> int:
        return self.status

    def setStatus(self, status: int) -> None:
        self.status = status

    def getNpc(self) -> int:
        return self.npc

    def setNpc(self, npc: int) -> None:
        self.npc = npc

    def isCustom(self) -> bool:
        return GameConstants.isCustomQuest(self.quest.getId())

    def registerMobs(self) -> None:
        self.killedMobs = {}
        for i in self.quest.getRelevantMobs().keys():
            self.killedMobs.put(i, 0)

    def maxMob(self, mobid: int) -> int:
        for (final Map.Entry<Integer, Integer> qs : self.quest.getRelevantMobs().items())
            if qs.getKey() == mobid:
                return qs.getValue()
        return 0

    def mobKilled(self, id: int, skillID: int) -> bool:
        if self.quest is not None and self.quest.getSkillID() > 0 and self.quest.getSkillID() != skillID:
            return False
        mob = self.killedMobs.get(id)
        if mob is None:
            for (final Map.Entry<Integer, Integer> mo : self.killedMobs.items())
                if self.questCount(mo.getKey(), id):
                    mobb = self.maxMob(mo.getKey())
                    if mo.getValue() >= mobb:
                        return False
                    self.killedMobs.put(mo.getKey(), min(mo.getValue() + 1, mobb))
                    return True
            return False
        mo2 = self.maxMob(id)
        if mob >= mo2:
            return False
        self.killedMobs.put(id, min(mob + 1, mo2))
        return True

    def questCount(self, mo: int, id: int) -> bool:
        if MapleLifeFactory.getQuestCount(mo) is not None:
            for i in MapleLifeFactory.getQuestCount(mo):
                if i == id:
                    return True
        return False

    def setMobKills(self, id: int, count: int) -> None:
        if self.killedMobs is None:
            self.registerMobs()
        self.killedMobs.put(id, count)

    def hasMobKills(self) -> bool:
        return self.killedMobs is not None and self.killedMobs > 0

    def getMobKills(self, id: int) -> int:
        mob = self.killedMobs.get(id)
        if mob is None:
            return 0
        return mob

    def getCompletionTime(self) -> int:
        return self.completionTime

    def setCompletionTime(self, completionTime: int) -> None:
        self.completionTime = completionTime

    def getForfeited(self) -> int:
        return self.forfeited

    def setForfeited(self, forfeited: int) -> None:
        if forfeited >= self.forfeited:
            self.forfeited = forfeited
            return
        raise ValueError("Can't set forfeits to something lower than before.")

    def setCustomData(self, customData: str) -> None:
        self.customData = customData

    def getCustomData(self) -> str:
        return self.customData

