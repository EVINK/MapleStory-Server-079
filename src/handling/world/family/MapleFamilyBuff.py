"""
MapleFamilyBuff - Converted from Java source
Original: handling/world/family/MapleFamilyBuff.java
Package: handling.world.family
"""

from concurrent.futures import Future
from typing import List
from typing import Optional, Any
import sched
import time

# Internal module imports
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleFamilyBuff:
    """
    Class MapleFamilyBuff
    """

    event = 2

    def __init__(self):
        self.name = ""
        self.desc = ""
        self.count = 0
        self.rep = 0
        self.type = 0
        self.index = 0
        self.questID = 0
        self.duration = 0
        self.effect = 0
        self.effects = []

    # Static initializer
    # type = new int[] { 0, 1, 2, 3, 4, 2, 3, 2, 3, 2, 3 }
    # duration = new int[] { 0, 0, 15, 15, 30, 15, 15, 30, 30, 30, 30 }
    # effect = new int[] { 0, 0, 150, 150, 200, 200, 200, 200, 200, 200, 200 }
    # rep = new int[] { 3, 5, 7, 8, 10, 12, 15, 20, 25, 40, 50 }
    # name = new String[] { "直接移动到学院成员身边", "直接召唤学院成员", "我的爆率 1.5倍(15分钟)", "我的经验值 1.5倍(15分钟)", "学院成员的团结(30分钟)", "我的爆率 2倍(15分钟)", "我的经验值 2倍(15分钟)", "我的爆率 2倍(30分钟)", "我的经验值 2倍(30分钟)", "我的组队爆率 2倍(30分钟)", "我的组队经验值 2倍(30分钟)" }
    # desc = new String[] { "[对象] 我\n[效果] 直接可以移动到指定的学院成员身边。", "[对象] 学院成员 1名\n[效果] 直接可以召唤指定的学院成员到现在的地图。", "[对象] 我\n[持续效果] 15分钟\n[效果] 打怪爆率增加到 #c1.5倍# \n※ 与爆率活动重叠时失效。", "[对象] 我\n[持续效果] 15分钟\n[效果] 打怪经验值增加到 #c1.5倍# \n※ 与经验值活动重叠时失效。", "[启动条件] 校谱最低层学院成员6名以上在线时\n[持续效果] 30分钟\n[效果] 爆率和经验值增加到 #c2倍# ※ 与爆率、经验值活动重叠时失效。", "[对象] 我\n[持续效果] 15分钟\n[效果] 打怪爆率增加到 #c2倍# \n※ 与爆率活动重叠时失效。", "[对象] 我\n[持续效果] 15分钟\n[效果] 打怪经验值增加到 #c2倍# \n※ 与经验值活动重叠时失效。", "[对象] 我\n[持续效果] 30分钟\n[效果] 打怪爆率增加到 #c2倍# \n※ 与爆率活动重叠时失效。", "[对象] 我\n[持续效果] 30分钟\n[效果] 打怪经验值增加到 #c2倍# \n※ 与经验值活动重叠时失效。", "[对象] 我所属组队\n[持续效果] 30分钟\n[效果] 打怪爆率增加到 #c2倍# \n※ 与爆率活动重叠时失效。", "[对象] 我所属组队\n[持续效果] 30分钟\n[效果] 打怪经验值增加到 #c2倍# \n※ 与经验值活动重叠时失效。" }
    # buffEntries = []
    # for i in range(2):
    # MapleFamilyBuff.buffEntries.add(MapleFamilyBuffEntry(i, MapleFamilyBuff.name[i], MapleFamilyBuff.desc[i], 1, MapleFamilyBuff.rep[i], MapleFamilyBuff.type[i], 190000 + i, MapleFamilyBuff.duration[i], MapleFamilyBuff.effect[i]))


    @staticmethod
    def getBuffEntry() -> list:
        return MapleFamilyBuff.buffEntries

    def getBuffEntry(self, i: int) -> Any:
        return MapleFamilyBuff.buffEntries.get(i)

    def getEffectId(self) -> int:
        # switch (self.type):
            # case 2:
                return 2022694
            # case 3:
                return 2450018
            # default:
                return 2022332

    def getEffects(self) -> list:
        ret = new ArrayList<Pair<MapleBuffStat, Integer>>()
        # switch (self.type):
            # case 2:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.掉落_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金币_率, self.effect))
                break
            # case 3:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.经验_率, self.effect))
                break
            # case 4:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.经验_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.掉落_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金币_率, self.effect))
                break
        return ret

    def applyTo(self, chr: Any) -> None:
        chr.getClient().getSession().write(MaplePacketCreator.giveBuff(-self.getEffectId(), self.duration * 60000, self.effects, None))
        eff = MapleItemInformationProvider.getInstance().getItemEffect(self.getEffectId())
        chr.cancelEffect(eff, True, -1, self.effects)
        starttime = int(time.time() * 1000)
        final MapleStatEffect.CancelEffectAction cancelAction = new MapleStatEffect.CancelEffectAction(chr, eff, starttime)
        final ScheduledFuture<?> schedule = Timer.BuffTimer.getInstance().schedule(cancelAction, starttime + self.duration * 60000 - starttime)
        chr.registerEffect(eff, starttime, schedule, self.effects)


# Inner class from Java (originally nested)
class MapleFamilyBuffEntry:
    """
    Class MapleFamilyBuffEntry
    """

    def __init__(self, index: int, name: str, desc: str, count: int, rep: int, type: int, questID: int, duration: int, effect: int):
        self.name = ""
        self.desc = ""
        self.count = 0
        self.rep = 0
        self.type = 0
        self.index = 0
        self.questID = 0
        self.duration = 0
        self.effect = 0
        self.effects = []
        self.name = name
        self.desc = desc
        self.count = count
        self.rep = rep
        self.type = type
        self.questID = questID
        self.index = index
        self.duration = duration
        self.effect = effect
        self.effects = self.getEffects()


    def getEffectId(self) -> int:
        # switch (self.type):
            # case 2:
                return 2022694
            # case 3:
                return 2450018
            # default:
                return 2022332

    def getEffects(self) -> list:
        ret = new ArrayList<Pair<MapleBuffStat, Integer>>()
        # switch (self.type):
            # case 2:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.掉落_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金币_率, self.effect))
                break
            # case 3:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.经验_率, self.effect))
                break
            # case 4:
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.经验_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.掉落_率, self.effect))
                ret.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金币_率, self.effect))
                break
        return ret

    def applyTo(self, chr: Any) -> None:
        chr.getClient().getSession().write(MaplePacketCreator.giveBuff(-self.getEffectId(), self.duration * 60000, self.effects, None))
        eff = MapleItemInformationProvider.getInstance().getItemEffect(self.getEffectId())
        chr.cancelEffect(eff, True, -1, self.effects)
        starttime = int(time.time() * 1000)
        final MapleStatEffect.CancelEffectAction cancelAction = new MapleStatEffect.CancelEffectAction(chr, eff, starttime)
        final ScheduledFuture<?> schedule = Timer.BuffTimer.getInstance().schedule(cancelAction, starttime + self.duration * 60000 - starttime)
        chr.registerEffect(eff, starttime, schedule, self.effects)

