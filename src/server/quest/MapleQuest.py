"""
MapleQuest - Converted from Java source
Original: server/quest/MapleQuest.java
Package: server.quest
"""

from enum import Enum, IntEnum
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import sys

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from scripting.NPCScriptManager import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleQuest:
    """
    Class MapleQuest
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, id: int):
        self.id = 0
        self.startReqs = []
        self.completeReqs = []
        self.startActs = []
        self.completeActs = []
        self.partyQuestInfo = {}
        self.relevantMobs = {}
        self.autoStart = False
        self.autoPreComplete = False
        self.repeatable = False
        self.customend = False
        self.viewMedalItem = 0
        self.selectedSkillID = 0
        self.name = ""
        self.questid = 0
        self.level = 0
        self.lquestid = 0
        self.autoStart = False
        self.autoPreComplete = False
        self.repeatable = False
        self.customend = False
        self.viewMedalItem = 0
        self.selectedSkillID = 0
        self.name = ""
        self.relevantMobs = {}
        self.startReqs = []
        self.completeReqs = []
        self.startActs = []
        self.completeActs = []
        self.partyQuestInfo = new LinkedHashMap<String, List<Pair<String, Pair<String, Integer>>>>()
        self.id = id

    # Static initializer
    # quests = {}


    def loadQuest(self, ret: Any, id: int) -> bool:
        basedata1 = MapleQuest.requirements.getChildByPath(str(id))
        basedata2 = MapleQuest.actions.getChildByPath(str(id))
        if basedata1 is None or basedata2 is None:
            return False
        startReqData = basedata1.getChildByPath("0")
        if startReqData is not None:
            startC = startReqData.getChildren()
            if startC is not None and startC > 0:
                for startReq in startC:
                    type = MapleQuestRequirementType.getByWZName(startReq.getName())
                    if type == (MapleQuestRequirementType.interval):
                        ret.repeatable = True
                    req = MapleQuestRequirement(ret, type, startReq)
                    if req.getType() == (MapleQuestRequirementType.mob):
                        for mob in startReq.getChildren():
                            ret.relevantMobs.put(MapleDataTool.getInt(mob.getChildByPath("id")), MapleDataTool.getInt(mob.getChildByPath("count"), 0))
                    ret.startReqs.add(req)
        completeReqData = basedata1.getChildByPath("1")
        if completeReqData is not None:
            completeC = completeReqData.getChildren()
            if completeC is not None and completeC > 0:
                for completeReq in completeC:
                    req = MapleQuestRequirement(ret, MapleQuestRequirementType.getByWZName(completeReq.getName()), completeReq)
                    if req.getType() == (MapleQuestRequirementType.mob):
                        for mob in completeReq.getChildren():
                            ret.relevantMobs.put(MapleDataTool.getInt(mob.getChildByPath("id")), MapleDataTool.getInt(mob.getChildByPath("count"), 0))
                    elif req.getType() == (MapleQuestRequirementType.endscript):
                        ret.customend = True
                    ret.completeReqs.add(req)
        startActData = basedata2.getChildByPath("0")
        if startActData is not None:
            startC2 = startActData.getChildren()
            for startAct in startC2:
                ret.startActs.add(MapleQuestAction(MapleQuestActionType.getByWZName(startAct.getName()), startAct, ret))
        completeActData = basedata2.getChildByPath("1")
        if completeActData is not None:
            completeC2 = completeActData.getChildren()
            for completeAct in completeC2:
                ret.completeActs.add(MapleQuestAction(MapleQuestActionType.getByWZName(completeAct.getName()), completeAct, ret))
        questInfo = MapleQuest.info.getChildByPath(str(id))
        if questInfo is not None:
            ret.name = MapleDataTool.getString("name", questInfo, "")
            ret.autoStart = (MapleDataTool.getInt("autoStart", questInfo, 0) == 1)
            ret.autoPreComplete = (MapleDataTool.getInt("autoPreComplete", questInfo, 0) == 1)
            ret.viewMedalItem = MapleDataTool.getInt("viewMedalItem", questInfo, 0)
            ret.selectedSkillID = MapleDataTool.getInt("selectedSkillID", questInfo, 0)
        pquestInfo = MapleQuest.pinfo.getChildByPath(str(id))
        if pquestInfo is not None:
            for d in pquestInfo.getChildByPath("rank"):
                pInfo = new ArrayList<Pair<String, Pair<String, Integer>>>()
                for c in d:
                    for b in c:
                        pInfo.add(new Pair<String, Pair<String, Integer>>(c.getName(), new Pair<String, Integer>(b.getName(), MapleDataTool.getInt(b, 0))))
                ret.partyQuestInfo.put(d.getName(), pInfo)
        return True

    def initQuests(self) -> None:
        MapleQuest.questData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Quest.wz"))
        MapleQuest.actions = MapleQuest.questData.getData("Act.img")
        MapleQuest.requirements = MapleQuest.questData.getData("Check.img")
        MapleQuest.info = MapleQuest.questData.getData("QuestInfo.img")
        MapleQuest.pinfo = MapleQuest.questData.getData("PQuest.img")

    def clearQuests(self) -> None:
        MapleQuest.quests.clear()
        initQuests()

    @classmethod
    def get_instance(cls, id: int) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getInfoByRank(self, rank: str) -> list:
        return self.partyQuestInfo.get(rank)

    def getSkillID(self) -> int:
        return self.selectedSkillID

    def getName(self) -> str:
        return self.name

    def canStart(self, c: Any, npcid: int) -> bool:
        if c.getQuest(this).getStatus() != 0 and (c.getQuest(this).getStatus() != 2 or not self.repeatable):
            return False
        for r in self.startReqs:
            if not r.check(c, npcid):
                return False
        return True

    def canComplete(self, c: Any, npcid: int) -> bool:
        if c.getQuest(this).getStatus() != 1:
            return False
        for r in self.completeReqs:
            if not r.check(c, npcid):
                return False
        return True

    def RestoreLostItem(self, c: Any, itemid: int) -> None:
        for a in self.startActs:
            if a.RestoreLostItem(c, itemid):
                break

    def start(self, c: Any, npc: int) -> None:
        if (self.autoStart or self.checkNPCOnMap(c, npc)) and self.canStart(c, npc):
            for a in self.startActs:
                if not a.checkEnd(c, None):
                    return
            for a in self.startActs:
                a.runStart(c, None)
            if not self.customend:
                self.forceStart(c, npc, None)
            else:
                NPCScriptManager.getInstance().endQuest(c.getClient(), npc, self.getId(), True)

    def complete(self, c: Any, npc: int) -> None:
        self.complete(c, npc, None)

    def complete_c_npc_selection(self, c: Any, npc: int, selection: int) -> None:
        if (self.autoPreComplete or self.checkNPCOnMap(c, npc)) and self.canComplete(c, npc):
            if npc != 9010000:
                for a in self.completeActs:
                    if not a.checkEnd(c, selection):
                        return
                self.forceComplete(c, npc)
                for a in self.completeActs:
                    a.runEnd(c, selection)
            c.getClient().getSession().write(MaplePacketCreator.showSpecialEffect(10))
            c.getMap().broadcastMessage(c, MaplePacketCreator.showSpecialEffect(c.getId(), 10), False)
        else:
            if npc != 9010000:
                for a in self.completeActs:
                    if not a.checkEnd(c, selection):
                        return
                self.forceComplete(c, npc)
                for a in self.completeActs:
                    a.runEnd(c, selection)
            c.getClient().getSession().write(MaplePacketCreator.showSpecialEffect(10))
            c.getMap().broadcastMessage(c, MaplePacketCreator.showSpecialEffect(c.getId(), 10), False)

    def forfeit(self, c: Any) -> None:
        if c.getQuest(this).getStatus() != 1:
            return
        oldStatus = c.getQuest(this)
        newStatus = MapleQuestStatus(this, 0)
        newStatus.setForfeited(oldStatus.getForfeited() + 1)
        newStatus.setCompletionTime(oldStatus.getCompletionTime())
        c.updateQuest(newStatus)

    def forceStart(self, c: Any, npc: int, customData: str) -> None:
        newStatus = MapleQuestStatus(this, 1, npc)
        newStatus.setForfeited(c.getQuest(this).getForfeited())
        newStatus.setCompletionTime(c.getQuest(this).getCompletionTime())
        newStatus.setCustomData(customData)
        c.updateQuest(newStatus)

    def forceComplete(self, c: Any, npc: int) -> None:
        newStatus = MapleQuestStatus(this, 2, npc)
        newStatus.setForfeited(c.getQuest(this).getForfeited())
        c.updateQuest(newStatus)
        c.getClient().getSession().write(MaplePacketCreator.showSpecialEffect(10))
        c.getMap().broadcastMessage(c, MaplePacketCreator.showSpecialEffect(c.getId(), 10), False)

    def getId(self) -> int:
        return self.id

    def getRelevantMobs(self) -> dict:
        return self.relevantMobs

    def checkNPCOnMap(self, player: Any, npcid: int) -> bool:
        return (GameConstants.isEvan(player.getJob()) and npcid == 1013000) or (player.getMap() is not None and player.getMap().containsNPC(npcid))

    def getMedalItem(self) -> int:
        return self.viewMedalItem


# Inner class from Java (originally nested)
class MedalQuest(Enum):
    """Enum MedalQuest"""

    新手冒险家 = (29005, 29015, 15, new int[])
    ElNath = (29006, 29012, 50, new int[])
    LudusLake = (29007, 29012, 40, new int[])
    Underwater = (29008, 29012, 40, new int[])
    MuLung = (29009, 29012, 50, new int[])
    NihalDesert = (29010, 29012, 70, new int[])
    MinarForest = (29011, 29012, 70, new int[])
    Sleepywood = (29014, 29015, 50, new int[])

