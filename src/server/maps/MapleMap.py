"""
MapleMap - Converted from Java source
Original: server/maps/MapleMap.java
Package: server.maps
"""

from concurrent.futures import Future
from datetime import datetime
from datetime import datetime, timezone, timedelta
from enum import Enum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
from weakref import ref
import math
import os
import pymysql
import sched
import sys
import threading
import time
import weakref

# Internal module imports
# from client.MapleBuffStat import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.status.MonsterStatus import *  # TODO: import specific classes
# from client.status.MonsterStatusEffect import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from scripting.EventManager import *  # TODO: import specific classes
# from server.MapleCarnivalFactory import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.MapleSquad import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.SpeedRunner import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.events.MapleEvent import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MapleMonsterInformationProvider import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from server.life.MonsterDropEntry import *  # TODO: import specific classes
# from server.life.MonsterGlobalDropEntry import *  # TODO: import specific classes
# from server.life.OverrideMonsterStats import *  # TODO: import specific classes
# from server.life.SpawnPoint import *  # TODO: import specific classes
# from server.life.SpawnPointAreaBoss import *  # TODO: import specific classes
# from server.life.Spawns import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes
# from tools.packet.MobPacket import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes


class MapleMap:
    """
    Class MapleMap
    """

    def __init__(self, mapid: int, channel: int, returnMapId: int, monsterRate: float):
        self.mapobjects = None
        self.mapobjectlocks = None
        self.characters = None
        self.charactersLock = None
        self.runningOid = 0
        self.runningOidLock = None
        self.monsterSpawn = None
        self.spawnedMonstersOnMap = None
        self.portals = None
        self.footholds = None
        self.monsterRate = 0.0
        self.recoveryRate = 0.0
        self.mapEffect = None
        self.channel = None
        self.decHP = 0
        self.createMobInterval = 0
        self.consumeItemCoolTime = 0
        self.protectItem = 0
        self.decHPInterval = 0
        self.mapid = None
        self.returnMapId = 0
        self.timeLimit = 0
        self.fieldLimit = 0
        self.maxRegularSpawn = 0
        self.fixedMob = 0
        self.forcedReturnMap = 0
        self.lvForceMove = 0
        self.lvLimit = 0
        self.permanentWeather = 0
        self.town = False
        self.clock = False
        self.personalShop = False
        self.everlast = False
        self.dropsDisabled = False
        self.gDropsDisabled = False
        self.soaring = False
        self.squadTimer = False
        self.isSpawns = False
        self.mapName = ""
        self.streetName = ""
        self.characters = []
        self.charactersLock = ReentrantReadWriteLock()
        self.runningOid = 100000
        self.runningOidLock = ReentrantLock()
        self.monsterSpawn = []
        self.spawnedMonstersOnMap = AtomicInteger(0)
        self.portals = {}
        self.footholds = None
        self.decHP = 0
        self.createMobInterval = 9000
        self.consumeItemCoolTime = 0
        self.protectItem = 0
        self.decHPInterval = 10000
        self.maxRegularSpawn = 0
        self.forcedReturnMap = 999999999
        self.lvForceMove = 0
        self.lvLimit = 0
        self.permanentWeather = 0
        self.everlast = False
        self.dropsDisabled = False
        self.gDropsDisabled = False
        self.soaring = False
        self.squadTimer = False
        self.isSpawns = True
        self.speedRunLeader = ""
        self.dced = []
        self.speedRunStart = 0
        self.lastSpawnTime = 0
        self.lastHurtTime = 0
        self.environment = {}
        self.mapid = mapid
        self.channel = channel
        self.returnMapId = returnMapId
        if self.returnMapId == 999999999:
            self.returnMapId = mapid
        self.monsterRate = monsterRate
        objsMap = new EnumMap<MapleMapObjectType, LinkedHashMap<Integer, MapleMapObject>>(MapleMapObjectType.class)
        objlockmap = new EnumMap<MapleMapObjectType, ReentrantReadWriteLock>(MapleMapObjectType.class)
        for type in MapleMapObjectType.values():
            objsMap.put(type, {})
            objlockmap.put(type, ReentrantReadWriteLock())
        self.mapobjects = Collections.unmodifiableMap((Map<? extends MapleMapObjectType, ? extends LinkedHashMap<Integer, MapleMapObject>>)objsMap)
        self.mapobjectlocks = Collections.unmodifiableMap((Map<? extends MapleMapObjectType, ? extends ReentrantReadWriteLock>)objlockmap)


    def setSpawns(self, fm: bool) -> None:
        self.isSpawns = fm

    def getSpawns(self) -> bool:
        return self.isSpawns

    def setFixedMob(self, fm: int) -> None:
        self.fixedMob = fm

    def setForceMove(self, fm: int) -> None:
        self.lvForceMove = fm

    def getForceMove(self) -> int:
        return self.lvForceMove

    def setLevelLimit(self, fm: int) -> None:
        self.lvLimit = fm

    def getLevelLimit(self) -> int:
        return self.lvLimit

    def setReturnMapId(self, rmi: int) -> None:
        self.returnMapId = rmi

    def setSoaring(self, b: bool) -> None:
        self.soaring = b

    def canSoar(self) -> bool:
        return self.soaring

    def toggleDrops(self) -> None:
        self.dropsDisabled = not self.dropsDisabled

    def setDrops(self, b: bool) -> None:
        self.dropsDisabled = b

    def toggleGDrops(self) -> None:
        self.gDropsDisabled = not self.gDropsDisabled

    def getId(self) -> int:
        return self.mapid

    def getReturnMap(self) -> Any:
        return ChannelServer.getInstance(self.channel).getMapFactory().getMap(self.returnMapId)

    def getReturnMapId(self) -> int:
        return self.returnMapId

    def getForcedReturnId(self) -> int:
        return self.forcedReturnMap

    def getForcedReturnMap(self) -> Any:
        return ChannelServer.getInstance(self.channel).getMapFactory().getMap(self.forcedReturnMap)

    def setForcedReturnMap(self, map: int) -> None:
        self.forcedReturnMap = map

    def getRecoveryRate(self) -> float:
        return self.recoveryRate

    def setRecoveryRate(self, recoveryRate: float) -> None:
        self.recoveryRate = recoveryRate

    def getFieldLimit(self) -> int:
        return self.fieldLimit

    def setFieldLimit(self, fieldLimit: int) -> None:
        self.fieldLimit = fieldLimit

    def setCreateMobInterval(self, createMobInterval: int) -> None:
        self.createMobInterval = createMobInterval

    def setTimeLimit(self, timeLimit: int) -> None:
        self.timeLimit = timeLimit

    def setMapName(self, mapName: str) -> None:
        self.mapName = mapName

    def getMapName(self) -> str:
        return self.mapName

    def getStreetName(self) -> str:
        return self.streetName

    def setFirstUserEnter(self, onFirstUserEnter: str) -> None:
        self.onFirstUserEnter = onFirstUserEnter

    def setUserEnter(self, onUserEnter: str) -> None:
        self.onUserEnter = onUserEnter

    def setOnUserEnter(self, onUserEnter: str) -> None:
        self.onUserEnter = onUserEnter

    def hasClock(self) -> bool:
        return self.clock

    def setClock(self, hasClock: bool) -> None:
        self.clock = hasClock

    def isTown(self) -> bool:
        return self.town

    def setTown(self, town: bool) -> None:
        self.town = town

    def allowPersonalShop(self) -> bool:
        return self.personalShop

    def setPersonalShop(self, personalShop: bool) -> None:
        self.personalShop = personalShop

    def setStreetName(self, streetName: str) -> None:
        self.streetName = streetName

    def setEverlast(self, everlast: bool) -> None:
        self.everlast = everlast

    def getEverlast(self) -> bool:
        return self.everlast

    def getHPDec(self) -> int:
        return self.decHP

    def setHPDec(self, delta: int) -> None:
        if delta > 0 or self.mapid == 749040100:
            self.lastHurtTime = int(time.time() * 1000)
        self.decHP = delta

    def getHPDecInterval(self) -> int:
        return self.decHPInterval

    def setHPDecInterval(self, delta: int) -> None:
        self.decHPInterval = delta

    def getHPDecProtect(self) -> int:
        return self.protectItem

    def setHPDecProtect(self, delta: int) -> None:
        self.protectItem = delta

    def getCurrentPartyId(self) -> int:
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if chr.getPartyId() != -1:
                    return chr.getPartyId()
        finally:
            self.charactersLock.readLock().unlock()
        return -1

    def addMapObject(self, mapobject: Any) -> None:
        self.runningOidLock.lock()
        newOid = None
        try:
            newOid = ++self.runningOid
        finally:
            self.runningOidLock.unlock()
        mapobject.setObjectId(newOid)
        self.mapobjectlocks.get(mapobject.getType()).writeLock().lock()
        try:
            self.mapobjects.get(mapobject.getType()).put(newOid, mapobject)
        finally:
            self.mapobjectlocks.get(mapobject.getType()).writeLock().unlock()

    def spawnAndAddRangedMapObject(self, mapobject: Any, packetbakery: Any, condition: Any) -> None:
        self.addMapObject(mapobject)
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if (condition is None or condition.canSpawn(chr)) and not chr.isClone() and chr.getPosition().distanceSq(mapobject.getPosition()) <= GameConstants.maxViewRangeSq():
                    packetbakery.sendPackets(chr.getClient())
                    chr.addVisibleMapObject(mapobject)
        finally:
            self.charactersLock.readLock().unlock()

    def removeMapObject(self, obj: Any) -> None:
        self.mapobjectlocks.get(obj.getType()).writeLock().lock()
        try:
            self.mapobjects.get(obj.getType()).remove(obj.getObjectId())
        finally:
            self.mapobjectlocks.get(obj.getType()).writeLock().unlock()

    def calcPointBelow(self, initial: Any) -> Any:
        fh = self.footholds.findBelow(initial)
        if fh is None:
            return None
        dropY = fh.getY1()
        if not fh.isWall() and fh.getY1() != fh.getY2():
            s1 = abs(fh.getY2() - fh.getY1())
            s2 = abs(fh.getX2() - fh.getX1())
            if fh.getY2() < fh.getY1():
                dropY = fh.getY1() - (int)(Math.cos(Math.atan(s2 / s1)) * (abs(initial.x - fh.getX1()) / Math.cos(Math.atan(s1 / s2))))
            else:
                dropY = fh.getY1() + (int)(Math.cos(Math.atan(s2 / s1)) * (abs(initial.x - fh.getX1()) / Math.cos(Math.atan(s1 / s2))))
        return Point(initial.x, dropY)

    def calcDropPos(self, initial: Any, fallback: Any) -> Any:
        ret = self.calcPointBelow(Point(initial.x, initial.y - 50))
        if ret is None:
            return fallback
        return ret

    def dropFromMonster(self, chr: Any, mob: Any) -> None:
        self.dropFromMonster(chr, mob, False)

    def dropFromMonster_chr_mob_instanced(self, chr: Any, mob: Any, instanced: bool) -> None:
        if mob is None or chr is None or ChannelServer.getInstance(self.channel) is None or self.dropsDisabled or mob.dropsDisabled() or chr.getPyramidSubway() is not None:
            return
        maxSize = 200
        if not instanced and maxSize >= 300 and self.mapobjects.get(MapleMapObjectType.ITEM) >= maxSize:
            self.removeDropsDelay()
            if chr.isGM():
                chr.dropMessage(6, "[系统提示] 当前地图的道具数量达到 " + maxSize + " 系统已自动清理掉所有地上的物品信息.")
        ii = MapleItemInformationProvider.getInstance()
        droptype = (byte)(mob.getStats().isExplosiveReward() ? 3 : (mob.getStats().isFfaLoot() ? 2 : ((chr.getParty() is not None) ? 1 : 0)))
        mobpos = mob.getPosition().x
        cmServerrate = ChannelServer.getInstance(self.channel).getMesoRate()
        chServerrate = ChannelServer.getInstance(self.channel).getDropRate()
        caServerrate = ChannelServer.getInstance(self.channel).getCashRate()
        d = 1
        pos = Point(0, mob.getPosition().y)
        showdown = 100.0
        mse = mob.getBuff(MonsterStatus.挑衅)
        if mse is not None:
            showdown += mse.getX()
        if mob.getStats().isBoss():
            chServerrate = ChannelServer.getInstance(self.channel).getBossDropRate()
        mi = MapleMonsterInformationProvider.getInstance()
        dropEntry = mi.retrieveDrop(mob.getId())
        Collections.shuffle(dropEntry)
        for de in dropEntry:
            if de.itemId == mob.getStolen():
                continue
            Rand = Randomizer.nextInt(999999)
            part1 = de.chance
            part2 = chServerrate
            part3 = chr.getDropMod()
            part4 = (int)(chr.getStat().dropBuff / 100.0)
            part5 = (int)(showdown / 100.0)
            last = part1 * part2 * part3 * part4 * part5
            if Rand >= last:
                continue
            if droptype == 3:
                pos.x = mobpos + ((d % 2 == 0) ? (40 * (d + 1) / 2) : (-(40 * (d / 2))))
            else:
                pos.x = mobpos + ((d % 2 == 0) ? (25 * (d + 1) / 2) : (-(25 * (d / 2))))
            if de.itemId != 0:
                idrop = None
                if GameConstants.getInventoryType(de.itemId) == MapleInventoryType.EQUIP:
                    idrop = ii.randomizeStats(ii.getEquipById(de.itemId))
                else:
                    range = abs(de.Maximum - de.Minimum)
                    idrop = Item(de.itemId, 0, (short)((de.Maximum != 1) ? (Randomizer.nextInt((range <= 0) ? 1 : range) + de.Minimum) : 1), 0)
                self.spawnMobDrop(idrop, self.calcDropPos(pos, mob.getPosition()), mob, chr, droptype, de.questid)
            d += 1
        mesoDecrease = math.pow(0.93, mob.getStats().getExp() / 350.0)
        if mesoDecrease > 1.0:
            mesoDecrease = 1.0
        tempmeso = min(30000, (int)(mesoDecrease * mob.getStats().getExp() * (1.0 + random.random() * 5.0) / 30.0))
        if tempmeso > 0:
            pos.x = min(max(mobpos - 25 * (d / 2), self.footholds.getMinDropX() + 25), self.footholds.getMaxDropX() - d * 25)
            self.spawnMobMesoDrop((int)(tempmeso * (chr.getStat().mesoBuff / 100.0) * chr.getDropMod() * cmServerrate), self.calcDropPos(pos, mob.getPosition()), mob, chr, False, droptype)
        globalEntry = [])
        Collections.shuffle(globalEntry)
        cashz = ((mob.getStats().isBoss() and mob.getStats().getHPDisplayType() == 0) ? 20 : 1) * caServerrate
        cashModifier = (int)(mob.getStats().isBoss() ? 0 : (mob.getMobExp() / 1000 + mob.getMobMaxHp() / 10000))
        for de2 in globalEntry:
            if Randomizer.nextInt(999999) < de2.chance and (de2.continent < 0 or (de2.continent < 10 and self.mapid / 100000000 == de2.continent) or (de2.continent < 100 and self.mapid / 10000000 == de2.continent) or (de2.continent < 1000 and self.mapid / 1000000 == de2.continent)):
                if droptype == 3:
                    pos.x = mobpos + ((d % 2 == 0) ? (40 * (d + 1) / 2) : (-(40 * (d / 2))))
                else:
                    pos.x = mobpos + ((d % 2 == 0) ? (25 * (d + 1) / 2) : (-(25 * (d / 2))))
                if de2.itemId == 0:
                    continue
                if self.gDropsDisabled:
                    continue
                idrop = None
                if GameConstants.getInventoryType(de2.itemId) == MapleInventoryType.EQUIP:
                    idrop = ii.randomizeStats(ii.getEquipById(de2.itemId))
                else:
                    idrop = Item(de2.itemId, 0, (short)((de2.Maximum != 1) ? (Randomizer.nextInt(de2.Maximum - de2.Minimum) + de2.Minimum) : 1), 0)
                self.spawnMobDrop(idrop, self.calcDropPos(pos, mob.getPosition()), mob, chr, (byte)(de2.onlySelf ? 0 : droptype), de2.questid)
                d += 1

    def dropFromMonster2(self, chr: Any, mob: Any) -> None:
        if mob is None or chr is None or ChannelServer.getInstance(self.channel) is None or self.dropsDisabled or mob.dropsDisabled() or chr.getPyramidSubway() is not None:
            return
        ii = MapleItemInformationProvider.getInstance()
        droptype = (byte)(mob.getStats().isExplosiveReward() ? 3 : (mob.getStats().isFfaLoot() ? 2 : ((chr.getParty() is not None) ? 1 : 0)))
        mobpos = mob.getPosition().x
        cmServerrate = ChannelServer.getInstance(self.channel).getMesoRate()
        chServerrate = ChannelServer.getInstance(self.channel).getDropRate()
        caServerrate = ChannelServer.getInstance(self.channel).getCashRate()
        d = 1
        pos = Point(0, mob.getPosition().y)
        showdown = 100.0
        mse = mob.getBuff(MonsterStatus.挑衅)
        if mse is not None:
            showdown += mse.getX()
        if mob.getStats().isBoss():
            chServerrate = ChannelServer.getInstance(self.channel).getBossDropRate()
        mi = MapleMonsterInformationProvider.getInstance()
        dropEntry = mi.retrieveDrop(mob.getId())
        Collections.shuffle(dropEntry)
        mesoDropped = False
        for de in dropEntry:
            if de.itemId == mob.getStolen():
                continue
            Rand = Randomizer.nextInt(999999)
            part1 = de.chance
            part2 = chServerrate
            part3 = chr.getDropMod()
            part4 = (int)(chr.getStat().dropBuff / 100.0)
            part5 = (int)(showdown / 100.0)
            last = part1 * part2 * part3 * part4 * part5
            if Rand >= last:
                continue
            if droptype == 3:
                pos.x = mobpos + ((d % 2 == 0) ? (40 * (d + 1) / 2) : (-(40 * (d / 2))))
            else:
                pos.x = mobpos + ((d % 2 == 0) ? (25 * (d + 1) / 2) : (-(25 * (d / 2))))
            if de.itemId == 0:
                mesos = Randomizer.nextInt(1 + abs(de.Maximum - de.Minimum)) + de.Minimum
                if mesos <= 0:
                    continue
                self.spawnMobMesoDrop((int)(mesos * (chr.getStat().mesoBuff / 100.0) * chr.getDropMod() * cmServerrate), self.calcDropPos(pos, mob.getPosition()), mob, chr, False, droptype)
                mesoDropped = True
                d += 1
            else:
                idrop = None
                if GameConstants.getInventoryType(de.itemId) == MapleInventoryType.EQUIP:
                    idrop = ii.randomizeStats(ii.getEquipById(de.itemId))
                else:
                    range = abs(de.Maximum - de.Minimum)
                    idrop = Item(de.itemId, 0, (short)((de.Maximum != 1) ? (Randomizer.nextInt((range <= 0) ? 1 : range) + de.Minimum) : 1), 0)
                if Randomizer.nextInt(100) <= 3 and not mob.getStats().isBoss() and chr.getEventInstance() is None:
                    idrop = Item(2370005, 0, 1, 0)
                self.spawnMobDrop(idrop, self.calcDropPos(pos, mob.getPosition()), mob, chr, droptype, de.questid)
                d += 1
        globalEntry = [])
        Collections.shuffle(globalEntry)
        for de2 in globalEntry:
            if de2.chance != 0:
                if de2.itemId == 0:
                    continue
                if Randomizer.nextInt(999999) >= de2.chance or (de2.continent >= 0 and (de2.continent >= 10 or self.mapid / 100000000 != de2.continent) and (de2.continent >= 100 or self.mapid / 10000000 != de2.continent) and (de2.continent >= 1000 or self.mapid / 1000000 != de2.continent)) or self.gDropsDisabled:
                    continue
                if droptype == 3:
                    pos.x = mobpos + ((d % 2 == 0) ? (40 * (d + 1) / 2) : (-(40 * (d / 2))))
                else:
                    pos.x = mobpos + ((d % 2 == 0) ? (25 * (d + 1) / 2) : (-(25 * (d / 2))))
                idrop = None
                if GameConstants.getInventoryType(de2.itemId) == MapleInventoryType.EQUIP:
                    idrop = ii.randomizeStats(ii.getEquipById(de2.itemId))
                else:
                    idrop = Item(de2.itemId, 0, (short)((de2.Maximum != 1) ? (Randomizer.nextInt(de2.Maximum - de2.Minimum) + de2.Minimum) : 1), 0)
                self.spawnMobDrop(idrop, self.calcDropPos(pos, mob.getPosition()), mob, chr, (byte)(de2.onlySelf ? 0 : droptype), de2.questid)
                d += 1

    def removeMonster(self, monster: Any) -> None:
        if monster is None:
            return
        self.spawnedMonstersOnMap.decrementAndGet()
        self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), 0))
        self.removeMapObject(monster)
        monster.killed()

    def killMonster(self, monster: Any) -> None:
        if monster is None:
            return
        self.spawnedMonstersOnMap.decrementAndGet()
        monster.setHp(0)
        monster.spawnRevives(this)
        self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), 1))
        self.removeMapObject(monster)
        monster.killed()

    def killMonster_monster_chr_withDrops_second_animation(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int) -> None:
        self.killMonster(monster, chr, withDrops, second, animation, 0)

    def killMonster_monster_chr_withDrops_second_animation_lastSkill(self, monster: Any, chr: Any, withDrops: bool, second: bool, animation: int, lastSkill: int) -> None:
        self.spawnedMonstersOnMap.decrementAndGet()
        self.removeMapObject(monster)
        monster.killed()
        dropOwner = monster.killBy(chr, lastSkill)
        if animation >= 0:
            self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), animation))
        if monster.getBuffToGive() > -1:
            buffid = monster.getBuffToGive()
            buff = MapleItemInformationProvider.getInstance().getItemEffect(buffid)
            self.charactersLock.readLock().lock()
            try:
                for mc in self.characters:
                    if mc.isAlive():
                        buff.applyTo(mc)
                        # switch (monster.getId()):
                            # case 8810018:
                            # case 8810122:
                            # case 8820001:
                                mc.getClient().getSession().write(MaplePacketCreator.showOwnBuffEffect(buffid, 11))
                                self.broadcastMessage(mc, MaplePacketCreator.showBuffeffect(mc.getId(), buffid, 11), False)
                                continue
            finally:
                self.charactersLock.readLock().unlock()
        mobid = monster.getId()
        type = SpeedRunType.NULL
        sqd = self.getSquadByMap()
        instanced = sqd is not None or monster.getEventInstance() is not None or self.getEMByMap() is not None
        if mobid == 8810018 and self.mapid == 240060200:
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "经过无数次的挑战，" + chr.getName() + "所带领的队伍终于击败了暗黑龙王的远征队！你们才是龙之林的真正英雄~").encode("utf-8"))
            if self.speedRunStart > 0:
                type = SpeedRunType.Horntail
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 8810122 and self.mapid == 240060201:
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, "经过无数次的挑战，" + chr.getName() + "所带领的队伍终于击败了混沌暗黑龙王的远征队！你们才是龙之林的真正英雄~").encode("utf-8"))
            if self.speedRunStart > 0:
                type = SpeedRunType.ChaosHT
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 8500002 and self.mapid == 220080001:
            if self.speedRunStart > 0:
                type = SpeedRunType.Papulatus
        elif mobid == 9400266 and self.mapid == 802000111:
            if self.speedRunStart > 0:
                type = SpeedRunType.Nameless_Magic_Monster
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400265 and self.mapid == 802000211:
            if self.speedRunStart > 0:
                type = SpeedRunType.Vergamot
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400270 and self.mapid == 802000411:
            if self.speedRunStart > 0:
                type = SpeedRunType.Dunas
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400273 and self.mapid == 802000611:
            if self.speedRunStart > 0:
                type = SpeedRunType.Nibergen
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400294 and self.mapid == 802000711:
            if self.speedRunStart > 0:
                type = SpeedRunType.Dunas_2
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400296 and self.mapid == 802000803:
            if self.speedRunStart > 0:
                type = SpeedRunType.Core_Blaze
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 9400289 and self.mapid == 802000821:
            if self.speedRunStart > 0:
                type = SpeedRunType.Aufhaven
            if sqd is not None:
                self.doShrine(True)
        elif (mobid == 9420549 or mobid == 9420544) and self.mapid == 551030200:
            if self.speedRunStart > 0:
                if mobid == 9420549:
                    type = SpeedRunType.Scarlion
                else:
                    type = SpeedRunType.Targa
        elif mobid == 8820001 and self.mapid == 270050100:
            World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(6, chr.getName() + "经过带领的队伍经过无数次的挑战，终于击败了时间的宠儿－品克缤的远征队！你们才是时间神殿的真正英雄~").encode("utf-8"))
            if self.speedRunStart > 0:
                type = SpeedRunType.Pink_Bean
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 8800002 and self.mapid == 280030000:
            if self.speedRunStart > 0:
                type = SpeedRunType.Zakum
            if sqd is not None:
                self.doShrine(True)
        elif mobid == 8800102 and self.mapid == 280030001:
            if self.speedRunStart > 0:
                type = SpeedRunType.Chaos_Zakum
            if sqd is not None:
                self.doShrine(True)
        elif mobid >= 8800003 and mobid <= 8800010:
            makeZakReal = True
            monsters = self.getAllMonstersThreadsafe()
            for mons in monsters:
                if mons.getId() >= 8800003 and mons.getId() <= 8800010:
                    makeZakReal = False
                    break
            if makeZakReal:
                for object in monsters:
                    mons2 = object
                    if mons2.getId() == 8800000:
                        pos = mons2.getPosition()
                        self.killAllMonsters(True)
                        self.spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(8800000), pos)
                        break
        elif mobid >= 8800103 and mobid <= 8800110:
            makeZakReal = True
            monsters = self.getAllMonstersThreadsafe()
            for mons in monsters:
                if mons.getId() >= 8800103 and mons.getId() <= 8800110:
                    makeZakReal = False
                    break
            if makeZakReal:
                for mons in monsters:
                    if mons.getId() == 8800100:
                        pos2 = mons.getPosition()
                        self.killAllMonsters(True)
                        self.spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(8800100), pos2)
                        break
        if type != SpeedRunType.NULL and self.speedRunStart > 0 and self.speedRunLeader > 0:
            endTime = int(time.time() * 1000)
            time = StringUtil.getReadableMillis(self.speedRunStart, endTime)
            self.broadcastMessage(MaplePacketCreator.serverNotice(5, self.speedRunLeader + "'远征队花了 " + time + " 时间打败了 " + type + "not "))
            self.getRankAndAdd(self.speedRunLeader, time, type, endTime - self.speedRunStart, (sqd is None) ? None : sqd.getMembers())
            self.endSpeedRun()
        if mobid == 8820008:
            for mmo in self.getAllMonstersThreadsafe():
                mons3 = mmo
                if mons3.getLinkOid() != monster.getObjectId():
                    self.killMonster(mons3, chr, False, False, animation)
        elif mobid >= 8820010 and mobid <= 8820014:
            for mmo in self.getAllMonstersThreadsafe():
                mons3 = mmo
                if mons3.getId() != 8820000 and mons3.getObjectId() != monster.getObjectId() and mons3.getLinkOid() != monster.getObjectId():
                    self.killMonster(mons3, chr, False, False, animation)
        if withDrops:
            drop = None
            if dropOwner <= 0:
                drop = chr
            else:
                drop = self.getCharacterById(dropOwner)
                if drop is None:
                    drop = chr
            self.dropFromMonster(drop, monster)
        chr.gainSG(1)

    def getAllReactor(self) -> list:
        return self.getAllReactorsThreadsafe()

    def getAllReactorsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()
        return ret

    def getAllDoor(self) -> list:
        return self.getAllDoorsThreadsafe()

    def getAllDoorsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.DOOR).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.DOOR).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.DOOR).readLock().unlock()
        return ret

    def getAllMerchant(self) -> list:
        return self.getAllHiredMerchantsThreadsafe()

    def getAllHiredMerchantsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.HIRED_MERCHANT).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.HIRED_MERCHANT).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.HIRED_MERCHANT).readLock().unlock()
        return ret

    def getAllMonster(self) -> list:
        return self.getAllMonstersThreadsafe()

    def getAllMonstersThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.MONSTER).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().unlock()
        return ret

    def killAllMonsters(self, animate: bool) -> None:
        for monstermo in self.getAllMonstersThreadsafe():
            monster = monstermo
            self.spawnedMonstersOnMap.decrementAndGet()
            monster.setHp(0)
            self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), (int)(animate ? 1 : 0)))
            self.removeMapObject(monster)
            monster.killed()

    def killMonster_monsId(self, monsId: int) -> None:
        for mmo in self.getAllMonstersThreadsafe():
            if (mmo).getId() == monsId:
                self.spawnedMonstersOnMap.decrementAndGet()
                self.removeMapObject(mmo)
                self.broadcastMessage(MobPacket.killMonster(mmo.getObjectId(), 1))
                break

    def MapDebug_Log(self) -> str:
        sb = ""
        sb.append(FileoutputUtil.CurrentReadable_Time())
        sb.append(" | Mapid : ").append(self.mapid)
        self.charactersLock.readLock().lock()
        try:
            sb.append(" Users [").append(self.characters).append("] | ")
            for mc in self.characters:
                sb.append(mc.getName()).append(", ")
        finally:
            self.charactersLock.readLock().unlock()
        return sb

    def limitReactor(self, rid: int, num: int) -> None:
        toDestroy = []
        contained = {}
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                mr = obj
                if (mr.getReactorId( in contained)):
                    if contained.get(mr.getReactorId()) >= num:
                        toDestroy.add(mr)
                    else:
                        contained.put(mr.getReactorId(), contained.get(mr.getReactorId()) + 1)
                else:
                    contained.put(mr.getReactorId(), 1)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()
        for mr2 in toDestroy:
            self.destroyReactor(mr2.getObjectId())

    def destroyReactors(self, first: int, last: int) -> None:
        toDestroy = []
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                mr = obj
                if mr.getReactorId() >= first and mr.getReactorId() <= last:
                    toDestroy.add(mr)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()
        for mr2 in toDestroy:
            self.destroyReactor(mr2.getObjectId())

    def destroyReactor(self, oid: int) -> None:
        def _task_1():
            MapleMap.self.respawnReactor(reactor)

        reactor = self.getReactorByOid(oid)
        self.broadcastMessage(MaplePacketCreator.destroyReactor(reactor))
        reactor.setAlive(False)
        self.removeMapObject(reactor)
        reactor.setTimerActive(False)
        if reactor.getDelay() > 0:
            Timer.MapTimer.getInstance().schedule(_task_1, reactor.getDelay())

    def run(self) -> None:
        MapleMap.self.respawnReactor(reactor)

    def reloadReactors(self) -> None:
        toSpawn = []
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                reactor = obj
                self.broadcastMessage(MaplePacketCreator.destroyReactor(reactor))
                reactor.setAlive(False)
                reactor.setTimerActive(False)
                toSpawn.add(reactor)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()
        for r in toSpawn:
            self.removeMapObject(r)
            if r.getReactorId() != 9980000 and r.getReactorId() != 9980001:
                self.respawnReactor(r)

    def resetReactors(self) -> None:
        self.setReactorState(0)

    def setReactorState(self) -> None:
        self.setReactorState(1)

    def setReactorState_state(self, state: int) -> None:
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                (obj).forceHitReactor(state)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()

    def shuffleReactors(self) -> None:
        self.shuffleReactors(0, 9999999)

    def shuffleReactors_first_last(self, first: int, last: int) -> None:
        points = []
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                mr = obj
                if mr.getReactorId() >= first and mr.getReactorId() <= last:
                    points.add(mr.getPosition())
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()
        Collections.shuffle(points)
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                mr = obj
                if mr.getReactorId() >= first and mr.getReactorId() <= last:
                    mr.setPosition(points.remove(points - 1))
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()

    def updateMonsterController(self, monster: Any) -> None:
        if not monster.isAlive():
            return
        if monster.getController() is not None:
            if monster.getController().getMap() == this:
                return
            monster.getController().stopControllingMonster(monster)
        mincontrolled = -1
        newController = None
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if not chr.isHidden() and not chr.isClone() and (chr.getControlledSize() < mincontrolled or mincontrolled == -1) and chr.getTruePosition().distanceSq(monster.getTruePosition()) <= monster.getRange():
                    mincontrolled = chr.getControlledSize()
                    newController = chr
        finally:
            self.charactersLock.readLock().unlock()
        if newController is not None:
            if monster.isFirstAttack():
                newController.controlMonster(monster, True)
                monster.setControllerHasAggro(True)
                monster.setControllerKnowsAboutAggro(True)
            else:
                newController.controlMonster(monster, False)

    def getMapObject(self, oid: int, type: Any) -> Any:
        self.mapobjectlocks.get(type).readLock().lock()
        try:
            return self.mapobjects.get(type).get(oid)
        finally:
            self.mapobjectlocks.get(type).readLock().unlock()

    def containsNPC(self, npcid: int) -> bool:
        (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().lock()
        try:
            itr = (self.mapobjects.get(MapleMapObjectType.NPC)).values().iterator()
            while itr.hasNext():
                n = itr.next()
                if n.getId() == npcid:
                return True
            return False
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().unlock()

    def getNPCById(self, id: int) -> Any:
        (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().lock()
        try:
            itr = (self.mapobjects.get(MapleMapObjectType.NPC)).values().iterator()
            while itr.hasNext():
                n = itr.next()
                if n.getId() == id:
                return n
            return None
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().unlock()

    def getMonsterById(self, id: int) -> Any:
        (self.mapobjectlocks.get(MapleMapObjectType.MONSTER)).readLock().lock()
        try:
            ret = None
            itr = (self.mapobjects.get(MapleMapObjectType.MONSTER)).values().iterator()
            while itr.hasNext():
                n = itr.next()
                if n.getId() == id:
                    ret = n
                    break
            return ret
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.MONSTER)).readLock().unlock()

    def countMonsterById(self, id: int) -> int:
        (self.mapobjectlocks.get(MapleMapObjectType.MONSTER)).readLock().lock()
        try:
            ret = 0
            itr = (self.mapobjects.get(MapleMapObjectType.MONSTER)).values().iterator()
            while itr.hasNext():
                n = itr.next()
                if n.getId() == id:
                ret += 1
            return ret
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.MONSTER)).readLock().unlock()

    def getReactorById(self, id: int) -> Any:
        (self.mapobjectlocks.get(MapleMapObjectType.REACTOR)).readLock().lock()
        try:
            ret = None
            itr = (self.mapobjects.get(MapleMapObjectType.REACTOR)).values().iterator()
            while itr.hasNext():
                n = itr.next()
                if n.getReactorId() == id:
                    ret = n
                    break
            return ret
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.REACTOR)).readLock().unlock()

    def getMonsterByOid(self, oid: int) -> Any:
        mmo = self.getMapObject(oid, MapleMapObjectType.MONSTER)
        if mmo is None:
            return None
        return mmo

    def getNPCByOid(self, oid: int) -> Any:
        mmo = self.getMapObject(oid, MapleMapObjectType.NPC)
        if mmo is None:
            return None
        return mmo

    def getReactorByOid(self, oid: int) -> Any:
        mmo = self.getMapObject(oid, MapleMapObjectType.REACTOR)
        if mmo is None:
            return None
        return mmo

    def getReactorByName(self, name: str) -> Any:
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for obj in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                mr = obj
                if mr.getName().lower() == name.lower():
                    return mr
            return None
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()

    def spawnNpc(self, id: int, pos: Any) -> None:
        npc = MapleLifeFactory.getNPC(id)
        npc.setPosition(pos)
        npc.setCy(pos.y)
        npc.setRx0(pos.x + 50)
        npc.setRx1(pos.x - 50)
        npc.setFh(self.getFootholds().findBelow(pos).getId())
        npc.setCustom(True)
        self.addMapObject(npc)
        self.broadcastMessage(MaplePacketCreator.spawnNPC(npc, True))

    def removeNpc(self, npcid: int) -> None:
        (self.mapobjectlocks.get(MapleMapObjectType.NPC)).writeLock().lock()
        try:
            itr = (self.mapobjects.get(MapleMapObjectType.NPC)).values().iterator()
            while itr.hasNext():
                npc = itr.next()
                if npc.isCustom() and npc.getId() == npcid:
                    broadcastMessage(MaplePacketCreator.removeNPC(npc.getObjectId()))
                    itr.remove()
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.NPC)).writeLock().unlock()

    def spawnMonster_sSack(self, mob: Any, pos: Any, spawnType: int) -> None:
        spos = self.calcPointBelow(Point(pos.x, pos.y - 1))
        mob.setPosition(spos)
        self.spawnMonster(mob, spawnType)

    def spawnMonsterOnGroundBelow(self, mob: Any, pos: Any) -> None:
        self.spawnMonster_sSack(mob, pos, -2)

    def spawnMonster_sSack_mob_pos_spawnType_hp(self, mob: Any, pos: Any, spawnType: int, hp: int) -> None:
        spos = self.calcPointBelow(Point(pos.x, pos.y - 1))
        mob.setPosition(spos)
        mob.setHp(hp)
        self.spawnMonster(mob, spawnType)

    def spawnMonsterOnGroundBelow_mob_pos_hp(self, mob: Any, pos: Any, hp: int) -> None:
        self.spawnMonster_sSack(mob, pos, -2, hp)

    def spawnMonsterWithEffectBelow(self, mob: Any, pos: Any, effect: int) -> int:
        spos = self.calcPointBelow(Point(pos.x, pos.y - 1))
        return self.spawnMonsterWithEffect(mob, effect, spos)

    def spawnZakum(self, x: int, y: int) -> None:
        pos = Point(x, y)
        mainb = MapleLifeFactory.getMonster(8800000)
        spos = self.calcPointBelow(Point(pos.x, pos.y - 1))
        mainb.setPosition(spos)
        mainb.setFake(True)
        mainb.getStats().setChange(True)
        self.spawnFakeMonster(mainb)
        array = None
        zakpart = array = new int[] { 8800003, 8800004, 8800005, 8800006, 8800007, 8800008, 8800009, 8800010 }
        for i in array:
            part = MapleLifeFactory.getMonster(i)
            part.setPosition(spos)
            self.spawnMonster(part, -2)
        if self.squadSchedule is not None:
            self.cancelSquadSchedule()

    def getAllMistsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.MIST).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.MIST).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.MIST).readLock().unlock()
        return ret

    def spawnFakeMonsterOnGroundBelow(self, mob: Any, pos: Any) -> None:
        calcPointBelow = None
        spos = calcPointBelow = self.calcPointBelow(Point(pos.x, pos.y - 1))
        calcPointBelow.y -= 1
        mob.setPosition(spos)
        self.spawnFakeMonster(mob)

    def getMobsSize(self) -> int:
        return self.mapobjects.get(MapleMapObjectType.MONSTER)

    def checkRemoveAfter(self, monster: Any) -> None:
        def _task_1():
            if monster is not None and monster == MapleMap.self.getMapObject(monster.getObjectId(), monster.getType()):
                MapleMap.self.killMonster(monster)

        ra = monster.getStats().getRemoveAfter()
        if ra > 0:
            Timer.MapTimer.getInstance().schedule(_task_1, ra * 1000)

    def spawnRevives(self, monster: Any, oid: int) -> None:
        monster.setMap(this)
        self.checkRemoveAfter(monster)
        monster.setLinkOid(oid)
        self.spawnAndAddRangedMapObject(monster, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MobPacket.spawnMonster(monster, False))
        self.updateMonsterController(monster)
        self.spawnedMonstersOnMap.incrementAndGet()

    def sendPackets(self, c: Any) -> None:
        c.getSession().write(MobPacket.spawnMonster(monster, False))

    def spawnMonster(self, monster: Any, spawnType: int) -> None:
        monster.setMap(this)
        self.checkRemoveAfter(monster)
        self.spawnAndAddRangedMapObject(monster, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MobPacket.spawnMonster(monster, True))
        self.updateMonsterController(monster)
        self.spawnedMonstersOnMap.incrementAndGet()

    def sendPackets_c(self, c: Any) -> None:
        c.getSession().write(MobPacket.spawnMonster(monster, True))

    def spawnMonsterWithEffect(self, monster: Any, effect: int, pos: Any) -> int:
        try:
            monster.setMap(this)
            monster.setPosition(pos)
            self.spawnAndAddRangedMapObject(monster, DelayedPacketCreation()
                public void sendPackets(final MapleClient c)
                    c.getSession().write(MobPacket.spawnMonster(monster, True, effect))
            self.updateMonsterController(monster)
            self.spawnedMonstersOnMap.incrementAndGet()
            return monster.getObjectId()
        except Exception as e:
            return -1

    def spawnFakeMonster(self, monster: Any) -> None:
        monster.setMap(this)
        monster.setFake(True)
        self.spawnAndAddRangedMapObject(monster, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MobPacket.spawnFakeMonster(monster, 0))
        self.updateMonsterController(monster)
        self.spawnedMonstersOnMap.incrementAndGet()

    def spawnReactor(self, reactor: Any) -> None:
        reactor.setMap(this)
        self.spawnAndAddRangedMapObject(reactor, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.spawnReactor(reactor))

    def respawnReactor(self, reactor: Any) -> None:
        reactor.setState(0)
        reactor.setAlive(True)
        self.spawnReactor(reactor)

    def spawnDoor(self, door: Any) -> None:
        self.spawnAndAddRangedMapObject(door, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.spawnDoor(door.getOwner().getId(), door.getTargetPosition(), False))
                if door.getOwner().getParty() is not None and (door.getOwner() == c.getPlayer() or door.getOwner().getParty().containsMembers(MaplePartyCharacter(c.getPlayer()))):
                    c.getSession().write(MaplePacketCreator.partyPortal(door.getTown().getId(), door.getTarget().getId(), door.getSkill(), door.getTargetPosition()))
                c.getSession().write(MaplePacketCreator.spawnPortal(door.getTown().getId(), door.getTarget().getId(), door.getSkill(), door.getTargetPosition()))
                c.getSession().write(MaplePacketCreator.enableActions())
        public boolean canSpawn(final MapleCharacter chr)
            return door.getTarget().getId() == chr.getMapId() or door.getOwnerId() == chr.getId() or (door.getOwner() is not None and door.getOwner().getParty() is not None and door.getOwner().getParty().getMemberById(chr.getId()) is not None)

    def canSpawn(self, chr: Any) -> bool:
        return door.getTarget().getId() == chr.getMapId() or door.getOwnerId() == chr.getId() or (door.getOwner() is not None and door.getOwner().getParty() is not None and door.getOwner().getParty().getMemberById(chr.getId()) is not None)

    def spawnSummon(self, summon: Any) -> None:
        summon.updateMap(this)
        self.spawnAndAddRangedMapObject(summon, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                if summon is not None and c.getPlayer() is not None and (not summon.isChangedMap() or summon.getOwnerId() == c.getPlayer().getId()):
                    c.getSession().write(MaplePacketCreator.spawnSummon(summon, True))

    def spawnDragon(self, summon: Any) -> None:
        self.spawnAndAddRangedMapObject(summon, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)

    def spawnMist(self, mist: Any, duration: int, fake: bool) -> None:
        def _task_1():
            for mo in MapleMap.self.getMapObjectsInRect(mist.getBox(), Collections.singletonList(MapleMapObjectType.MONSTER)):
                if mist.makeChanceResult() and not (mo).isBuffed(MonsterStatus.中毒):
                (mo).applyStatus(owner, MonsterStatusEffect(MonsterStatus.中毒, Integer.valueOf(1), mist.getSourceSkill().getId(), None, False), True, duration, True)

        def _task_2():
            for mo in MapleMap.self.getMapObjectsInRect(mist.getBox(), Collections.singletonList(MapleMapObjectType.PLAYER)):
                if mist.makeChanceResult():
                    chr = mo
                    chr.addMP((int)(mist.getSource().getX() * chr.getStat().getMaxMp() / 100.0))

        def _task_3():
            MapleMap.self.broadcastMessage(MaplePacketCreator.removeMist(mist.getObjectId(), False))
            MapleMap.self.removeMapObject(mist)
            if poisonSchedule is not None:
            poisonSchedule.cancel(False)

        final ScheduledFuture<?> poisonSchedule
        owner = None
        spawnAndAddRangedMapObject(mist, DelayedPacketCreation()
            public void sendPackets(MapleClient c)
                mist.sendSpawnData(c)
        Timer.MapTimer tMan = Timer.MapTimer.getInstance()
        # switch (mist.isPoisonMist()):
            # case 1:
            owner = getCharacterById(mist.getOwnerId())
            poisonSchedule = tMan.register(_task_1,2000, 2500)
            break
            # case 2:
            poisonSchedule = tMan.register(_task_2,2000, 2500)
            break
            # default:
            poisonSchedule = None
            break
        tMan.schedule(_task_3,duration)

    def disappearingItemDrop(self, dropper: Any, owner: Any, item: Any, pos: Any) -> None:
        droppos = self.calcDropPos(pos, pos)
        drop = MapleMapItem(item, droppos, dropper, owner, 1, False)
        self.broadcastMessage(MaplePacketCreator.dropItemFromMapObject(drop, dropper.getPosition(), droppos, 3), drop.getPosition())

    def spawnMesoDrop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> None:
        droppos = self.calcDropPos(position, position)
        mdrop = MapleMapItem(meso, droppos, dropper, owner, droptype, playerDrop)
        self.spawnAndAddRangedMapObject(mdrop, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.dropItemFromMapObject(mdrop, dropper.getPosition(), droppos, 1))
        if not self.everlast:
            mdrop.registerExpire(120000)
            if droptype == 0 or droptype == 1:
                mdrop.registerFFA(30000)

    def spawnMobMesoDrop(self, meso: int, position: Any, dropper: Any, owner: Any, playerDrop: bool, droptype: int) -> None:
        mdrop = MapleMapItem(meso, position, dropper, owner, droptype, playerDrop)
        self.spawnAndAddRangedMapObject(mdrop, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.dropItemFromMapObject(mdrop, dropper.getPosition(), position, 1))
        mdrop.registerExpire(120000)
        if droptype == 0 or droptype == 1:
            mdrop.registerFFA(30000)

    def spawnMobDrop(self, idrop: Any, dropPos: Any, mob: Any, chr: Any, droptype: int, questid: int) -> None:
        mdrop = MapleMapItem(idrop, dropPos, mob, chr, droptype, False, questid)
        self.spawnAndAddRangedMapObject(mdrop, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                if questid <= 0 or c.getPlayer().getQuestStatus(questid) == 1:
                    c.getSession().write(MaplePacketCreator.dropItemFromMapObject(mdrop, mob.getPosition(), dropPos, 1))
        mdrop.registerExpire(120000)
        if droptype == 0 or droptype == 1:
            mdrop.registerFFA(30000)
        self.activateItemReactors(mdrop, chr.getClient())

    def spawnRandDrop(self) -> None:
        pass

    def spawnAutoDrop(self, itemid: int, pos: Any) -> None:
        idrop = None
        ii = MapleItemInformationProvider.getInstance()
        if GameConstants.getInventoryType(itemid) == MapleInventoryType.EQUIP:
            idrop = ii.randomizeStats(ii.getEquipById(itemid))
        else:
            idrop = Item(itemid, 0, 1, 0)
        mdrop = MapleMapItem(pos, idrop)
        self.spawnAndAddRangedMapObject(mdrop, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.dropItemFromMapObject(mdrop, pos, pos, 1))
        self.broadcastMessage(MaplePacketCreator.dropItemFromMapObject(mdrop, pos, pos, 0))
        mdrop.registerExpire(120000)

    def spawnItemDrop(self, dropper: Any, owner: Any, item: Any, pos: Any, ffaDrop: bool, playerDrop: bool) -> None:
        droppos = self.calcDropPos(pos, pos)
        drop = MapleMapItem(item, droppos, dropper, owner, 2, playerDrop)
        self.spawnAndAddRangedMapObject(drop, DelayedPacketCreation()
            public void sendPackets(final MapleClient c)
                c.getSession().write(MaplePacketCreator.dropItemFromMapObject(drop, dropper.getPosition(), droppos, 1))
        self.broadcastMessage(MaplePacketCreator.dropItemFromMapObject(drop, dropper.getPosition(), droppos, 0))
        if not self.everlast:
            drop.registerExpire(120000)
            self.activateItemReactors(drop, owner.getClient())

    def activateItemReactors(self, drop: Any, c: Any) -> None:
        item = drop.getItem()
        self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().lock()
        try:
            for o in self.mapobjects.get(MapleMapObjectType.REACTOR).values():
                react = o
                if react.getReactorType() == 100 and GameConstants.isCustomReactItem(react.getReactorId(), item.getItemId(), react.getReactItem().getLeft()) and react.getReactItem().getRight() == item.getQuantity() and react.getArea().__contains__(drop.getPosition()) and not react.isTimerActive():
                    Timer.MapTimer.getInstance().schedule(ActivateItemReactor(drop, react, c), 1000)
                    react.setTimerActive(True)
                    break
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.REACTOR).readLock().unlock()

    def getItemsSize(self) -> int:
        return self.mapobjects.get(MapleMapObjectType.ITEM)

    def getAllItems(self) -> list:
        return self.getAllItemsThreadsafe()

    def getAllItemsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.ITEM).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().unlock()
        return ret

    def returnEverLastItem(self, chr: Any) -> None:
        for o in self.getAllItemsThreadsafe():
            item = o
            if item.getOwner() == chr.getId():
                item.setPickedUp(True)
                self.broadcastMessage(MaplePacketCreator.removeItemFromMap(item.getObjectId(), 2, chr.getId()), item.getPosition())
                if item.getMeso() > 0:
                    chr.gainMeso(item.getMeso(), False)
                else:
                    MapleInventoryManipulator.addFromDrop(chr.getClient(), item.getItem(), False)
                self.removeMapObject(item)

    def talkMonster(self, msg: str, itemId: int, objectid: int) -> None:
        if itemId > 0:
            self.startMapEffect(msg, itemId, False)
        self.broadcastMessage(MobPacket.talkMonster(objectid, itemId, msg))
        self.broadcastMessage(MobPacket.removeTalkMonster(objectid))

    def startMapEffect(self, msg: str, itemId: int) -> None:
        self.startMapEffect(msg, itemId, False)

    def startMapEffect_msg_itemId_jukebox(self, msg: str, itemId: int, jukebox: bool) -> None:
        def _task_1():
            MapleMap.self.broadcastMessage(MapleMap.self.mapEffect.makeDestroyData())
            MapleMap.self.mapEffect = None

        if self.mapEffect is not None:
            return
        (self.mapEffect = MapleMapEffect(msg, itemId)).setJukebox(jukebox)
        self.broadcastMessage(self.mapEffect.makeStartData())
        Timer.MapTimer.getInstance().schedule(_task_1, jukebox ? 300000 : 30000)

    def startExtendedMapEffect(self, msg: str, itemId: int) -> None:
        def _task_1():
            MapleMap.self.broadcastMessage(MaplePacketCreator.removeMapEffect())
            MapleMap.self.broadcastMessage(MaplePacketCreator.startMapEffect(msg, itemId, False))

        self.broadcastMessage(MaplePacketCreator.startMapEffect(msg, itemId, True))
        Timer.MapTimer.getInstance().schedule(_task_1, 60000)

    def startJukebox(self, msg: str, itemId: int) -> None:
        self.startMapEffect(msg, itemId, True)

    def addPlayer(self, chr: Any) -> None:
        self.mapobjectlocks.get(MapleMapObjectType.PLAYER).writeLock().lock()
        try:
            self.mapobjects.get(MapleMapObjectType.PLAYER).put(chr.getObjectId(), chr)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.PLAYER).writeLock().unlock()
        self.charactersLock.writeLock().lock()
        try:
            self.characters.add(chr)
        finally:
            self.charactersLock.writeLock().unlock()
        进入地图开启显示数据 = False
        if self.mapid == 109080000 or self.mapid == 109080001 or self.mapid == 109080002 or self.mapid == 109080003 or self.mapid == 109080010 or self.mapid == 109080011 or self.mapid == 109080012:
            chr.setCoconutTeam(self.getAndSwitchTeam() ? 0 : 1)
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据A")
        packet = MaplePacketCreator.spawnPlayerMapobject(chr)
        if not chr.isHidden():
            self.broadcastMessage(chr, packet, False)
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据B")
            if chr.isGM() and self.speedRunStart > 0:
                self.endSpeedRun()
                self.broadcastMessage(MaplePacketCreator.serverNotice(5, "The speed run has ended."))
                if ServerConstants.封包显示 or 进入地图开启显示数据:
                    print("进入地图加载数据C")
        else:
            self.broadcastGMMessage(chr, packet, False)
        if not chr.isClone():
            self.sendObjectPlacement(chr)
            chr.getClient().getSession().write(MaplePacketCreator.spawnPlayerMapobject(chr))
            if not self.onUserEnter == (""):
                MapScriptMethods.startScript_User(chr.getClient(), self.onUserEnter)
            if not self.onFirstUserEnter == ("") and self.getCharactersSize() == 1:
                MapScriptMethods.startScript_FirstUser(chr.getClient(), self.onFirstUserEnter)
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据D")
            # switch (self.mapid):
                # case 109030001:
                # case 109040000:
                # case 109060001:
                # case 109080000:
                # case 109080010:
                    chr.getClient().getSession().write(MaplePacketCreator.showEventInstructions())
                    break
                # case 809000101:
                # case 809000201:
                    chr.getClient().getSession().write(MaplePacketCreator.showEquipEffect())
                    break
        for pet in chr.getPets():
            if pet.getSummoned():
                pet.setPos(chr.getTruePosition())
                chr.getClient().getSession().write(PetPacket.updatePet(pet, chr.getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))
                self.broadcastMessage(chr, PetPacket.showPet(chr, pet, False, False), False)
                if not ServerConstants.封包显示 and not 进入地图开启显示数据:
                    continue
                print("进入地图加载数据F")
        if self.hasForcedEquip():
            chr.getClient().getSession().write(MaplePacketCreator.showForcedEquip())
        chr.getClient().getSession().write(MaplePacketCreator.removeTutorialStats())
        if chr.getMapId() >= 914000200 and chr.getMapId() <= 914000220:
            chr.getClient().getSession().write(MaplePacketCreator.addTutorialStats())
        if (chr.getMapId() >= 140090100 and chr.getMapId() <= 140090500) or (chr.getJob() == 1000 and chr.getMapId() != 130030000):
            chr.getClient().getSession().write(MaplePacketCreator.spawnTutorialSummon(1))
        else:
            chr.getClient().getSession().write(MaplePacketCreator.spawnTutorialSummon(0))
        if not self.onUserEnter == (""):
            MapScriptMethods.startScript_User(chr.getClient(), self.onUserEnter)
        if not self.onFirstUserEnter == ("") and self.getCharacters() == 1:
            MapScriptMethods.startScript_FirstUser(chr.getClient(), self.onFirstUserEnter)
        if not chr.isClone():
            ss = chr.getSummonsReadLock()
            try:
                for summon in ss:
                    summon.setPosition(chr.getTruePosition())
                    chr.addVisibleMapObject(summon)
                    self.spawnSummon(summon)
            finally:
                chr.unlockSummonsReadLock()
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据H")
        if chr.getChalkboard() is not None:
            chr.getClient().getSession().write(MTSCSPacket.useChalkboard(chr.getId(), chr.getChalkboard()))
        self.broadcastMessage(MaplePacketCreator.loveEffect())
        if self.timeLimit > 0 and self.getForcedReturnMap() is not None and not chr.isClone():
            chr.startMapTimeLimitTask(self.timeLimit, self.getForcedReturnMap())
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据I")
        if self.getSquadBegin() is not None and self.getSquadBegin().getTimeLeft() > 0 and self.getSquadBegin().getStatus() == 1:
            chr.getClient().getSession().write(MaplePacketCreator.getClock((int)(self.getSquadBegin().getTimeLeft() / 1000)))
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据O")
        if chr.getCarnivalParty() is not None and chr.getEventInstance() is not None:
            chr.getClient().getSession().write(chr.getCoconutTeam())
            chr.getEventInstance().onMapLoad(chr)
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据M")
        MapleEvent.mapLoad(chr, self.channel)
        if chr.getEventInstance() is not None and chr.getEventInstance().isTimerStarted() and not chr.isClone():
            chr.getClient().getSession().write(MaplePacketCreator.getClock((int)(chr.getEventInstance().getTimeLeft() / 1000)))
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据K")
        if self.hasClock():
            cal = Calendar.getInstance()
            chr.getClient().getSession().write(MaplePacketCreator.getClockTime(cal.get(11), cal.get(12), cal.get(13)))
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据L")
        if self.isTown():
            chr.cancelEffectFromBuffStat(MapleBuffStat.RAINING_MINES)
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据W-------------完")
        if chr.getParty() is not None and not chr.isClone():
            chr.receivePartyMemberHP()
            chr.updatePartyMemberHP()
            if ServerConstants.封包显示 or 进入地图开启显示数据:
                print("进入地图加载数据G")
        if self.permanentWeather > 0:
            chr.getClient().getSession().write(MaplePacketCreator.startMapEffect("", self.permanentWeather, False))
        if self.getPlatforms() > 0:
            chr.getClient().getSession().write(MaplePacketCreator.getMovingPlatforms(this))
        if self.environment > 0:
            chr.getClient().getSession().write(MaplePacketCreator.getUpdateEnvironment(this))
        if self.getNumMonsters() > 0 and (self.mapid == 280030001 or self.mapid == 240060201 or self.mapid == 280030000 or self.mapid == 280030100 or self.mapid == 240060200 or self.mapid == 220080001 or self.mapid == 541020800 or self.mapid == 541010100):
            music = "Bgm09/TimeAttack"
            # switch (self.mapid):
                # case 240060200:
                # case 240060201:
                    music = "Bgm14/HonTale"
                    break
                # case 280030000:
                # case 280030001:
                # case 280030100:
                    music = "Bgm06/FinalFight"
                    break
            chr.getClient().getSession().write(MaplePacketCreator.musicChange(music))

    def getNumItems(self) -> int:
        self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().lock()
        try:
            return self.mapobjects.get(MapleMapObjectType.ITEM)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().unlock()

    def hasForcedEquip(self) -> bool:
        return self.fieldType == 81 or self.fieldType == 82

    def setFieldType(self, fieldType: int) -> None:
        self.fieldType = fieldType

    def getNumMonsters(self) -> int:
        self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().lock()
        try:
            return self.mapobjects.get(MapleMapObjectType.MONSTER)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().unlock()

    def doShrine(self, spawned: bool) -> None:
        def _task_1():
            sqnow = MapleMap.self.getSquadByMap()
            if MapleMap.self.getCharactersSize() > 0 and MapleMap.self.getNumMonsters() == monsterz and sqnow is not None and sqnow.getStatus() == 2 and sqnow.getLeaderName() == (leaderName) and MapleMap.self.getEMByMap().getProperty("state") == (state):
                passed = monsterz == 0
                for m in MapleMap.self.getAllMonstersThreadsafe():
                    for i in monsteridz:
                        if m.getObjectId() == i:
                            passed = True
                            break
                    if passed:
                        break
                if passed:
                    packet = None
                    # switch (mode):
                        # case 1:
                            packet = MaplePacketCreator.showZakumShrine(spawned, 0)
                            break
                        # case 2:
                            packet = MaplePacketCreator.showChaosZakumShrine(spawned, 0)
                            break
                        # default:
                            packet = MaplePacketCreator.showHorntailShrine(spawned, 0)
                            break
                    for chr in MapleMap.self.getCharactersThreadsafe():
                        chr.getClient().getSession().write(packet)
                        chr.changeMap(returnMapz, returnMapz.getPortal(0))
                    MapleMap.self.checkStates("")
                    MapleMap.self.resetFully()

        def _task_2():
            sqnow = MapleMap.self.getSquadByMap()
            if MapleMap.self.getCharactersSize() > 0 and sqnow is not None and sqnow.getStatus() == 2 and sqnow.getLeaderName() == (leaderName) and MapleMap.self.getEMByMap().getProperty("state") == (state):
                packet = None
                # switch (mode):
                    # case 1:
                        packet = MaplePacketCreator.showZakumShrine(spawned, 0)
                        break
                    # case 2:
                        packet = MaplePacketCreator.showChaosZakumShrine(spawned, 0)
                        break
                    # default:
                        packet = MaplePacketCreator.showHorntailShrine(spawned, 0)
                        break
                for chr in MapleMap.self.getCharactersThreadsafe():
                    chr.getClient().getSession().write(packet)
                    chr.changeMap(returnMapz, returnMapz.getPortal(0))
                MapleMap.self.checkStates("")
                MapleMap.self.resetFully()

        if self.squadSchedule is not None:
            self.cancelSquadSchedule()
        sqd = self.getSquadByMap()
        mode = (self.mapid == 280030000 or self.mapid == 280030100) ? 1 : ((self.mapid == 280030001) ? 2 : ((self.mapid == 240060200 or self.mapid == 240060201) ? 3 : 0))
        em = self.getEMByMap()
        if sqd is not None and em is not None and self.getCharactersSize() > 0:
            leaderName = sqd.getLeaderName()
            state = em.getProperty("state")
            returnMapa = self.getForcedReturnMap()
            if returnMapa is None or returnMapa.getId() == self.mapid:
                returnMapa = self.getReturnMap()
            # switch (mode):
                # case 1:
                    self.broadcastMessage(MaplePacketCreator.showZakumShrine(spawned, 5))
                    break
                # case 2:
                    self.broadcastMessage(MaplePacketCreator.showChaosZakumShrine(spawned, 5))
                    break
                # case 3:
                    self.broadcastMessage(MaplePacketCreator.showChaosHorntailShrine(spawned, 5))
                    break
                # default:
                    self.broadcastMessage(MaplePacketCreator.showHorntailShrine(spawned, 5))
                    break
            if mode == 1 or spawned:
                self.broadcastMessage(MaplePacketCreator.getClock(300))
            returnMapz = returnMapa
            run = None
            if not spawned:
                monsterz = self.getAllMonstersThreadsafe()
                monsteridz = []
                for m in monsterz:
                    monsteridz.add(m.getObjectId())
                run = _task_1
            else:
                run = _task_2
            self.squadSchedule = Timer.MapTimer.getInstance().schedule(run, 300000)

    def getSquadByMap(self) -> Any:
        MapleSquad.MapleSquadType zz = None
        # switch (self.mapid):
            # case 105100300:
            # case 105100400:
                zz = MapleSquad.MapleSquadType.bossbalrog
                break
            # case 280030000:
                zz = MapleSquad.MapleSquadType.zak
                break
            # case 280030001:
                zz = MapleSquad.MapleSquadType.chaoszak
                break
            # case 240060200:
                zz = MapleSquad.MapleSquadType.horntail
                break
            # case 240060201:
                zz = MapleSquad.MapleSquadType.chaosht
                break
            # case 270050100:
                zz = MapleSquad.MapleSquadType.pinkbean
                break
            # case 802000111:
                zz = MapleSquad.MapleSquadType.nmm_squad
                break
            # case 802000211:
                zz = MapleSquad.MapleSquadType.vergamot
                break
            # case 802000311:
                zz = MapleSquad.MapleSquadType.tokyo_2095
                break
            # case 802000411:
                zz = MapleSquad.MapleSquadType.dunas
                break
            # case 802000611:
                zz = MapleSquad.MapleSquadType.nibergen_squad
                break
            # case 802000711:
                zz = MapleSquad.MapleSquadType.dunas2
                break
            # case 802000801:
            # case 802000802:
            # case 802000803:
                zz = MapleSquad.MapleSquadType.core_blaze
                break
            # case 802000821:
            # case 802000823:
                zz = MapleSquad.MapleSquadType.aufheben
                break
            # case 211070100:
            # case 211070101:
            # case 211070110:
                zz = MapleSquad.MapleSquadType.vonleon
                break
            # case 551030200:
                zz = MapleSquad.MapleSquadType.scartar
                break
            # case 271040100:
                zz = MapleSquad.MapleSquadType.cygnus
                break
            # default:
                return None
        return ChannelServer.getInstance(self.channel).getMapleSquad(zz)

    def getSquadBegin(self) -> Any:
        if self.squad is not None:
            return ChannelServer.getInstance(self.channel).getMapleSquad(self.squad)
        return None

    def getEMByMap(self) -> Any:
        em = None
        # switch (self.mapid):
            # case 105100400:
                em = "BossBalrog_EASY"
                break
            # case 105100300:
                em = "BossBalrog_NORMAL"
                break
            # case 280030000:
                em = "ZakumBattle"
                break
            # case 240060200:
                em = "HorntailBattle"
                break
            # case 280030001:
                em = "ChaosZakum"
                break
            # case 240060201:
                em = "ChaosHorntail"
                break
            # case 270050100:
                em = "PinkBeanBattle"
                break
            # case 802000111:
                em = "NamelessMagicMonster"
                break
            # case 802000211:
                em = "Vergamot"
                break
            # case 802000311:
                em = "2095_tokyo"
                break
            # case 802000411:
                em = "Dunas"
                break
            # case 802000611:
                em = "Nibergen"
                break
            # case 802000711:
                em = "Dunas2"
                break
            # case 802000801:
            # case 802000802:
            # case 802000803:
                em = "CoreBlaze"
                break
            # case 802000821:
            # case 802000823:
                em = "Aufhaven"
                break
            # case 211070100:
            # case 211070101:
            # case 211070110:
                em = "VonLeonBattle"
                break
            # case 551030200:
                em = "ScarTarBattle"
                break
            # case 271040100:
                em = "CygnusBattle"
                break
            # case 262030300:
                em = "HillaBattle"
                break
            # case 262031300:
                em = "DarkHillaBattle"
                break
            # case 272020110:
            # case 272030400:
                em = "ArkariumBattle"
                break
            # case 955000100:
            # case 955000200:
            # case 955000300:
                em = "AswanOffSeason"
                break
            # case 280030100:
                em = "ZakumBattle"
                break
            # case 272020200:
                em = "Akayile"
                break
            # case 689013000:
                em = "PinkZakum"
                break
            # case 703200400:
                em = "0AllBoss"
                break
            # default:
                return None
        return ChannelServer.getInstance(self.channel).getEventSM().getEventManager(em)

    def removePlayer(self, chr: Any) -> None:
        if self.everlast:
            self.returnEverLastItem(chr)
        self.charactersLock.writeLock().lock()
        try:
            self.characters.remove(chr)
        finally:
            self.charactersLock.writeLock().unlock()
        self.removeMapObject(chr)
        self.broadcastMessage(MaplePacketCreator.removePlayerFromMap(chr.getId(), chr))
        toCancel = []
        ss = chr.getSummonsReadLock()
        try:
            for summon in ss:
                self.broadcastMessage(MaplePacketCreator.removeSummon(summon, True))
                self.removeMapObject(summon)
                if summon.getMovementType() == SummonMovementType.不会移动 or summon.getMovementType() == SummonMovementType.CIRCLE_STATIONARY or summon.getMovementType() == SummonMovementType.WALK_STATIONARY:
                    toCancel.add(summon)
                else:
                    summon.setChangedMap(True)
        finally:
            chr.unlockSummonsReadLock()
        for summon in toCancel:
            chr.removeSummon(summon)
            chr.dispelSkill(summon.getSkill())
        if not chr.isClone():
            self.checkStates(chr.getName())
            if self.mapid == 109020001:
                chr.canTalk(True)
            for chrz in chr.getClones():
                if chrz.get() is not None:
                    self.removePlayer(chrz.get())
            chr.leaveMap(this)

    def getAllPlayers(self) -> list:
        return self.getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.PLAYER))

    def broadcastMessage(self, packet: Any) -> None:
        self.broadcastMessage(None, packet, Double.POSITIVE_INFINITY, None)

    def broadcastMessage_source_packet_repeatToSource(self, source: Any, packet: Any, repeatToSource: bool) -> None:
        self.broadcastMessage(repeatToSource ? None : source, packet, Double.POSITIVE_INFINITY, source.getPosition())

    def broadcastMessage_packet_rangedFrom(self, packet: Any, rangedFrom: Any) -> None:
        self.broadcastMessage(None, packet, GameConstants.maxViewRangeSq(), rangedFrom)

    def broadcastMessage_source_packet_rangedFrom(self, source: Any, packet: Any, rangedFrom: Any) -> None:
        self.broadcastMessage(source, packet, GameConstants.maxViewRangeSq(), rangedFrom)

    def broadcastMessage_source_packet_rangeSq_rangedFrom(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> None:
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if chr != source:
                    if rangeSq < Double.POSITIVE_INFINITY:
                        if rangedFrom.distanceSq(chr.getPosition()) > rangeSq:
                            continue
                        chr.getClient().getSession().write(packet)
                    else:
                        chr.getClient().getSession().write(packet)
        finally:
            self.charactersLock.readLock().unlock()

    def sendObjectPlacement(self, chr: Any) -> None:
        if chr is None:
            return
        for o in self.getMapObjectsInRange(chr.getTruePosition(), GameConstants.maxViewRangeSq(), GameConstants.rangedMapobjectTypes):
            if o.getType() == MapleMapObjectType.REACTOR and not (o).isAlive():
                continue
            o.sendSpawnData(chr.getClient())
            chr.addVisibleMapObject(o)

    def getMapObjectsInRange(self, from: Any, rangeSq: float) -> list:
        ret = []
        for type in MapleMapObjectType.values():
            self.mapobjectlocks.get(type).readLock().lock()
            try:
                for mmo in self.mapobjects.get(type).values():
                    if from.distanceSq(mmo.getPosition()) <= rangeSq:
                        ret.add(mmo)
            finally:
                self.mapobjectlocks.get(type).readLock().unlock()
        return ret

    def getItemsInRange(self, from: Any, rangeSq: float) -> list:
        return self.getMapObjectsInRange(from, rangeSq, Arrays.asList(MapleMapObjectType.ITEM))

    def getMapObjectsInRange_from_rangeSq_MapObject_types(self, from: Any, rangeSq: float, MapObject_types: list) -> list:
        ret = []
        for type in MapObject_types:
            self.mapobjectlocks.get(type).readLock().lock()
            try:
                for mmo in self.mapobjects.get(type).values():
                    if from.distanceSq(mmo.getPosition()) <= rangeSq:
                        ret.add(mmo)
            finally:
                self.mapobjectlocks.get(type).readLock().unlock()
        return ret

    def getMapObjectsInRect(self, box: Any, MapObject_types: list) -> list:
        ret = []
        for type in MapObject_types:
            self.mapobjectlocks.get(type).readLock().lock()
            try:
                for mmo in self.mapobjects.get(type).values():
                    if (mmo.getPosition( in box)):
                        ret.add(mmo)
            finally:
                self.mapobjectlocks.get(type).readLock().unlock()
        return ret

    def getPlayersInRectAndInList(self, box: Any, chrList: list) -> list:
        character = []
        self.charactersLock.readLock().lock()
        try:
            for a in self.characters:
                if (a in chrList) and (a.getPosition( in box)):
                    character.add(a)
        finally:
            self.charactersLock.readLock().unlock()
        return character

    def addPortal(self, myPortal: Any) -> None:
        self.portals.put(myPortal.getId(), myPortal)

    def getPortal(self, portalname: str) -> Any:
        for port in self.portals.values():
            if port.getName() == (portalname):
                return port
        return None

    def getPortal_portalid(self, portalid: int) -> Any:
        return self.portals.get(portalid)

    def resetPortals(self) -> None:
        for port in self.portals.values():
            port.setPortalState(True)

    def setFootholds(self, footholds: Any) -> None:
        self.footholds = footholds

    def getFootholds(self) -> Any:
        return self.footholds

    def loadMonsterRate(self, first: bool) -> None:
        spawnSize = self.monsterSpawn
        self.maxRegularSpawn = Math.round(spawnSize * self.monsterRate)
        if self.maxRegularSpawn < 2:
            self.maxRegularSpawn = 2
        elif self.maxRegularSpawn > spawnSize:
            self.maxRegularSpawn = spawnSize - spawnSize / 15
        if self.fixedMob > 0:
            self.maxRegularSpawn = self.fixedMob
        newSpawn = []
        newBossSpawn = []
        for s in self.monsterSpawn:
            if s.getCarnivalTeam() >= 2:
                continue
            if s.getMonster().getStats().isBoss():
                newBossSpawn.add(s)
            else:
                newSpawn.add(s)
        self.monsterSpawn.clear()
        self.monsterSpawn.addAll(newBossSpawn)
        self.monsterSpawn.addAll(newSpawn)
        if first and spawnSize > 0:
            self.lastSpawnTime = int(time.time() * 1000)
            if GameConstants.isForceRespawn(self.mapid):
                self.createMobInterval = 15000

    def addMonsterSpawn(self, monster: Any, mobTime: int, carnivalTeam: int, msg: str) -> Any:
        calcPointBelow = None
        newpos = calcPointBelow = self.calcPointBelow(monster.getPosition())
        calcPointBelow.y -= 1
        sp = SpawnPoint(monster, newpos, mobTime, carnivalTeam, msg)
        if carnivalTeam > -1:
            self.monsterSpawn.add(0, sp)
        else:
            self.monsterSpawn.add(sp)
        return sp

    def addAreaMonsterSpawn(self, monster: Any, pos1: Any, pos2: Any, pos3: Any, mobTime: int, msg: str) -> None:
        pos1 = self.calcPointBelow(pos1)
        pos2 = self.calcPointBelow(pos2)
        pos3 = self.calcPointBelow(pos3)
        if pos1 is not None:
            point = pos1
            point.y -= 1
        if pos2 is not None:
            point2 = pos2
            point2.y -= 1
        if pos3 is not None:
            point3 = pos3
            point3.y -= 1
        if pos1 is None and pos2 is None and pos3 is None:
            print("WARNING: mapid " + self.mapid + ", monster " + monster.getId() + " could not be spawned.")
            return
        if pos1 is not None:
            if pos2 is None:
                pos2 = Point(pos1)
            if pos3 is None:
                pos3 = Point(pos1)
        elif pos2 is not None:
            if pos1 is None:
                pos1 = Point(pos2)
            if pos3 is None:
                pos3 = Point(pos2)
        elif pos3 is not None:
            if pos1 is None:
                pos1 = Point(pos3)
            if pos2 is None:
                pos2 = Point(pos3)
        self.monsterSpawn.add(SpawnPointAreaBoss(monster, pos1, pos2, pos3, mobTime, msg))

    def getCharacters(self) -> list:
        return self.getCharactersThreadsafe()

    def getCharactersThreadsafe(self) -> list:
        chars = []
        self.charactersLock.readLock().lock()
        try:
            for mc in self.characters:
                chars.add(mc)
        finally:
            self.charactersLock.readLock().unlock()
        return chars

    def getCharacterById_InMap(self, id: int) -> Any:
        return self.getCharacterById(id)

    def getCharacterById(self, id: int) -> Any:
        self.charactersLock.readLock().lock()
        try:
            for mc in self.characters:
                if mc.getId() == id:
                    return mc
        finally:
            self.charactersLock.readLock().unlock()
        return None

    def updateMapObjectVisibility(self, chr: Any, mo: Any) -> None:
        if chr is None or chr.isClone():
            return
        if not chr.isMapObjectVisible(mo):
            if mo.getType() == MapleMapObjectType.MIST or mo.getType() == MapleMapObjectType.SUMMON or mo.getPosition().distanceSq(chr.getPosition()) <= GameConstants.maxViewRangeSq():
                chr.addVisibleMapObject(mo)
                mo.sendSpawnData(chr.getClient())
        elif mo.getType() != MapleMapObjectType.MIST and mo.getType() != MapleMapObjectType.SUMMON and mo.getPosition().distanceSq(chr.getPosition()) > GameConstants.maxViewRangeSq():
            chr.removeVisibleMapObject(mo)
            mo.sendDestroyData(chr.getClient())
        elif mo.getType() == MapleMapObjectType.MONSTER and chr.getTruePosition().distanceSq(mo.getPosition()) <= GameConstants.maxViewRangeSq():
            self.updateMonsterController(mo)

    def moveMonster(self, monster: Any, reportedPos: Any) -> None:
        monster.setPosition(reportedPos)
        self.charactersLock.readLock().lock()
        try:
            for mc in self.characters:
                self.updateMapObjectVisibility(mc, monster)
        finally:
            self.charactersLock.readLock().unlock()

    def movePlayer(self, player: Any, newPosition: Any) -> None:
        player.setPosition(newPosition)
        if not player.isClone():
            try:
                visibleObjects = player.getAndWriteLockVisibleMapObjects()
                copy = []
                for mo in copy:
                    if mo is not None and self.getMapObject(mo.getObjectId(), mo.getType()) == mo:
                        self.updateMapObjectVisibility(player, mo)
                    else:
                        if mo is None:
                            continue
                        visibleObjects.remove(mo)
                for mo2 in self.getMapObjectsInRange(player.getPosition(), GameConstants.maxViewRangeSq()):
                    if mo2 is not None and not player.isMapObjectVisible(mo2):
                        mo2.sendSpawnData(player.getClient())
                        visibleObjects.add(mo2)
            finally:
                player.unlockWriteVisibleMapObjects()

    def findClosestSpawnpoint(self, from: Any) -> Any:
        closest = None
        shortestDistance = Double.POSITIVE_INFINITY
        for portal in self.portals.values():
            distance = portal.getPosition().distanceSq(from)
            if portal.getType() >= 0 and portal.getType() <= 2 and distance < shortestDistance and portal.getTargetMapId() == 999999999:
                closest = portal
                shortestDistance = distance
        return closest

    def spawnDebug(self) -> str:
        sb = ""
        sb.append(self.getMapObjectSize())
        sb.append(" spawnedMonstersOnMap: ")
        sb.append(self.spawnedMonstersOnMap)
        sb.append(" spawnpoints: ")
        sb.append(self.monsterSpawn)
        sb.append(" maxRegularSpawn: ")
        sb.append(self.maxRegularSpawn)
        sb.append(" actual monsters: ")
        sb.append(self.getNumMonsters())
        return sb

    def characterSize(self) -> int:
        return self.characters

    def getMapObjectSize(self) -> int:
        return self.mapobjects + self.getCharactersSize() - self.characters

    def getCharactersSize(self) -> int:
        ret = 0
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if not chr.isClone():
                    ret += 1
        finally:
            self.charactersLock.readLock().unlock()
        return ret

    def getPortals(self) -> list:
        return Collections.unmodifiableCollection((Collection<? extends MaplePortal>)self.portals.values())

    def getSpawnedMonstersOnMap(self) -> int:
        return self.spawnedMonstersOnMap.get()

    def spawnLove(self, love: Any) -> None:
        def _task_1():
            MapleMap.self.removeMapObject(love)
            MapleMap.self.broadcastMessage(love.makeDestroyData())

        self.addMapObject(love)
        self.broadcastMessage(love.makeSpawnData())
        final Timer.MapTimer tMan = Timer.MapTimer.getInstance()
        tMan.schedule(_task_1, 3600000)

    def AutoNx(self, dy: int) -> None:
        # Boolean a = Boolean.parseBoolean(System.getProperty("RoyMS.AutoMessage"));
        for chr in self.characters:
            dy = Randomizer.rand(1, 5)
            # chr.modifyCSPoints(2, dy);
            # chr.modifyCSPoints(1, dy);
            chr.gainExp(chr.getLevel() * dy, True, False, True)
            # chr.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "[系统奖励] 随机获得[" + dy + "] 点券奖励!"));
            # chr.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "[系统奖励] 随机获得[" + dy + "] 抵用奖励!"));
            chr.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "[系统奖励] 随机获得[" + chr.getLevel() * dy + "] 经验!"))
            # chr.getClient().getSession().write(MaplePacketCreator.serverNotice(5, "[系统奖励] 随机获得[" + dy + "] 点券 和[" + dy + "] 抵用奖励! 挂机获得[" + chr.getLevel() * dy + "] 经验!"));

    def getCharacterByName(self, id: str) -> Any:
        self.charactersLock.readLock().lock()
        try:
            for mc in self.characters:
                if mc.getName().lower() == id.lower():
                    return mc
        finally:
            self.charactersLock.readLock().unlock()
        return None

    def hideNpc(self, npcid: int) -> None:
        (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().lock()
        try:
            itr = (self.mapobjects.get(MapleMapObjectType.NPC)).values().iterator()
            while itr.hasNext():
                npc = itr.next()
                if npcid == -1 or npc.getId() == npcid:
                    broadcastMessage(MaplePacketCreator.removeNPCController(npc.getObjectId()))
                    broadcastMessage(MaplePacketCreator.removeNPC(npc.getObjectId()))
        finally:
            (self.mapobjectlocks.get(MapleMapObjectType.NPC)).readLock().unlock()

    def respawn(self, force: bool) -> None:
        self.lastSpawnTime = int(time.time() * 1000)
        if force:
            numShouldSpawn = self.monsterSpawn - self.spawnedMonstersOnMap.get()
            if numShouldSpawn > 0:
                spawned = 0
                for spawnPoint in self.monsterSpawn:
                    spawnPoint.spawnMonster(this)
                    if ++spawned >= numShouldSpawn:
                        break
        else:
            numShouldSpawn = self.maxRegularSpawn - self.spawnedMonstersOnMap.get()
            if numShouldSpawn > 0:
                spawned = 0
                randomSpawn = []
                Collections.shuffle(randomSpawn)
                for spawnPoint2 in randomSpawn:
                    if not self.isSpawns and spawnPoint2.getMobTime() > 0:
                        continue
                    if spawnPoint2.shouldSpawn() or GameConstants.isForceRespawn(self.mapid):
                        spawnPoint2.spawnMonster(this)
                        spawned += 1
                    if spawned >= numShouldSpawn:
                        break

    def getMaxRegularSpawn(self) -> int:
        return (int)(self.monsterSpawn / self.monsterRate)

    def getSnowballPortal(self) -> str:
        teamss = new int[2]
        for chr in self.getCharactersThreadsafe():
            if chr.getPosition().y > -80:
                array = teamss
                n = 0
                ++array[n]
            else:
                array2 = teamss
                n2 = 1
                ++array2[n2]
        if teamss[0] > teamss[1]:
            return "st01"
        return "st00"

    def isDisconnected(self, id: int) -> bool:
        return (id in self.dced)

    def addDisconnected(self, id: int) -> None:
        self.dced.add(id)

    def resetDisconnected(self) -> None:
        self.dced.clear()

    def startSpeedRun(self) -> None:
        squad = self.getSquadByMap()
        if squad is not None:
            for chr in self.getCharactersThreadsafe():
                if chr.getName() == (squad.getLeaderName()):
                    self.startSpeedRun(chr.getName())

    def startSpeedRun_leader(self, leader: str) -> None:
        self.speedRunStart = int(time.time() * 1000)
        self.speedRunLeader = leader

    def endSpeedRun(self) -> None:
        self.speedRunStart = 0
        self.speedRunLeader = ""

    def getRankAndAdd(self, leader: str, time: str, type: Any, timz: int, squad: list) -> None:
        try:
            rett = ""
            if squad is not None:
                for chr in squad:
                    rett.append(chr)
                    rett.append(",")
            z = rett
            if squad is not None:
                z = z[0:z.__len__(] - 1)
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("INSERT INTO speedruns(`type`, `leader`, `timestring`, `time`, `members`) VALUES (?,?,?,?,?)")
            ps.setString(1, type.name())
            ps.setString(2, leader)
            ps.setString(3, time)
            ps.setLong(4, timz)
            ps.setString(5, z)
            ps.executeUpdate()
            ps.close()
            if SpeedRunner.getInstance().getSpeedRunData(type) is None:
                SpeedRunner.getInstance().addSpeedRunData(type, SpeedRunner.getInstance().addSpeedRunData("", {}, z, leader, 1, time))
            else:
                SpeedRunner.getInstance().removeSpeedRunData(type)
                SpeedRunner.getInstance().loadSpeedRunData(type)
        except Exception as e:
            e.printStackTrace()

    def getSpeedRunStart(self) -> int:
        return self.speedRunStart

    def disconnectAll(self) -> None:
        for chr in self.getCharactersThreadsafe():
            if not chr.isGM():
                chr.getClient().disconnect(True, False)
                chr.getClient().getSession().close(True)

    def getAllNPCs(self) -> list:
        return self.getAllNPCsThreadsafe()

    def getAllNPCsThreadsafe(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.NPC).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.NPC).values():
                ret.add(mmo)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.NPC).readLock().unlock()
        return ret

    def resetNPCs(self) -> None:
        npcs = self.getAllNPCsThreadsafe()
        for npc in npcs:
            if npc.isCustom():
                self.broadcastMessage(MaplePacketCreator.spawnNPC(npc, False))
                self.removeMapObject(npc)

    def resetFully(self) -> None:
        self.resetFully(True)

    def resetFully_respawn(self, respawn: bool) -> None:
        self.killAllMonsters(False)
        self.reloadReactors()
        self.removeDrops()
        self.resetNPCs()
        self.resetSpawns()
        self.resetDisconnected()
        self.endSpeedRun()
        self.cancelSquadSchedule()
        self.resetPortals()
        self.environment.clear()
        if respawn:
            self.respawn(True)

    def cancelSquadSchedule(self) -> None:
        self.squadTimer = False
        if self.squadSchedule is not None:
            self.squadSchedule.cancel(False)
            self.squadSchedule = None

    def removeDrops(self) -> None:
        items = self.getAllItemsThreadsafe()
        for i in items:
            i.expire(this)

    def removeDropsDelay(self) -> None:
        mapItems = self.getAllItemsThreadsafe()
        delay = 0
        i = 0
        for mapItem in mapItems:
            if ++i < 50:
                mapItem.expire(this)
            else:
                delay += 1
                if mapItem.hasFFA():
                    mapItem.registerFFA(delay * 20)
                else:
                    mapItem.registerExpire(delay * 30)

    def resetAllSpawnPoint(self, mobid: int, mobTime: int) -> None:
        sss = []
        self.resetFully()
        self.monsterSpawn.clear()
        for s in sss:
            newMons = MapleLifeFactory.getMonster(mobid)
            oldMons = s.getMonster()
            newMons.setCy(oldMons.getCy())
            newMons.setF(oldMons.getF())
            newMons.setFh(oldMons.getFh())
            newMons.setRx0(oldMons.getRx0())
            newMons.setRx1(oldMons.getRx1())
            newMons.setPosition(Point(oldMons.getPosition()))
            newMons.setHide(oldMons.isHidden())
            self.addMonsterSpawn(newMons, mobTime, (byte)(-1), None)
        self.loadMonsterRate(True)

    def resetSpawns(self) -> None:
        changed = False
        sss = self.monsterSpawn.iterator()
        while sss.hasNext():
            if sss.next().getCarnivalId() > -1:
                sss.remove()
                changed = True
        self.setSpawns(True)
        if changed:
            self.loadMonsterRate(True)

    def makeCarnivalSpawn(self, team: int, newMons: Any, num: int) -> bool:
        MapleNodes.MonsterPoint ret = None
        for (MapleNodes.MonsterPoint mp : self.nodes.getMonsterPoints())
            if mp.team == team or mp.team == -1:
                newpos = calcPointBelow(Point(mp.x, mp.y))
                newpos.y -= 1
                found = False
                for s in self.monsterSpawn:
                    if s.getCarnivalId() > -1 and (mp.team == -1 or s.getCarnivalTeam() == mp.team) and (s.getPosition()).x == newpos.x and (s.getPosition()).y == newpos.y:
                        found = True
                        break
                if not found:
                    ret = mp
                    break
                if not found:
                    ret = mp
                    break
        if ret is not None:
            newMons.setCy(ret.cy)
            newMons.setF(0)
            newMons.setFh(ret.fh)
            newMons.setRx0(ret.x + 50)
            newMons.setRx1(ret.x - 50)
            newMons.setPosition(Point(ret.x, ret.y))
            newMons.setHide(False)
            sp = addMonsterSpawn(newMons, 1, team, None)
            sp.setCarnival(num)
        return (ret is not None)

    def makeCarnivalReactor(self, team: int, num: int) -> bool:
        old = self.getReactorByName(team + "" + num)
        if old is not None and old.getState() < 5:
            return False
        guardz = None
        react = self.getAllReactorsThreadsafe()
        for guard in self.nodes.getGuardians():
            if guard.right == team or guard.right == -1:
                found = False
                for r in react:
                    if r.getPosition().x == guard.left.x and r.getPosition().y == guard.left.y and r.getState() < 5:
                        found = True
                        break
                if not found:
                    guardz = guard.left
                    break
                continue
        if guardz is not None:
            stats = MapleReactorFactory.getReactor(9980000 + team)
            my = MapleReactor(stats, 9980000 + team)
            stats.setFacingDirection(0)
            my.setPosition(guardz)
            my.setState(1)
            my.setDelay(0)
            my.setName(team + "" + num)
            self.spawnReactor(my)
            final MapleCarnivalFactory.MCSkill skil = MapleCarnivalFactory.getInstance().getGuardian(num)
            for mons in self.getAllMonstersThreadsafe():
                if mons.getCarnivalTeam() == team:
                    skil.getSkill().applyEffect(None, mons, False)
        return guardz is not None

    def blockAllPortal(self) -> None:
        for p in self.portals.values():
            p.setPortalState(False)

    def getAndSwitchTeam(self) -> bool:
        return self.getCharactersSize() % 2 != 0

    def setSquad(self, s: Any) -> None:
        self.squad = s

    def getChannel(self) -> int:
        return self.channel

    def getConsumeItemCoolTime(self) -> int:
        return self.consumeItemCoolTime

    def setConsumeItemCoolTime(self, ciit: int) -> None:
        self.consumeItemCoolTime = ciit

    def setPermanentWeather(self, pw: int) -> None:
        self.permanentWeather = pw

    def getPermanentWeather(self) -> int:
        return self.permanentWeather

    def checkStates(self, chr: str) -> None:
        sqd = self.getSquadByMap()
        em = self.getEMByMap()
        size = self.getCharactersSize()
        if sqd is not None:
            sqd.removeMember(chr)
            if em is not None:
                if sqd.getLeaderName() == (chr):
                    em.setProperty("leader", "False")
                if chr == ("") or size == 0:
                    sqd.clear()
                    em.setProperty("state", "0")
                    em.setProperty("leader", "True")
                    self.cancelSquadSchedule()
        if em is not None and em.getProperty("state") is not None and size == 0:
            em.setProperty("state", "0")
            if em.getProperty("leader") is not None:
                em.setProperty("leader", "True")
        if self.speedRunStart > 0 and self.speedRunLeader.lower() == chr.lower():
            if size > 0:
                self.broadcastMessage(MaplePacketCreator.serverNotice(5, "队长不在地图上！你的挑战失败"))
            self.endSpeedRun()

    def setNodes(self, mn: Any) -> None:
        self.nodes = mn

    def getPlatforms(self) -> list:
        return self.nodes.getPlatforms()

    def getNodes(self) -> list:
        return self.nodes.getNodes()

    def getNode(self, index: int) -> Any:
        return self.nodes.getNode(index)

    def getAreas(self) -> list:
        return self.nodes.getAreas()

    def getArea(self, index: int) -> Any:
        return self.nodes.getArea(index)

    def changeEnvironment(self, ms: str, type: int) -> None:
        self.broadcastMessage(MaplePacketCreator.environmentChange(ms, type))

    def getEnvironment(self) -> dict:
        return self.environment

    def getNumPlayersInArea(self, index: int) -> int:
        ret = 0
        self.charactersLock.readLock().lock()
        try:
            ltr = self.characters.iterator()
            while ltr.hasNext():
                if self.getArea(index).__contains__(ltr.next().getPosition()):
                    ret += 1
        finally:
            self.charactersLock.readLock().unlock()
        return ret

    def broadcastGMMessage(self, source: Any, packet: Any, repeatToSource: bool) -> None:
        self.broadcastGMMessage(repeatToSource ? None : source, packet, Double.POSITIVE_INFINITY, source.getPosition())

    def broadcastGMMessage_source_packet_rangeSq_rangedFrom(self, source: Any, packet: Any, rangeSq: float, rangedFrom: Any) -> None:
        self.charactersLock.readLock().lock()
        try:
            if source is None:
                for chr in self.characters:
                    if chr.isStaff():
                        chr.getClient().getSession().write(packet)
            else:
                for chr in self.characters:
                    if chr != source and chr.getGMLevel() >= source.getGMLevel():
                        chr.getClient().getSession().write(packet)
        finally:
            self.charactersLock.readLock().unlock()

    def getMobsToSpawn(self) -> list:
        return self.nodes.getMobsToSpawn()

    def getSkillIds(self) -> list:
        return self.nodes.getSkillIds()

    def canHurt(self) -> bool:
        if self.lastHurtTime > 0 and self.lastHurtTime + self.decHPInterval < int(time.time() * 1000):
            self.lastHurtTime = int(time.time() * 1000)
            return True
        return False

    def getAllUniqueMonsters(self) -> list:
        ret = []
        self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.MONSTER).values():
                theId = (mmo).getId()
                if not (theId in ret):
                    ret.add(theId)
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.MONSTER).readLock().unlock()
        return (List<Integer>)ret

    def getNumPlayersItemsInArea(self, index: int) -> int:
        return self.getNumPlayersItemsInRect(self.getArea(index))

    def getNumPlayersItemsInRect(self, rect: Any) -> int:
        ret = self.getNumPlayersInRect(rect)
        self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().lock()
        try:
            for mmo in self.mapobjects.get(MapleMapObjectType.ITEM).values():
                if (mmo.getPosition( in rect)):
                    ret += 1
        finally:
            self.mapobjectlocks.get(MapleMapObjectType.ITEM).readLock().unlock()
        return ret

    def getNumPlayersInRect(self, rect: Any) -> int:
        ret = 0
        self.charactersLock.readLock().lock()
        try:
            for mmo in (self.mapobjects.get(MapleMapObjectType.ITEM)).values():
                if (mmo.getPosition( in rect)):
                ret += 1
        finally:
            self.charactersLock.readLock().unlock()
        return ret

    def hasBoat(self) -> int:
        if self.boat and self.docked:
            return 2
        if self.boat:
            return 1
        return 0

    def setBoat(self, hasBoat: bool) -> None:
        self.boat = hasBoat

    def setDocked(self, isDocked: bool) -> None:
        self.docked = isDocked

    def spawnRabbit(self, hp: int) -> None:
        hp = 100000
        mid = 9300061
        onemob = MapleLifeFactory.getMonster(mid)
        overrideStats = OverrideMonsterStats(hp, onemob.getMobMaxMp(), 0, False)
        mob = MapleLifeFactory.getMonster(mid)
        mob.setHp(hp)
        mob.setOverrideStats(overrideStats)
        self.spawnMonsterOnGroundBelow(mob, Point(-183, -433))

    def KillFk(self, animate: bool) -> None:
        monsters = self.getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.MONSTER))
        for monstermo in monsters:
            monster = monstermo
            if monster.getId() == 3230300 or monster.getId() == 3230301:
                self.spawnedMonstersOnMap.decrementAndGet()
                monster.setHp(0)
                self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), (int)(animate ? 1 : 0)))
                self.removeMapObject(monster)
                monster.killed()

    def mobCount(self) -> int:
        mobsCount = self.getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.MONSTER))
        return mobsCount

    def playerCount(self) -> int:
        players = self.getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.PLAYER))
        return players

    def killMonster_2(self, monster: Any) -> None:
        if monster is None:
            return
        self.spawnedMonstersOnMap.decrementAndGet()
        monster.setHp(0)
        self.broadcastMessage(MobPacket.killMonster(monster.getObjectId(), (monster.getStats().getSelfD() < 0) ? 1 : monster.getStats().getSelfD()))
        self.removeMapObject(monster)
        monster.killed()

    def reloadCPQ(self) -> None:
        maps = { 980000101, 980000201, 980000301, 980000401, 980000501, 980000601 }
        for i in range(len(maps)):
            mapid = maps[i]
            for cserv in ChannelServer.getAllInstances():
                cserv.getMapFactory().destroyMap(mapid, True)
                cserv.getMapFactory().HealMap(mapid)

    def getCharactersIntersect(self, box: Any) -> list:
        ret = []
        self.charactersLock.readLock().lock()
        try:
            for chr in self.characters:
                if chr.getBounds().intersects(box):
                    ret.add(chr)
        finally:
            self.charactersLock.readLock().unlock()
        return (List<MapleCharacter>)ret

    def isPvpMap(self) -> bool:
        个人PK地图 = LoginServer.个人PK地图()
        return self.mapid == 个人PK地图

    def isPartyPvpMap(self) -> bool:
        组队PK地图 = LoginServer.组队PK地图()
        return self.mapid == 组队PK地图

    def isGuildPvpMap(self) -> bool:
        家族PK地图 = LoginServer.家族PK地图()
        return self.mapid == 家族PK地图

    def isBossMap(self) -> bool:
        # switch (self.mapid):
            # case 105100300:
            # case 105100400:
            # case 211070100:
            # case 211070101:
            # case 211070110:
            # case 220080001:
            # case 240040700:
            # case 240060200:
            # case 240060201:
            # case 262031300:
            # case 262031310:
            # case 270050100:
            # case 271040100:
            # case 271040200:
            # case 272030400:
            # case 272030420:
            # case 280030000:
            # case 280030001:
            # case 280030100:
            # case 300030310:
            # case 551030200:
            # case 802000111:
            # case 802000211:
            # case 802000311:
            # case 802000411:
            # case 802000611:
            # case 802000711:
            # case 802000801:
            # case 802000802:
            # case 802000803:
            # case 802000821:
            # case 802000823:
                return True
            # default:
                return False


# Inner class from Java (originally nested)
class ActivateItemReactor(Runnable):
    """
    Class ActivateItemReactor
    Implements: Runnable
    """

    pass


# Inner class from Java (originally nested)
from abc import ABC, abstractmethod

class SpawnCondition(ABC):
    """Interface SpawnCondition"""

    @abstractmethod
    def Runnable(self) -> Any:
        pass

    @abstractmethod
    def run(self) -> Any:
        pass


# Inner class from Java (originally nested)
from abc import ABC, abstractmethod

class DelayedPacketCreation(ABC):
    """Interface DelayedPacketCreation"""

    @abstractmethod
    def run(self) -> Any:
        pass

