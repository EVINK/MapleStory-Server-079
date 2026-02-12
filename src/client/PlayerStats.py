"""
PlayerStats - Converted from Java source
Original: client/PlayerStats.java
Package: client
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from threading import RLock
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
from weakref import ref
import math
import threading
import weakref

# Internal module imports
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IEquip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MapleWeaponType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.StructSetItem import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class PlayerStats:
    """
    Class PlayerStats
    Implements: Serializable
    """

    serialVersionUID = -679541993413738569

    def __init__(self, chr: Any):
        self.chr = None
        self.setHandling = None
        self.durabilityHandling = None
        self.equipLevelHandling = None
        self.shouldHealHP = None
        self.shouldHealMP = None
        self.str = 0
        self.dex = 0
        self.luk = 0
        self.int_ = 0
        self.hp = 0
        self.maxhp = 0
        self.mp = 0
        self.maxmp = 0
        self.passive_sharpeye_percent = None
        self.localmaxhp = None
        self.localmaxmp = None
        self.passive_mastery = None
        self.passive_sharpeye_rate = None
        self.localstr = None
        self.localdex = None
        self.localluk = None
        self.localint_ = None
        self.magic = None
        self.watk = None
        self.hands = None
        self.accuracy = None
        self.equippedWelcomeBackRing = None
        self.equippedFairy = None
        self.hasMeso = None
        self.hasItem = None
        self.hasVac = None
        self.hasClone = None
        self.hasPartyBonus = None
        self.Berserk = None
        self.isRecalc = None
        self.equipmentBonusExp = None
        self.expMod = None
        self.dropMod = None
        self.cashMod = None
        self.setHandling = {}
        self.durabilityHandling = []
        self.equipLevelHandling = []
        self.Berserk = False
        self.isRecalc = False
        self.lock = ReentrantLock()
        self.chr = new WeakReference<MapleCharacter>(chr)


    def init(self) -> None:
        self.recalcLocalStats()
        self.relocHeal()

    def getStr(self) -> int:
        return self.str

    def getDex(self) -> int:
        return self.dex

    def getLuk(self) -> int:
        return self.luk

    def getInt(self) -> int:
        return self.int_

    def setStr(self, str: int) -> None:
        self.str = str
        self.recalcLocalStats()

    def setDex(self, dex: int) -> None:
        self.dex = dex
        self.recalcLocalStats()

    def setLuk(self, luk: int) -> None:
        self.luk = luk
        self.recalcLocalStats()

    def setInt(self, int_: int) -> None:
        self.int_ = int_
        self.recalcLocalStats()

    def setHp(self, newhp: int) -> bool:
        return self.setHp(newhp, False)

    def setHp_newhp_silent(self, newhp: int, silent: bool) -> bool:
        oldHp = self.hp
        thp = newhp
        if thp < 0:
            thp = 0
        if thp > self.localmaxhp:
            thp = self.localmaxhp
        self.hp = thp
        chra = self.chr.get()
        if chra is not None:
            if not silent:
                chra.updatePartyMemberHP()
            if oldHp > self.hp and not chra.isAlive():
                chra.playerDead()
        return self.hp != oldHp

    def setMp(self, newmp: int) -> bool:
        oldMp = self.mp
        tmp = newmp
        if tmp < 0:
            tmp = 0
        if tmp > self.localmaxmp:
            tmp = self.localmaxmp
        self.mp = tmp
        return self.mp != oldMp

    def setMaxHp(self, hp: int) -> None:
        self.maxhp = hp
        self.recalcLocalStats()

    def setMaxMp(self, mp: int) -> None:
        self.maxmp = mp
        self.recalcLocalStats()

    def getHp(self) -> int:
        return self.hp

    def getMaxHp(self) -> int:
        return self.maxhp

    def getMp(self) -> int:
        return self.mp

    def getMaxMp(self) -> int:
        return self.maxmp

    def getTotalDex(self) -> int:
        return self.localdex

    def getTotalInt(self) -> int:
        return self.localint_

    def getTotalStr(self) -> int:
        return self.localstr

    def getTotalLuk(self) -> int:
        return self.localluk

    def getTotalMagic(self) -> int:
        return self.magic

    def getSpeedMod(self) -> float:
        return self.speedMod

    def getJumpMod(self) -> float:
        return self.jumpMod

    def getTotalWatk(self) -> int:
        return self.watk

    def getCurrentMaxHp(self) -> int:
        return self.localmaxhp

    def getCurrentMaxMp(self) -> int:
        return self.localmaxmp

    def getHands(self) -> int:
        return self.hands

    def getCurrentMaxBaseDamage(self) -> float:
        return self.localmaxbasedamage

    def recalcLocalStats(self) -> None:
        self.recalcLocalStats(False)

    def recalcLocalStats_first_login(self, first_login: bool) -> None:
        chra = self.chr.get()
        if chra is None:
            return
        self.lock.lock()
        try:
            if self.isRecalc:
                return
            self.isRecalc = True
        finally:
            self.lock.unlock()
        ii = MapleItemInformationProvider.getInstance()
        oldmaxhp = self.localmaxhp
        localmaxhp_ = self.getMaxHp()
        localmaxmp_ = self.getMaxMp()
        self.localdex = self.getDex()
        self.localint_ = self.getInt()
        self.localstr = self.getStr()
        self.localluk = self.getLuk()
        speed = 100
        jump = 100
        percent_hp = 0
        percent_mp = 0
        percent_str = 0
        percent_dex = 0
        percent_int = 0
        percent_luk = 0
        percent_acc = 0
        percent_atk = 0
        percent_matk = 0
        added_sharpeye_rate = 0
        added_sharpeye_dmg = 0
        self.magic = self.localint_
        self.watk = 0
        if chra.getJob() == 500 or (chra.getJob() >= 520 and chra.getJob() <= 522):
            self.watk = 20
        elif chra.getJob() == 400 or (chra.getJob() >= 410 and chra.getJob() <= 412) or (chra.getJob() >= 1400 and chra.getJob() <= 1412):
            self.watk = 30
        self.dam_r = 1.0
        self.bossdam_r = 1.0
        self.expBuff = 100.0
        self.cashBuff = 100.0
        self.dropBuff = 100.0
        self.mesoBuff = 100.0
        self.recoverHP = 0
        self.recoverMP = 0
        self.mpconReduce = 0
        self.incMesoProp = 0
        self.incRewardProp = 0
        self.DAMreflect = 0
        self.DAMreflect_rate = 0
        self.hpRecover = 0
        self.hpRecoverProp = 0
        self.mpRecover = 0
        self.mpRecoverProp = 0
        self.mpRestore = 0
        self.equippedWelcomeBackRing = False
        self.equippedFairy = False
        self.hasMeso = False
        self.hasItem = False
        self.hasPartyBonus = False
        self.hasVac = False
        self.hasClone = False
        canEquipLevel = chra.getLevel() >= 120 and not GameConstants.isKOC(chra.getJob())
        self.equipmentBonusExp = 0
        self.RecoveryUP = 0
        self.dropMod = 1
        self.expMod = 1
        self.cashMod = 1
        self.levelBonus = 0
        self.incAllskill = 0
        self.durabilityHandling.clear()
        self.equipLevelHandling.clear()
        self.setHandling.clear()
        self.element_fire = 100
        self.element_ice = 100
        self.element_light = 100
        self.element_psn = 100
        self.def = 100
        self.canFish = False
        self.canFishVIP = False
        for item in chra.getInventory(MapleInventoryType.EQUIPPED):
            equip = item
            if equip.getPosition() == -11 and GameConstants.isMagicWeapon(equip.getItemId()):
                eqstat = MapleItemInformationProvider.getInstance().getEquipStats(equip.getItemId())
                self.element_fire = eqstat.get("incRMAF")
                self.element_ice = eqstat.get("incRMAI")
                self.element_light = eqstat.get("incRMAL")
                self.element_psn = eqstat.get("incRMAS")
                self.def = eqstat.get("elemDefault")
            self.accuracy += equip.getAcc()
            localmaxhp_ += equip.getHp()
            localmaxmp_ += equip.getMp()
            self.localdex += equip.getDex()
            self.localint_ += equip.getInt()
            self.localstr += equip.getStr()
            self.localluk += equip.getLuk()
            self.magic += equip.getMatk() + equip.getInt()
            self.watk += equip.getWatk()
            speed += equip.getSpeed()
            jump += equip.getJump()
            # switch (equip.getItemId()):
                # case 1112127:
                    self.equippedWelcomeBackRing = True
                    break
                # case 1122017:
                    self.equippedFairy = True
                    break
                # case 1812000:
                    self.hasMeso = True
                    break
                # case 1812001:
                    self.hasItem = True
                    break
                # default:
                    for eb_bonus in GameConstants.Equipments_Bonus:
                        if equip.getItemId() == eb_bonus:
                            self.equipmentBonusExp += GameConstants.道具佩戴附加经验值(eb_bonus)
                            break
                    break
            percent_hp += equip.getHpR()
            percent_mp += equip.getMpR()
            set = ii.getSetItemID(equip.getItemId())
            if set > 0:
                value = 1
                if self.setHandling.get(set) is not None:
                    value += self.setHandling.get(set)
                self.setHandling.put(set, value)
        for (final Map.Entry<Integer, Integer> entry : self.setHandling.items())
            set2 = ii.getSetItem(entry.getKey())
            if set2 is not None:
                final Map<Integer, StructSetItem.SetItem> itemz = set2.getItems()
                for (final Map.Entry<Integer, StructSetItem.SetItem> ent : itemz.items())
                    if ent.getKey() <= entry.getValue():
                        final StructSetItem.SetItem se = ent.getValue()
                        self.localstr += se.incSTR
                        self.localdex += se.incDEX
                        self.localint_ += se.incINT
                        self.localluk += se.incLUK
                        self.watk += se.incPAD
                        self.magic += se.incINT + se.incMAD
                        speed += se.incSpeed
                        self.accuracy += se.incACC
                        localmaxhp_ += se.incMHP
                        localmaxmp_ += se.incMMP
        day = Calendar.getInstance().get(7)
        hour = Calendar.getInstance().get(11)
        for item2 in chra.getInventory(MapleInventoryType.CASH):
            if self.expMod < 3 and (item2.getItemId() == 5211060 or item2.getItemId() == 5211050 or item2.getItemId() == 5211051 or item2.getItemId() == 5211052 or item2.getItemId() == 5211053 or item2.getItemId() == 5211054):
                self.expMod = 3
            elif self.expMod == 1 and (item2.getItemId() == 5210001 or item2.getItemId() == 5210004 or item2.getItemId() == 5211061 or item2.getItemId() == 5211000 or item2.getItemId() == 5211001 or item2.getItemId() == 5211002 or item2.getItemId() == 5211003 or item2.getItemId() == 5211046 or item2.getItemId() == 5211047 or item2.getItemId() == 5211048 or item2.getItemId() == 5211049):
                self.expMod = 2
            elif self.expMod == 1 and (item2.getItemId() == 5210005 or item2.getItemId() == 5210000):
                if day >= 2 and day <= 6:
                    if hour >= 18 or hour < 6:
                        self.expMod = 2
                elif day == 1 or day == 7:
                    self.expMod = 2
            elif self.expMod == 1 and (item2.getItemId() == 5210003 or item2.getItemId() == 5210002):
                if day >= 2 and day <= 6:
                    if hour < 18 and hour >= 6:
                        self.expMod = 2
                elif day == 1 or day == 7:
                    self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210006 and (hour >= 22 or hour <= 2):
                self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210007 and hour >= 2 and hour <= 6:
                self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210008 and hour >= 6 and hour <= 10:
                self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210009 and hour >= 10 and hour <= 14:
                self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210010 and hour >= 14 and hour <= 18:
                self.expMod = 2
            elif self.expMod == 1 and item2.getItemId() == 5210011 and hour >= 18 and hour <= 22:
                self.expMod = 2
            if self.dropMod == 1:
                if item2.getItemId() == 5360009 or item2.getItemId() == 5360010 or item2.getItemId() == 5360011 or item2.getItemId() == 5360012 or item2.getItemId() == 5360013 or item2.getItemId() == 5360014 or item2.getItemId() == 5360017 or item2.getItemId() == 5360050 or item2.getItemId() == 5360053 or item2.getItemId() == 5360042 or item2.getItemId() == 5360052 or item2.getItemId() == 5360016 or item2.getItemId() == 5360015:
                    self.dropMod = 2
                elif item2.getItemId() == 5360000 and hour >= 0 and hour <= 6:
                    self.dropMod = 2
                elif item2.getItemId() == 5360001 and hour >= 6 and hour <= 12:
                    self.dropMod = 2
                elif item2.getItemId() == 5360002 and hour >= 12 and hour <= 18:
                    self.dropMod = 2
                elif item2.getItemId() == 5360003 and hour >= 18 and hour <= 24:
                    self.dropMod = 2
            if item2.getItemId() == 5650000:
                self.hasPartyBonus = True
            elif item2.getItemId() == 5590001:
                self.levelBonus = 10
            elif self.levelBonus == 0 and item2.getItemId() == 5590000:
                self.levelBonus = 5
            else:
                if item2.getItemId() != 5340001:
                    continue
                self.canFish = True
                self.canFishVIP = True
        for item2 in chra.getInventory(MapleInventoryType.ETC):
            # switch (item2.getItemId()):
                # case 4030003:
                    self.hasVac = True
                    continue
                # case 4030004:
                    self.hasClone = True
                    continue
                # case 4030005:
                    self.cashMod = 2
                    continue
        self.magic += chra.getSkillLevel(SkillFactory.getSkill(22000000))
        self.localstr += (int)(percent_str * self.localstr / 100.0)
        self.localdex += (int)(percent_dex * self.localdex / 100.0)
        before_ = self.localint_
        self.localint_ += (int)(percent_int * self.localint_ / 100.0)
        self.magic += self.localint_ - before_
        self.localluk += (int)(percent_luk * self.localluk / 100.0)
        self.accuracy += (int)(percent_acc * self.accuracy / 100.0)
        self.watk += (int)(percent_atk * self.watk / 100.0)
        self.magic += (int)(percent_matk * self.magic / 100.0)
        localmaxhp_ += (int)(percent_hp * localmaxhp_ / 100.0)
        localmaxmp_ += (int)(percent_mp * localmaxmp_ / 100.0)
        buff = chra.getBuffedValue(MapleBuffStat.冒险岛勇士)
        if buff is not None:
            d = buff / 100.0
            self.localstr += (int)(d * self.str)
            self.localdex += (int)(d * self.dex)
            self.localluk += (int)(d * self.luk)
            before = self.localint_
            self.localint_ += (int)(d * self.int_)
            self.magic += self.localint_ - before
        buff = chra.getBuffedValue(MapleBuffStat.英雄之回声)
        if buff is not None:
            d = buff / 100.0
            self.watk += (int)(self.watk * d)
            self.magic += (int)(self.magic * d)
        buff = chra.getBuffedValue(MapleBuffStat.矛连击强化)
        if buff is not None:
            self.watk += buff / 10
        buff = chra.getBuffedValue(MapleBuffStat.最大HP)
        if buff is not None:
            localmaxhp_ += (int)(buff / 100.0 * localmaxhp_)
        buff = chra.getBuffedValue(MapleBuffStat.CONVERSION)
        if buff is not None:
            localmaxhp_ += (int)(buff / 100.0 * localmaxhp_)
        buff = chra.getBuffedValue(MapleBuffStat.最大MP)
        if buff is not None:
            localmaxmp_ += (int)(buff / 100.0 * localmaxmp_)
        buff = chra.getBuffedValue(MapleBuffStat.MP_BUFF)
        if buff is not None:
            localmaxmp_ += (int)(buff / 100.0 * localmaxmp_)
        buff = chra.getBuffedValue(MapleBuffStat.增强_最大HP)
        if buff is not None:
            localmaxhp_ += buff
        buff = chra.getBuffedValue(MapleBuffStat.增强_最大MP)
        if buff is not None:
            localmaxmp_ += buff
        # switch (chra.getJob()):
            # case 322:
                expert = SkillFactory.getSkill(3220004)
                boostLevel = chra.getSkillLevel(expert)
                if boostLevel > 0:
                    self.watk += expert.getEffect(boostLevel).getX()
                    break
                break
            # case 312:
                expert = SkillFactory.getSkill(3120005)
                boostLevel = chra.getSkillLevel(expert)
                if boostLevel > 0:
                    self.watk += expert.getEffect(boostLevel).getX()
                    break
                break
            # case 211:
            # case 212:
                amp = SkillFactory.getSkill(2110001)
                level = chra.getSkillLevel(amp)
                if level > 0:
                    self.dam_r *= amp.getEffect(level).getY() / 100.0
                    self.bossdam_r *= amp.getEffect(level).getY() / 100.0
                    break
                break
            # case 221:
            # case 222:
                amp = SkillFactory.getSkill(2210001)
                level = chra.getSkillLevel(amp)
                if level > 0:
                    self.dam_r *= amp.getEffect(level).getY() / 100.0
                    self.bossdam_r *= amp.getEffect(level).getY() / 100.0
                    break
                break
            # case 1211:
            # case 1212:
                amp = SkillFactory.getSkill(12110001)
                level = chra.getSkillLevel(amp)
                if level > 0:
                    self.dam_r *= amp.getEffect(level).getY() / 100.0
                    self.bossdam_r *= amp.getEffect(level).getY() / 100.0
                    break
                break
            # case 2215:
            # case 2216:
            # case 2217:
            # case 2218:
                amp = SkillFactory.getSkill(22150000)
                level = chra.getSkillLevel(amp)
                if level > 0:
                    self.dam_r *= amp.getEffect(level).getY() / 100.0
                    self.bossdam_r *= amp.getEffect(level).getY() / 100.0
                    break
                break
            # case 2112:
                expert = SkillFactory.getSkill(21120001)
                boostLevel = chra.getSkillLevel(expert)
                if boostLevel > 0:
                    self.watk += expert.getEffect(boostLevel).getX()
                    break
                break
        blessoffairy = SkillFactory.getSkill(GameConstants.getBOF_ForJob(chra.getJob()))
        boflevel = chra.getSkillLevel(blessoffairy)
        if boflevel > 0:
            self.watk += blessoffairy.getEffect(boflevel).getX()
            self.magic += blessoffairy.getEffect(boflevel).getY()
            self.accuracy += blessoffairy.getEffect(boflevel).getX()
        buff = chra.getBuffedValue(MapleBuffStat.经验_率)
        if buff is not None:
            if chra.getBuffSource(MapleBuffStat.经验_率) == 0:
                chra.getMapId()
            else:
                self.expBuff *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.掉落_率)
        if buff is not None:
            if chra.getBuffSource(MapleBuffStat.掉落_率) == 0:
                chra.getMapId()
            else:
                self.dropBuff *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.现金_率)
        if buff is not None:
            self.cashBuff *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.金币_率)
        if buff is not None:
            self.mesoBuff *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.聚财术)
        if buff is not None:
            self.mesoBuff *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.命中率)
        if buff is not None:
            self.accuracy += buff
        buff = chra.getBuffedValue(MapleBuffStat.物理攻击)
        if buff is not None:
            self.watk += buff
        buff = chra.getBuffedValue(MapleBuffStat.增强_物理攻击)
        if buff is not None:
            self.watk += buff
        buff = chra.getBuffedValue(MapleBuffStat.魔法攻击)
        if buff is not None:
            self.magic += buff
        buff = chra.getBuffedValue(MapleBuffStat.移动速度)
        if buff is not None:
            speed += buff
        buff = chra.getBuffedValue(MapleBuffStat.跳跃力)
        if buff is not None:
            jump += buff
        buff = chra.getBuffedValue(MapleBuffStat.疾驰跳跃)
        if buff is not None:
            speed += buff
        buff = chra.getBuffedValue(MapleBuffStat.疾驰跳跃)
        if buff is not None:
            jump += buff
        buff = chra.getBuffedValue(MapleBuffStat.提高队员攻击力_BUFF)
        if buff is not None:
            self.dam_r += buff
            self.bossdam_r += buff
        buff = chra.getBuffedSkill_Y(MapleBuffStat.FINAL_CUT)
        if buff is not None:
            self.dam_r *= buff / 100.0
            self.bossdam_r *= buff / 100.0
        buff = chra.getBuffedSkill_Y(MapleBuffStat.OWL_SPIRIT)
        if buff is not None:
            self.dam_r *= buff / 100.0
            self.bossdam_r *= buff / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.狂暴战魂)
        if buff is not None:
            self.dam_r *= 2.0
            self.bossdam_r *= 2.0
        bx = SkillFactory.getSkill(1320006)
        if chra.getSkillLevel(bx) > 0:
            self.dam_r *= bx.getEffect(chra.getSkillLevel(bx)).getDamage() / 100.0
            self.bossdam_r *= bx.getEffect(chra.getSkillLevel(bx)).getDamage() / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.PYRAMID_PQ)
        if buff is not None:
            eff = chra.getStatForBuff(MapleBuffStat.PYRAMID_PQ)
            self.dam_r *= eff.getBerserk() / 100.0
            self.bossdam_r *= eff.getBerserk() / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.属性攻击)
        if buff is not None:
            eff = chra.getStatForBuff(MapleBuffStat.属性攻击)
            self.dam_r *= eff.getDamage() / 100.0
            self.bossdam_r *= eff.getDamage() / 100.0
        buff = chra.getBuffedValue(MapleBuffStat.LIGHTNING_CHARGE)
        if buff is not None:
            eff = chra.getStatForBuff(MapleBuffStat.LIGHTNING_CHARGE)
            self.dam_r *= eff.getDamage() / 100.0
            self.bossdam_r *= eff.getDamage() / 100.0
        buff = chra.getBuffedSkill_X(MapleBuffStat.THORNS)
        if buff is not None:
            added_sharpeye_rate += buff
        buff = chra.getBuffedSkill_Y(MapleBuffStat.THORNS)
        if buff is not None:
            added_sharpeye_dmg += buff - 100
        buff = chra.getBuffedSkill_X(MapleBuffStat.火眼晶晶)
        if buff is not None:
            added_sharpeye_rate += buff
        buff = chra.getBuffedSkill_Y(MapleBuffStat.火眼晶晶)
        if buff is not None:
            added_sharpeye_dmg += buff
        buff = chra.getBuffedValue(MapleBuffStat.CRITICAL_RATE_BUFF)
        if buff is not None:
            added_sharpeye_rate += buff
        if speed > 140:
            speed = 140
        if jump > 123:
            jump = 123
        self.speedMod = speed / 100.0
        self.jumpMod = jump / 100.0
        mount = chra.getBuffedValue(MapleBuffStat.骑兽技能)
        if mount is not None:
            self.jumpMod = 1.23
            # switch (mount):
                # case 1:
                    self.speedMod = 1.5
                    break
                # case 2:
                    self.speedMod = 1.7
                    break
                # case 3:
                    self.speedMod = 1.8
                    break
                # default:
                    print("Unhandeled monster riding level, Speedmod = " + self.speedMod + "")
                    break
        self.hands = self.localdex + self.localint_ + self.localluk
        self.localmaxhp = min(30000, abs(max(-30000, localmaxhp_)))
        self.localmaxmp = min(30000, abs(max(-30000, localmaxmp_)))
        self.CalcPassive_SharpEye(chra, added_sharpeye_rate, added_sharpeye_dmg)
        self.CalcPassive_Mastery(chra)
        if first_login:
            chra.silentEnforceMaxHpMp()
        else:
            chra.enforceMaxHpMp()
        self.localmaxbasedamage = self.calculateMaxBaseDamage(self.watk, self.magic - self.localint_)
        if oldmaxhp != 0 and oldmaxhp != self.localmaxhp:
            chra.updatePartyMemberHP()
        self.lock.lock()
        try:
            self.isRecalc = False
        finally:
            self.lock.unlock()

    def checkEquipLevels(self, chr: Any, gain: int) -> bool:
        changed = False
        ii = MapleItemInformationProvider.getInstance()
        all = []
        for eq in all:
            lvlz = eq.getEquipLevels()
            eq.setItemEXP(eq.getItemEXP() + gain)
            if eq.getEquipLevels() > lvlz:
                i = eq.getEquipLevels() - lvlz
                while i > 0:
                    inc = ii.getEquipIncrements(eq.getItemId())
                    if inc is not None and (lvlz + i in inc):
                        eq = ii.levelUpEquip(eq, inc.get(lvlz + i))
                    if GameConstants.getStatFromWeapon(eq.getItemId()) is None:
                        ins = ii.getEquipSkills(eq.getItemId())
                        if ins is not None and (lvlz + i in ins):
                            for z in ins.get(lvlz + i):
                                if random.random() < 0.1:
                                    skil = SkillFactory.getSkill(z)
                                    if skil is None or not skil.canBeLearnedBy(chr.getJob()) or chr.getSkillLevel(skil) >= chr.getMasterLevel(skil):
                                        continue
                                    chr.changeSkillLevel(skil, (byte)(chr.getSkillLevel(skil) + 1), chr.getMasterLevel(skil))
                changed = True
            chr.forceReAddItem(eq.copy(), MapleInventoryType.EQUIPPED)
        if changed:
            chr.equipChanged()
            chr.getClient().getSession().write(MaplePacketCreator.showItemLevelupEffect())
            chr.getMap().broadcastMessage(chr, MaplePacketCreator.showForeignItemLevelupEffect(chr.getId()), False)
        return changed

    def checkEquipDurabilitys(self, chr: Any, gain: int) -> bool:
        for item in self.durabilityHandling:
            item.setDurability(item.getDurability() + gain)
            if item.getDurability() < 0:
                item.setDurability(0)
        all = []
        for eqq in all:
            if eqq.getDurability() == 0:
                if chr.getInventory(MapleInventoryType.EQUIP).isFull():
                    chr.getClient().getSession().write(MaplePacketCreator.getInventoryFull())
                    chr.getClient().getSession().write(MaplePacketCreator.getShowInventoryFull())
                    return False
                self.durabilityHandling.remove(eqq)
                pos = chr.getInventory(MapleInventoryType.EQUIP).getNextFreeSlot()
                MapleInventoryManipulator.unequip(chr.getClient(), eqq.getPosition(), pos)
                chr.getClient().getSession().write(MaplePacketCreator.updateSpecialItemUse(eqq, 1, pos))
            else:
                chr.forceReAddItem(eqq.copy(), MapleInventoryType.EQUIPPED)
        return True

    def CalcPassive_Mastery(self, player: Any) -> None:
        if player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-11)) is None:
            self.passive_mastery = 0
            return
        skil = 0
        # switch (GameConstants.getWeaponType(player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-11)).getItemId())):
            # case BOW:
                skil = (GameConstants.isKOC(player.getJob()) ? 13100000 : (GameConstants.isResist(player.getJob()) ? 33100000 : 3100000))
                break
            # case CLAW:
                skil = 4100000
                break
            # case KATARA:
            # case DAGGER:
                skil = ((player.getJob() >= 430 and player.getJob() <= 434) ? 4300000 : 4200000)
                break
            # case CROSSBOW:
                skil = 3200000
                break
            # case AXE1H:
            # case AXE2H:
                skil = 1100001
                break
            # case SWORD1H:
            # case SWORD2H:
                skil = (GameConstants.isKOC(player.getJob()) ? 11100000 : ((player.getJob() > 112) ? 1200000 : 1100000))
                break
            # case BLUNT1H:
            # case BLUNT2H:
                skil = 1200001
                break
            # case POLE_ARM:
                skil = (GameConstants.isAran(player.getJob()) ? 21100000 : 1300001)
                break
            # case SPEAR:
                skil = 1300000
                break
            # case KNUCKLE:
                skil = (GameConstants.isKOC(player.getJob()) ? 15100001 : 5100001)
                break
            # case GUN:
                skil = (GameConstants.isResist(player.getJob()) ? 35100000 : 5200000)
                break
            # case STAFF:
                skil = 32100006
                break
            # default:
                self.passive_mastery = 0
                return
        if player.getSkillLevel(skil) <= 0:
            self.passive_mastery = 0
            return
        self.passive_mastery = (byte)(player.getSkillLevel(skil) / 2 + player.getSkillLevel(skil) % 2)

    def CalcPassive_SharpEye(self, player: Any, added_sharpeye_rate: int, added_sharpeye_dmg: int) -> None:
        # switch (player.getJob()):
            # case 410:
            # case 411:
            # case 412:
                critSkill = SkillFactory.getSkill(4100001)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 1410:
            # case 1411:
            # case 1412:
                critSkill = SkillFactory.getSkill(14100001)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 511:
            # case 512:
                critSkill = SkillFactory.getSkill(5110000)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate += (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 1511:
            # case 1512:
                critSkill = SkillFactory.getSkill(15110000)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 2111:
            # case 2112:
                critSkill = SkillFactory.getSkill(21110000)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getX() * critSkill.getEffect(critlevel).getDamage() + added_sharpeye_dmg + 100)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getX() * critSkill.getEffect(critlevel).getY() + added_sharpeye_rate)
                    return
                break
            # case 300:
            # case 310:
            # case 311:
            # case 312:
            # case 320:
            # case 321:
            # case 322:
                critSkill = SkillFactory.getSkill(3000001)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 1300:
            # case 1310:
            # case 1311:
            # case 1312:
                critSkill = SkillFactory.getSkill(13000000)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
            # case 2214:
            # case 2215:
            # case 2216:
            # case 2217:
            # case 2218:
                critSkill = SkillFactory.getSkill(22140000)
                critlevel = player.getSkillLevel(critSkill)
                if critlevel > 0:
                    self.passive_sharpeye_percent = (short)(critSkill.getEffect(critlevel).getDamage() - 100 + added_sharpeye_dmg)
                    self.passive_sharpeye_rate = (byte)(critSkill.getEffect(critlevel).getProb() + added_sharpeye_rate)
                    return
                break
        self.passive_sharpeye_percent = added_sharpeye_dmg
        self.passive_sharpeye_rate = added_sharpeye_rate

    def passive_sharpeye_percent(self) -> int:
        return self.passive_sharpeye_percent

    def passive_sharpeye_rate(self) -> int:
        return self.passive_sharpeye_rate

    def passive_mastery(self) -> int:
        return self.passive_mastery

    def calculateMaxBaseDamage(self, watk: int, matk: int) -> float:
        chra = self.chr.get()
        if chra is None:
            return 0.0
        maxbasedamage = None
        if watk == 0:
            maxbasedamage = 1.0
        else:
            weapon_item = chra.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-11))
            job = chra.getJob()
            weapon = (weapon_item is None) ? MapleWeaponType.NOT_A_WEAPON : GameConstants.getWeaponType(weapon_item.getItemId())
            mainstat = 0
            secondarystat = 0
            # switch (weapon):
                # case BOW:
                # case CROSSBOW:
                    mainstat = self.localdex
                    secondarystat = self.localstr
                    break
                # case CLAW:
                # case KATARA:
                # case DAGGER:
                    if (job >= 400 and job <= 434) or (job >= 1400 and job <= 1412):
                        mainstat = self.localluk
                        secondarystat = self.localdex + self.localstr
                        break
                    mainstat = self.localstr
                    secondarystat = self.localdex
                    break
                # case KNUCKLE:
                    mainstat = self.localstr
                    secondarystat = self.localdex
                    break
                # case GUN:
                    mainstat = self.localdex
                    secondarystat = self.localstr
                    break
                # case NOT_A_WEAPON:
                    if (job >= 500 and job <= 522) or (job >= 1500 and job <= 1512) or (job >= 3500 and job <= 3512):
                        mainstat = self.localstr
                        secondarystat = self.localdex
                        break
                    mainstat = 0
                    secondarystat = 0
                    break
                # default:
                    if (job >= 200 and job <= 232) or (job >= 1200 and job <= 1211 and (weapon == MapleWeaponType.WAND or weapon == MapleWeaponType.STAFF)):
                        mainstat = self.localint_
                        secondarystat = self.localluk
                        watk = matk
                        break
                    mainstat = self.localstr
                    secondarystat = self.localdex
                    break
            maxbasedamage = (weapon.getMaxDamageMultiplier() * mainstat + secondarystat) * watk / 100.0
        return maxbasedamage

    def getHealHP(self) -> float:
        return self.shouldHealHP

    def getHealMP(self) -> float:
        return self.shouldHealMP

    def relocHeal(self) -> None:
        chra = self.chr.get()
        if chra is None:
            return
        playerjob = chra.getJob()
        self.shouldHealHP = (float)(10 + self.recoverHP)
        self.shouldHealMP = (float)(3 + self.mpRestore + self.recoverMP)
        if GameConstants.isJobFamily(200, playerjob):
            self.shouldHealMP += chra.getSkillLevel(SkillFactory.getSkill(2000000)) / 10.0 * chra.getLevel()
        elif GameConstants.isJobFamily(111, playerjob):
            effect = SkillFactory.getSkill(1110000)
            lvl = chra.getSkillLevel(effect)
            if lvl > 0:
                self.shouldHealMP += effect.getEffect(lvl).getMp()
        elif GameConstants.isJobFamily(121, playerjob):
            effect = SkillFactory.getSkill(1210000)
            lvl = chra.getSkillLevel(effect)
            if lvl > 0:
                self.shouldHealMP += effect.getEffect(lvl).getMp()
        elif GameConstants.isJobFamily(1111, playerjob):
            effect = SkillFactory.getSkill(11110000)
            lvl = chra.getSkillLevel(effect)
            if lvl > 0:
                self.shouldHealMP += effect.getEffect(lvl).getMp()
        elif GameConstants.isJobFamily(410, playerjob):
            effect = SkillFactory.getSkill(4100002)
            lvl = chra.getSkillLevel(effect)
            if lvl > 0:
                self.shouldHealHP += effect.getEffect(lvl).getHp()
                self.shouldHealMP += effect.getEffect(lvl).getMp()
        elif GameConstants.isJobFamily(420, playerjob):
            effect = SkillFactory.getSkill(4200001)
            lvl = chra.getSkillLevel(effect)
            if lvl > 0:
                self.shouldHealHP += effect.getEffect(lvl).getHp()
                self.shouldHealMP += effect.getEffect(lvl).getMp()
        if chra.isGM():
            self.shouldHealHP += 1000.0
            self.shouldHealMP += 1000.0
        if chra.getChair() != 0:
            self.shouldHealHP += 99.0
            self.shouldHealMP += 99.0
        else:
            recvRate = chra.getMap().getRecoveryRate()
            self.shouldHealHP *= recvRate
            self.shouldHealMP *= recvRate
        self.shouldHealHP *= 2.0
        self.shouldHealMP *= 2.0

    def connectData(self, mplew: Any) -> None:
        mplew.writeShort(self.str)
        mplew.writeShort(self.dex)
        mplew.writeShort(self.int_)
        mplew.writeShort(self.luk)
        mplew.writeShort(self.hp)
        mplew.writeShort(self.maxhp)
        mplew.writeShort(self.mp)
        mplew.writeShort(self.maxmp)

    def getSkillByJob(self, skillID: int, job: int) -> int:
        if GameConstants.isKOC(job):
            return skillID + 10000000
        if GameConstants.isAran(job):
            return skillID + 20000000
        if GameConstants.isEvan(job):
            return skillID + 20010000
        if GameConstants.isResist(job):
            return skillID + 30000000
        return skillID

    def getLimitBreak(self, chra: Any) -> int:
        ii = MapleItemInformationProvider.getInstance()
        limitBreak = 999999
        weapon = chra.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-11))
        if weapon is not None:
            limitBreak = ii.getLimitBreak(weapon.getItemId())
            subweapon = chra.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-10))
            if subweapon is not None and GameConstants.is物理武器(subweapon.getItemId()):
                subWeaponLB = ii.getLimitBreak(subweapon.getItemId())
                if subWeaponLB > limitBreak:
                    limitBreak = subWeaponLB
        return limitBreak

    def resetLocalStats(self, job: int) -> None:
        self.accuracy = 0
        self.localdex = self.getDex()
        self.localint_ = self.getInt()
        self.localstr = self.getStr()
        self.localluk = self.getLuk()
        self.decreaseDebuff = 0
        self.passive_sharpeye_rate = 5
        self.magic = 0
        self.watk = 0
        self.expBuff = 100.0
        self.cashBuff = 100.0
        self.dropBuff = 100.0
        self.mesoBuff = 100.0
        self.recoverHP = 0
        self.recoverMP = 0
        self.mpconReduce = 0
        self.incMesoProp = 0
        self.DAMreflect = 0
        self.DAMreflect_rate = 0
        self.hpRecover = 0
        self.hpRecoverProp = 0
        self.mpRecover = 0
        self.mpRecoverProp = 0
        self.mpRestore = 0
        self.equippedWelcomeBackRing = False
        self.hasPartyBonus = False
        self.hasClone = False
        self.Berserk = False
        self.canFish = False
        self.canFishVIP = False
        self.equipmentBonusExp = 0
        self.RecoveryUP = 100
        self.dropMod = 1
        self.cashMod = 1
        self.levelBonus = 0
        self.incAllskill = 0
        self.durabilityHandling.clear()
        self.equipLevelHandling.clear()
        self.setHandling.clear()
        self.element_fire = 100
        self.element_ice = 100
        self.element_light = 100
        self.element_psn = 100
        self.def = 100

