"""
MapleMonster - Converted from Java source
Original: server/life/MapleMonster.java
Package: server.life
"""

from concurrent.futures import Future
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
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
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleDisease import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from scripting.EventInstanceManager import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapScriptMethods import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from tools.ConcurrentEnumMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes


class MapleMonster(AbstractLoadedMapleLife):
    """
    Class MapleMonster
    Extends: AbstractLoadedMapleLife
    """

    def __init__(self, id: int, stats: Any):
        self.poisonsLock = None
        self.poisons = None
        self.overrideStats = None
        self.stats = None
        self.ostats = None
        self.hp = 0
        self.mp = 0
        self.venom_counter = 0
        self.carnivalTeam = 0
        self.map = None
        self.sponge = None
        self.linkoid = 0
        self.lastNode = 0
        self.lastNodeController = 0
        self.highestDamageChar = 0
        self.controller = None
        self.fake = False
        self.dropsDisabled = False
        self.controllerHasAggro = False
        self.controllerKnowsAboutAggro = False
        self.attackers = None
        self.eventInstance = None
        self.listener = None
        self.reflectpack = None
        self.nodepack = None
        self.stati = {}
        self.usedSkills = {}
        self.stolen = 0
        self.shouldDropItem = False
        self.attacker = None
        self.lastAttackTime = 0
        self.exp = 0
        self.ptysize = 0
        self.Class_Bonus_EXP = 0
        self.网吧特别经验 = 0
        self.lastKnownParty = None
        self.damage = 0
        self.lastAttackTime = 0
        self.poisonDamage = None
        self.chr = None
        super(id)
        self.poisonsLock = ReentrantReadWriteLock()
        self.poisons = []
        self.ostats = None
        self.sponge = new WeakReference<MapleMonster>(None)
        self.linkoid = 0
        self.lastNode = -1
        self.lastNodeController = -1
        self.highestDamageChar = 0
        self.controller = new WeakReference<MapleCharacter>(None)
        self.attackers = []
        self.listener = None
        self.reflectpack = None
        self.nodepack = None
        self.stati = new ConcurrentEnumMap<MonsterStatus, MonsterStatusEffect>(MonsterStatus.class)
        self.stolen = -1
        self.shouldDropItem = False
        self.initWithStats(stats)


    def initWithStats(self, stats: Any) -> None:
        self.setStance(5)
        self.stats = stats
        self.hp = stats.getHp()
        self.mp = stats.getMp()
        self.venom_counter = 0
        self.carnivalTeam = -1
        self.fake = False
        self.dropsDisabled = False
        if stats.getNoSkills() > 0:
            self.usedSkills = {}

    def getStats(self) -> Any:
        return self.stats

    def disableDrops(self) -> None:
        self.dropsDisabled = True

    def dropsDisabled(self) -> bool:
        return self.dropsDisabled

    def setSponge(self, mob: Any) -> None:
        self.sponge = new WeakReference<MapleMonster>(mob)

    def setMap(self, map: Any) -> None:
        self.map = map
        self.startDropItemSchedule()

    def getHp(self) -> int:
        return self.hp

    def setHp(self, hp: int) -> None:
        self.hp = hp

    def getMobMaxHp(self) -> int:
        if self.ostats is not None:
            return self.ostats.getHp()
        return self.stats.getHp()

    def getMp(self) -> int:
        return self.mp

    def setMp(self, mp: int) -> None:
        if mp < 0:
            mp = 0
        self.mp = mp

    def getMobMaxMp(self) -> int:
        if self.ostats is not None:
            return self.ostats.getMp()
        return self.stats.getMp()

    def getMobExp(self) -> int:
        if self.ostats is not None:
            return self.ostats.getExp()
        return self.stats.getExp()

    def setOverrideStats(self, ostats: Any) -> None:
        self.ostats = ostats
        self.hp = ostats.getHp()
        self.mp = ostats.getMp()

    def getSponge(self) -> Any:
        return self.sponge.get()

    def getVenomMulti(self) -> int:
        return self.venom_counter

    def setVenomMulti(self, venom_counter: int) -> None:
        self.venom_counter = venom_counter

    def damage(self, from: Any, damage: int, updateAttackTime: bool) -> None:
        self.damage(from, damage, updateAttackTime, 0)

    def damage_from_damage_updateAttackTime_lastSkill(self, from: Any, damage: int, updateAttackTime: bool, lastSkill: int) -> None:
        if from is None or damage <= 0 or not self.isAlive():
            return
        attacker = None
        if from.getParty() is not None:
            attacker = PartyAttackerEntry(from.getParty().getId(), self.map.getChannel())
        else:
            attacker = SingleAttackerEntry(from, self.map.getChannel())
        replaced = False
        for aentry in self.attackers:
            if aentry == (attacker):
                attacker = aentry
                replaced = True
                break
        if not replaced:
            self.attackers.add(attacker)
        rDamage = max(0, min(damage, self.hp))
        attacker.addDamage(from, rDamage, updateAttackTime)
        if self.stats.getSelfD() != -1:
            self.hp -= rDamage
            if self.hp > 0:
                if self.hp < self.stats.getSelfDHp():
                    self.map.killMonster(this, from, False, False, self.stats.getSelfD(), lastSkill)
                else:
                    for mattacker in self.attackers:
                        for cattacker in mattacker.getAttackers():
                            if cattacker.getAttacker().getMap() == from.getMap() and cattacker.getLastAttackTime() >= int(time.time() * 1000) - 4000:
                                cattacker.getAttacker().getClient().getSession().write(MobPacket.showMonsterHP(self.getObjectId(), math.ceil(self.hp * 100.0 / self.getMobMaxHp())))
            else:
                self.map.killMonster(this, from, True, False, 1, lastSkill)
        else:
            if self.sponge.get() is not None and self.sponge.get().hp > 0:
                mapleMonster = self.sponge.get()
                mapleMonster.hp -= rDamage
                if self.sponge.get().hp <= 0:
                    self.map.broadcastMessage(MobPacket.showBossHP(self.sponge.get().getId(), -1, self.sponge.get().getMobMaxHp()))
                    self.map.killMonster(self.sponge.get(), from, True, False, 1, lastSkill)
                else:
                    self.map.broadcastMessage(MobPacket.showBossHP(self.sponge.get()))
            if self.hp > 0:
                self.hp -= rDamage
                if self.eventInstance is not None:
                    self.eventInstance.monsterDamaged(from, this, rDamage)
                else:
                    em = from.getEventInstance()
                    if em is not None:
                        em.monsterDamaged(from, this, rDamage)
                if self.sponge.get() is None and self.hp > 0:
                    # switch (self.stats.getHPDisplayType()):
                        # case 0:
                            self.map.broadcastMessage(MobPacket.showBossHP(this), self.getPosition())
                            break
                        # case 1:
                            self.map.broadcastMessage(from, MobPacket.damageFriendlyMob(this, damage, True), False)
                            break
                        # case -1:
                        # case 2:
                            oid = self.getObjectId()
                            percent = self.hp * 100.0 / self.getMobMaxHp()
                            show = math.ceil(percent)
                            self.map.broadcastMessage(MobPacket.showMonsterHP(self.getObjectId(), math.ceil(self.hp * 100.0 / self.getMobMaxHp())))
                            from.mulung_EnergyModify(True)
                            break
                        # case 3:
                            for mattacker2 in self.attackers:
                                for cattacker2 in mattacker2.getAttackers():
                                    if cattacker2.getAttacker().getMap() == from.getMap() and cattacker2.getLastAttackTime() >= int(time.time() * 1000) - 4000:
                                        cattacker2.getAttacker().getClient().getSession().write(MobPacket.showMonsterHP(self.getObjectId(), math.ceil(self.hp * 100.0 / self.getMobMaxHp())))
                            break
                        # default:
                            print(self.stats.isBoss() + " " + self.stats.getHPDisplayType())
                            break
                if self.hp <= 0:
                    if self.stats.getHPDisplayType() == 0 or self.stats.getHPDisplayType() == -1:
                        self.map.broadcastMessage(MobPacket.showBossHP(self.getId(), -1, self.getMobMaxHp()), self.getPosition())
                    self.map.killMonster(this, from, True, False, 1, lastSkill)
        self.startDropItemSchedule()

    def heal(self, hp: int, mp: int, broadcast: bool) -> None:
        TotalHP = self.getHp() + hp
        TotalMP = self.getMp() + mp
        if TotalHP >= self.getMobMaxHp():
            self.setHp(self.getMobMaxHp())
        else:
            self.setHp(TotalHP)
        if TotalMP >= self.getMp():
            self.setMp(self.getMp())
        else:
            self.setMp(TotalMP)
        if broadcast:
            self.map.broadcastMessage(MobPacket.healMonster(self.getObjectId(), hp))
        elif self.sponge.get() is not None:
            mapleMonster = self.sponge.get()
            mapleMonster.hp += hp

    def giveExpToCharacter(self, attacker: Any, exp: int, highestDamage: bool, numExpSharers: int, pty: int, Class_Bonus_EXP_PERCENT: int, 网吧特别经验_百分比: int, lastskillID: int) -> None:
        if highestDamage:
            if self.eventInstance is not None:
                self.eventInstance.monsterKilled(attacker, this)
            else:
                em = attacker.getEventInstance()
                if em is not None:
                    em.monsterKilled(attacker, this)
            self.highestDamageChar = attacker.getId()
        if exp > 0:
            mse = self.stati.get(MonsterStatus.挑衅)
            if mse is not None:
                exp += (int)(exp * (mse.getX() / 100.0))
            holySymbol = attacker.getBuffedValue(MapleBuffStat.神圣祈祷)
            if holySymbol is not None:
                if numExpSharers == 1:
                    exp *= (int)(1.0 + holySymbol / 500.0)
                else:
                    exp *= (int)(1.0 + holySymbol / 100.0)
            if attacker.hasDisease(MapleDisease.诅咒):
                exp /= 2
            exp *= attacker.getEXPMod() * (int)(attacker.getStat().expBuff / 100.0)
            exp = min(Integer.MAX_VALUE, exp * ((attacker.getLevel() < 10) ? GameConstants.getExpRate_Below10(attacker.getJob()) : ChannelServer.getInstance(self.map.getChannel()).getExpRate()))
            Class_Bonus_EXP = 0
            if Class_Bonus_EXP_PERCENT > 0:
                Class_Bonus_EXP = (int)(exp / 100.0 * Class_Bonus_EXP_PERCENT)
            网吧特别经验 = 0
            if 网吧特别经验_百分比 > 0:
                网吧特别经验 = (int)(exp / 100.0 * 网吧特别经验_百分比)
            attacker.gainExpMonster(exp, True, highestDamage, pty, Class_Bonus_EXP, 网吧特别经验)
        attacker.mobKilled(self.getId(), lastskillID)

    def killBy(self, killer: Any, lastSkill: int) -> int:
        totalBaseExp = self.getMobExp()
        highest = None
        highdamage = 0
        for attackEntry in self.attackers:
            if attackEntry.getDamage() > highdamage:
                highest = attackEntry
                highdamage = attackEntry.getDamage()
        for attackEntry2 in self.attackers:
            baseExp = math.ceil(totalBaseExp * (attackEntry2.getDamage() / self.getMobMaxHp()))
            attackEntry2.killedMob(self.getMap(), baseExp, attackEntry2 == highest, lastSkill)
        controll = self.controller.get()
        if controll is not None:
            controll.getClient().getSession().write(MobPacket.stopControllingMonster(self.getObjectId()))
            controll.stopControllingMonster(this)
        # switch (self.getId()):
            # default:
                self.spawnRevives(self.getMap())
                if self.eventInstance is not None:
                    self.eventInstance.unregisterMonster(this)
                    self.eventInstance = None
                if killer is not None and killer.getPyramidSubway() is not None:
                    killer.getPyramidSubway().onKill(killer)
                oldSponge = self.getSponge()
                self.sponge = new WeakReference<MapleMonster>(None)
                if oldSponge is not None and oldSponge.isAlive():
                    set = True
                    for mon in self.map.getAllMonstersThreadsafe():
                        mons = mon
                        if mons.getObjectId() != oldSponge.getObjectId() and mons.getObjectId() != self.getObjectId() and (mons.getSponge() == oldSponge or mons.getLinkOid() == oldSponge.getObjectId()):
                            set = False
                            break
                    if set:
                        self.map.killMonster(oldSponge, killer, True, False, 1)
                self.nodepack = None
                self.reflectpack = None
                self.stati.clear()
                self.cancelDropItem()
                if self.listener is not None:
                    self.listener.monsterKilled()
                v1 = self.highestDamageChar
                self.highestDamageChar = 0
                return v1

    def spawnRevives(self, map: Any) -> None:
        toSpawn = self.stats.getRevives()
        if toSpawn is None:
            return
        spongy = None
        # switch (self.getId()):
            # case 8810118:
            # case 8810119:
            # case 8810120:
            # case 8810121:
                for i in toSpawn:
                    mob = MapleLifeFactory.getMonster(i)
                    mob.setPosition(self.getPosition())
                    if self.eventInstance is not None:
                        self.eventInstance.registerMonster(mob)
                    if self.dropsDisabled():
                        mob.disableDrops()
                    # switch (mob.getId()):
                        # case 8810119:
                        # case 8810120:
                        # case 8810121:
                        # case 8810122:
                            spongy = mob
                            continue
                if spongy is not None:
                    map.spawnRevives(spongy, self.getObjectId())
                    for mon in map.getAllMonstersThreadsafe():
                        mons = mon
                        if mons.getObjectId() != spongy.getObjectId() and (mons.getSponge() == this or mons.getLinkOid() == self.getObjectId()):
                            mons.setSponge(spongy)
                            mons.setLinkOid(spongy.getObjectId())
                    break
                break
            # case 8810026:
            # case 8810130:
            # case 8820008:
            # case 8820009:
            # case 8820010:
            # case 8820011:
            # case 8820012:
            # case 8820013:
                mobs = []
                for j in toSpawn:
                    mob2 = MapleLifeFactory.getMonster(j)
                    mob2.setPosition(self.getPosition())
                    if self.eventInstance is not None:
                        self.eventInstance.registerMonster(mob2)
                    if self.dropsDisabled():
                        mob2.disableDrops()
                    # switch (mob2.getId()):
                        # case 8810018:
                        # case 8810118:
                        # case 8820009:
                        # case 8820010:
                        # case 8820011:
                        # case 8820012:
                        # case 8820013:
                        # case 8820014:
                            spongy = mob2
                            continue
                        # default:
                            mobs.add(mob2)
                            continue
                if spongy is not None:
                    map.spawnRevives(spongy, self.getObjectId())
                    for k in mobs:
                        k.setSponge(spongy)
                        map.spawnRevives(k, self.getObjectId())
                    break
                break
            # default:
                for i in toSpawn:
                    mob = MapleLifeFactory.getMonster(i)
                    if self.eventInstance is not None:
                        self.eventInstance.registerMonster(mob)
                    mob.setPosition(self.getPosition())
                    if self.dropsDisabled():
                        mob.disableDrops()
                    map.spawnRevives(mob, self.getObjectId())
                    if mob.getId() == 9300216:
                        map.broadcastMessage(MaplePacketCreator.environmentChange("Dojang/clear", 4))
                        map.broadcastMessage(MaplePacketCreator.environmentChange("dojang/end/clear", 3))
                break

    def isAlive(self) -> bool:
        return self.hp > 0

    def setCarnivalTeam(self, team: int) -> None:
        self.carnivalTeam = team

    def getCarnivalTeam(self) -> int:
        return self.carnivalTeam

    def getController(self) -> Any:
        return self.controller.get()

    def setController(self, controller: Any) -> None:
        self.controller = new WeakReference<MapleCharacter>(controller)

    def switchController(self, newController: Any, immediateAggro: bool) -> None:
        controllers = self.getController()
        if controllers == newController:
            return
        if controllers is not None:
            controllers.stopControllingMonster(this)
            controllers.getClient().getSession().write(MobPacket.stopControllingMonster(self.getObjectId()))
        newController.controlMonster(this, immediateAggro)
        self.setController(newController)
        if immediateAggro:
            self.setControllerHasAggro(True)
        self.setControllerKnowsAboutAggro(False)
        if self.getId() == 9300275 and self.map.getId() >= 921120100 and self.map.getId() < 921120500:
            if self.lastNodeController != -1 and self.lastNodeController != newController.getId():
                self.resetShammos(newController.getClient())
            else:
                self.setLastNodeController(newController.getId())

    def resetShammos(self, c: Any) -> None:
        def _task_1():
            if c.getPlayer() is not None:
                c.getPlayer().changeMap(c.getPlayer().getMap(), c.getPlayer().getMap().getPortal(0))
                if MapleMonster.self.map.getCharactersThreadsafe() > 1:
                    MapScriptMethods.startScript_FirstUser(c, "shammos_Fenter")

        self.map.killAllMonsters(True)
        self.map.broadcastMessage(MaplePacketCreator.serverNotice(5, "A player has moved too far from Shammos. Shammos is going back to the start."))
        Timer.EtcTimer.getInstance().schedule(_task_1, 500)

    def run(self) -> None:
        if c.getPlayer() is not None:
            c.getPlayer().changeMap(c.getPlayer().getMap(), c.getPlayer().getMap().getPortal(0))
            if MapleMonster.self.map.getCharactersThreadsafe() > 1:
                MapScriptMethods.startScript_FirstUser(c, "shammos_Fenter")

    def addListener(self, listener: Any) -> None:
        self.listener = listener

    def isControllerHasAggro(self) -> bool:
        return self.controllerHasAggro

    def setControllerHasAggro(self, controllerHasAggro: bool) -> None:
        self.controllerHasAggro = controllerHasAggro

    def isControllerKnowsAboutAggro(self) -> bool:
        return self.controllerKnowsAboutAggro

    def setControllerKnowsAboutAggro(self, controllerKnowsAboutAggro: bool) -> None:
        self.controllerKnowsAboutAggro = controllerKnowsAboutAggro

    def sendSpawnData(self, client: Any) -> None:
        if not self.isAlive():
            return
        if self.isFake():
            client.getSession().write(MobPacket.spawnFakeMonster(this, 0))
        else:
            client.getSession().write(MobPacket.spawnMonster(this, False))
        if self.reflectpack is not None:
            client.getSession().write(self.reflectpack)
        if self.lastNode >= 0 and self.getId() == 9300275 and self.map.getId() >= 921120100 and self.map.getId() < 921120500:
            if self.lastNodeController != -1:
                self.resetShammos(client)
            else:
                self.setLastNodeController(client.getPlayer().getId())

    def sendDestroyData(self, client: Any) -> None:
        if self.getEventInstance() is not None and self.lastNode >= 0:
            self.resetShammos(client)
        else:
            client.getSession().write(MobPacket.killMonster(self.getObjectId(), 0))
        if self.getController() is not None and client.getPlayer() is not None and client.getPlayer().getId() == self.getController().getId():
            client.getPlayer().stopControllingMonster(this)

    def toString(self) -> str:
        sb = ""
        sb.append(self.stats.getName())
        sb.append("(")
        sb.append(self.getId())
        sb.append(") (等級 ")
        sb.append(self.stats.getLevel())
        sb.append(") 在 (X")
        sb.append(self.getPosition().x)
        sb.append("/ Y")
        sb.append(self.getPosition().y)
        sb.append(") 坐标 ")
        sb.append(self.getHp())
        sb.append("/ ")
        sb.append(self.getMobMaxHp())
        sb.append("血量, ")
        sb.append(self.getMp())
        sb.append("/ ")
        sb.append(self.getMobMaxMp())
        sb.append(" 魔力, 反应堆: ")
        sb.append(self.getObjectId())
        sb.append(" or 仇恨目标 : ")
        chr = self.controller.get()
        sb.append((chr is not None) ? chr.getName() : "无")
        return sb

    def getType(self) -> Any:
        return MapleMapObjectType.MONSTER

    def getEventInstance(self) -> Any:
        return self.eventInstance

    def setEventInstance(self, eventInstance: Any) -> None:
        self.eventInstance = eventInstance

    def getStatusSourceID(self, status: Any) -> int:
        effect = self.stati.get(status)
        if effect is not None:
            return effect.getSkill()
        return -1

    def getEffectiveness(self, e: Any) -> Any:
        if self.stati > 0 and self.stati.get(MonsterStatus.巫毒术) is not None:
            return ElementalEffectiveness.正常
        return self.stats.getEffectiveness(e)

    def applyStatus(self, from: Any, status: Any, poison: bool, duration: int, venom: bool) -> None:
        self.applyStatus(from, status, poison, duration, venom, True)

    def applyStatus_from_status_poison_duration_venom_checkboss(self, from: Any, status: Any, poison: bool, duration: int, venom: bool, checkboss: bool) -> None:
        def _task_1():
            MapleMonster.self.cancelStatus(stat)

        if not self.isAlive():
            return
        skilz = SkillFactory.getSkill(status.getSkill())
        if skilz is not None:
            # switch (self.stats.getEffectiveness(skilz.getElement())):
                # case 免疫:
                # case 增强:
                    return
                # case 正常:
                # case 虚弱:
                    break
                # default:
                    return
        statusSkill = status.getSkill()
        Label_0277:
            # switch (statusSkill):
                # case 2111006:
                    # switch (self.stats.getEffectiveness(Element.POISON)):
                        # case 免疫:
                        # case 增强:
                            return
                        # default:
                            Label_0277 = None
                # case 2211006:
                    # switch (self.stats.getEffectiveness(Element.ICE)):
                        # case 免疫:
                        # case 增强:
                            return
                        # default:
                            Label_0277 = None
                # case 4120005:
                # case 4220005:
                # case 14110004:
                    # switch (self.stats.getEffectiveness(Element.POISON)):
                        # case 免疫:
                        # case 增强:
                            return
                        # default:
                            Label_0277 = None
        stat = status.getStati()
        if self.stats.isNoDoom() and stat == MonsterStatus.巫毒术:
            return
        if self.getId() == 9600000 and (stat == MonsterStatus.冻结 or stat == MonsterStatus.中毒 or stat == MonsterStatus.眩晕):
            return
        if self.stats.isBoss():
            if self.stats.isBoss() and (stat == MonsterStatus.眩晕 or stat == MonsterStatus.中毒):
                return
            if checkboss and stat != MonsterStatus.速度 and stat != MonsterStatus.忍者伏击 and stat != MonsterStatus.中毒 and stat != MonsterStatus.物攻:
                return
        if (self.stats.isFriendly() or self.isFake()) and (stat == MonsterStatus.眩晕 or stat == MonsterStatus.速度 or stat == MonsterStatus.中毒):
            return
        oldEffect = self.stati.get(stat)
        if oldEffect is not None:
            self.stati.remove(stat)
            if oldEffect.getStati() is None:
                oldEffect.cancelTask()
                oldEffect.cancelPoisonSchedule()
        final Timer.MobTimer timerManager = Timer.MobTimer.getInstance()
        cancelTask = _task_1
        if poison and self.getHp() > 1:
            poisonDamage = min(32767, (long)(self.getMobMaxHp() / (70.0 - from.getSkillLevel(status.getSkill())) + 0.999))
            status.setValue(MonsterStatus.中毒, poisonDamage)
            status.setPoisonSchedule(timerManager.register(PoisonTask(poisonDamage, from, status, cancelTask, False), 1000, 1000))
            if from.isGM():
                from.dropMessage(6, "正在给予 怪物: " + self.getId() + " BUFF状态: " + status.getStati().name() + " 是否中毒: " + poison + " BUFF持续时间: " + duration)
            if duration >= 60000:
                duration = 10000
        elif venom:
            poisonLevel = 0
            matk = 0
            # switch (from.getJob()):
                # case 412:
                    poisonLevel = from.getSkillLevel(SkillFactory.getSkill(4120005))
                    if poisonLevel <= 0:
                        return
                    matk = SkillFactory.getSkill(4120005).getEffect(poisonLevel).getMatk()
                    break
                # case 422:
                    poisonLevel = from.getSkillLevel(SkillFactory.getSkill(4220005))
                    if poisonLevel <= 0:
                        return
                    matk = SkillFactory.getSkill(4220005).getEffect(poisonLevel).getMatk()
                    break
                # case 1411:
                # case 1412:
                    poisonLevel = from.getSkillLevel(SkillFactory.getSkill(14110004))
                    if poisonLevel <= 0:
                        return
                    matk = SkillFactory.getSkill(14110004).getEffect(poisonLevel).getMatk()
                    break
                # case 434:
                    poisonLevel = from.getSkillLevel(SkillFactory.getSkill(4340001))
                    if poisonLevel <= 0:
                        return
                    matk = SkillFactory.getSkill(4340001).getEffect(poisonLevel).getMatk()
                    break
                # default:
                    return
            luk = from.getStat().getLuk()
            maxDmg = math.ceil(min(32767.0, 0.2 * luk * matk))
            minDmg = math.ceil(min(32767.0, 0.1 * luk * matk))
            gap = maxDmg - minDmg
            if gap == 0:
                gap = 1
            poisonDamage2 = 0
            for i in range(self.getVenomMulti()):
                poisonDamage2 += Randomizer.nextInt(gap) + minDmg
            poisonDamage2 = min(32767, poisonDamage2)
            status.setValue(MonsterStatus.中毒, poisonDamage2)
            status.setPoisonSchedule(timerManager.register(PoisonTask(poisonDamage2, from, status, cancelTask, False), 1000, 1000))
        elif statusSkill == 4111003 or statusSkill == 14111001:
            status.setPoisonSchedule(timerManager.schedule(PoisonTask((int)(self.getMobMaxHp() / 50.0 + 0.999), from, status, cancelTask, True), 3500))
        elif statusSkill == 4121004 or statusSkill == 4221004:
            damage = (from.getStat().getStr() + from.getStat().getLuk()) * 2 * 0 + 100
            status.setPoisonSchedule(timerManager.register(PoisonTask(damage, from, status, cancelTask, False), 1000, 1000))
            if damage > 0:
                if damage >= self.hp:
                    damage = (int)(self.hp - 1)
                self.damage(from, damage, False)
        self.stati.put(stat, status)
        self.map.broadcastMessage(MobPacket.applyMonsterStatus(self.getObjectId(), status), self.getPosition())
        if self.getController() is not None and not self.getController().isMapObjectVisible(this):
            self.getController().getClient().getSession().write(MobPacket.applyMonsterStatus(self.getObjectId(), status))
        aniTime = 0
        if skilz is not None:
            aniTime = skilz.getAnimationTime()
        final ScheduledFuture<?> schedule = timerManager.schedule(cancelTask, duration + aniTime)
        status.setCancelTask(schedule)

    def dispelSkill(self, skillId: Any) -> None:
        toCancel = []
        for (final Map.Entry<MonsterStatus, MonsterStatusEffect> effects : self.stati.items())
            if effects.getValue().getMobSkill() is not None and effects.getValue().getMobSkill().getSkillId() == skillId.getSkillId():
                toCancel.add(effects.getKey())
        for stat in toCancel:
            self.cancelStatus(stat)

    def applyMonsterBuff(self, effect: dict, skillId: int, duration: int, skill: Any, reflection: list) -> None:
        def _task_1():
            if reflection > 0:
                MapleMonster.self.reflectpack = None
            if MapleMonster.self.isAlive():
                for z in effect.keys():
                    MapleMonster.self.cancelStatus(z)

        final Timer.MobTimer timerManager = Timer.MobTimer.getInstance()
        cancelTask = _task_1
        for (final Map.Entry<MonsterStatus, Integer> z : effect.items())
            effectz = MonsterStatusEffect(z.getKey(), z.getValue(), 0, skill, True)
            self.stati.put(z.getKey(), effectz)
        if reflection > 0:
            self.reflectpack = MobPacket.applyMonsterStatus(self.getObjectId(), effect, reflection, skill)
            self.map.broadcastMessage(self.reflectpack, self.getPosition())
            if self.getController() is not None and not self.getController().isMapObjectVisible(this):
                self.getController().getClient().getSession().write(self.reflectpack)
        else:
            for (final Map.Entry<MonsterStatus, Integer> z : effect.items())
                self.map.broadcastMessage(MobPacket.applyMonsterStatus(self.getObjectId(), z.getKey(), z.getValue(), skill), self.getPosition())
                if self.getController() is not None and not self.getController().isMapObjectVisible(this):
                    self.getController().getClient().getSession().write(MobPacket.applyMonsterStatus(self.getObjectId(), z.getKey(), z.getValue(), skill))
        timerManager.schedule(cancelTask, duration)

    def setTempEffectiveness(self, e: Any, milli: int) -> None:
        def _task_1():
            MapleMonster.self.stats.removeEffectiveness(e)

        self.stats.setEffectiveness(e, ElementalEffectiveness.虚弱)
        Timer.MobTimer.getInstance().schedule(_task_1, milli)

    def isBuffed(self, status: Any) -> bool:
        return (status in self.stati)

    def getBuff(self, status: Any) -> Any:
        return self.stati.get(status)

    def setFake(self, fake: bool) -> None:
        self.fake = fake

    def isFake(self) -> bool:
        return self.fake

    def getMap(self) -> Any:
        return self.map

    def getSkills(self) -> list:
        return self.stats.getSkills()

    def hasSkill(self, skillId: int, level: int) -> bool:
        return self.stats.hasSkill(skillId, level)

    def getLastSkillUsed(self, skillId: int) -> int:
        if (skillId in self.usedSkills):
            return self.usedSkills.get(skillId)
        return 0

    def setLastSkillUsed(self, skillId: int, now: int, cooltime: int) -> None:
        # switch (skillId):
            # case 140:
                self.usedSkills.put(skillId, now + cooltime * 2)
                self.usedSkills.put(141, now)
                break
            # case 141:
                self.usedSkills.put(skillId, now + cooltime * 2)
                self.usedSkills.put(140, now + cooltime)
                break
            # default:
                self.usedSkills.put(skillId, now + cooltime)
                break

    def getNoSkills(self) -> int:
        return self.stats.getNoSkills()

    def isFirstAttack(self) -> bool:
        return self.stats.isFirstAttack()

    def getBuffToGive(self) -> int:
        return self.stats.getBuffToGive()

    def getExp(self) -> int:
        if self.overrideStats is not None:
            return self.overrideStats.getExp()
        return self.stats.getExp()

    def getLinkOid(self) -> int:
        return self.linkoid

    def setLinkOid(self, lo: int) -> None:
        self.linkoid = lo

    def getStati(self) -> dict:
        return self.stati

    def addEmpty(self) -> None:
        self.stati.put(MonsterStatus.空白BUFF, MonsterStatusEffect(MonsterStatus.空白BUFF, 0, 0, None, False))
        self.stati.put(MonsterStatus.召唤怪物, MonsterStatusEffect(MonsterStatus.召唤怪物, 0, 0, None, False))

    def getStolen(self) -> int:
        return self.stolen

    def setStolen(self, s: int) -> None:
        self.stolen = s

    def handleSteal(self, chr: Any) -> None:
        showdown = 100.0
        mse = self.getBuff(MonsterStatus.挑衅)
        if mse is not None:
            showdown += mse.getX()
        steal = SkillFactory.getSkill(4201004)
        level = chr.getSkillLevel(steal)
        chServerrate = ChannelServer.getInstance(chr.getClient().getChannel()).getDropRate()
        if level > 0 and not self.getStats().isBoss() and self.stolen == -1 and steal.getEffect(level).makeChanceResult():
            mi = MapleMonsterInformationProvider.getInstance()
            de = mi.retrieveDrop(self.getId())
            if de is None:
                self.stolen = 0
                return
            dropEntry = []
            Collections.shuffle(dropEntry)
            for d in dropEntry:
                if d.itemId > 0 and d.questid == 0 and d.itemId / 10000 != 238 and Randomizer.nextInt(999999) < (int)(10 * d.chance * chServerrate * chr.getDropMod() * (chr.getStat().dropBuff / 100.0) * (showdown / 100.0)):
                    idrop = None
                    if GameConstants.getInventoryType(d.itemId) == MapleInventoryType.EQUIP:
                        eq = MapleItemInformationProvider.getInstance().getEquipById(d.itemId)
                        idrop = MapleItemInformationProvider.getInstance().randomizeStats(eq)
                    else:
                        idrop = Item(d.itemId, 0, (short)((d.Maximum != 1) ? (Randomizer.nextInt(d.Maximum - d.Minimum) + d.Minimum) : 1), 0)
                    self.stolen = d.itemId
                    self.map.spawnMobDrop(idrop, self.map.calcDropPos(self.getPosition(), self.getTruePosition()), this, chr, 0, 0)
                    break
        else:
            self.stolen = 0

    def setLastNode(self, lastNode: int) -> None:
        self.lastNode = lastNode

    def getLastNode(self) -> int:
        return self.lastNode

    def setLastNodeController(self, lastNode: int) -> None:
        self.lastNodeController = lastNode

    def getLastNodeController(self) -> int:
        return self.lastNodeController

    def cancelStatus(self, stat: Any) -> None:
        if stat == MonsterStatus.空白BUFF or stat == MonsterStatus.召唤怪物:
            return
        mse = self.stati.get(stat)
        if mse is None or not self.isAlive():
            return
        if mse.isReflect():
            self.reflectpack = None
        mse.cancelPoisonSchedule()
        con = self.getController()
        if con is not None:
            self.map.broadcastMessage(con, MobPacket.cancelMonsterStatus(self.getObjectId(), stat), self.getTruePosition())
            con.getClient().getSession().write(MobPacket.cancelMonsterStatus(self.getObjectId(), stat))
        else:
            self.map.broadcastMessage(MobPacket.cancelMonsterStatus(self.getObjectId(), stat), self.getTruePosition())
        self.stati.remove(stat)

    def cancelDropItem(self) -> None:
        if self.dropItemSchedule is not None:
            self.dropItemSchedule.cancel(False)
            self.dropItemSchedule = None

    def startDropItemSchedule(self) -> None:
        def _task_1():
            if MapleMonster.self.isAlive() and MapleMonster.self.map is not None:
            if MapleMonster.self.shouldDropItem:
                MapleMonster.self.map.spawnAutoDrop(itemId, MapleMonster.self.getPosition())
            else:
                MapleMonster.self.shouldDropItem = True

        itemId = None
        cancelDropItem()
        if self.stats.getDropItemPeriod() <= 0 or not isAlive():
        return
        # switch (getId()):
            # case 9300061:
            itemId = 4001101
            break
            # case 9300102:
            itemId = 4031507
            break
            # default:
            return
        self.shouldDropItem = False
        self.dropItemSchedule = Timer.MobTimer.getInstance().register(_task_1,(self.stats.getDropItemPeriod() * 1000))

    def getNodePacket(self) -> Any:
        return self.nodepack

    def setNodePacket(self, np: Any) -> None:
        self.nodepack = np

    def killed(self) -> None:
        if self.listener is not None:
            self.listener.monsterKilled()
        self.listener = None

    def changeLevel(self, newLevel: int, pqMob: bool) -> None:
        self.ostats = ChangeableStats(self.stats, newLevel, pqMob)
        self.hp = self.ostats.getHp()
        self.mp = self.ostats.getMp()

    def getRange(self) -> float:
        return GameConstants.maxViewRangeSq()

    def getLastAttackTime(self) -> int:
        return self.lastAttackTime

    def setLastAttackTime(self, lastAttackTime: int) -> None:
        self.lastAttackTime = lastAttackTime

    def getAttacker(self) -> Any:
        return self.attacker

    def addDamage(self, from: Any, damage: int, updateAttackTime: bool) -> None:
        if self.chrid == from.getId():
            self.damage += damage
            if updateAttackTime:
                self.lastAttackTime = int(time.time() * 1000)

    def getAttackers(self) -> list:
        chr = MapleMonster.self.map.getCharacterById(self.chrid)
        if chr is not None:
            return Collections.singletonList(AttackingMapleCharacter(chr, self.lastAttackTime))
        return Collections.emptyList()

    def contains(self, chr: Any) -> bool:
        return self.chrid == chr.getId()

    def getDamage(self) -> int:
        return self.damage

    def killedMob(self, map: Any, baseExp: int, mostDamage: bool, lastSkill: int) -> None:
        chr = map.getCharacterById(self.chrid)
        if chr is not None and chr.isAlive():
            MapleMonster.self.giveExpToCharacter(chr, baseExp, mostDamage, 1, 0, 0, 0, lastSkill)

    def hashCode(self) -> int:
        return self.chrid

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.chrid == other.chrid

    def resolveAttackers(self) -> dict:
        ret = {})
        for (final Map.Entry<Integer, OnePartyAttacker> aentry : self.attackers.items())
            chr = MapleMonster.self.map.getCharacterById(aentry.getKey())
            if chr is not None:
                ret.put(chr, aentry.getValue())
        return ret

    def contains_chr(self, chr: Any) -> bool:
        return (chr.getId( in self.attackers))

    def addDamage_from_damage_updateAttackTime(self, from: Any, damage: int, updateAttackTime: bool) -> None:
        oldPartyAttacker = self.attackers.get(from.getId())
        if oldPartyAttacker is not None:
            onePartyAttacker2 = oldPartyAttacker
            onePartyAttacker2.damage += damage
            oldPartyAttacker.lastKnownParty = from.getParty()
            if updateAttackTime:
                oldPartyAttacker.lastAttackTime = int(time.time() * 1000)
        else:
            onePartyAttacker = OnePartyAttacker(from.getParty(), damage)
            self.attackers.put(from.getId(), onePartyAttacker)
            if not updateAttackTime:
                onePartyAttacker.lastAttackTime = 0
        self.totDamage += damage

    def killedMob_map_baseExp_mostDamage_lastSkill(self, map: Any, baseExp: int, mostDamage: bool, lastSkill: int) -> None:
        highest = None
        highestDamage = 0
        iexp = 0
        expMap = {}
        added_组队经验值 = 0
        for (final Map.Entry<MapleCharacter, OnePartyAttacker> attacker : self.resolveAttackers().items())
            party = attacker.getValue().lastKnownParty
            averagePartyLevel = 0.0
            Class_Bonus_EXP = 0
            网吧特别经验 = 0
            expApplicable = []
            for partychar in party.getMembers():
                if attacker.getKey().getLevel() - partychar.getLevel() <= 5 or MapleMonster.self.stats.getLevel() - partychar.getLevel() <= 5:
                    pchr = map.getCharacterById(partychar.getId())
                    if pchr is None or not pchr.isAlive() or pchr.getMap() != map:
                        continue
                    expApplicable.add(pchr)
                    averagePartyLevel += pchr.getLevel()
                    if Class_Bonus_EXP == 0:
                        Class_Bonus_EXP = ServerConstants.Class_Bonus_EXP(pchr.getJob())
                    if pchr.getStat().equippedWelcomeBackRing and 网吧特别经验 == 0:
                        网吧特别经验 = 80
                    if not pchr.getStat().hasPartyBonus or added_组队经验值 >= 4:
                        continue
                    added_组队经验值 += 1
            iDamage = attacker.getValue().damage
            if iDamage > highestDamage:
                highest = attacker.getKey()
                highestDamage = iDamage
            innerBaseExp = baseExp * (iDamage / self.totDamage)
            expBonus = 1.0
            if expApplicable > 1:
                expBonus = 1.1 + 0.05 * expApplicable
                averagePartyLevel /= expApplicable
            expFraction = innerBaseExp * expBonus / (expApplicable + 1)
            for expReceiver in expApplicable:
                oexp = (expMap.get(expReceiver) is None) ? 0 : expMap.get(expReceiver).exp
                if oexp is None:
                    iexp = 0
                else:
                    iexp = oexp
                expWeight = (expReceiver == attacker.getKey()) ? 2.0 : 1.0
                levelMod = expReceiver.getLevel() / averagePartyLevel
                if levelMod > 1.0 or (expReceiver.getId( in self.attackers)):
                    levelMod = 1.0
                iexp += Math.round(expFraction * expWeight * levelMod)
                expMap.put(expReceiver, ExpMap(iexp, (byte)(expApplicable + added_组队经验值), Class_Bonus_EXP, 网吧特别经验))
        for (final Map.Entry<MapleCharacter, ExpMap> expReceiver2 : expMap.items())
            expmap = expReceiver2.getValue()
            MapleMonster.self.giveExpToCharacter(expReceiver2.getKey(), expmap.exp, mostDamage and expReceiver2.getKey() == highest, expMap, expmap.ptysize, expmap.Class_Bonus_EXP, expmap.网吧特别经验, lastSkill)

    def equals_obj(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.partyid == other.partyid


# Inner class from Java (originally nested)
class AttackingMapleCharacter:
    """
    Class AttackingMapleCharacter
    """

    def __init__(self, attacker: Any, lastAttackTime: int):
        self.attacker = None
        self.lastAttackTime = 0
        self.attacker = attacker
        self.lastAttackTime = lastAttackTime


    def getLastAttackTime(self) -> int:
        return self.lastAttackTime

    def setLastAttackTime(self, lastAttackTime: int) -> None:
        self.lastAttackTime = lastAttackTime

    def getAttacker(self) -> Any:
        return self.attacker


# Inner class from Java (originally nested)
class ExpMap:
    """
    Class ExpMap
    """

    def __init__(self, exp: int, ptysize: int, Class_Bonus_EXP: int, 网吧特别经验: int):
        self.exp = 0
        self.ptysize = 0
        self.Class_Bonus_EXP = 0
        self.网吧特别经验 = 0
        self.exp = exp
        self.ptysize = ptysize
        self.Class_Bonus_EXP = Class_Bonus_EXP
        self.网吧特别经验 = 网吧特别经验



# Inner class from Java (originally nested)
class OnePartyAttacker:
    """
    Class OnePartyAttacker
    """

    def __init__(self, lastKnownParty: Any, damage: int):
        self.lastKnownParty = None
        self.damage = 0
        self.lastAttackTime = 0
        self.lastKnownParty = lastKnownParty
        self.damage = damage
        self.lastAttackTime = int(time.time() * 1000)



# Inner class from Java (originally nested)
class PoisonTask(Runnable):
    """
    Class PoisonTask
    Implements: Runnable
    """

    def __init__(self, poisonDamage: int, chr: Any, status: Any, cancelTask: Any, shadowWeb: bool):
        self.poisonDamage = None
        self.chr = None
        self.status = None
        self.cancelTask = None
        self.shadowWeb = None
        self.map = None
        self.poisonDamage = poisonDamage
        self.chr = chr
        self.status = status
        self.cancelTask = cancelTask
        self.shadowWeb = shadowWeb
        self.map = chr.getMap()


    def run(self) -> None:
        damage = self.poisonDamage
        if damage >= MapleMonster.self.hp:
            damage = MapleMonster.self.hp - 1
            if not self.shadowWeb:
                self.cancelTask.run()
                self.status.cancelTask()
        if MapleMonster.self.hp > 1 and damage > 0:
            MapleMonster.self.damage(self.chr, damage, False)
            if self.shadowWeb:
                self.map.broadcastMessage(MobPacket.damageMonster(MapleMonster.self.getObjectId(), damage), MapleMonster.self.getPosition())


# Inner class from Java (originally nested)
class SingleAttackerEntry(AttackerEntry):
    """
    Class SingleAttackerEntry
    Implements: AttackerEntry
    """

    def __init__(self, from: Any, cserv: int):
        self.damage = 0
        self.chrid = None
        self.lastAttackTime = 0
        self.channel = None
        self.damage = 0
        self.chrid = from.getId()
        self.channel = cserv


    def addDamage(self, from: Any, damage: int, updateAttackTime: bool) -> None:
        if self.chrid == from.getId():
            self.damage += damage
            if updateAttackTime:
                self.lastAttackTime = int(time.time() * 1000)

    def getAttackers(self) -> list:
        chr = MapleMonster.self.map.getCharacterById(self.chrid)
        if chr is not None:
            return Collections.singletonList(AttackingMapleCharacter(chr, self.lastAttackTime))
        return Collections.emptyList()

    def contains(self, chr: Any) -> bool:
        return self.chrid == chr.getId()

    def getDamage(self) -> int:
        return self.damage

    def killedMob(self, map: Any, baseExp: int, mostDamage: bool, lastSkill: int) -> None:
        chr = map.getCharacterById(self.chrid)
        if chr is not None and chr.isAlive():
            MapleMonster.self.giveExpToCharacter(chr, baseExp, mostDamage, 1, 0, 0, 0, lastSkill)

    def hashCode(self) -> int:
        return self.chrid

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.chrid == other.chrid


# Inner class from Java (originally nested)
class PartyAttackerEntry(AttackerEntry):
    """
    Class PartyAttackerEntry
    Implements: AttackerEntry
    """

    def __init__(self, partyid: int, cserv: int):
        self.totDamage = 0
        self.attackers = None
        self.partyid = None
        self.channel = None
        self.attackers = {}
        self.partyid = partyid
        self.channel = cserv


    def getAttackers(self) -> list:
        ret = [])
        for (final Map.Entry<Integer, OnePartyAttacker> entry : self.attackers.items())
            chr = MapleMonster.self.map.getCharacterById(entry.getKey())
            if chr is not None:
                ret.add(AttackingMapleCharacter(chr, entry.getValue().lastAttackTime))
        return ret

    def resolveAttackers(self) -> dict:
        ret = {})
        for (final Map.Entry<Integer, OnePartyAttacker> aentry : self.attackers.items())
            chr = MapleMonster.self.map.getCharacterById(aentry.getKey())
            if chr is not None:
                ret.put(chr, aentry.getValue())
        return ret

    def contains(self, chr: Any) -> bool:
        return (chr.getId( in self.attackers))

    def getDamage(self) -> int:
        return self.totDamage

    def addDamage(self, from: Any, damage: int, updateAttackTime: bool) -> None:
        oldPartyAttacker = self.attackers.get(from.getId())
        if oldPartyAttacker is not None:
            onePartyAttacker2 = oldPartyAttacker
            onePartyAttacker2.damage += damage
            oldPartyAttacker.lastKnownParty = from.getParty()
            if updateAttackTime:
                oldPartyAttacker.lastAttackTime = int(time.time() * 1000)
        else:
            onePartyAttacker = OnePartyAttacker(from.getParty(), damage)
            self.attackers.put(from.getId(), onePartyAttacker)
            if not updateAttackTime:
                onePartyAttacker.lastAttackTime = 0
        self.totDamage += damage

    def killedMob(self, map: Any, baseExp: int, mostDamage: bool, lastSkill: int) -> None:
        highest = None
        highestDamage = 0
        iexp = 0
        expMap = {}
        added_组队经验值 = 0
        for (final Map.Entry<MapleCharacter, OnePartyAttacker> attacker : self.resolveAttackers().items())
            party = attacker.getValue().lastKnownParty
            averagePartyLevel = 0.0
            Class_Bonus_EXP = 0
            网吧特别经验 = 0
            expApplicable = []
            for partychar in party.getMembers():
                if attacker.getKey().getLevel() - partychar.getLevel() <= 5 or MapleMonster.self.stats.getLevel() - partychar.getLevel() <= 5:
                    pchr = map.getCharacterById(partychar.getId())
                    if pchr is None or not pchr.isAlive() or pchr.getMap() != map:
                        continue
                    expApplicable.add(pchr)
                    averagePartyLevel += pchr.getLevel()
                    if Class_Bonus_EXP == 0:
                        Class_Bonus_EXP = ServerConstants.Class_Bonus_EXP(pchr.getJob())
                    if pchr.getStat().equippedWelcomeBackRing and 网吧特别经验 == 0:
                        网吧特别经验 = 80
                    if not pchr.getStat().hasPartyBonus or added_组队经验值 >= 4:
                        continue
                    added_组队经验值 += 1
            iDamage = attacker.getValue().damage
            if iDamage > highestDamage:
                highest = attacker.getKey()
                highestDamage = iDamage
            innerBaseExp = baseExp * (iDamage / self.totDamage)
            expBonus = 1.0
            if expApplicable > 1:
                expBonus = 1.1 + 0.05 * expApplicable
                averagePartyLevel /= expApplicable
            expFraction = innerBaseExp * expBonus / (expApplicable + 1)
            for expReceiver in expApplicable:
                oexp = (expMap.get(expReceiver) is None) ? 0 : expMap.get(expReceiver).exp
                if oexp is None:
                    iexp = 0
                else:
                    iexp = oexp
                expWeight = (expReceiver == attacker.getKey()) ? 2.0 : 1.0
                levelMod = expReceiver.getLevel() / averagePartyLevel
                if levelMod > 1.0 or (expReceiver.getId( in self.attackers)):
                    levelMod = 1.0
                iexp += Math.round(expFraction * expWeight * levelMod)
                expMap.put(expReceiver, ExpMap(iexp, (byte)(expApplicable + added_组队经验值), Class_Bonus_EXP, 网吧特别经验))
        for (final Map.Entry<MapleCharacter, ExpMap> expReceiver2 : expMap.items())
            expmap = expReceiver2.getValue()
            MapleMonster.self.giveExpToCharacter(expReceiver2.getKey(), expmap.exp, mostDamage and expReceiver2.getKey() == highest, expMap, expmap.ptysize, expmap.Class_Bonus_EXP, expmap.网吧特别经验, lastSkill)

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + self.partyid
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        return self.partyid == other.partyid


# Inner class from Java (originally nested)
from abc import ABC, abstractmethod

class AttackerEntry(ABC):
    """Interface AttackerEntry"""

    @abstractmethod
    def getAttackers(self) -> list:
        pass

    @abstractmethod
    def addDamage(self, p0: Any, p1: int, p2: bool) -> None:
        pass

    @abstractmethod
    def getDamage(self) -> int:
        pass

    @abstractmethod
    def contains(self, p0: Any) -> bool:
        pass

    @abstractmethod
    def killedMob(self, p0: Any, p1: int, p2: bool, p3: int) -> None:
        pass

