"""
MapleQuestAction - Converted from Java source
Original: server/quest/MapleQuestAction.java
Package: server.quest
"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import math

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.InventoryException import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleQuestAction:
    """
    Class MapleQuestAction
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, type: Any, data: Any, quest: Any):
        self.type = None
        self.data = None
        self.quest = None
        self.type = type
        self.data = data
        self.quest = quest


    def canGetItem(self, item: Any, c: Any) -> bool:
        if item.getChildByPath("gender") is not None:
            gender = MapleDataTool.getInt(item.getChildByPath("gender"))
            if gender != 2 and gender != c.getGender():
                return False
        if item.getChildByPath("job") is not None:
            job = MapleDataTool.getInt(item.getChildByPath("job"))
            code = getJobBy5ByteEncoding(job)
            jobFound = False
            for codec in code:
                if codec / 100 == c.getJob() / 100:
                    jobFound = True
                    break
            if not jobFound and item.getChildByPath("jobEx") is not None:
                jobEx = MapleDataTool.getInt(item.getChildByPath("jobEx"))
                codeEx = getJobBy5ByteEncoding(jobEx)
                for codec2 in codeEx:
                    if codec2 / 100 == c.getJob() / 100:
                        jobFound = True
                        break
            return jobFound
        return True

    def getJobBy5ByteEncoding(self, encoded: int) -> list:
        ret = []
        if (encoded & 0x1) != 0x0:
            ret.add(0)
        if (encoded & 0x2) != 0x0:
            ret.add(100)
        if (encoded & 0x4) != 0x0:
            ret.add(200)
        if (encoded & 0x8) != 0x0:
            ret.add(300)
        if (encoded & 0x10) != 0x0:
            ret.add(400)
        if (encoded & 0x20) != 0x0:
            ret.add(500)
        if (encoded & 0x400) != 0x0:
            ret.add(1000)
        if (encoded & 0x800) != 0x0:
            ret.add(1100)
        if (encoded & 0x1000) != 0x0:
            ret.add(1200)
        if (encoded & 0x2000) != 0x0:
            ret.add(1300)
        if (encoded & 0x4000) != 0x0:
            ret.add(1400)
        if (encoded & 0x8000) != 0x0:
            ret.add(1500)
        if (encoded & 0x20000) != 0x0:
            ret.add(2001)
            ret.add(2200)
        if (encoded & 0x100000) != 0x0:
            ret.add(2000)
            ret.add(2001)
        if (encoded & 0x200000) != 0x0:
            ret.add(2100)
        if (encoded & 0x400000) != 0x0:
            ret.add(2001)
            ret.add(2200)
        if (encoded & 0x40000000) != 0x0:
            ret.add(3000)
            ret.add(3200)
            ret.add(3300)
            ret.add(3500)
        return ret

    def RestoreLostItem(self, c: Any, itemid: int) -> bool:
        if self.type == MapleQuestActionType.item:
            for iEntry in self.data.getChildren():
                retitem = MapleDataTool.getInt(iEntry.getChildByPath("id"), -1)
                counts = MapleDataTool.getInt(iEntry.getChildByPath("count"), -1)
                if retitem == itemid:
                    if not c.haveItem(retitem, counts, True, False):
                        c.removeAll(retitem)
                        MapleInventoryManipulator.addById(c.getClient(), retitem, counts, 0)
                    return True
        return False

    def runStart(self, c: Any, extSelection: int) -> None:
        # switch (self.type):
            # case exp:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                c.gainExp(MapleDataTool.getInt(self.data, 0) * GameConstants.getExpRate_Quest(c.getLevel()), True, True, True)
                break
            # case item:
                props = {}
                for iEntry in self.data.getChildren():
                    prop = iEntry.getChildByPath("prop")
                    if prop is not None and MapleDataTool.getInt(prop) != -1 and canGetItem(iEntry, c):
                        for i in range(MapleDataTool.getInt(iEntry.getChildByPath("prop"))):
                            props.put(props, MapleDataTool.getInt(iEntry.getChildByPath("id")))
                selection = 0
                extNum = 0
                if props > 0:
                    selection = props.get(Randomizer.nextInt(props))
                for iEntry2 in self.data.getChildren():
                    if not canGetItem(iEntry2, c):
                        continue
                    id = MapleDataTool.getInt(iEntry2.getChildByPath("id"), -1)
                    if iEntry2.getChildByPath("prop") is not None:
                        if MapleDataTool.getInt(iEntry2.getChildByPath("prop")) == -1:
                            if extSelection != extNum++:
                                continue
                        elif id != selection:
                            continue
                    count = MapleDataTool.getInt(iEntry2.getChildByPath("count"), 1)
                    if count < 0:
                        try:
                            MapleInventoryManipulator.removeById(c.getClient(), GameConstants.getInventoryType(id), id, count * -1, True, False)
                        except InventoryException as ie:
                            print("[h4x] Completing a quest without meeting the requirements" + ie)
                        c.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, count, True))
                    else:
                        period = MapleDataTool.getInt(iEntry2.getChildByPath("period"), 0) / 1440
                        name = MapleItemInformationProvider.getInstance().getName(id)
                        if id / 10000 == 114 and name is not None and name > 0:
                            msg = "你已獲得稱號 <" + name + ">"
                            c.dropMessage(5, msg)
                            c.dropMessage(5, msg)
                        MapleInventoryManipulator.addById(c.getClient(), id, count, "", None, period, 0)
                        c.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, count, True))
                break
            # case nextQuest:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                c.getClient().getSession().write(MaplePacketCreator.updateQuestFinish(self.quest.getId(), status.getNpc(), MapleDataTool.getInt(self.data)))
                break
            # case money:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                c.gainMeso(MapleDataTool.getInt(self.data, 0), True, False, True)
                break
            # case quest:
                for qEntry in self.data:
                    c.updateQuest(MapleQuestStatus(MapleQuest.getInstance(MapleDataTool.getInt(qEntry.getChildByPath("id"))), MapleDataTool.getInt(qEntry.getChildByPath("state"), 0)))
                break
            # case skill:
                for sEntry in self.data:
                    skillid = MapleDataTool.getInt(sEntry.getChildByPath("id"))
                    skillLevel = MapleDataTool.getInt(sEntry.getChildByPath("skillLevel"), 0)
                    masterLevel = MapleDataTool.getInt(sEntry.getChildByPath("masterLevel"), 0)
                    skillObject = SkillFactory.getSkill(skillid)
                    for applicableJob in sEntry.getChildByPath("job"):
                        if skillObject.isBeginnerSkill() or c.getJob() == MapleDataTool.getInt(applicableJob):
                            c.changeSkillLevel(skillObject, max(skillLevel, c.getSkillLevel(skillObject)), max(masterLevel, c.getMasterLevel(skillObject)))
                            break
                break
            # case pop:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                fameGain = MapleDataTool.getInt(self.data, 0)
                c.addFame(fameGain)
                c.updateSingleStat(MapleStat.FAME, c.getFame())
                c.getClient().getSession().write(MaplePacketCreator.getShowFameGain(fameGain))
                break
            # case buffItemID:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                tobuff = MapleDataTool.getInt(self.data, -1)
                if tobuff == -1:
                    break
                MapleItemInformationProvider.getInstance().getItemEffect(tobuff).applyTo(c)
                break
            # case sp:
                status = c.getQuest(self.quest)
                if status.getForfeited() > 0:
                    break
                for iEntry3 in self.data.getChildren():
                    sp_val = MapleDataTool.getInt(iEntry3.getChildByPath("sp_value"), 0)
                    if iEntry3.getChildByPath("job") is not None:
                        finalJob = 0
                        for jEntry in iEntry3.getChildByPath("job").getChildren():
                            job_val = MapleDataTool.getInt(jEntry, 0)
                            if c.getJob() >= job_val and job_val > finalJob:
                                finalJob = job_val
                        if finalJob == 0:
                            c.gainSP(sp_val)
                        else:
                            c.gainSP(sp_val, GameConstants.getSkillBook(finalJob))
                    else:
                        c.gainSP(sp_val)
                break

    def checkEnd(self, c: Any, extSelection: int) -> bool:
        # switch (self.type):
            # case item:
                props = {}
                for iEntry in self.data.getChildren():
                    prop = iEntry.getChildByPath("prop")
                    if prop is not None and MapleDataTool.getInt(prop) != -1 and canGetItem(iEntry, c):
                        for i in range(MapleDataTool.getInt(iEntry.getChildByPath("prop"))):
                            props.put(props, MapleDataTool.getInt(iEntry.getChildByPath("id")))
                selection = 0
                extNum = 0
                if props > 0:
                    selection = props.get(Randomizer.nextInt(props))
                eq = 0
                use = 0
                setup = 0
                etc = 0
                cash = 0
                for iEntry2 in self.data.getChildren():
                    if not canGetItem(iEntry2, c):
                        continue
                    id = MapleDataTool.getInt(iEntry2.getChildByPath("id"), -1)
                    if iEntry2.getChildByPath("prop") is not None:
                        if MapleDataTool.getInt(iEntry2.getChildByPath("prop")) == -1:
                            if extSelection != extNum++:
                                continue
                        elif id != selection:
                            continue
                    count = MapleDataTool.getInt(iEntry2.getChildByPath("count"), 1)
                    if count < 0:
                        if not c.haveItem(id, count, False, True):
                            c.dropMessage(1, "You are short of some item to complete quest.")
                            return False
                        continue
                    else:
                        if MapleItemInformationProvider.getInstance().isPickupRestricted(id) and c.haveItem(id, 1, True, False):
                            c.dropMessage(1, "You have this item already: " + MapleItemInformationProvider.getInstance().getName(id))
                            return False
                        # switch (GameConstants.getInventoryType(id)):
                            # case EQUIP:
                                eq += 1
                                continue
                            # case USE:
                                use += 1
                                continue
                            # case SETUP:
                                setup += 1
                                continue
                            # case ETC:
                                etc += 1
                                continue
                            # case CASH:
                                cash += 1
                                continue
                if c.getInventory(MapleInventoryType.EQUIP).getNumFreeSlot() < eq:
                    c.dropMessage(1, "请为您的装备栏腾出空间.")
                    return False
                if c.getInventory(MapleInventoryType.USE).getNumFreeSlot() < use:
                    c.dropMessage(1, "请为您的消耗栏腾出空间.")
                    return False
                if c.getInventory(MapleInventoryType.SETUP).getNumFreeSlot() < setup:
                    c.dropMessage(1, "请为您的设置栏腾出空间.")
                    return False
                if c.getInventory(MapleInventoryType.ETC).getNumFreeSlot() < etc:
                    c.dropMessage(1, "请为您的其他栏腾出空间.")
                    return False
                if c.getInventory(MapleInventoryType.CASH).getNumFreeSlot() < cash:
                    c.dropMessage(1, "请为您的特殊栏腾出空间.")
                    return False
                return True
            # case money:
                meso = MapleDataTool.getInt(self.data, 0)
                if c.getMeso() + meso < 0:
                    c.dropMessage(1, "Meso exceed the max amount, 2147483647.")
                    return False
                if meso < 0 and c.getMeso() < abs(meso):
                    c.dropMessage(1, "Insufficient meso.")
                    return False
                return True
            # default:
                return True

    def runEnd(self, c: Any, extSelection: int) -> None:
        # switch (self.type):
            # case exp:
                c.gainExp(MapleDataTool.getInt(self.data, 0) * GameConstants.getExpRate_Quest(c.getLevel()), True, True, True)
                break
            # case item:
                props = {}
                for iEntry in self.data.getChildren():
                    prop = iEntry.getChildByPath("prop")
                    if prop is not None and MapleDataTool.getInt(prop) != -1 and canGetItem(iEntry, c):
                        for i in range(MapleDataTool.getInt(iEntry.getChildByPath("prop"))):
                            props.put(props, MapleDataTool.getInt(iEntry.getChildByPath("id")))
                selection = 0
                extNum = 0
                if props > 0:
                    selection = props.get(Randomizer.nextInt(props))
                for iEntry2 in self.data.getChildren():
                    if not canGetItem(iEntry2, c):
                        continue
                    id = MapleDataTool.getInt(iEntry2.getChildByPath("id"), -1)
                    if iEntry2.getChildByPath("prop") is not None:
                        if MapleDataTool.getInt(iEntry2.getChildByPath("prop")) == -1:
                            if extSelection != extNum++:
                                continue
                        elif id != selection:
                            continue
                    count = MapleDataTool.getInt(iEntry2.getChildByPath("count"), 1)
                    if count < 0:
                        MapleInventoryManipulator.removeById(c.getClient(), GameConstants.getInventoryType(id), id, count * -1, True, False)
                        c.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, count, True))
                    else:
                        period = MapleDataTool.getInt(iEntry2.getChildByPath("period"), 0) / 1440
                        name = MapleItemInformationProvider.getInstance().getName(id)
                        if id / 10000 == 114 and name is not None and name > 0:
                            msg = "You have attained title <" + name + ">"
                            c.dropMessage(5, msg)
                            c.dropMessage(5, msg)
                        MapleInventoryManipulator.addById(c.getClient(), id, count, "", None, period, 0)
                        c.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, count, True))
                break
            # case nextQuest:
                c.getClient().getSession().write(MaplePacketCreator.updateQuestFinish(self.quest.getId(), c.getQuest(self.quest).getNpc(), MapleDataTool.getInt(self.data)))
                break
            # case money:
                c.gainMeso(MapleDataTool.getInt(self.data, 0), True, False, True)
                break
            # case quest:
                for qEntry in self.data:
                    c.updateQuest(MapleQuestStatus(MapleQuest.getInstance(MapleDataTool.getInt(qEntry.getChildByPath("id"))), MapleDataTool.getInt(qEntry.getChildByPath("state"), 0)))
                break
            # case skill:
                for sEntry in self.data:
                    skillid = MapleDataTool.getInt(sEntry.getChildByPath("id"))
                    skillLevel = MapleDataTool.getInt(sEntry.getChildByPath("skillLevel"), 0)
                    masterLevel = MapleDataTool.getInt(sEntry.getChildByPath("masterLevel"), 0)
                    skillObject = SkillFactory.getSkill(skillid)
                    for applicableJob in sEntry.getChildByPath("job"):
                        if skillObject.isBeginnerSkill() or c.getJob() == MapleDataTool.getInt(applicableJob):
                            c.changeSkillLevel(skillObject, max(skillLevel, c.getSkillLevel(skillObject)), max(masterLevel, c.getMasterLevel(skillObject)))
                            break
                break
            # case pop:
                fameGain = MapleDataTool.getInt(self.data, 0)
                c.addFame(fameGain)
                c.updateSingleStat(MapleStat.FAME, c.getFame())
                c.getClient().getSession().write(MaplePacketCreator.getShowFameGain(fameGain))
                break
            # case buffItemID:
                tobuff = MapleDataTool.getInt(self.data, -1)
                if tobuff == -1:
                    break
                MapleItemInformationProvider.getInstance().getItemEffect(tobuff).applyTo(c)
                break
            # case sp:
                for iEntry3 in self.data.getChildren():
                    sp_val = MapleDataTool.getInt(iEntry3.getChildByPath("sp_value"), 0)
                    if iEntry3.getChildByPath("job") is not None:
                        finalJob = 0
                        for jEntry in iEntry3.getChildByPath("job").getChildren():
                            job_val = MapleDataTool.getInt(jEntry, 0)
                            if c.getJob() >= job_val and job_val > finalJob:
                                finalJob = job_val
                        c.gainSP(sp_val, GameConstants.getSkillBook(finalJob))
                    else:
                        c.gainSP(sp_val)
                break

    def getType(self) -> Any:
        return self.type

    def toString(self) -> str:
        return self.type + ": " + self.data

