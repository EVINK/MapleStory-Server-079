"""
CheatTracker - Converted from Java source
Original: client/anticheat/CheatTracker.java
Package: client.anticheat
"""

from concurrent.futures import Future
from threading import Lock
from threading import RLock
from typing import Dict
from typing import List
from typing import Optional, Any
from weakref import ref
import math
import sched
import threading
import time
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class CheatTracker:
    """
    Class CheatTracker
    """

    def __init__(self, chr: Any):
        self.lock = None
        self.rL = None
        self.wL = None
        self.offenses = None
        self.chr = None
        self.lastAttackTickCount = 0
        self.Attack_tickResetCount = 0
        self.Server_ClientAtkTickDiff = 0
        self.lastDamage = 0
        self.takingDamageSince = 0
        self.numSequentialDamage = 0
        self.lastDamageTakenTime = 0
        self.numZeroDamageTaken = 0
        self.numSequentialSummonAttack = 0
        self.summonSummonTime = 0
        self.numSameDamage = 0
        self.lastMonsterMove = None
        self.monsterMoveCount = 0
        self.attacksWithoutHit = 0
        self.dropsPerSecond = 0
        self.lastDropTime = 0
        self.msgsPerSecond = 0
        self.lastMsgTime = 0
        self.gm_message = 0
        self.lastTickCount = 0
        self.tickSame = 0
        self.lastASmegaTime = 0
        self.lastSaveTime = 0
        self.lock = ReentrantReadWriteLock()
        self.rL = self.lock.readLock()
        self.wL = self.lock.writeLock()
        self.offenses = {}
        self.lastAttackTickCount = 0
        self.Attack_tickResetCount = 0
        self.Server_ClientAtkTickDiff = 0
        self.lastDamage = 0
        self.numSequentialDamage = 0
        self.lastDamageTakenTime = 0
        self.numZeroDamageTaken = 0
        self.numSequentialSummonAttack = 0
        self.summonSummonTime = 0
        self.numSameDamage = 0
        self.attacksWithoutHit = 0
        self.dropsPerSecond = 0
        self.lastDropTime = 0
        self.msgsPerSecond = 0
        self.lastMsgTime = 0
        self.gm_message = 50
        self.lastTickCount = 0
        self.tickSame = 0
        self.lastASmegaTime = 0
        self.lastTime = new long[6]
        self.lastSaveTime = 0
        self.chr = new WeakReference<MapleCharacter>(chr)
        self.invalidationTask = Timer.CheatTimer.getInstance().register(InvalidationTask(), 60000)
        self.takingDamageSince = int(time.time() * 1000)


    def checkAttack(self, skillId: int, tickcount: int) -> None:
        AtkDelay = GameConstants.getAttackDelay(skillId)
        if tickcount - self.lastAttackTickCount < AtkDelay:
            self.registerOffense(CheatingOffense.快速攻击)
        STime_TC = int(time.time() * 1000) - tickcount
        if self.Server_ClientAtkTickDiff - STime_TC > 250:
            self.registerOffense(CheatingOffense.快速攻击2)
        self.Attack_tickResetCount += 1
        if self.Attack_tickResetCount >= ((AtkDelay <= 200) ? 2 : 4):
            self.Attack_tickResetCount = 0
            self.Server_ClientAtkTickDiff = STime_TC
        self.chr.get().updateTick(tickcount)
        self.lastAttackTickCount = tickcount

    def checkTakeDamage(self, damage: int) -> None:
        self.numSequentialDamage += 1
        self.lastDamageTakenTime = int(time.time() * 1000)
        if self.lastDamageTakenTime - self.takingDamageSince / 500 < self.numSequentialDamage:
            self.registerOffense(CheatingOffense.怪物碰撞过快)
        if self.lastDamageTakenTime - self.takingDamageSince > 4500:
            self.takingDamageSince = self.lastDamageTakenTime
            self.numSequentialDamage = 0
        if damage == 0:
            self.numZeroDamageTaken += 1
            if self.numZeroDamageTaken >= 35:
                self.numZeroDamageTaken = 0
                self.registerOffense(CheatingOffense.回避率过高)
        elif damage != -1:
            self.numZeroDamageTaken = 0

    def checkSameDamage(self, dmg: int) -> None:
        if dmg > 2000 and self.lastDamage == dmg:
            self.numSameDamage += 1
            if self.numSameDamage > 5:
                self.numSameDamage = 0
                self.registerOffense(CheatingOffense.伤害相同, self.numSameDamage + " times: " + dmg)
        else:
            self.lastDamage = dmg
            self.numSameDamage = 0

    def checkMoveMonster(self, pos: Any, chr: Any) -> None:
        if pos == (self.lastMonsterMove):
            self.monsterMoveCount += 1
            if self.monsterMoveCount > 50:
                self.registerOffense(CheatingOffense.吸怪)
                self.monsterMoveCount = 0
                World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, "[管理员信息] 开挂玩家[" + MapleCharacterUtil.makeMapleReadable(chr.getName()) + "] 地图ID[" + chr.getMapId() + "] 怀疑使用吸怪! ").encode("utf-8"))
                note = "时间：" + FileoutputUtil.CurrentReadable_Time() + " or 玩家名字：" + chr.getName() + " or 玩家地图：" + chr.getMapId() + "\r\n"
                FileoutputUtil.packetLog("logs/吸怪检测/" + chr.getName() + ".log", note)
        else:
            self.lastMonsterMove = pos
            self.monsterMoveCount = 1

    def resetSummonAttack(self) -> None:
        self.summonSummonTime = int(time.time() * 1000)
        self.numSequentialSummonAttack = 0

    def checkSummonAttack(self) -> bool:
        self.numSequentialSummonAttack += 1
        if (int(time.time() * 1000) - self.summonSummonTime) / 2001 < self.numSequentialSummonAttack:
            self.registerOffense(CheatingOffense.召唤兽快速攻击)
            return False
        return True

    def checkDrop(self) -> None:
        self.checkDrop(False)

    def checkDrop_dc(self, dc: bool) -> None:
        if int(time.time() * 1000) - self.lastDropTime < 1000:
            self.dropsPerSecond += 1
            if self.dropsPerSecond >= (dc ? 32 : 16) and self.chr.get() is not None:
                self.chr.get().getClient().setMonitored(True)
        else:
            self.dropsPerSecond = 0
        self.lastDropTime = int(time.time() * 1000)

    def canAvatarSmega2(self) -> bool:
        if self.lastASmegaTime + 10000 > int(time.time() * 1000) and self.chr.get() is not None and not self.chr.get().isGM():
            return False
        self.lastASmegaTime = int(time.time() * 1000)
        return True

    def GMSpam(self, limit: int, type: int) -> bool:
        if type < 0 or self.len(lastTime) < type:
            type = 1
        if int(time.time() * 1000) < limit + self.lastTime[type]:
            return True
        self.lastTime[type] = int(time.time() * 1000)
        return False

    def checkMsg(self) -> None:
        if int(time.time() * 1000) - self.lastMsgTime < 1000:
            self.msgsPerSecond += 1
        else:
            self.msgsPerSecond = 0
        self.lastMsgTime = int(time.time() * 1000)

    def getAttacksWithoutHit(self) -> int:
        return self.attacksWithoutHit

    def setAttacksWithoutHit(self, increase: bool) -> None:
        if increase:
            self.attacksWithoutHit += 1
        else:
            self.attacksWithoutHit = 0

    def registerOffense(self, offense: Any) -> None:
        self.registerOffense(offense, None)

    def registerOffense_offense_param(self, offense: Any, param: str) -> None:
        chrhardref = self.chr.get()
        if chrhardref is None or not offense.isEnabled() or chrhardref.isClone() or chrhardref.isGM():
            return
        entry = None
        self.rL.lock()
        try:
            entry = self.offenses.get(offense)
        finally:
            self.rL.unlock()
        if entry is not None and entry.isExpired():
            self.expireEntry(entry)
            entry = None
        if entry is None:
            entry = CheatingOffenseEntry(offense, chrhardref.getId())
        if param is not None:
            entry.setParam(param)
        entry.incrementCount()
        if offense.shouldAutoban(entry.getCount()):
            type = offense.getBanType()
            if type != 1:
                if type != 2:
                    if (type == 3) {}
            self.gm_message = 50
            return
        self.wL.lock()
        try:
            self.offenses.put(offense, entry)
        finally:
            self.wL.unlock()
        # switch (offense):
            # case 魔法伤害过高:
            # case 魔法伤害过高2:
            # case 攻击过高2:
            # case 攻击力过高:
            # case 快速攻击:
            # case 快速攻击2:
            # case 攻击范围过大:
            # case 召唤兽攻击范围过大:
            # case 伤害相同:
            # case 吸怪:
            # case 怪物移动:
            # case 回避率过高:
                show = offense.name()
                self.gm_message -= 1
                if self.gm_message % 5 == 0:
                    msg = "[管理员信息] " + chrhardref.getName() + " 疑似 " + show + "地图ID [" + chrhardref.getMapId() + "]" + ((param is None) ? "" : (" - " + param))
                    World.Broadcast.broadcastGMMessage(MaplePacketCreator.serverNotice(6, msg).encode("utf-8"))
                    FileoutputUtil.logToFile_chr(chrhardref, FileoutputUtil.hack_log, show)
                if self.gm_message == 0:
                    self.gm_message = 50
                    break
                break
        CheatingOffensePersister.getInstance().persistEntry(entry)

    def updateTick(self, newTick: int) -> None:
        if newTick == self.lastTickCount:
            self.tickSame += 1
        else:
            self.tickSame = 0
        self.lastTickCount = newTick

    def expireEntry(self, coe: Any) -> None:
        self.wL.lock()
        try:
            self.offenses.remove(coe.getOffense())
        finally:
            self.wL.unlock()

    def getPoints(self) -> int:
        ret = 0
        self.rL.lock()
        offenses_copy = None
        try:
            offenses_copy = self.offenses.values()])
        finally:
            self.rL.unlock()
        for entry in offenses_copy:
            if entry.isExpired():
                self.expireEntry(entry)
            else:
                ret += entry.getPoints()
        return ret

    def getOffenses(self) -> dict:
        return Collections.unmodifiableMap((Map<? extends CheatingOffense, ? extends CheatingOffenseEntry>)self.offenses)

    def getSummary(self) -> str:
        ret = ""
        offenseList = []
        self.rL.lock()
        try:
            for entry in self.offenses.values():
                if not entry.isExpired():
                    offenseList.add(entry)
        finally:
            self.rL.unlock()
        Collections.sort(offenseList, new Comparator<CheatingOffenseEntry>()
            public final int compare(final CheatingOffenseEntry o1, final CheatingOffenseEntry o2)
                thisVal = o1.getPoints()
                anotherVal = o2.getPoints()
                return (thisVal < anotherVal) ? 1 : ((thisVal == anotherVal) ? 0 : -1)
        to = min(offenseList, 4), x = 0
        while x < to:
            ret.append(StringUtil.makeEnumHumanReadable(offenseList.get(x).getOffense().name()))
            ret.append(": ")
            ret.append(offenseList.get(x).getCount())
            if x != to - 1:
                ret.append(" ")
        return ret

    def compare(self, o1: Any, o2: Any) -> int:
        thisVal = o1.getPoints()
        anotherVal = o2.getPoints()
        return (thisVal < anotherVal) ? 1 : ((thisVal == anotherVal) ? 0 : -1)

    def dispose(self) -> None:
        if self.invalidationTask is not None:
            self.invalidationTask.cancel(False)
        self.invalidationTask = None

    def canSaveDB(self) -> bool:
        if self.lastSaveTime + 180000 > int(time.time() * 1000) and self.chr.get() is not None:
            return False
        self.lastSaveTime = int(time.time() * 1000)
        return True

    def getlastSaveTime(self) -> int:
        if self.lastSaveTime <= 0:
            self.lastSaveTime = int(time.time() * 1000)
        seconds = (int)((self.lastSaveTime + 180000 - int(time.time() * 1000)) / 1000)
        return seconds

    def run(self) -> None:
        CheatTracker.self.rL.lock()
        offenses_copy = None
        try:
            offenses_copy = (CheatingOffenseEntry[])CheatTracker.self.offenses.values()])
        finally:
            CheatTracker.self.rL.unlock()
        for offense in offenses_copy:
            if offense.isExpired():
                CheatTracker.self.expireEntry(offense)
        if CheatTracker.self.chr.get() is None:
            CheatTracker.self.dispose()


# Inner class from Java (originally nested)
class InvalidationTask(Runnable):
    """
    Class InvalidationTask
    Implements: Runnable
    """


    def run(self) -> None:
        CheatTracker.self.rL.lock()
        offenses_copy = None
        try:
            offenses_copy = (CheatingOffenseEntry[])CheatTracker.self.offenses.values()])
        finally:
            CheatTracker.self.rL.unlock()
        for offense in offenses_copy:
            if offense.isExpired():
                CheatTracker.self.expireEntry(offense)
        if CheatTracker.self.chr.get() is None:
            CheatTracker.self.dispose()

