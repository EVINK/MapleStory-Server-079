"""
MapleStatEffect - Converted from Java source
Original: server/MapleStatEffect.java
Package: server
"""

from concurrent.futures import Future
from enum import Enum
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
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCoolDownValueHolder import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.MapleStat import *  # TODO: import specific classes
# from client.PlayerStats import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.maps.MapleDoor import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from server.maps.MapleMist import *  # TODO: import specific classes
# from server.maps.MapleSummon import *  # TODO: import specific classes
# from server.maps.SummonMovementType import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleStatEffect:
    """
    Class MapleStatEffect
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self):
        self.mastery = 0
        self.mhpR = 0
        self.mmpR = 0
        self.mobCount = 0
        self.attackCount = 0
        self.bulletCount = 0
        self.hp = 0
        self.mp = 0
        self.watk = 0
        self.matk = 0
        self.wdef = 0
        self.mdef = 0
        self.acc = 0
        self.avoid = 0
        self.hands = 0
        self.speed = 0
        self.jump = 0
        self.mpCon = 0
        self.hpCon = 0
        self.damage = 0
        self.prop = 0
        self.ehp = 0
        self.emp = 0
        self.ewatk = 0
        self.ewdef = 0
        self.emdef = 0
        self.hpR = 0.0
        self.mpR = 0.0
        self.duration = 0
        self.sourceid = 0
        self.moveTo = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.itemCon = 0
        self.itemConNo = 0
        self.bulletConsume = 0
        self.moneyCon = 0
        self.cooldown = 0
        self.morphId = 0
        self.morphId = 0
        self.partyBuff = True


    def loadSkillEffectFromData(self, source: Any, skillid: int, overtime: bool, level: int) -> Any:
        return loadFromData(source, skillid, True, overtime, level)

    def loadItemEffectFromData(self, source: Any, itemid: int) -> Any:
        return loadFromData(source, itemid, False, False, 1)

    def addBuffStatPairToListIfNotZero(self, list: list, buffstat: Any, val: int) -> None:
        if val != 0:
            list.add(new Pair<MapleBuffStat, Integer>(buffstat, val))

    def loadFromData(self, source: Any, sourceid: int, skill: bool, overTime: bool, level: int) -> Any:
        ret = MapleStatEffect()
        ret.sourceid = sourceid
        ret.skill = skill
        ret.level = level
        if source is None:
            return ret
        ret.duration = MapleDataTool.getIntConvert("time", source, -1)
        ret.hp = MapleDataTool.getInt("hp", source, 0)
        ret.hpR = MapleDataTool.getInt("hpR", source, 0) / 100.0
        ret.mp = MapleDataTool.getInt("mp", source, 0)
        ret.mpR = MapleDataTool.getInt("mpR", source, 0) / 100.0
        ret.mhpR = MapleDataTool.getInt("mhpR", source, 0)
        ret.mmpR = MapleDataTool.getInt("mmpR", source, 0)
        ret.mpCon = MapleDataTool.getInt("mpCon", source, 0)
        ret.hpCon = MapleDataTool.getInt("hpCon", source, 0)
        ret.prop = MapleDataTool.getInt("prop", source, 100)
        ret.cooldown = MapleDataTool.getInt("cooltime", source, 0)
        ret.expinc = MapleDataTool.getInt("expinc", source, 0)
        ret.morphId = MapleDataTool.getInt("morph", source, 0)
        ret.cp = MapleDataTool.getInt("cp", source, 0)
        ret.nuffSkill = MapleDataTool.getInt("nuffSkill", source, 0)
        ret.mobCount = MapleDataTool.getInt("mobCount", source, 1)
        if skill:
            # switch (sourceid):
                # case 1100002:
                # case 1100003:
                # case 1200002:
                # case 1200003:
                # case 1300002:
                # case 1300003:
                # case 3100001:
                # case 3200001:
                # case 11101002:
                # case 13101002:
                    ret.mobCount = 6
                    break
        if not ret.skill and ret.duration > -1:
            ret.overTime = True
        else:
            mapleStatEffect = ret
            mapleStatEffect.duration *= 1000
            ret.overTime = (overTime or ret.isMorph() or ret.isPirateMorph() or ret.isFinalAttack())
        statups = new ArrayList<Pair<MapleBuffStat, Integer>>()
        ret.mastery = MapleDataTool.getInt("mastery", source, 0)
        ret.watk = MapleDataTool.getInt("pad", source, 0)
        ret.wdef = MapleDataTool.getInt("pdd", source, 0)
        ret.matk = MapleDataTool.getInt("mad", source, 0)
        ret.mdef = MapleDataTool.getInt("mdd", source, 0)
        ret.ehp = MapleDataTool.getInt("emhp", source, 0)
        ret.emp = MapleDataTool.getInt("emmp", source, 0)
        ret.ewatk = MapleDataTool.getInt("epad", source, 0)
        ret.ewdef = MapleDataTool.getInt("epdd", source, 0)
        ret.emdef = MapleDataTool.getInt("emdd", source, 0)
        ret.acc = MapleDataTool.getIntConvert("acc", source, 0)
        ret.avoid = MapleDataTool.getInt("eva", source, 0)
        ret.speed = MapleDataTool.getInt("speed", source, 0)
        ret.jump = MapleDataTool.getInt("jump", source, 0)
        ret.expBuff = MapleDataTool.getInt("expBuff", source, 0)
        ret.cashup = MapleDataTool.getInt("cashBuff", source, 0)
        ret.itemup = MapleDataTool.getInt("itemupbyitem", source, 0)
        ret.mesoup = MapleDataTool.getInt("mesoupbyitem", source, 0)
        ret.berserk = MapleDataTool.getInt("berserk", source, 0)
        ret.berserk2 = MapleDataTool.getInt("berserk2", source, 0)
        ret.booster = MapleDataTool.getInt("booster", source, 0)
        ret.illusion = MapleDataTool.getInt("illusion", source, 0)
        cure = []
        if MapleDataTool.getInt("poison", source, 0) > 0:
            cure.add(MapleDisease.中毒)
        if MapleDataTool.getInt("seal", source, 0) > 0:
            cure.add(MapleDisease.封印)
        if MapleDataTool.getInt("darkness", source, 0) > 0:
            cure.add(MapleDisease.黑暗)
        if MapleDataTool.getInt("weakness", source, 0) > 0:
            cure.add(MapleDisease.虚弱)
        if MapleDataTool.getInt("curse", source, 0) > 0:
            cure.add(MapleDisease.诅咒)
        ret.cureDebuffs = cure
        ltd = source.getChildByPath("lt")
        if ltd is not None:
            ret.lt = ltd.getData()
            ret.rb = source.getChildByPath("rb").getData()
        ret.x = MapleDataTool.getInt("x", source, 0)
        ret.y = MapleDataTool.getInt("y", source, 0)
        ret.z = MapleDataTool.getInt("z", source, 0)
        ret.damage = MapleDataTool.getIntConvert("damage", source, 100)
        ret.attackCount = MapleDataTool.getIntConvert("attackCount", source, 1)
        ret.bulletCount = MapleDataTool.getIntConvert("bulletCount", source, 1)
        ret.bulletConsume = MapleDataTool.getIntConvert("bulletConsume", source, 0)
        ret.moneyCon = MapleDataTool.getIntConvert("moneyCon", source, 0)
        ret.itemCon = MapleDataTool.getInt("itemCon", source, 0)
        ret.itemConNo = MapleDataTool.getInt("itemConNo", source, 0)
        ret.moveTo = MapleDataTool.getInt("moveTo", source, -1)
        monsterStatus = new EnumMap<MonsterStatus, Integer>(MonsterStatus.class)
        if ret.overTime and ret.getSummonMovementType() is None:
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.物理攻击, ret.watk)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.物理防御, ret.wdef)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.魔法攻击, ret.matk)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.魔法防御, ret.mdef)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.命中率, ret.acc)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.回避率, ret.avoid)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.移动速度, ret.speed)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.跳跃力, ret.jump)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.最大HP, ret.mhpR)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.最大MP, ret.mmpR)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.经验_率, ret.expBuff)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.现金_率, ret.cashup)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.掉落_率, ret.itemup * 200)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.金币_率, ret.mesoup * 200)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.狂暴战魂, ret.berserk2)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.PYRAMID_PQ, ret.berserk)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.攻击加速, ret.booster)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.ILLUSION, ret.illusion)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.增强_物理攻击, ret.ewatk)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.增强_物理防御力, ret.ewdef)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.增强_魔法防御力, ret.emdef)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.增强_最大HP, ret.ehp)
            addBuffStatPairToListIfNotZero(statups, MapleBuffStat.增强_最大MP, ret.ehp)
        if skill:
            # switch (sourceid):
                # case 2001002:
                # case 12001001:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.魔法盾, ret.x))
                    break
                # case 2301003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.神之保护, ret.x))
                    break
                # case 9001004:
                    ret.duration = 2100000000
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.GM_隐藏术, ret.x))
                    break
                # case 5101007:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.隐身术, ret.x))
                    break
                # case 4001003:
                # case 13101006:
                # case 14001003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.隐身术, ret.x))
                    break
                # case 4211003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.敛财术, ret.x))
                    break
                # case 4211005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金钱护盾, ret.x))
                    break
                # case 4111001:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.聚财术, ret.x))
                    break
                # case 4111002:
                # case 14111000:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.影分身, ret.x))
                    break
                # case 11101002:
                # case 13101002:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.终极弓剑, ret.x))
                    break
                # case 2311002:
                # case 3101004:
                # case 3201004:
                # case 13101003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.无形箭弩, ret.x))
                    break
                # case 1211003:
                # case 1211004:
                # case 1211005:
                # case 1211006:
                # case 1211007:
                # case 1211008:
                # case 1221003:
                # case 1221004:
                # case 11111007:
                # case 15101006:
                # case 21111005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.属性攻击, ret.x))
                    break
                # case 12101005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.自然力重置, ret.x))
                    break
                # case 3121008:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.集中精力, ret.x))
                    break
                # case 5110001:
                # case 15100004:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, 0))
                    break
                # case 1101004:
                # case 1101005:
                # case 1201004:
                # case 1201005:
                # case 1301004:
                # case 1301005:
                # case 2111005:
                # case 2211005:
                # case 3101002:
                # case 3201002:
                # case 4101003:
                # case 4201002:
                # case 5101006:
                # case 5201003:
                # case 11101001:
                # case 12101004:
                # case 13101001:
                # case 14101002:
                # case 15101002:
                # case 21001003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.攻击加速, ret.x))
                    break
                # case 5121009:
                # case 15111005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.攻击加速, ret.x))
                    break
                # case 5001005:
                    ret.duration = 5000
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.疾驰移动, ret.x))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.疾驰跳跃, ret.y))
                    break
                # case 15001003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.疾驰移动, ret.x * 2))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.疾驰跳跃, ret.y * 2))
                    break
                # case 1101007:
                # case 1201007:
                # case 21101003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.伤害反击, ret.x))
                    break
                # case 1301007:
                # case 9001008:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.最大HP, ret.x))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.最大MP, ret.y))
                    break
                # case 1001:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.团队治疗, ret.x))
                    break
                # case 1111002:
                # case 11111001:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.斗气集中, 1))
                    break
                # case 21120007:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.战神之盾, ret.x))
                    break
                # case 5211006:
                # case 5220011:
                    ret.duration = 7200000
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.导航辅助, ret.x))
                    break
                # case 1011:
                # case 10001011:
                # case 20001011:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.狂暴战魂, 1))
                    break
                # case 1010:
                # case 10001010:
                # case 20001010:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金刚霸体, 1))
                    break
                # case 1311006:
                    ret.hpR = -ret.x / 100.0
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.龙咆哮, ret.y))
                    break
                # case 1311008:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.龙之力, ret.x))
                    break
                # case 1121000:
                # case 1221000:
                # case 1321000:
                # case 2121000:
                # case 2221000:
                # case 2321000:
                # case 3121000:
                # case 3221000:
                # case 4121000:
                # case 4221000:
                # case 5121000:
                # case 5221000:
                # case 21121000:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.冒险岛勇士, ret.x))
                    break
                # case 15111006:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.闪光击, ret.x))
                    break
                # case 3121002:
                # case 3221002:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.火眼晶晶, ret.x << 8 | ret.y))
                    break
                # case 21000000:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.矛连击强化, 100))
                    break
                # case 21100005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.连环吸血, ret.x))
                    break
                # case 21111001:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.灵巧击退, ret.x))
                    break
                # case 4001002:
                # case 14001002:
                    monsterStatus.put(MonsterStatus.物攻, ret.x)
                    monsterStatus.put(MonsterStatus.物防, ret.y)
                    break
                # case 5221009:
                    monsterStatus.put(MonsterStatus.心灵控制, 1)
                    break
                # case 1201006:
                    monsterStatus.put(MonsterStatus.物攻, ret.x)
                    monsterStatus.put(MonsterStatus.物防, ret.y)
                    break
                # case 1111005:
                # case 1111006:
                # case 1111008:
                # case 1211002:
                # case 3101005:
                # case 4121008:
                # case 4201004:
                # case 4211002:
                # case 4221007:
                # case 5101002:
                # case 5101003:
                # case 5111002:
                # case 5121004:
                # case 5121005:
                # case 5121007:
                # case 5201004:
                # case 15101005:
                    monsterStatus.put(MonsterStatus.眩晕, 1)
                    break
                # case 4121003:
                # case 4221003:
                    monsterStatus.put(MonsterStatus.挑衅, ret.x)
                    monsterStatus.put(MonsterStatus.魔防, ret.x)
                    monsterStatus.put(MonsterStatus.物防, ret.x)
                    break
                # case 2121006:
                # case 2201004:
                # case 2211006:
                # case 2221007:
                # case 3211003:
                # case 5211005:
                # case 21120006:
                    monsterStatus.put(MonsterStatus.冻结, 1)
                    mapleStatEffect2 = ret
                    mapleStatEffect2.duration *= 2
                    break
                # case 2101003:
                # case 2201003:
                # case 12101001:
                    monsterStatus.put(MonsterStatus.速度, ret.x)
                    break
                # case 2101005:
                # case 2111006:
                # case 2121003:
                # case 2221003:
                    monsterStatus.put(MonsterStatus.中毒, 1)
                    break
                # case 4121004:
                # case 4221004:
                    monsterStatus.put(MonsterStatus.忍者伏击, ret.damage)
                    break
                # case 2311005:
                    monsterStatus.put(MonsterStatus.巫毒术, 1)
                    break
                # case 3111002:
                # case 3211002:
                # case 5211001:
                # case 5220002:
                # case 13111004:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.替身术, 1))
                    break
                # case 3111005:
                # case 3211005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.召唤兽, 1))
                    monsterStatus.put(MonsterStatus.眩晕, 1)
                    break
                # case 2121005:
                # case 3221005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.召唤兽, 1))
                    monsterStatus.put(MonsterStatus.冻结, 1)
                    break
                # case 2221005:
                # case 2311006:
                # case 2321003:
                # case 3121006:
                # case 5211002:
                # case 11001004:
                # case 12001004:
                # case 12111004:
                # case 13001004:
                # case 14001005:
                # case 15001004:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.召唤兽, 1))
                    break
                # case 1321007:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.召唤兽, 1))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.灵魂助力, ret.level))
                    break
                # case 2311003:
                # case 9001002:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.神圣祈祷, ret.x))
                    break
                # case 2111004:
                # case 2211004:
                # case 12111002:
                    monsterStatus.put(MonsterStatus.封印, 1)
                    break
                # case 4111003:
                # case 14111001:
                    monsterStatus.put(MonsterStatus.影网术, 1)
                    break
                # case 4121006:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.暗器伤人, 0))
                    break
                # case 2121004:
                # case 2221004:
                # case 2321004:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.终极无限, ret.x))
                    break
                # case 1121002:
                # case 1221002:
                # case 1321002:
                # case 21121003:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.稳如泰山, ret.prop))
                    break
                # case 1005:
                # case 10001005:
                # case 20001005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.英雄之回声, ret.x))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.物理攻击, ret.x))
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.魔法攻击, ret.x))
                    break
                # case 2121002:
                # case 2221002:
                # case 2321002:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.魔法反击, 1))
                    break
                # case 2321005:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.圣灵之盾, ret.x))
                    break
                # case 3121007:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.击退箭, ret.x))
                    monsterStatus.put(MonsterStatus.速度, ret.x)
                    break
                # case 3221006:
                    statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.刺眼箭, ret.x))
                    monsterStatus.put(MonsterStatus.命中, ret.x)
                    break
        if ret.isMonsterRiding():
            statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.骑兽技能, 1))
        if ret.isMorph() or ret.isPirateMorph():
            statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.变身, ret.getMorph()))
        ret.monsterStatus = monsterStatus
        statups.trimToSize()
        ret.statups = statups
        return ret

    def makeHealHP(self, rate: float, stat: float, lowerfactor: float, upperfactor: float) -> int:
        return (int)(random.random() * ((int)(stat * upperfactor * rate) - (int)(stat * lowerfactor * rate) + 1) + (int)(stat * lowerfactor * rate))

    def getElementalAmp(self, job: int) -> int:
        # switch (job):
            # case 211:
            # case 212:
                return 2110001
            # case 221:
            # case 222:
                return 2210001
            # case 1211:
            # case 1212:
                return 12110001
            # case 2215:
            # case 2216:
            # case 2217:
            # case 2218:
                return 22150000
            # default:
                return -1

    def applyPassive(self, applyto: Any, obj: Any) -> None:
        if self.makeChanceResult():
            # switch (self.sourceid):
                # case 2100000:
                # case 2200000:
                # case 2300000:
                    if obj is None or obj.getType() != MapleMapObjectType.MONSTER:
                        return
                    mob = obj
                    if mob.getStats().isBoss():
                        break
                    absorbMp = min((int)(mob.getMobMaxMp() * (self.getX() / 100.0)), mob.getMp())
                    if absorbMp > 0:
                        mob.setMp(mob.getMp() - absorbMp)
                        tmpMp = applyto.getStat().getMp() + absorbMp
                        if tmpMp > applyto.getStat().getMaxMp():
                            tmpMp = applyto.getStat().getMaxMp()
                        elif tmpMp < 0:
                            tmpMp = 0
                        applyto.getStat().setMp(tmpMp)
                        applyto.getClient().getSession().write(MaplePacketCreator.showOwnBuffEffect(self.sourceid, 1))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.showBuffeffect(applyto.getId(), self.sourceid, 1), False)
                        break
                    break

    def applyTo(self, chr: Any) -> bool:
        return self.applyTo(chr, chr, True, None, self.duration)

    def applyTo_chr_pos(self, chr: Any, pos: Any) -> bool:
        return self.applyTo(chr, chr, True, pos, self.duration)

    def applyTo_applyfrom_applyto_primary_pos(self, applyfrom: Any, applyto: Any, primary: bool, pos: Any) -> bool:
        return self.applyTo(applyfrom, applyto, primary, pos, self.duration)

    def applyTo_applyfrom_applyto_primary_pos_newDuration(self, applyfrom: Any, applyto: Any, primary: bool, pos: Any, newDuration: int) -> bool:
        if self.is群体治愈() and (applyfrom.getMapId() == 749040100 or applyto.getMapId() == 749040100):
            return False
        if self.sourceid == 4341006 and applyfrom.getBuffedValue(MapleBuffStat.MIRROR_IMAGE) is None:
            applyfrom.getClient().getSession().write(MaplePacketCreator.enableActions())
            return False
        if self.sourceid == 33101004 and applyfrom.getMap().isTown():
            applyfrom.dropMessage(5, "你不能在城镇使用这种技能.")
            applyfrom.getClient().getSession().write(MaplePacketCreator.enableActions())
            return False
        hpchange = self.calcHPChange(applyfrom, primary)
        mpchange = self.calcMPChange(applyfrom, primary)
        if primary:
            if self.itemConNo != 0 and not applyto.isClone():
                MapleInventoryManipulator.removeById(applyto.getClient(), GameConstants.getInventoryType(self.itemCon), self.itemCon, self.itemConNo, False, True)
        elif not primary and self.is复活术():
            hpchange = applyto.getMaxHp()
            applyto.setStance(0)
        if self.is净化() and self.makeChanceResult():
            applyto.dispelDebuffs()
        elif self.is勇士的意志():
            applyto.dispelDebuff(MapleDisease.诱惑)
        elif self.cureDebuffs > 0:
            for debuff in self.cureDebuffs:
                applyfrom.dispelDebuff(debuff)
        elif self.is生命分流():
            toDecreaseHP = applyto.getMaxHp() / 100 * 10
            if applyto.getHp() > toDecreaseHP:
                hpchange += -toDecreaseHP
                mpchange += toDecreaseHP / 100 * self.getY()
            else:
                hpchange = ((applyto.getHp() == 1) ? 0 : (applyto.getHp() - 1))
        hpmpupdate = new ArrayList<Pair<MapleStat, Integer>>(2)
        if applyto.getMapId() != LoginServer.家族PK地图() or applyto.getMapId() != LoginServer.个人PK地图() or applyto.getMapId() != LoginServer.组队PK地图():
            if hpchange != 0:
                if hpchange < 0 and -hpchange > applyto.getHp() and not applyto.hasDisease(MapleDisease.ZOMBIFY):
                    return False
                applyto.setHp(applyto.getHp() + hpchange)
                hpmpupdate.add(new Pair<MapleStat, Integer>(MapleStat.HP, applyto.getHp()))
                applyto.updateSingleStat(MapleStat.HP, applyto.getHp())
            if mpchange != 0:
                if mpchange < 0 and -mpchange > applyto.getMp():
                    applyto.getClient().getSession().write(MaplePacketCreator.enableActions())
                    return False
                applyto.setMp(applyto.getMp() + mpchange)
                hpmpupdate.add(new Pair<MapleStat, Integer>(MapleStat.MP, applyto.getMp()))
                applyto.updateSingleStat(MapleStat.MP, applyto.getMp())
            applyto.getClient().getSession().write(MaplePacketCreator.updatePlayerStats(hpmpupdate, True, applyto.getJob()))
        else:
            applyto.dropMessage(5, "当前为Pvp地图禁止手动加血加蓝")
            applyto.getClient().getSession().write(MaplePacketCreator.enableActions())
        if self.expinc != 0:
            applyto.gainExp(self.expinc, True, True, False)
        elif GameConstants.isMonsterCard(self.sourceid):
            applyto.getMonsterBook().addCard(applyto.getClient(), self.sourceid)
        elif self.is暗器伤人() and not applyto.isClone():
            use = applyto.getInventory(MapleInventoryType.USE)
            itemz = False
            for i in range(use.getSlotLimit()):
                item = use.getItem(i)
                if item is not None and GameConstants.is飞镖道具(item.getItemId()) and item.getQuantity() >= 200:
                    MapleInventoryManipulator.removeById(applyto.getClient(), MapleInventoryType.USE, item.getItemId(), 200, False, True)
                    itemz = True
                    break
            if not itemz:
                return False
        elif self.cp != 0 and applyto.getCarnivalParty() is not None:
            applyto.getCarnivalParty().addCP(applyto, self.cp)
            applyto.CPUpdate(False, applyto.getAvailableCP(), applyto.getTotalCP(), 0)
            for chr in applyto.getMap().getCharactersThreadsafe():
                chr.CPUpdate(True, applyto.getCarnivalParty().getAvailableCP(), applyto.getCarnivalParty().getTotalCP(), applyto.getCarnivalParty().getTeam())
        elif self.nuffSkill != 0 and applyto.getParty() is not None:
            final MapleCarnivalFactory.MCSkill skil = MapleCarnivalFactory.getInstance().getSkill(self.nuffSkill)
            if skil is not None:
                dis = skil.getDisease()
                for chr2 in applyto.getMap().getCharactersThreadsafe():
                    if (chr2.getParty() is None or chr2.getParty().getId() != applyto.getParty().getId()) and (skil.targetsAll or Randomizer.nextBoolean()):
                        if dis is None:
                            chr2.dispel()
                        elif skil.getSkill() is None:
                            chr2.giveDebuff(dis, 1, 30000, MapleDisease.getByDisease(dis), 1)
                        else:
                            chr2.giveDebuff(dis, skil.getSkill())
                        if not skil.targetsAll:
                            break
                        continue
        if self.overTime and not self.is能量获得():
            self.applyBuffEffect(applyfrom, applyto, primary, newDuration)
        if self.skill:
            self.removeMonsterBuff(applyfrom)
        if primary:
            if (self.overTime or self.is群体治愈()) and not self.is能量获得():
                self.applyBuff(applyfrom, newDuration)
            if self.isMonsterBuff():
                self.applyMonsterBuff(applyfrom)
        summonMovementType = self.getSummonMovementType()
        if summonMovementType is not None:
            tosummon = MapleSummon(applyfrom, this, Point((pos is None) ? applyfrom.getPosition() : pos), summonMovementType)
            if not tosummon.is替身术():
                applyfrom.getCheatTracker().resetSummonAttack()
            applyfrom.getMap().spawnSummon(tosummon)
            applyfrom.addSummon(tosummon)
            tosummon.addHP(self.x)
            if self.is灵魂助力():
                tosummon.addHP(1)
            if self.sourceid == 4341006:
                applyfrom.cancelEffectFromBuffStat(MapleBuffStat.MIRROR_IMAGE)
        elif self.is时空门():
            door = MapleDoor(applyto, Point(applyto.getPosition()), self.sourceid)
            if door.getTownPortal() is not None:
                applyto.getMap().spawnDoor(door)
                applyto.addDoor(door)
                townDoor = MapleDoor(door)
                applyto.addDoor(townDoor)
                door.getTown().spawnDoor(townDoor)
                if applyto.getParty() is not None:
                    applyto.silentPartyUpdate()
            else:
                applyto.dropMessage(5, "村庄里已经没有可开启时空门的位置..")
        elif self.isMist():
            bounds = self.calculateBoundingBox((pos is not None) ? pos : Point(applyfrom.getPosition()), applyfrom.isFacingLeft())
            mist = MapleMist(bounds, applyfrom, this)
            applyfrom.getMap().spawnMist(mist, self.getDuration(), False)
        elif self.is伺机待发():
            for j in applyto.getCooldowns():
                if j.skillId != 5121010:
                    applyto.removeCooldown(j.skillId)
                    applyto.getClient().getSession().write(MaplePacketCreator.skillCooldown(j.skillId, 0))
        else:
            for chrz in applyto.getClones():
                if chrz.get() is not None:
                    self.applyTo(chrz.get(), chrz.get(), primary, pos, newDuration)
        return True

    def applyReturnScroll(self, applyto: Any) -> bool:
        if self.moveTo != -1:
            target = None
            if self.moveTo == 999999999:
                target = applyto.getMap().getReturnMap()
            else:
                target = ChannelServer.getInstance(applyto.getClient().getChannel()).getMapFactory().getMap(self.moveTo)
                if target.getId() / 10000000 != 60 and applyto.getMapId() / 10000000 != 61 and target.getId() / 10000000 != 21 and applyto.getMapId() / 10000000 != 20 and target.getId() / 10000000 != 12 and target.getId() / 10000000 != applyto.getMapId() / 10000000:
                    return False
            try:
                applyto.changeMap(target, target.getPortal(0))
            except Exception as ex:
                applyto.dropMessage(5, "本地图目前尚未开放.")
                return False
            return True
        return False

    def isSoulStone(self) -> bool:
        return self.skill and self.sourceid == 22181003

    def applyBuff(self, applyfrom: Any, newDuration: int) -> None:
        if self.isSoulStone():
            if applyfrom.getParty() is not None:
                membrs = 0
                for chr in applyfrom.getMap().getCharactersThreadsafe():
                    if chr.getParty() is not None and chr.getParty() == (applyfrom.getParty()) and chr.isAlive():
                        membrs += 1
                awarded = []
                while awarded < min(membrs, self.y):
                    for chr2 in applyfrom.getMap().getCharactersThreadsafe():
                        if chr2.isAlive() and chr2.getParty() == (applyfrom.getParty()) and not (chr2 in awarded) and Randomizer.nextInt(self.y) == 0:
                            awarded.add(chr2)
                for chr2 in awarded:
                    self.applyTo(applyfrom, chr2, False, None, newDuration)
                    chr2.getClient().getSession().write(MaplePacketCreator.showOwnBuffEffect(self.sourceid, 2))
                    chr2.getMap().broadcastMessage(chr2, MaplePacketCreator.showBuffeffect(chr2.getId(), self.sourceid, 2), False)
        elif self.isPartyBuff() and (applyfrom.getParty() is not None or self.isGmBuff()):
            bounds = self.calculateBoundingBox(applyfrom.getPosition(), applyfrom.isFacingLeft())
            affecteds = applyfrom.getMap().getMapObjectsInRect(bounds, Arrays.asList(MapleMapObjectType.PLAYER))
            for affectedmo in affecteds:
                affected = affectedmo
                if affected != applyfrom and (self.isGmBuff() or applyfrom.getParty() == (affected.getParty())):
                    if (self.is复活术() and not affected.isAlive()) or (not self.is复活术() and affected.isAlive()):
                        self.applyTo(applyfrom, affected, False, None, newDuration)
                        affected.getClient().getSession().write(MaplePacketCreator.showOwnBuffEffect(self.sourceid, 2))
                        affected.getMap().broadcastMessage(affected, MaplePacketCreator.showBuffeffect(affected.getId(), self.sourceid, 2), False)
                    if not self.is伺机待发():
                        continue
                    for i in affected.getCooldowns():
                        if i.skillId != 5121010:
                            affected.removeCooldown(i.skillId)
                            affected.getClient().getSession().write(MaplePacketCreator.skillCooldown(i.skillId, 0))

    def removeMonsterBuff(self, applyfrom: Any) -> None:
        cancel = []
        # switch (self.sourceid):
            # case 1111007:
                cancel.add(MonsterStatus.物防)
                cancel.add(MonsterStatus.物理防御提升)
                break
            # case 1211009:
                cancel.add(MonsterStatus.魔防)
                cancel.add(MonsterStatus.魔法防御提升)
                break
            # case 1311007:
                cancel.add(MonsterStatus.物攻)
                cancel.add(MonsterStatus.物理攻击提升)
                cancel.add(MonsterStatus.魔攻)
                cancel.add(MonsterStatus.魔法攻击提升)
                break
            # default:
                return
        bounds = self.calculateBoundingBox(applyfrom.getPosition(), applyfrom.isFacingLeft())
        affected = applyfrom.getMap().getMapObjectsInRect(bounds, Arrays.asList(MapleMapObjectType.MONSTER))
        i = 0
        for mo in affected:
            if self.makeChanceResult():
                for stat in cancel:
                    (mo).cancelStatus(stat)
            if ++i >= self.mobCount:
                break

    def applyMonsterBuff(self, applyfrom: Any) -> None:
        bounds = self.calculateBoundingBox(applyfrom.getPosition(), applyfrom.isFacingLeft())
        affected = applyfrom.getMap().getMapObjectsInRect(bounds, Arrays.asList(MapleMapObjectType.MONSTER))
        i = 0
        for mo in affected:
            if self.makeChanceResult():
                for (final Map.Entry<MonsterStatus, Integer> stat : self.getMonsterStati().items())
                    (mo).applyStatus(applyfrom, MonsterStatusEffect(stat.getKey(), stat.getValue(), self.sourceid, None, False), self.isPoison(), self.getDuration(), False)
            if ++i >= self.mobCount:
                break

    def calculateBoundingBox(self, posFrom: Any, facingLeft: bool) -> Any:
        if self.lt is None or self.rb is None:
            return Rectangle(posFrom.x, posFrom.y, facingLeft ? 1 : -1, 1)
        mylt = None
        myrb = None
        if facingLeft:
            mylt = Point(self.lt.x + posFrom.x, self.lt.y + posFrom.y)
            myrb = Point(self.rb.x + posFrom.x, self.rb.y + posFrom.y)
        else:
            myrb = Point(self.lt.x * -1 + posFrom.x, self.rb.y + posFrom.y)
            mylt = Point(self.rb.x * -1 + posFrom.x, self.lt.y + posFrom.y)
        return Rectangle(mylt.x, mylt.y, myrb.x - mylt.x, myrb.y - mylt.y)

    def setDuration(self, d: int) -> None:
        self.duration = d

    def silentApplyBuff(self, chr: Any, starttime: int) -> None:
        localDuration = self.alchemistModifyVal(chr, self.duration, False)
        chr.registerEffect(this, starttime, Timer.BuffTimer.getInstance().schedule(CancelEffectAction(chr, this, starttime), starttime + localDuration - int(time.time() * 1000)))
        summonMovementType = self.getSummonMovementType()
        if summonMovementType is not None and not summonMovementType == (SummonMovementType.WALK_STATIONARY):
            tosummon = MapleSummon(chr, this, chr.getPosition(), summonMovementType)
            if not tosummon.is替身术():
                chr.getCheatTracker().resetSummonAttack()
                chr.getMap().spawnSummon(tosummon)
                chr.addSummon(tosummon)
                tosummon.addHP(self.x)
                if self.is灵魂助力():
                    tosummon.addHP(1)

    def applyComboBuff(self, applyto: Any, combo: int) -> None:
        statups = new ArrayList<Pair<MapleBuffStat, Integer>>()
        statups.add(new Pair<MapleBuffStat, Integer>(MapleBuffStat.矛连击强化, combo / 10))
        applyto.getClient().getSession().write(MaplePacketCreator.giveBuff(self.sourceid, 29999, statups, this))
        starttime = int(time.time() * 1000)
        applyto.cancelEffect(this, True, -1, statups)
        cancelAction = CancelEffectAction(applyto, this, starttime)
        final ScheduledFuture<?> schedule = Timer.BuffTimer.getInstance().schedule(cancelAction, starttime + 29999 - int(time.time() * 1000))
        applyto.registerEffect(this, starttime, schedule)

    def applyEnergyBuff(self, applyto: Any, infinity: bool) -> None:
        stat = self.statups
        starttime = int(time.time() * 1000)
        if infinity:
            applyto.setBuffedValue(MapleBuffStat.能量获得, 0)
            applyto.getClient().getSession().write(MaplePacketCreator.能量条(stat, self.duration / 1000))
            applyto.registerEffect(this, starttime, None)
        else:
            applyto.cancelEffect(this, True, -1)
            applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveEnergyChargeTest(applyto.getId(), 10000, self.duration / 1000), False)
            cancelAction = CancelEffectAction(applyto, this, starttime)
            final ScheduledFuture<?> schedule = Timer.BuffTimer.getInstance().schedule(cancelAction, starttime + self.duration - int(time.time() * 1000))
            self.statups = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.能量获得, 10000))
            applyto.registerEffect(this, starttime, schedule)
            self.statups = stat

    def applyBuffEffect(self, applyfrom: Any, applyto: Any, primary: bool, newDuration: int) -> None:
        localDuration = newDuration
        if primary:
            localDuration = self.alchemistModifyVal(applyfrom, localDuration, False)
        localstatups = self.statups
        normal = True
        # switch (self.sourceid):
            # case 15001003:
            # case 15111005:
                applyto.getClient().getSession().write(MaplePacketCreator.givePirate(self.statups, localDuration / 1000, self.sourceid))
                normal = False
                break
            # case 5211006:
            # case 5220011:
                if applyto.getLinkMid() > 0:
                    applyto.getClient().getSession().write(MaplePacketCreator.cancelHoming())
                    applyto.getClient().getSession().write(MaplePacketCreator.giveHoming(5211006, applyto.getLinkMid(), 1))
                    normal = False
                    break
                return
            # case 4001003:
            # case 13101006:
            # case 14001003:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.隐身术, 0))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                break
            # case 32001003:
            # case 32120000:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.黑暗灵气, 1))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.蓝色灵气)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.黄色灵气)
                break
            # case 32101002:
            # case 32110000:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.蓝色灵气, 1))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.黄色灵气)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.黑暗灵气)
                break
            # case 32101003:
            # case 32120001:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.黄色灵气, 1))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.蓝色灵气)
                applyto.cancelEffectFromBuffStat(MapleBuffStat.黑暗灵气)
                break
            # case 35001001:
            # case 35101002:
            # case 35101009:
            # case 35111007:
            # case 35121005:
            # case 35121013:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金属机甲, 1))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                break
            # case 1111002:
            # case 11111001:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.斗气集中, 1))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                break
            # case 3101004:
            # case 3201004:
            # case 13101003:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.无形箭弩, 0))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                break
            # case 4111002:
            # case 14111000:
                stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.影分身, 0))
                applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                break
            # case 15111006:
                localstatups = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.闪光击, self.x))
                applyto.getClient().getSession().write(MaplePacketCreator.giveBuff(self.sourceid, localDuration, localstatups, this))
                normal = False
                break
            # case 1121010:
                applyto.handleOrbconsume()
                break
            # default:
                if self.isMorph() or self.isPirateMorph():
                    stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.变身, self.getMorph(applyto)))
                    applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                    break
                if self.isMonsterRiding():
                    localDuration = 2100000000
                    mountid = parseMountInfo(applyto, self.sourceid)
                    mountid2 = parseMountInfo_Pure(applyto, self.sourceid)
                    if mountid != 0 and mountid2 != 0:
                        stat2 = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.骑兽技能, 0))
                        applyto.cancelEffectFromBuffStat(MapleBuffStat.战神抗压)
                        applyto.cancelEffectFromBuffStat(MapleBuffStat.伤害反击)
                        applyto.cancelEffectFromBuffStat(MapleBuffStat.魔法反击)
                        applyto.getClient().getSession().write(MaplePacketCreator.giveMount(applyto, mountid, self.sourceid, stat2))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.showMonsterRiding(applyto.getId(), stat2, mountid, self.sourceid), False)
                        normal = False
                        break
                    if applyto.isAdmin():
                        applyto.dropMessage(6, "骑宠BUFF " + self.sourceid + " 错误，未找到这个骑宠的外形ID。")
                    return
                elif self.isMonsterS():
                    if applyto.getskillzq() <= 0:
                        return
                    mountid = parseMountInfoA(applyto, self.sourceid, applyto.getskillzq())
                    if mountid != 0:
                        stat3 = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.骑兽技能, 0))
                        applyto.getClient().getSession().write(MaplePacketCreator.giveMount(applyto, mountid, self.sourceid, stat3))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.showMonsterRiding(applyto.getId(), stat3, mountid, self.sourceid), False)
                        normal = False
                        break
                    return
                else:
                    if self.isSoaring():
                        localstatups = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.SOARING, 1))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), localstatups, this), False)
                        applyto.getClient().getSession().write(MaplePacketCreator.giveBuff(self.sourceid, localDuration, localstatups, this))
                        break
                    if self.isBerserkFury() or self.berserk2 > 0:
                        stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.狂暴战魂, 1))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                        break
                    if self.isDivineBody():
                        stat = Collections.singletonList(new Pair<MapleBuffStat, Integer>(MapleBuffStat.金刚霸体, 1))
                        applyto.getMap().broadcastMessage(applyto, MaplePacketCreator.giveForeignBuff(applyto, applyto.getId(), stat, this), False)
                        break
                    break
        if not self.isMonsterRiding_():
            applyto.cancelEffect(this, True, -1, localstatups)
        if normal and self.statups > 0:
            applyto.getClient().getSession().write(MaplePacketCreator.giveBuff(self.skill ? self.sourceid : (-self.sourceid), localDuration, self.statups, this))
        starttime = int(time.time() * 1000)
        if localDuration > 0:
            cancelAction = CancelEffectAction(applyto, this, starttime)
            final ScheduledFuture<?> schedule = Timer.BuffTimer.getInstance().schedule(cancelAction, starttime + localDuration - int(time.time() * 1000))
            applyto.registerEffect(this, starttime, schedule, localstatups)

    def parseMountInfoA(self, player: Any, skillid: int, s: int) -> int:
        # switch (skillid):
            # case 1017:
            # case 10001019:
            # case 20001019:
                return GameConstants.getMountS(s)
            # default:
                return GameConstants.getMountS(s)

    def parseMountInfo(self, player: Any, skillid: int) -> int:
        # switch (skillid):
            # case 1004:
            # case 10001004:
            # case 20001004:
            # case 20011004:
            # case 30001004:
                if player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-118)) is not None and player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-119)) is not None:
                    return player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-118)).getItemId()
                return parseMountInfo_Pure(player, skillid)
            # default:
                return GameConstants.getMountItem(skillid)

    def parseMountInfo_Pure(self, player: Any, skillid: int) -> int:
        # switch (skillid):
            # case 1004:
            # case 11004:
            # case 10001004:
            # case 20001004:
            # case 20011004:
            # case 20021004:
            # case 80001000:
                if player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18)) is not None and player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-19)) is not None:
                    return player.getInventory(MapleInventoryType.EQUIPPED).getItem((short)(-18)).getItemId()
                return 0
            # default:
                return GameConstants.getMountItem(skillid)

    def calcHPChange(self, applyfrom: Any, primary: bool) -> int:
        hpchange = 0
        if self.hp != 0:
            if not self.skill:
                if primary:
                    hpchange += self.alchemistModifyVal(applyfrom, self.hp, True)
                else:
                    hpchange += self.hp
                if applyfrom.hasDisease(MapleDisease.ZOMBIFY):
                    hpchange /= 2
            else:
                hpchange += makeHealHP(self.hp / 100.0, applyfrom.getStat().getTotalMagic(), 3.0, 5.0)
                if applyfrom.hasDisease(MapleDisease.ZOMBIFY):
                    hpchange = -hpchange
        if self.hpR != 0.0:
            hpchange += (int)(applyfrom.getStat().getCurrentMaxHp() * self.hpR) / (applyfrom.hasDisease(MapleDisease.ZOMBIFY) ? 2 : 1)
        if primary and self.hpCon != 0:
            hpchange -= self.hpCon
        # switch (self.sourceid):
            # case 4211001:
                stat = applyfrom.getStat()
                v42 = self.getY() + 100
                v43 = Randomizer.rand(1, 100) + 100
                hpchange = (int)((v43 * stat.getLuk() * 0.033 + stat.getDex()) * v42 * 0.002)
                hpchange += makeHealHP(self.getY() / 100.0, applyfrom.getStat().getTotalLuk(), 2.3, 3.5)
                break
        return hpchange

    def calcMPChange(self, applyfrom: Any, primary: bool) -> int:
        mpchange = 0
        if self.mp != 0:
            if primary:
                mpchange += self.alchemistModifyVal(applyfrom, self.mp, True)
            else:
                mpchange += self.mp
        if self.mpR != 0.0:
            mpchange += (int)(applyfrom.getStat().getCurrentMaxMp() * self.mpR)
        if primary and self.mpCon != 0:
            mod = 1.0
            ElemSkillId = getElementalAmp(applyfrom.getJob())
            if ElemSkillId != -1:
                amp = SkillFactory.getSkill(ElemSkillId)
                ampLevel = applyfrom.getSkillLevel(amp)
                if ampLevel > 0:
                    ampStat = amp.getEffect(ampLevel)
                    mod = ampStat.getX() / 100.0
            Concentrate = applyfrom.getBuffedSkill_X(MapleBuffStat.集中精力)
            percent_off = applyfrom.getStat().mpconReduce + ((Concentrate is None) ? 0 : Concentrate)
            if applyfrom.getBuffedValue(MapleBuffStat.终极无限) is not None:
                mpchange = 0
            else:
                mpchange -= (int)((self.mpCon - self.mpCon * percent_off / 100) * mod)
        return mpchange

    def alchemistModifyVal(self, chr: Any, val: int, withX: bool) -> int:
        if not self.skill:
            offset = chr.getStat().RecoveryUP
            alchemistEffect = self.getAlchemistEffect(chr)
            if alchemistEffect is not None:
                offset += (withX ? alchemistEffect.getX() : alchemistEffect.getY())
            else:
                offset += 100
            return val * offset / 100
        return val

    def getAlchemistEffect(self, chr: Any) -> Any:
        # switch (chr.getJob()):
            # case 411:
            # case 412:
                al = SkillFactory.getSkill(4110000)
                if chr.getSkillLevel(al) <= 0:
                    return None
                return al.getEffect(chr.getSkillLevel(al))
            # case 1411:
            # case 1412:
                al = SkillFactory.getSkill(14110003)
                if chr.getSkillLevel(al) <= 0:
                    return None
                return al.getEffect(chr.getSkillLevel(al))
            # default:
                if not GameConstants.isResist(chr.getJob()):
                    return None
                al = SkillFactory.getSkill(30000002)
                if chr.getSkillLevel(al) <= 0:
                    return None
                return al.getEffect(chr.getSkillLevel(al))

    def setSourceId(self, newid: int) -> None:
        self.sourceid = newid

    def isGmBuff(self) -> bool:
        # switch (self.sourceid):
            # case 1005:
            # case 9001000:
            # case 9001001:
            # case 9001002:
            # case 9001003:
            # case 9001005:
            # case 9001008:
            # case 10001005:
            # case 20001005:
            # case 20011005:
            # case 30001005:
                return True
            # default:
                return False

    def translated_is能量获得(self) -> bool:
        return self.skill and (self.sourceid == 5110001 or self.sourceid == 15100004)

    def isMonsterBuff(self) -> bool:
        # switch (self.sourceid):
            # case 1201006:
            # case 2101003:
            # case 2111004:
            # case 2201003:
            # case 2211004:
            # case 2311005:
            # case 4111003:
            # case 4121004:
            # case 4221004:
            # case 4321002:
            # case 12101001:
            # case 12111002:
            # case 14111001:
            # case 22121000:
            # case 22141003:
            # case 22151001:
            # case 22161002:
                return self.skill
            # default:
                return False

    def setPartyBuff(self, pb: bool) -> None:
        self.partyBuff = pb

    def isPartyBuff(self) -> bool:
        if self.lt is None or self.rb is None or not self.partyBuff:
            return self.isSoulStone()
        # switch (self.sourceid):
            # case 1211003:
            # case 1211004:
            # case 1211005:
            # case 1211006:
            # case 1211007:
            # case 1211008:
            # case 1221003:
            # case 1221004:
            # case 4311001:
            # case 11111007:
            # case 12101005:
                return False
            # default:
                return True

    def translated_is群体治愈(self) -> bool:
        return self.sourceid == 2301002 or self.sourceid == 9101000

    def translated_is复活术(self) -> bool:
        return self.sourceid == 9001005 or self.sourceid == 2321006

    def translated_is伺机待发(self) -> bool:
        return self.sourceid == 5121010

    def getHp(self) -> int:
        return self.hp

    def getMp(self) -> int:
        return self.mp

    def getMastery(self) -> int:
        return self.mastery

    def getWatk(self) -> int:
        return self.watk

    def getMatk(self) -> int:
        return self.matk

    def getWdef(self) -> int:
        return self.wdef

    def getMdef(self) -> int:
        return self.mdef

    def getAcc(self) -> int:
        return self.acc

    def getAvoid(self) -> int:
        return self.avoid

    def getHands(self) -> int:
        return self.hands

    def getSpeed(self) -> int:
        return self.speed

    def getJump(self) -> int:
        return self.jump

    def getDuration(self) -> int:
        return self.duration

    def isOverTime(self) -> bool:
        return self.overTime

    def getStatups(self) -> list:
        return self.statups

    def sameSource(self, effect: Any) -> bool:
        return effect is not None and self.sourceid == effect.sourceid and self.skill == effect.skill

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getZ(self) -> int:
        return self.z

    def getDamage(self) -> int:
        return self.damage

    def getAttackCount(self) -> int:
        return self.attackCount

    def getBulletCount(self) -> int:
        return self.bulletCount

    def getBulletConsume(self) -> int:
        return self.bulletConsume

    def getMobCount(self) -> int:
        return self.mobCount

    def getMoneyCon(self) -> int:
        return self.moneyCon

    def getCooldown(self) -> int:
        return self.cooldown

    def getMonsterStati(self) -> dict:
        return self.monsterStatus

    def getBerserk(self) -> int:
        return self.berserk

    def translated_is隐藏术(self) -> bool:
        return self.skill and self.sourceid == 9001004

    def isDragonBlood(self) -> bool:
        return self.skill and self.sourceid == 1311008

    def isBerserk(self) -> bool:
        return self.skill and self.sourceid == 1320006

    def translated_is灵魂助力(self) -> bool:
        return self.skill and self.sourceid == 1321007

    def translated_is生命分流(self) -> bool:
        return self.skill and self.sourceid == 5101005

    def isMonsterRiding_(self) -> bool:
        return self.skill and (self.sourceid == 1004 or self.sourceid == 10001004 or self.sourceid == 20001004 or self.sourceid == 20011004 or self.sourceid == 30001004)

    def isMonsterRiding(self) -> bool:
        return self.skill and (self.isMonsterRiding_() or GameConstants.getMountItem(self.sourceid) != 0)

    def isMonsterS(self) -> bool:
        return (self.skill and self.sourceid == 1017) or self.sourceid == 20001019 or self.sourceid == 10001019

    def translated_is神圣祈祷(self) -> bool:
        return self.skill and self.sourceid == 2311003

    def translated_is时空门(self) -> bool:
        return self.skill and (self.sourceid == 2311002 or self.sourceid == 8001 or self.sourceid == 10008001 or self.sourceid == 20008001 or self.sourceid == 20018001 or self.sourceid == 30008001)

    def isMesoGuard(self) -> bool:
        return self.skill and self.sourceid == 4211005

    def isCharge(self) -> bool:
        # switch (self.sourceid):
            # case 1211003:
            # case 1211008:
            # case 11111007:
            # case 12101005:
            # case 15101006:
            # case 21111005:
                return self.skill
            # default:
                return False

    def isPoison(self) -> bool:
        # switch (self.sourceid):
            # case 2101005:
            # case 2111003:
            # case 2111006:
            # case 2121003:
            # case 2221003:
            # case 12111005:
            # case 22161002:
                return self.skill
            # default:
                return False

    def isMist(self) -> bool:
        return self.skill and (self.sourceid == 2111003 or self.sourceid == 4221006 or self.sourceid == 12111005 or self.sourceid == 14111006 or self.sourceid == 22161003)

    def translated_is暗器伤人(self) -> bool:
        return self.skill and self.sourceid == 4121006

    def translated_is净化(self) -> bool:
        return self.skill and (self.sourceid == 2311001 or self.sourceid == 9001000)

    def translated_is勇士的意志(self) -> bool:
        # switch (self.sourceid):
            # case 1121011:
            # case 1221012:
            # case 1321010:
            # case 2121008:
            # case 2221008:
            # case 2321009:
            # case 3121009:
            # case 3221008:
            # case 4121009:
            # case 4221008:
            # case 5121008:
            # case 5221010:
            # case 21121008:
                return self.skill
            # default:
                return False

    def isAranCombo(self) -> bool:
        return self.sourceid == 21000000

    def translated_is斗气集中(self) -> bool:
        # switch (self.sourceid):
            # case 1111002:
            # case 11111001:
                return self.skill
            # default:
                return False

    def isPirateMorph(self) -> bool:
        # switch (self.sourceid):
            # case 5111005:
            # case 5121003:
            # case 15111002:
                return self.skill
            # default:
                return False

    def isMorph(self) -> bool:
        return self.morphId > 0

    def getMorph(self) -> int:
        # switch (self.sourceid):
            # case 5111005:
            # case 15111002:
                return 1000
            # case 5121003:
                return 1001
            # case 5101007:
                return 1002
            # case 13111005:
                return 1003
            # default:
                return self.morphId

    def isDivineBody(self) -> bool:
        # switch (self.sourceid):
            # case 1010:
            # case 10001010:
            # case 20001010:
            # case 20011010:
            # case 30001010:
                return self.skill
            # default:
                return False

    def isBerserkFury(self) -> bool:
        # switch (self.sourceid):
            # case 1011:
            # case 10001011:
            # case 20001011:
            # case 20011011:
            # case 30001011:
                return self.skill
            # default:
                return False

    def getMorph_chr(self, chr: Any) -> int:
        morph = self.getMorph()
        # switch (morph):
            # case 1000:
            # case 1001:
            # case 1003:
                return morph + ((chr.getGender() == 1) ? 100 : 0)
            # default:
                return morph

    def getLevel(self) -> int:
        return self.level

    def getSummonMovementType(self) -> Any:
        if not self.skill:
            return None
        # switch (self.sourceid):
            # case 3111002:
            # case 3211002:
            # case 5211001:
            # case 5220002:
            # case 13111004:
                return SummonMovementType.不会移动
            # case 2311006:
            # case 3111005:
            # case 3121006:
            # case 3211005:
            # case 3221005:
                return SummonMovementType.跟随并且随机移动打怪
            # case 5211002:
                return SummonMovementType.CIRCLE_STATIONARY
            # case 32111006:
                return SummonMovementType.WALK_STATIONARY
            # case 1321007:
            # case 2121005:
            # case 2221005:
            # case 2321003:
            # case 11001004:
            # case 12001004:
            # case 12111004:
            # case 13001004:
            # case 14001005:
            # case 15001004:
                return SummonMovementType.飞行跟随
            # default:
                return None

    def isSkill(self) -> bool:
        return self.skill

    def getSourceId(self) -> int:
        return self.sourceid

    def isSoaring(self) -> bool:
        # switch (self.sourceid):
            # case 1026:
            # case 10001026:
            # case 20001026:
            # case 20011026:
            # case 30001026:
                return self.skill
            # default:
                return False

    def isFinalAttack(self) -> bool:
        # switch (self.sourceid):
            # case 11101002:
            # case 13101002:
                return self.skill
            # default:
                return False

    def makeChanceResult(self) -> bool:
        return self.prop == 100 or Randomizer.nextInt(99) < self.prop

    def getProb(self) -> int:
        return self.prop

    def isBattleShip(self) -> bool:
        return self.skill and self.sourceid == 5221006

    def getMpCon(self) -> int:
        return self.mpCon

    def calculateBoundingBox_posFrom_facingLeft_addedRange(self, posFrom: Any, facingLeft: bool, addedRange: int) -> Any:
        if self.lt is None or self.rb is None:
            return Rectangle((facingLeft ? (-200 - addedRange) : 0) + posFrom.x, -100 - addedRange + posFrom.y, 200 + addedRange, 100 + addedRange)
        mylt = None
        myrb = None
        if facingLeft:
            mylt = Point(self.lt.x + posFrom.x - addedRange, self.lt.y + posFrom.y)
            myrb = Point(self.rb.x + posFrom.x, self.rb.y + posFrom.y)
        else:
            myrb = Point(self.lt.x * -1 + posFrom.x + addedRange, self.rb.y + posFrom.y)
            mylt = Point(self.rb.x * -1 + posFrom.x, self.lt.y + posFrom.y)
        return Rectangle(mylt.x, mylt.y, myrb.x - mylt.x, myrb.y - mylt.y)

    def run(self) -> None:
        realTarget = self.target.get()
        if realTarget is not None and not realTarget.isClone():
            realTarget.cancelEffect(self.effect, False, self.startTime)


# Inner class from Java (originally nested)
class CancelEffectAction(Runnable):
    """
    Class CancelEffectAction
    Implements: Runnable
    """

    def __init__(self, target: Any, effect: Any, startTime: int):
        self.effect = None
        self.target = None
        self.startTime = None
        self.effect = effect
        self.target = new WeakReference<MapleCharacter>(target)
        self.startTime = startTime


    def run(self) -> None:
        realTarget = self.target.get()
        if realTarget is not None and not realTarget.isClone():
            realTarget.cancelEffect(self.effect, False, self.startTime)

