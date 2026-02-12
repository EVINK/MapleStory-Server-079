"""
MapleQuestRequirement - Converted from Java source
Original: server/quest/MapleQuestRequirement.java
Package: server.quest
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from typing import List
from typing import Optional, Any
import time

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleQuestRequirement:
    """
    Class MapleQuestRequirement
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, quest: Any, type: Any, data: Any):
        self.quest = None
        self.type = None
        self.intStore = 0
        self.stringStore = ""
        self.dataStore = []
        self.type = type
        self.quest = quest
        # switch (type):
            # case job:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    self.dataStore.add(new Pair<Integer, Integer>(i, MapleDataTool.getInt(child.get(i), -1)))
                break
            # case skill:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    childdata = child.get(i)
                    self.dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("acquire"), 0)))
                break
            # case quest:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    childdata = child.get(i)
                    self.dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id")), MapleDataTool.getInt(childdata.getChildByPath("state"), 0)))
                break
            # case item:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    childdata = child.get(i)
                    self.dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id")), MapleDataTool.getInt(childdata.getChildByPath("count"), 0)))
                break
            # case pettamenessmin:
            # case npc:
            # case questComplete:
            # case pop:
            # case interval:
            # case mbmin:
            # case lvmax:
            # case lvmin:
                self.intStore = MapleDataTool.getInt(data, -1)
                break
            # case end:
                self.stringStore = MapleDataTool.getString(data, None)
                break
            # case mob:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    childdata = child.get(i)
                    self.dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("count"), 0)))
                break
            # case fieldEnter:
                zeroField = data.getChildByPath("0")
                if zeroField is not None:
                    self.intStore = MapleDataTool.getInt(zeroField)
                    break
                self.intStore = -1
                break
            # case mbcard:
                child = data.getChildren()
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for i in range(child):
                    childdata = child.get(i)
                    self.dataStore.add(new Pair<Integer, Integer>(MapleDataTool.getInt(childdata.getChildByPath("id"), 0), MapleDataTool.getInt(childdata.getChildByPath("min"), 0)))
                break
            # case pet:
                self.dataStore = new LinkedList<Pair<Integer, Integer>>()
                for child2 in data:
                    self.dataStore.add(new Pair<Integer, Integer>(-1, MapleDataTool.getInt("id", child2, 0)))
                break


    def check(self, c: Any, npcid: int) -> bool:
        timeStr = None
        cal = None
        # switch (self.type):
            # case job:
            for a in self.dataStore:
                if (a.getRight()) == c.getJob() or c.isGM():
                return True
            return False
            # case skill:
            for a in self.dataStore:
                acquire = ((a.getRight()) > 0)
                skill = (a.getLeft())
                skil = SkillFactory.getSkill(skill)
                if acquire:
                    if skil.isFourthJob():
                        if c.getMasterLevel(skil) == 0:
                        return False
                        continue
                    if c.getSkillLevel(skil) == 0:
                    return False
                    continue
                if c.getSkillLevel(skil) > 0 or c.getMasterLevel(skil) > 0:
                return False
            return True
            # case quest:
            for a in self.dataStore:
                q = c.getQuest(MapleQuest.getInstance((a.getLeft())))
                state = (a.getRight())
                if (state == 0 or (
                q = = None and state == 0))
                continue
                if q is None or q.getStatus() != state:
                return False
            return True
            # case item:
            for a in self.dataStore:
                itemId = (a.getLeft())
                quantity = 0
                iType = GameConstants.getInventoryType(itemId)
                for item in c.getInventory(iType).listById(itemId):
                quantity = (short)(quantity + item.getQuantity())
                count = (a.getRight())
                if quantity < count or (count <= 0 and quantity > 0):
                return False
            return True
            # case lvmin:
            return (c.getLevel() >= self.intStore)
            # case lvmax:
            return (c.getLevel() <= self.intStore)
            # case end:
            timeStr = self.stringStore
            cal = Calendar.getInstance()
            cal.set(int(timeStr[0:4]), int(timeStr[4:6]), int(timeStr[6:8]), int(timeStr[8:10]), 0)
            return (cal.getTimeInMillis() >= int(time.time() * 1000))
            # case mob:
            for a in self.dataStore:
                mobId = (a.getLeft())
                killReq = (a.getRight())
                if c.getQuest(self.quest).getMobKills(mobId) < killReq:
                return False
            return True
            # case npc:
            return (npcid is None or npcid == self.intStore)
            # case fieldEnter:
            if self.intStore != -1:
            return (self.intStore == c.getMapId())
            return False
            # case mbmin:
            if c.getMonsterBook().getTotalCards() >= self.intStore:
            return True
            return False
            # case mbcard:
            for a in self.dataStore:
                cardId = (a.getLeft())
                killReq = (a.getRight())
                if c.getMonsterBook().getLevelByCard(cardId) < killReq:
                return False
            return True
            # case pop:
            return (c.getFame() <= self.intStore)
            # case questComplete:
            return (c.getNumQuest() >= self.intStore)
            # case interval:
            return (c.getQuest(self.quest).getStatus() != 2 or c.getQuest(self.quest).getCompletionTime() <= int(time.time() * 1000) - (self.intStore * 60) * 1000)
            # case pet:
            for a in self.dataStore:
                if c.getPetIndexById((a.getRight())) == -1:
                return False
            return True
            # case pettamenessmin:
            for pet in c.getPets():
                if pet.getSummoned() and pet.getCloseness() >= self.intStore:
                return True
            return False
        return True

    def getType(self) -> Any:
        return self.type

    def toString(self) -> str:
        return self.type

