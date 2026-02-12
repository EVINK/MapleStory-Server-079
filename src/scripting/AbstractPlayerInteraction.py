"""
AbstractPlayerInteraction - Converted from Java source
Original: scripting/AbstractPlayerInteraction.java
Package: scripting
"""

from datetime import datetime
from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Iterator
from typing import List
from typing import Optional, Any
import math
import pymysql
import threading
import time

# Internal module imports
# from KinMS.db.CherryMSLottery import *  # TODO: import specific classes
# from KinMS.db.CherryMScustomEventFactory import *  # TODO: import specific classes
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventory import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from handling.world.guild.MapleGuild import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.custom.auction.AuctionItem import *  # TODO: import specific classes
# from server.custom.auction.AuctionManager import *  # TODO: import specific classes
# from server.custom.auction.AuctionPoint import *  # TODO: import specific classes
# from server.custom.bossrank.BossRankInfo import *  # TODO: import specific classes
# from server.custom.bossrank.BossRankManager import *  # TODO: import specific classes
# from server.events.MapleEvent import *  # TODO: import specific classes
# from server.events.MapleEventType import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.OverrideMonsterStats import *  # TODO: import specific classes
# from server.maps.Event_DojoAgent import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleReactor import *  # TODO: import specific classes
# from server.maps.SavedLocationType import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.PetPacket import *  # TODO: import specific classes
# from tools.packet.UIPacket import *  # TODO: import specific classes


class AbstractPlayerInteraction:
    """
    Class AbstractPlayerInteraction
    """

    def __init__(self, c: Any):
        self.c = None
        self.c = c


    def getClient(self) -> Any:
        return self.c

    def getC(self) -> Any:
        return self.c

    def getChar(self) -> Any:
        self.c.getPlayer().getInventory(MapleInventoryType.USE).listById(1).iterator()
        return self.c.getPlayer()

    def getChannelServer(self) -> Any:
        return self.c.getChannelServer()

    def getPlayer(self) -> Any:
        return self.c.getPlayer()

    def getMap(self) -> Any:
        return self.c.getPlayer().getMap()

    def getEventManager(self, event: str) -> Any:
        return self.c.getChannelServer().getEventSM().getEventManager(event)

    def getEventInstance(self) -> Any:
        return self.c.getPlayer().getEventInstance()

    def forceRemovePlayerByCharName(self, name: str) -> None:
        ChannelServer.forceRemovePlayerByCharName(name)

    def warp(self, map: int) -> None:
        mapz = self.getWarpMap(map)
        try:
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(Randomizer.nextInt(mapz.getPortals())))
        except Exception as e:
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(0))

    def warpPlayer(self, map: int, map2: int) -> None:
        if self.c.getPlayer().getMapId() == map:
            mapz = self.getWarpMap(map2)
            try:
                self.c.getPlayer().changeMap(mapz, mapz.getPortal(Randomizer.nextInt(mapz.getPortals())))
            except Exception as e:
                self.c.getPlayer().changeMap(mapz, mapz.getPortal(0))
        else:
            self.c.getPlayer().dropMessage(5, "NPC传送地图函数不匹配！")

    def warp_Instanced(self, map: int) -> None:
        mapz = self.getMap_Instanced(map)
        try:
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(Randomizer.nextInt(mapz.getPortals())))
        except Exception as e:
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(0))

    def warp_map_portal(self, map: int, portal: int) -> None:
        mapz = self.getWarpMap(map)
        if portal != 0 && map == self.c.getPlayer().getMapId():
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(portal))
        else:
            self.c.getPlayer().changeMap(mapz, mapz.getPortal(portal))

    def warpS(self, map: int, portal: int) -> None:
        mapz = self.getWarpMap(map)
        self.c.getPlayer().changeMap(mapz, mapz.getPortal(portal))

    def warpS_map_portal(self, map: int, portal: str) -> None:
        mapz = self.getWarpMap(map)
        if map == 109060000 || map == 109060002 || map == 109060004:
            portal = mapz.getSnowballPortal()
        self.c.getPlayer().changeMap(mapz, mapz.getPortal(portal))

    def warpMap(self, mapid: int, portal: int) -> None:
        map = self.getMap(mapid)
        for chr in self.c.getPlayer().getMap().getCharactersThreadsafe():
            chr.changeMap(map, map.getPortal(portal))

    def playPortalSE(self) -> None:
        self.c.getSession().write(MaplePacketCreator.showOwnBuffEffect(0, 5))

    def getWarpMap(self, map: int) -> Any:
        return ChannelServer.getInstance(self.c.getChannel()).getMapFactory().getMap(map)

    def getMap_map(self, map: int) -> Any:
        return self.getWarpMap(map)

    def getMap_Instanced(self, map: int) -> Any:
        return (self.c.getPlayer().getEventInstance() is None) ? self.getMap(map) : self.c.getPlayer().getEventInstance().getMapInstance(map)

    def spawnMap(self, MapID: int, MapID2: int) -> None:
        for chan in ChannelServer.getAllInstances():
            for chr in chan.getPlayerStorage().getAllCharacters():
                if chr is None:
                    continue
                if self.getC().getChannel() != chr.getClient().getChannel() || chr.getMapId() != MapID:
                    continue
                self.warp(MapID2)

    def spawnMap_MapID(self, MapID: int) -> None:
        for chan in ChannelServer.getAllInstances():
            for chr in chan.getPlayerStorage().getAllCharacters():
                if chr is None:
                    continue
                if self.getC().getChannel() != chr.getClient().getChannel() || chr.getMapId() != self.getMapId():
                    continue
                self.warp(MapID)

    def spawnMobLevel(self, mobId: int, level: int) -> None:
        self.spawnMobLevel(mobId, 1, level, self.c.getPlayer().getTruePosition())

    def spawnMobLevel_mobId_quantity_level(self, mobId: int, quantity: int, level: int) -> None:
        self.spawnMobLevel(mobId, quantity, level, self.c.getPlayer().getTruePosition())

    def spawnMobLevel_mobId_quantity_level_x_y(self, mobId: int, quantity: int, level: int, x: int, y: int) -> None:
        self.spawnMobLevel(mobId, quantity, level, Point(x, y))

    def spawnMobLevel_mobId_quantity_level_pos(self, mobId: int, quantity: int, level: int, pos: Any) -> None:
        for i in range(quantity):
            mob = MapleLifeFactory.getMonster(mobId)
            if mob is None || !mob.getStats().isChangeable():
                if self.c.getPlayer().isAdmin():
                    self.c.getPlayer().dropMessage(6, "[系统提示] spawnMobLevel召唤怪物出错，ID为: " + mobId + " 怪物不存在或者该怪物无法使用这个函数来改变怪物的属性！")
            else:
                mob.changeLevel(level, False)
                self.c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, pos)

    def spawnMobStats(self, mobId: int, newhp: int, newExp: int) -> None:
        self.spawnMobStats(mobId, 1, newhp, newExp, self.c.getPlayer().getTruePosition())

    def spawnMobStats_mobId_quantity_newhp_newExp(self, mobId: int, quantity: int, newhp: int, newExp: int) -> None:
        self.spawnMobStats(mobId, quantity, newhp, newExp, self.c.getPlayer().getTruePosition())

    def spawnMobStats_mobId_quantity_newhp_newExp_x_y(self, mobId: int, quantity: int, newhp: int, newExp: int, x: int, y: int) -> None:
        self.spawnMobStats(mobId, quantity, newhp, newExp, Point(x, y))

    def spawnMobStats_mobId_quantity_newhp_newExp_pos(self, mobId: int, quantity: int, newhp: int, newExp: int, pos: Any) -> None:
        for i in range(quantity):
            mob = MapleLifeFactory.getMonster(mobId)
            if mob is None:
                if self.c.getPlayer().isAdmin():
                    self.c.getPlayer().dropMessage(6, "[系统提示] spawnMobStats召唤怪物出错，ID为: " + mobId + " 怪物不存在！")
            else:
                overrideStats = OverrideMonsterStats(newhp, mob.getMobMaxMp(), (newExp <= 0) ? mob.getMobExp() : newExp, False)
                mob.setOverrideStats(overrideStats)
                self.c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, pos)

    def spawnMobMultipler(self, mobId: int, multipler: int) -> None:
        self.spawnMobMultipler(mobId, 1, multipler, self.c.getPlayer().getTruePosition())

    def spawnMobMultipler_mobId_quantity_multipler(self, mobId: int, quantity: int, multipler: int) -> None:
        self.spawnMobMultipler(mobId, quantity, multipler, self.c.getPlayer().getTruePosition())

    def spawnMobMultipler_mobId_quantity_multipler_x_y(self, mobId: int, quantity: int, multipler: int, x: int, y: int) -> None:
        self.spawnMobMultipler(mobId, quantity, multipler, Point(x, y))

    def spawnMobMultipler_mobId_quantity_multipler_pos(self, mobId: int, quantity: int, multipler: int, pos: Any) -> None:
        for i in range(quantity):
            mob = MapleLifeFactory.getMonster(mobId)
            if mob is None:
                if self.c.getPlayer().isAdmin():
                    self.c.getPlayer().dropMessage(6, "[系统提示] spawnMobMultipler召唤怪物出错，ID为: " + mobId + " 怪物不存在！")
            else:
                overrideStats = OverrideMonsterStats(mob.getMobMaxHp() * multipler, mob.getMobMaxMp() * multipler, mob.getMobExp() + multipler * 100, False)
                mob.setOverrideStats(overrideStats)
                self.c.getPlayer().getMap().spawnMonsterOnGroundBelow(mob, pos)

    def spawnMonster(self, id: int, qty: int) -> None:
        self.spawnMob(id, qty, Point(self.c.getPlayer().getPosition()))

    def spawnMobOnMap(self, id: int, qty: int, x: int, y: int, map: int) -> None:
        for i in range(qty):
            self.getMap(map).spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), Point(x, y))

    def spawnMobOnMap_id_qty_x_y_map_hp(self, id: int, qty: int, x: int, y: int, map: int, hp: int) -> None:
        for i in range(qty):
            self.getMap(map).spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), Point(x, y), hp)

    def spawnMob(self, id: int, qty: int, x: int, y: int) -> None:
        self.spawnMob(id, qty, Point(x, y))

    def spawnMob_map(self, id: int, mapid: int, x: int, y: int) -> None:
        self.spawnMob_map(id, mapid, Point(x, y))

    def spawnMob_map_id_mapid_pos(self, id: int, mapid: int, pos: Any) -> None:
        self.c.getChannelServer().getMapFactory().getMap(mapid).spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), pos)

    def spawnMob_id_x_y(self, id: int, x: int, y: int) -> None:
        self.spawnMob(id, 1, Point(x, y))

    def spawnMob_id_qty_pos(self, id: int, qty: int, pos: Any) -> None:
        for i in range(qty):
            self.c.getPlayer().getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), pos)

    def killMob(self, ids: int) -> None:
        self.c.getPlayer().getMap().killMonster(ids)

    def killAllMob(self) -> None:
        self.c.getPlayer().getMap().killAllMonsters(True)

    def addHP(self, delta: int) -> None:
        self.c.getPlayer().addHP(delta)

    def setPlayerStat(self, type: str, x: int) -> None:
        # switch (type):
            # case "LVL":
                self.c.getPlayer().setLevel(x)
                break
            # case "STR":
                self.c.getPlayer().getStat().setStr(x)
                break
            # case "DEX":
                self.c.getPlayer().getStat().setDex(x)
                break
            # case "INT":
                self.c.getPlayer().getStat().setInt(x)
                break
            # case "LUK":
                self.c.getPlayer().getStat().setLuk(x)
                break
            # case "HP":
                self.c.getPlayer().getStat().setHp(x)
                break
            # case "MP":
                self.c.getPlayer().getStat().setMp(x)
                break
            # case "MAXHP":
                self.c.getPlayer().getStat().setMaxHp(x)
                break
            # case "MAXMP":
                self.c.getPlayer().getStat().setMaxMp(x)
                break
            # case "RAP":
                self.c.getPlayer().setRemainingAp(x)
                break
            # case "RSP":
                self.c.getPlayer().setRemainingSp(x)
                break
            # case "GID":
                self.c.getPlayer().setGuildId(x)
                break
            # case "GRANK":
                self.c.getPlayer().setGuildRank(x)
                break
            # case "ARANK":
                self.c.getPlayer().setAllianceRank(x)
                break
            # case "GENDER":
                self.c.getPlayer().setGender(x)
                break
            # case "FACE":
                self.c.getPlayer().setFace(x)
                break
            # case "HAIR":
                self.c.getPlayer().setHair(x)
                break

    def getPlayerStat(self, type: str) -> int:
        # switch (type):
            # case "LVL":
                return self.c.getPlayer().getLevel()
            # case "STR":
                return self.c.getPlayer().getStat().getStr()
            # case "DEX":
                return self.c.getPlayer().getStat().getDex()
            # case "INT":
                return self.c.getPlayer().getStat().getInt()
            # case "LUK":
                return self.c.getPlayer().getStat().getLuk()
            # case "HP":
                return self.c.getPlayer().getStat().getHp()
            # case "MP":
                return self.c.getPlayer().getStat().getMp()
            # case "MAXHP":
                return self.c.getPlayer().getStat().getMaxHp()
            # case "MAXMP":
                return self.c.getPlayer().getStat().getMaxMp()
            # case "RAP":
                return self.c.getPlayer().getRemainingAp()
            # case "RSP":
                return self.c.getPlayer().getRemainingSp()
            # case "GID":
                return self.c.getPlayer().getGuildId()
            # case "GRANK":
                return self.c.getPlayer().getGuildRank()
            # case "ARANK":
                return self.c.getPlayer().getAllianceRank()
            # case "GM":
                return self.c.getPlayer().isGM() ? 1 : 0
            # case "ADMIN":
                return self.c.getPlayer().isAdmin() ? 1 : 0
            # case "GENDER":
                return self.c.getPlayer().getGender()
            # case "FACE":
                return self.c.getPlayer().getFace()
            # case "HAIR":
                return self.c.getPlayer().getHair()
            # default:
                return -1

    def getName(self) -> str:
        return self.c.getPlayer().getName()

    def haveItem(self, itemid: int) -> bool:
        return self.haveItem(itemid, 1)

    def haveItem_itemid_quantity(self, itemid: int, quantity: int) -> bool:
        return self.haveItem(itemid, quantity, False, True)

    def haveItem_itemid_quantity_checkEquipped_greaterOrEquals(self, itemid: int, quantity: int, checkEquipped: bool, greaterOrEquals: bool) -> bool:
        return self.c.getPlayer().haveItem(itemid, quantity, checkEquipped, greaterOrEquals)

    def canHold(self) -> bool:
        for i in range(1, = 5):
            if self.c.getPlayer().getInventory(MapleInventoryType.getByType(i)).getNextFreeSlot() <= -1:
                return False
        return True

    def canHold_itemid(self, itemid: int) -> bool:
        return self.c.getPlayer().getInventory(GameConstants.getInventoryType(itemid)).getNextFreeSlot() > -1

    def canHold_itemid_quantity(self, itemid: int, quantity: int) -> bool:
        return MapleInventoryManipulator.checkSpace(self.c, itemid, quantity, "")

    def getQuestRecord(self, id: int) -> Any:
        return self.c.getPlayer().getQuestNAdd(MapleQuest.getInstance(id))

    def getQuestStatus(self, id: int) -> int:
        return self.c.getPlayer().getQuestStatus(id)

    def completeQuest(self, id: int) -> None:
        self.c.getPlayer().setQuestAdd(id)

    def isQuestActive(self, id: int) -> bool:
        return self.getQuestStatus(id) == 1

    def isQuestFinished(self, id: int) -> bool:
        return self.getQuestStatus(id) == 2

    def showQuestMsg(self, msg: str) -> None:
        self.c.getSession().write(MaplePacketCreator.showQuestMsg(msg))

    def forceStartQuest(self, id: int, data: str) -> None:
        MapleQuest.getInstance(id).forceStart(self.c.getPlayer(), 0, data)

    def forceStartQuest_id_data_filler(self, id: int, data: int, filler: bool) -> None:
        MapleQuest.getInstance(id).forceStart(self.c.getPlayer(), 0, filler ? str(data) : None)

    def clearAranPolearm(self) -> None:
        self.c.getPlayer().getInventory(MapleInventoryType.EQUIPPED).removeItem((short)(-11))

    def forceStartQuest_id(self, id: int) -> None:
        MapleQuest.getInstance(id).forceStart(self.c.getPlayer(), 0, None)

    def forceCompleteQuest(self, id: int) -> None:
        MapleQuest.getInstance(id).forceComplete(self.getPlayer(), 0)

    def spawnNpc(self, npcId: int) -> None:
        self.c.getPlayer().getMap().spawnNpc(npcId, self.c.getPlayer().getPosition())

    def spawnNpc_npcId_x_y(self, npcId: int, x: int, y: int) -> None:
        self.c.getPlayer().getMap().spawnNpc(npcId, Point(x, y))

    def spawnNpc_npcId_pos(self, npcId: int, pos: Any) -> None:
        self.c.getPlayer().getMap().spawnNpc(npcId, pos)

    def removeNpc(self, mapid: int, npcId: int) -> None:
        self.c.getChannelServer().getMapFactory().getMap(mapid).removeNpc(npcId)

    def forceStartReactor(self, mapid: int, id: int) -> None:
        map = self.c.getChannelServer().getMapFactory().getMap(mapid)
        for remo in map.getAllReactorsThreadsafe():
            react = remo
            if react.getReactorId() == id:
                react.forceStartReactor(self.c)
                break

    def destroyReactor(self, mapid: int, id: int) -> None:
        map = self.c.getChannelServer().getMapFactory().getMap(mapid)
        for remo in map.getAllReactorsThreadsafe():
            react = remo
            if react.getReactorId() == id:
                react.hitReactor(self.c)
                break

    def hitReactor(self, mapid: int, id: int) -> None:
        map = self.c.getChannelServer().getMapFactory().getMap(mapid)
        for remo in map.getAllReactorsThreadsafe():
            react = remo
            if react.getReactorId() == id:
                react.hitReactor(self.c)
                break

    def getJob(self) -> int:
        return self.c.getPlayer().getJob()

    def getNX(self, 类型: int) -> int:
        return self.c.getPlayer().getCSPoints(类型)

    def gainD(self, amount: int) -> None:
        self.c.getPlayer().modifyCSPoints(2, amount, True)

    def gainNX(self, amount: int) -> None:
        self.c.getPlayer().modifyCSPoints(1, amount, True)

    def gainItemPeriod(self, id: int, quantity: int, period: int) -> None:
        self.gainItem(id, quantity, False, period, -1, "", 0)

    def gainItemPeriod_id_quantity_period_owner(self, id: int, quantity: int, period: int, owner: str) -> None:
        self.gainItem(id, quantity, False, period, -1, owner, 0)

    def gainItem(self, id: int, quantity: int) -> None:
        self.gainItem(id, quantity, False, 0, -1, "", 0)

    def gainItem_id_quantity_period_Flag(self, id: int, quantity: int, period: int, Flag: int) -> None:
        self.gainItem(id, quantity, False, period, -1, "", Flag)

    def gainItem_id_quantity_randomStats(self, id: int, quantity: int, randomStats: bool) -> None:
        self.gainItem(id, quantity, randomStats, 0, -1, "", 0)

    def gainItem_id_quantity_randomStats_slots(self, id: int, quantity: int, randomStats: bool, slots: int) -> None:
        self.gainItem(id, quantity, randomStats, 0, slots, "", 0)

    def gainItem_id_quantity_period(self, id: int, quantity: int, period: int) -> None:
        self.gainItem(id, quantity, False, period, -1, "", 0)

    def gainItem_id_quantity_randomStats_period_slots(self, id: int, quantity: int, randomStats: bool, period: int, slots: int) -> None:
        self.gainItem(id, quantity, randomStats, period, slots, "", 0)

    def gainItem_id_quantity_randomStats_period_slots_owner_Flag(self, id: int, quantity: int, randomStats: bool, period: int, slots: int, owner: str, Flag: int) -> None:
        self.gainItem(id, quantity, randomStats, period, slots, owner, self.c, Flag)

    def gainItem_id_quantity_randomStats_period_slots_owner_cg_Flag(self, id: int, quantity: int, randomStats: bool, period: int, slots: int, owner: str, cg: Any, Flag: int) -> None:
        if quantity >= 0:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(id)
            if !MapleInventoryManipulator.checkSpace(cg, id, quantity, ""):
                return
            if type == (MapleInventoryType.EQUIP) && !GameConstants.is飞镖道具(id) && !GameConstants.is子弹道具(id):
                item = (Equip)(randomStats ? ii.randomizeStats(ii.getEquipById(id)) : ii.getEquipById(id))
                if period > 0:
                    item.setExpiration(int(time.time() * 1000) + period * 60 * 60 * 1000)
                if slots > 0:
                    item.setUpgradeSlots((byte)(item.getUpgradeSlots() + slots))
                if owner is not None:
                    item.setOwner(owner)
                name = ii.getName(id)
                if id / 10000 == 114 && name is not None && name > 0:
                    msg = "你已获得称号 <" + name + ">"
                    cg.getPlayer().dropMessage(5, msg)
                    cg.getPlayer().dropMessage(5, msg)
                MapleInventoryManipulator.addbyItem(cg, item.copy())
            else:
                MapleInventoryManipulator.addById(cg, id, quantity, (owner is None) ? "" : owner, None, period, Flag)
        else:
            MapleInventoryManipulator.removeById(cg, GameConstants.getInventoryType(id), id, -quantity, True, False)
        cg.getSession().write(MaplePacketCreator.getShowItemGain(id, quantity, True))

    def gainItem_id_str_dex_luk_Int_watk_matk(self, id: int, str: int, dex: int, luk: int, Int: int, watk: int, matk: int) -> None:
        self.gainItem(id, str, dex, luk, Int, 0, 0, watk, matk, 0, 0, 0, 0, 0, 0)

    def gainItem_id_str_dex_luk_Int_hp_mp_watk_matk_wdef_mdef_hb_mz_ty_yd(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int) -> None:
        self.gainItemS(id, str, dex, luk, Int, hp, mp, watk, matk, wdef, mdef, hb, mz, ty, yd, self.c, 0)

    def gainItem_id_str_dex_luk_Int_hp_mp_watk_matk_wdef_mdef_hb_mz_ty_yd_time(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int, time: int) -> None:
        self.gainItemS(id, str, dex, luk, Int, hp, mp, watk, matk, wdef, mdef, hb, mz, ty, yd, self.c, time)

    def gainItemS(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int, cg: Any, time: int) -> None:
        ii = MapleItemInformationProvider.getInstance()
        type = GameConstants.getInventoryType(id)
        if !MapleInventoryManipulator.checkSpace(cg, id, 1, ""):
            return
        if type == (MapleInventoryType.EQUIP) && !GameConstants.isThrowingStar(id) && !GameConstants.isBullet(id):
            item = ii.getEquipById(id)
            name = ii.getName(id)
            if id / 10000 == 114 && name is not None && name > 0:
                msg = "你已获得称号 <" + name + ">"
                cg.getPlayer().dropMessage(5, msg)
                cg.getPlayer().dropMessage(5, msg)
            if time > 0:
                item.setExpiration(int(time.time() * 1000) + time * 60 * 60 * 1000)
            if str > 0:
                item.setStr(str)
            if dex > 0:
                item.setDex(dex)
            if luk > 0:
                item.setLuk(luk)
            if Int > 0:
                item.setInt(Int)
            if hp > 0:
                item.setHp(hp)
            if mp > 0:
                item.setMp(mp)
            if watk > 0:
                item.setWatk(watk)
            if matk > 0:
                item.setMatk(matk)
            if wdef > 0:
                item.setWdef(wdef)
            if mdef > 0:
                item.setMdef(mdef)
            if hb > 0:
                item.setAvoid(hb)
            if mz > 0:
                item.setAcc(mz)
            if ty > 0:
                item.setJump(ty)
            if yd > 0:
                item.setSpeed(yd)
            MapleInventoryManipulator.addbyItem(cg, item.copy())
        else:
            MapleInventoryManipulator.addById(cg, id, 1, "", 0)
        cg.getSession().write(MaplePacketCreator.getShowItemGain(id, 1, True))

    def gainItem_id_str_dex_luk_Int_watk_matk_suo(self, id: int, str: int, dex: int, luk: int, Int: int, watk: int, matk: int, suo: int) -> None:
        self.给予道具(id, str, dex, luk, Int, 0, 0, watk, matk, 0, 0, 0, 0, 0, 0, self.c, 0, 0, 0, 0, suo)

    def translated_给予道具(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int, ksjcs: int, ysjcs: int, jcz: int, suo: int) -> None:
        self.给予道具(id, str, dex, luk, Int, hp, mp, watk, matk, wdef, mdef, hb, mz, ty, yd, self.c, 0, ksjcs, ysjcs, jcz, suo)

    def translated_给予道具_id_str_dex_luk_Int_hp_mp_watk_matk_wdef_mdef_hb_mz_ty_yd_time_ksjcs_ysjcs_jcz_suo(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int, time: int, ksjcs: int, ysjcs: int, jcz: int, suo: int) -> None:
        self.给予道具(id, str, dex, luk, Int, hp, mp, watk, matk, wdef, mdef, hb, mz, ty, yd, self.c, time, ksjcs, ysjcs, jcz, suo)

    def translated_给予道具_id_str_dex_luk_Int_hp_mp_watk_matk_wdef_mdef_hb_mz_ty_yd_cg_time_ksjcs_ysjcs_jcz_suo(self, id: int, str: int, dex: int, luk: int, Int: int, hp: int, mp: int, watk: int, matk: int, wdef: int, mdef: int, hb: int, mz: int, ty: int, yd: int, cg: Any, time: int, ksjcs: int, ysjcs: int, jcz: int, suo: int) -> None:
        ii = MapleItemInformationProvider.getInstance()
        type = GameConstants.getInventoryType(id)
        if !MapleInventoryManipulator.checkSpace(cg, id, 1, ""):
            return
        if type == (MapleInventoryType.EQUIP) && !GameConstants.is飞镖道具(id) && !GameConstants.is子弹道具(id):
            item = ii.getEquipById(id)
            name = ii.getName(id)
            if id / 10000 == 114 && name is not None && name > 0:
                msg = "你已获得称号 <" + name + ">"
                cg.getPlayer().dropMessage(5, msg)
                cg.getPlayer().dropMessage(5, msg)
            if time > 0:
                item.setExpiration(int(time.time() * 1000) + time * 60 * 60 * 1000)
            if str > 0:
                item.setStr(str)
            if dex > 0:
                item.setDex(dex)
            if luk > 0:
                item.setLuk(luk)
            if Int > 0:
                item.setInt(Int)
            if hp > 0:
                item.setHp(hp)
            if mp > 0:
                item.setMp(mp)
            if watk > 0:
                item.setWatk(watk)
            if matk > 0:
                item.setMatk(matk)
            if wdef > 0:
                item.setWdef(wdef)
            if mdef > 0:
                item.setMdef(mdef)
            if hb > 0:
                item.setAvoid(hb)
            if mz > 0:
                item.setAcc(mz)
            if ty > 0:
                item.setJump(ty)
            if yd > 0:
                item.setSpeed(yd)
            if ksjcs >= 0:
                item.setUpgradeSlots(ksjcs)
            if ysjcs > 0:
                item.setLevel(ysjcs)
            if jcz > 0:
                item.setViciousHammer(jcz)
            if suo > 0:
                item.setLocked(suo)
            MapleInventoryManipulator.addbyItem(cg, item.copy())
        else:
            MapleInventoryManipulator.addById(cg, id, 1, "", 0)
        cg.getSession().write(MaplePacketCreator.getShowItemGain(id, 1, True))

    def transferCashEquipStat(self, fromSlot: int, toSlot: int) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        equip = self.getPlayer().getInventory(MapleInventoryType.EQUIP)
        fromEquip = equip.getItem(fromSlot)
        toEquip = equip.getItem(toSlot)
        if fromEquip is None || toEquip is None:
            return False
        isCash1 = ii.isCash(fromEquip.getItemId())
        isCash2 = ii.isCash(toEquip.getItemId())
        if !isCash1 || !isCash2:
            return False
        if fromEquip.getStr() > 0:
            toEquip.setStr(fromEquip.getStr())
        if fromEquip.getDex() > 0:
            toEquip.setDex(fromEquip.getDex())
        if fromEquip.getInt() > 0:
            toEquip.setInt(fromEquip.getInt())
        if fromEquip.getLuk() > 0:
            toEquip.setLuk(fromEquip.getLuk())
        if fromEquip.getHp() > 0:
            toEquip.setHp(fromEquip.getHp())
        if fromEquip.getMp() > 0:
            toEquip.setMp(fromEquip.getMp())
        if fromEquip.getWatk() > 0:
            toEquip.setWatk(fromEquip.getWatk())
        if fromEquip.getWdef() > 0:
            toEquip.setWdef(fromEquip.getWdef())
        if fromEquip.getMatk() > 0:
            toEquip.setMatk(fromEquip.getMatk())
        if fromEquip.getMdef() > 0:
            toEquip.setMdef(fromEquip.getMdef())
        self.getPlayer().getInventory(MapleInventoryType.EQUIP).removeItem(fromSlot)
        self.c.getSession().write(MaplePacketCreator.clearInventoryItem(MapleInventoryType.EQUIP, fromSlot, False))
        self.c.getSession().write(MaplePacketCreator.updateSpecialItemUse_(toEquip, GameConstants.getInventoryType(toEquip.getItemId()).getType()))
        self.c.getSession().write(MaplePacketCreator.enableActions())
        return True

    def enableActions(self) -> None:
        NPCScriptManager.getInstance().dispose(self.c)
        self.c.getSession().write(MaplePacketCreator.enableActions())
        self.c.getPlayer().dropMessage(1, "假死已处理完毕.")
        self.c.getPlayer().dropMessage(6, "当前延迟 " + self.c.getPlayer().getClient().getLatency() + " 毫秒")

    def changeMusic(self, songName: str) -> None:
        self.getPlayer().getMap().broadcastMessage(MaplePacketCreator.musicChange(songName))

    def cs(self, songName: str) -> None:
        self.getPlayer().getMap().broadcastMessage(MaplePacketCreator.showEffect(songName))

    def worldMessage(self, type: int, channel: int, message: str, smegaEar: bool) -> None:
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(type, channel, message, smegaEar).encode("utf-8"))

    def worldMessage_type_message(self, type: int, message: str) -> None:
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(type, message).encode("utf-8"))

    def givePartyExp_PQ(self, maxLevel: int, mod: float) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            amount = Math.round(GameConstants.getExpNeededForLevel((self.getPlayer().getLevel() > maxLevel) ? (maxLevel + self.getPlayer().getLevel() / 10) : self.getPlayer().getLevel()) / (min(self.getPlayer().getLevel(), maxLevel) / 10.0) / mod)
            self.gainExp(amount)
            return
        cMap = self.getPlayer().getMapId()
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None && (curChar.getMapId() == cMap || curChar.getEventInstance() == self.getPlayer().getEventInstance()):
                amount2 = Math.round(GameConstants.getExpNeededForLevel((curChar.getLevel() > maxLevel) ? (maxLevel + curChar.getLevel() / 10) : curChar.getLevel()) / (min(curChar.getLevel(), maxLevel) / 10.0) / mod)
                curChar.gainExp(amount2, True, True, True)

    def playerMessage(self, message: str) -> None:
        self.playerMessage(5, message)

    def mapMessage(self, message: str) -> None:
        self.mapMessage(5, message)

    def guildMessage(self, message: str) -> None:
        self.guildMessage(5, message)

    def playerMessage_type_message(self, type: int, message: str) -> None:
        self.c.getSession().write(MaplePacketCreator.serverNotice(type, message))

    def mapMessage_type_message(self, type: int, message: str) -> None:
        self.c.getPlayer().getMap().broadcastMessage(MaplePacketCreator.serverNotice(type, message))

    def guildMessage_type_message(self, type: int, message: str) -> None:
        if self.getPlayer().getGuildId() > 0:
            World.Guild.guildPacket(self.getPlayer().getGuildId(), MaplePacketCreator.serverNotice(type, message))

    def getGuild(self) -> Any:
        return self.getGuild(self.getPlayer().getGuildId())

    def getGuild_guildid(self, guildid: int) -> Any:
        return World.Guild.getGuild(guildid)

    def getParty(self) -> Any:
        return self.c.getPlayer().getParty()

    def getCurrentPartyId(self, mapid: int) -> int:
        return self.getMap(mapid).getCurrentPartyId()

    def czdt(self, MapID: int) -> None:
        player = self.c.getPlayer()
        mapid = MapID
        map = player.getMap()
        if player.getClient().getChannelServer().getMapFactory().destroyMap(mapid):
            newMap = player.getClient().getChannelServer().getMapFactory().getMap(mapid)
            newPor = newMap.getPortal(0)
            mcs = new LinkedHashSet<MapleCharacter>(map.getCharacters())
            for m in mcs:
                x = 0
                if x < 5:
                    continue

    def isLeader(self) -> bool:
        return self.getParty() is not None && self.getParty().getLeader().getId() == self.c.getPlayer().getId()

    def isParty(self) -> bool:
        return self.getParty() is not None

    def isAllPartyMembersAllowedJob(self, job: int) -> bool:
        if self.c.getPlayer().getParty() is None:
            return False
        for mem in self.c.getPlayer().getParty().getMembers():
            if mem.getJobId() / 100 != job:
                return False
        return True

    def allMembersHere(self) -> bool:
        if self.c.getPlayer().getParty() is None:
            return False
        for mem in self.c.getPlayer().getParty().getMembers():
            chr = self.c.getPlayer().getMap().getCharacterById(mem.getId())
            if chr is None:
                return False
        return True

    def resetPartyBossLog(self, bosslog: str) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.getPlayer().resetBossLog(bosslog)
            return
        cMap = self.getPlayer().getMapId()
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None && (curChar.getMapId() == cMap || curChar.getEventInstance() == self.getPlayer().getEventInstance()):
                curChar.resetBossLog(bosslog)

    def warpParty(self, mapId: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.warp(mapId, 0)
            return
        target = self.getMap(mapId)
        cMap = self.getPlayer().getMapId()
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None && (curChar.getMapId() == cMap || curChar.getEventInstance() == self.getPlayer().getEventInstance()):
                curChar.changeMap(target, target.getPortal(0))

    def warpParty_mapId_portal(self, mapId: int, portal: str) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.warp(mapId, portal)
            return
        target = self.getMap(mapId)
        cMap = self.getPlayer().getMapId()
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None && (curChar.getMapId() == cMap || curChar.getEventInstance() == self.getPlayer().getEventInstance()):
                curChar.changeMap(target, target.getPortal(portal))

    def warpParty_Instanced(self, mapId: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.warp_Instanced(mapId)
            return
        target = self.getMap_Instanced(mapId)
        cMap = self.getPlayer().getMapId()
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is not None && (curChar.getMapId() == cMap || curChar.getEventInstance() == self.getPlayer().getEventInstance()):
                curChar.changeMap(target, target.getPortal(0))

    def gainDY(self, gain: int) -> None:
        self.c.getPlayer().modifyCSPoints(2, gain, True)

    def gainMeso(self, gain: int) -> None:
        self.c.getPlayer().gainMeso(gain, True, False, True)

    def gainExp(self, gain: int) -> None:
        self.c.getPlayer().gainExp(gain, True, True, True)

    def gainExpR(self, gain: int) -> None:
        self.c.getPlayer().gainExp(gain * self.c.getChannelServer().getExpRate(), True, True, True)

    def givePartyItems(self, id: int, quantity: int, party: list) -> None:
        for chr in party:
            if quantity >= 0:
                MapleInventoryManipulator.addById(chr.getClient(), id, quantity, 0)
            else:
                MapleInventoryManipulator.removeById(chr.getClient(), GameConstants.getInventoryType(id), id, -quantity, True, False)
            chr.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, quantity, True))

    def translated_给组队物品(self, id: int, quantity: int) -> None:
        self.givePartyItems(id, quantity, False)

    def translated_给予组队经验队长双倍(self, amount: int, party: list) -> None:
        for chr in party:
            if party == (chr.getParty().getLeader()):
                self.getPlayer().dropMessage(5, "由于你是队长系统给了你双倍的经验值")
                chr.gainExp(amount * 2, True, True, True)
            else:
                chr.gainExp(amount, True, True, True)

    def translated_给予组队物品队长双倍(self, id: int, quantity: int, removeAll: bool) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainItem(id, (short)(removeAll ? (-self.getPlayer().itemQuantity(id)) : quantity))
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                if chr == (self.getPlayer().getParty().getLeader()):
                    self.getPlayer().dropMessage(5, "由于你是队长系统给了你双倍数量的奖励")
                    self.gainItem(id, (short)(removeAll ? (-curChar.itemQuantity(id)) : (quantity * 2)), False, 0, 0, "", curChar.getClient(), 0)
                else:
                    self.gainItem(id, (short)(removeAll ? (-curChar.itemQuantity(id)) : quantity), False, 0, 0, "", curChar.getClient(), 0)

    def givePartyItems_id_quantity_removeAll(self, id: int, quantity: int, removeAll: bool) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainItem(id, (short)(removeAll ? (-self.getPlayer().itemQuantity(id)) : quantity))
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                self.gainItem(id, (short)(removeAll ? (-curChar.itemQuantity(id)) : quantity), False, 0, 0, "", curChar.getClient(), 0)

    def givePartyExp(self, amount: int, party: list) -> None:
        for chr in party:
            chr.gainExp(amount, True, True, True)

    def translated_给组队经验(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainExp(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.gainExp(amount, True, True, True)

    def givePartyNX(self, amount: int, party: list) -> None:
        for chr in party:
            chr.modifyCSPoints(1, amount, True)

    def translated_给组队抵用卷(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainDY(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.modifyCSPoints(2, amount, True)

    def translated_给组队金币(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainMeso(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.gainMeso(amount, True)

    def translated_给组队点卷(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.gainNX(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.modifyCSPoints(1, amount, True)

    def givePartyFb(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            if self.getPlayer().getmrfbrws() > self.getFBRW():
                self.gainFBRW(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None && curChar.getmrfbrws() > curChar.getFBRW():
                curChar.gainFBRW(amount)

    def givePartyFba(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            if self.getPlayer().getmrfbrwas() > self.getFBRWA():
                self.gainFBRWA(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None && curChar.getmrfbrwas() > curChar.getFBRWA():
                curChar.gainFBRWA(amount)

    def endPartyQuest(self, amount: int, party: list) -> None:
        for chr in party:
            chr.endPartyQuest(amount)

    def endPartyQuest_amount(self, amount: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.getPlayer().endPartyQuest(amount)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.endPartyQuest(amount)

    def removeFromParty(self, id: int, party: list) -> None:
        for chr in party:
            possesed = chr.getInventory(GameConstants.getInventoryType(id)).countById(id)
            if possesed > 0:
                MapleInventoryManipulator.removeById(self.c, GameConstants.getInventoryType(id), id, possesed, True, False)
                chr.getClient().getSession().write(MaplePacketCreator.getShowItemGain(id, (short)(-possesed), True))

    def removeFromParty_id(self, id: int) -> None:
        self.givePartyItems(id, 0, True)

    def useSkill(self, skill: int, level: int) -> None:
        if level <= 0:
            return
        SkillFactory.getSkill(skill).getEffect(level).applyTo(self.c.getPlayer())

    def useItem(self, id: int) -> None:
        MapleItemInformationProvider.getInstance().getItemEffect(id).applyTo(self.c.getPlayer())
        self.c.getSession().write(UIPacket.getStatusMsg(id))

    def cancelItem(self, id: int) -> None:
        self.c.getPlayer().cancelEffect(MapleItemInformationProvider.getInstance().getItemEffect(id), False, -1)

    def getMorphState(self) -> int:
        return self.c.getPlayer().getMorphState()

    def removeAll(self, id: int) -> None:
        self.c.getPlayer().removeAll(id)

    def gainCloseness(self, closeness: int, index: int) -> None:
        pet = self.getPlayer().getPet(index)
        if pet is not None:
            pet.setCloseness(pet.getCloseness() + closeness)
            self.getClient().getSession().write(PetPacket.updatePet(pet, self.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))

    def gainClosenessAll(self, closeness: int) -> None:
        for pet in self.getPlayer().getPets():
            if pet is not None:
                pet.setCloseness(pet.getCloseness() + closeness)
                self.getClient().getSession().write(PetPacket.updatePet(pet, self.getPlayer().getInventory(MapleInventoryType.CASH).getItem(pet.getInventoryPosition()), True))

    def resetMap(self, mapid: int) -> None:
        self.getMap(mapid).resetFully()

    def resetMapS(self) -> None:
        player = self.c.getPlayer()
        mapid = player.getMapId()
        map = player.getMap()
        if player.getClient().getChannelServer().getMapFactory().destroyMap(mapid):
            newMap = player.getClient().getChannelServer().getMapFactory().getMap(mapid)
            newPor = newMap.getPortal(0)
            mcs = new LinkedHashSet<MapleCharacter>(map.getCharacters())
            for m in mcs:
                x = 0
                while x < 5:
                    try:
                        m.changeMap(newMap, newPor)
                    except Exception as t:
                        x += 1
                        continue
                    break

    def openNpc(self, id: int) -> None:
        NPCScriptManager.getInstance().start(self.getClient(), id)

    def openNpc_id_wh(self, id: int, wh: int) -> None:
        NPCScriptManager.getInstance().start(self.getClient(), id, wh)

    def serverNotice(self, Text: str) -> None:
        self.getClient().getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(6, Text))

    def openNpc_cg_id(self, cg: Any, id: int) -> None:
        NPCScriptManager.getInstance().start(cg, id)

    def getMapId(self) -> int:
        return self.c.getPlayer().getMap().getId()

    def haveMonster(self, mobid: int) -> bool:
        for obj in self.c.getPlayer().getMap().getAllMonstersThreadsafe():
            mob = obj
            if mob.getId() == mobid:
                return True
        return False

    def getChannelNumber(self) -> int:
        return self.c.getChannel()

    def getMonsterCount(self, mapid: int) -> int:
        return self.c.getChannelServer().getMapFactory().getMap(mapid).getNumMonsters()

    def teachSkill(self, id: int, level: int, masterlevel: int) -> None:
        self.getPlayer().changeSkillLevel(SkillFactory.getSkill(id), level, masterlevel)

    def teachSkill_id_level(self, id: int, level: int) -> None:
        skil = SkillFactory.getSkill(id)
        if self.getPlayer().getSkillLevel(skil) > level:
            level = self.getPlayer().getSkillLevel(skil)
        self.getPlayer().changeSkillLevel(skil, level, skil.getMaxLevel())

    def getPlayerCount(self, mapid: int) -> int:
        return self.c.getChannelServer().getMapFactory().getMap(mapid).getCharactersSize()

    def getMobCount(self, mapId: int) -> int:
        return self.c.getChannelServer().getMapFactory().getMap(mapId).getNumMonsters()

    def dojo_getUp(self) -> None:
        self.c.getSession().write(MaplePacketCreator.updateInfoQuest(1207, "pt=1;min=4;belt=1;tuto=1"))
        self.c.getSession().write(MaplePacketCreator.dojoWarpUp())

    def dojoAgent_NextMap(self, dojo: bool, fromresting: bool) -> bool:
        if dojo:
            return Event_DojoAgent.warpNextMap(self.c.getPlayer(), fromresting)
        return Event_DojoAgent.warpNextMap_Agent(self.c.getPlayer(), fromresting)

    def dojo_getPts(self) -> int:
        return self.c.getPlayer().getDojo()

    def getShopType(self) -> int:
        return self.c.getPlayer().getPlayerShop().getShopType()

    def getEvent(self, loc: str) -> Any:
        return self.c.getChannelServer().getEvent(MapleEventType.valueOf(loc))

    def getSavedLocation(self, loc: str) -> int:
        ret = self.c.getPlayer().getSavedLocation(SavedLocationType.fromString(loc))
        if ret is None || ret == -1:
            return 100000000
        return ret

    def saveLocation(self, loc: str) -> None:
        self.c.getPlayer().saveLocation(SavedLocationType.fromString(loc))

    def saveReturnLocation(self, loc: str) -> None:
        self.c.getPlayer().saveLocation(SavedLocationType.fromString(loc), self.c.getPlayer().getMap().getReturnMap().getId())

    def clearSavedLocation(self, loc: str) -> None:
        self.c.getPlayer().clearSavedLocation(SavedLocationType.fromString(loc))

    def summonMsg(self, msg: str) -> None:
        if !self.c.getPlayer().hasSummon():
            self.playerSummonHint(True)
        self.c.getSession().write(UIPacket.summonMessage(msg))

    def summonMsg_type(self, type: int) -> None:
        if !self.c.getPlayer().hasSummon():
            self.playerSummonHint(True)
        self.c.getSession().write(UIPacket.summonMessage(type))

    def HSText(self, msg: str) -> None:
        self.c.getSession().write(MaplePacketCreator.HSText(msg))

    def showInstruction(self, msg: str, width: int, height: int) -> None:
        self.c.getSession().write(MaplePacketCreator.sendHint(msg, width, height))

    def playerSummonHint(self, summon: bool) -> None:
        self.c.getPlayer().setHasSummon(summon)
        self.c.getSession().write(UIPacket.summonHelper(summon))

    def getInfoQuest(self, id: int) -> str:
        return self.c.getPlayer().getInfoQuest(id)

    def updateInfoQuest(self, id: int, data: str) -> None:
        self.c.getPlayer().updateInfoQuest(id, data)

    def getEvanIntroState(self, data: str) -> bool:
        return self.getInfoQuest(22013) == (data)

    def updateEvanIntroState(self, data: str) -> None:
        self.updateInfoQuest(22013, data)

    def Aran_Start(self) -> None:
        self.c.getSession().write(UIPacket.Aran_Start())

    def evanTutorial(self, data: str, v1: int) -> None:
        self.c.getSession().write(MaplePacketCreator.getEvanTutorial(data))

    def AranTutInstructionalBubble(self, data: str) -> None:
        self.c.getSession().write(UIPacket.AranTutInstructionalBalloon(data))

    def ShowWZEffect(self, data: str) -> None:
        self.c.getSession().write(UIPacket.AranTutInstructionalBalloon(data))

    def showWZEffect(self, data: str, info: int) -> None:
        self.c.getSession().write(UIPacket.ShowWZEffect(data, info))

    def MovieClipIntroUI(self, enabled: bool) -> None:
        self.c.getSession().write(UIPacket.IntroDisableUI(enabled))
        self.c.getSession().write(UIPacket.IntroLock(enabled))

    def getInvType(self, i: int) -> Any:
        return MapleInventoryType.getByType(i)

    def getItemName(self, id: int) -> str:
        return MapleItemInformationProvider.getInstance().getName(id)

    def gainPet(self, id: int, name: str, level: int, closeness: int, fullness: int, period: int) -> None:
        if id > 5010000 || id < 5000000:
            id = 5000000
        if level > 30:
            level = 30
        if closeness > 30000:
            closeness = 30000
        if fullness > 100:
            fullness = 100
        name = self.getItemName(id)
        try:
            MapleInventoryManipulator.addById(self.c, id, 1, "", MaplePet.createPet(id, name, level, closeness, fullness, MapleInventoryIdentifier.getInstance(), (id == 5000054) ? (period) : 0), period, 0)
        except TypeError as ex:
            ex.printStackTrace()

    def removeSlot(self, invType: int, slot: int, quantity: int) -> None:
        MapleInventoryManipulator.removeFromSlot(self.c, self.getInvType(invType), slot, quantity, True)

    def gainGP(self, gp: int) -> None:
        if self.getPlayer().getGuildId() <= 0:
            return
        World.Guild.gainGP(self.getPlayer().getGuildId(), gp)

    def getGP(self) -> int:
        if self.getPlayer().getGuildId() <= 0:
            return 0
        return World.Guild.getGP(self.getPlayer().getGuildId())

    def showMapEffect(self, path: str) -> None:
        self.getClient().getSession().write(UIPacket.MapEff(path))

    def translated_判断物品数量(self, itemid: int) -> int:
        return self.getPlayer().itemQuantity(itemid)

    def getDisconnected(self, event: str) -> Any:
        em = self.getEventManager(event)
        if em is None:
            return None
        for eim in em.getInstances():
            if eim.isDisconnected(self.c.getPlayer()) && eim.getPlayerCount() > 0:
                return eim
        return None

    def isAllReactorState(self, reactorId: int, state: int) -> bool:
        ret = False
        for r in self.getMap().getAllReactorsThreadsafe():
            if r.getReactorId() == reactorId:
                ret = (r.getState() == state)
        return ret

    def getCurrentTime(self) -> int:
        return int(time.time() * 1000)

    def spawnMonster_id(self, id: int) -> None:
        self.spawnMonster(id, 1, Point(self.getPlayer().getPosition()))

    def spawnMonster_id_x_y(self, id: int, x: int, y: int) -> None:
        self.spawnMonster(id, 1, Point(x, y))

    def spawnMonster_id_qty_x_y(self, id: int, qty: int, x: int, y: int) -> None:
        self.spawnMonster(id, qty, Point(x, y))

    def spawnMonster_id_qty_pos(self, id: int, qty: int, pos: Any) -> None:
        for i in range(qty):
            self.getMap().spawnMonsterOnGroundBelow(MapleLifeFactory.getMonster(id), pos)

    def sendNPCText(self, text: str, npc: int) -> None:
        self.getMap().broadcastMessage(MaplePacketCreator.getNPCTalk(npc, 0, text, "00 00", 0))

    def getTempFlag(self, flag: int) -> bool:
        return (self.c.getChannelServer().getTempFlag() & flag) == flag

    def getGamePoints(self) -> int:
        return self.c.getPlayer().getGamePoints()

    def gainGamePoints(self, amount: int) -> None:
        self.c.getPlayer().gainGamePoints(amount)

    def resetGamePoints(self) -> None:
        self.c.getPlayer().resetGamePoints()

    def getGamePointsPD(self) -> int:
        return self.c.getPlayer().getGamePointsPD()

    def gainGamePointsPD(self, amount: int) -> None:
        self.c.getPlayer().gainGamePointsPD(amount)

    def resetGamePointsPD(self) -> None:
        self.c.getPlayer().resetGamePointsPD()

    def getPS(self) -> int:
        return self.c.getPlayer().getGamePointsPS()

    def gainPS(self, amount: int) -> None:
        self.c.getPlayer().gainGamePointsPS(amount)

    def resetPS(self) -> None:
        self.c.getPlayer().resetGamePointsPS()

    def getskillzq(self) -> int:
        return self.c.getPlayer().getskillzq()

    def setskillzq(self, amount: int) -> None:
        self.c.getPlayer().setskillzq(amount)

    def getscjs(self) -> int:
        return self.c.getPlayer().getskillzq()

    def getSJRW(self) -> int:
        return self.c.getPlayer().getSJRW()

    def gainSJRW(self, amount: int) -> None:
        self.c.getPlayer().gainSJRW(amount)

    def resetSJRW(self) -> None:
        self.c.getPlayer().resetSJRW()

    def getFBRW(self) -> int:
        return self.c.getPlayer().getFBRW()

    def gainFBRW(self, amount: int) -> None:
        self.c.getPlayer().gainFBRW(amount)

    def resetFBRW(self) -> None:
        self.c.getPlayer().resetFBRW()

    def getFBRWA(self) -> int:
        return self.c.getPlayer().getFBRWA()

    def gainFBRWA(self, amount: int) -> None:
        self.c.getPlayer().gainFBRWA(amount)

    def resetFBRWA(self) -> None:
        self.c.getPlayer().resetFBRWA()

    def getSGRW(self) -> int:
        return self.c.getPlayer().getSGRW()

    def gainSGRW(self, amount: int) -> None:
        self.c.getPlayer().gainSGRW(amount)

    def resetSGRW(self) -> None:
        self.c.getPlayer().resetSGRW()

    def getSGRWA(self) -> int:
        return self.c.getPlayer().getSGRWA()

    def gainSGRWA(self, amount: int) -> None:
        self.c.getPlayer().gainSGRWA(amount)

    def resetSGRWA(self) -> None:
        self.c.getPlayer().resetSGRWA()

    def getSBOSSRW(self) -> int:
        return self.c.getPlayer().getSBOSSRW()

    def gainSBOSSRW(self, amount: int) -> None:
        self.c.getPlayer().gainSBOSSRW(amount)

    def resetSBOSSRW(self) -> None:
        self.c.getPlayer().resetSBOSSRW()

    def getSBOSSRWA(self) -> int:
        return self.c.getPlayer().getSBOSSRWA()

    def gainSBOSSRWA(self, amount: int) -> None:
        self.c.getPlayer().gainSBOSSRWA(amount)

    def resetSBOSSRWA(self) -> None:
        self.c.getPlayer().resetSBOSSRWA()

    def getlb(self) -> int:
        return self.c.getPlayer().getlb()

    def gainlb(self, amount: int) -> None:
        self.c.getPlayer().gainlb(amount)

    def resetlb(self) -> None:
        self.c.getPlayer().resetlb()

    def getvip(self) -> int:
        return self.c.getPlayer().getvip()

    def gainvip(self, amount: int) -> None:
        self.c.getPlayer().gainvip(amount)

    def setvip(self, s: int) -> None:
        self.c.getPlayer().setvip(s)

    def beibao(self, A: int) -> bool:
        return (self.c.getPlayer().getInventory(MapleInventoryType.EQUIP).getNextFreeSlot() > -1 && A == 1) || (self.c.getPlayer().getInventory(MapleInventoryType.USE).getNextFreeSlot() > -1 && A == 2) || (self.c.getPlayer().getInventory(MapleInventoryType.SETUP).getNextFreeSlot() > -1 && A == 3) || (self.c.getPlayer().getInventory(MapleInventoryType.ETC).getNextFreeSlot() > -1 && A == 4) || (self.c.getPlayer().getInventory(MapleInventoryType.CASH).getNextFreeSlot() > -1 && A == 5)

    def translated_记录组队bosslog(self, bossid: int) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.getPlayer().setbosslog(bossid)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.setbosslog(bossid)

    def beibao_A_kw(self, A: int, kw: int) -> bool:
        return (self.c.getPlayer().getInventory(MapleInventoryType.EQUIP).getNextFreeSlot() > kw && A == 1) || (self.c.getPlayer().getInventory(MapleInventoryType.USE).getNextFreeSlot() > kw && A == 2) || (self.c.getPlayer().getInventory(MapleInventoryType.SETUP).getNextFreeSlot() > kw && A == 3) || (self.c.getPlayer().getInventory(MapleInventoryType.ETC).getNextFreeSlot() > kw && A == 4) || (self.c.getPlayer().getInventory(MapleInventoryType.CASH).getNextFreeSlot() > kw && A == 5)

    def getFishingJF(self) -> int:
        return self.c.getPlayer().getFishingJF(1)

    def gainFishingJF(self, amount: int) -> None:
        self.c.getPlayer().gainFishingJF(amount)

    def addFishingJF(self, amount: int) -> None:
        self.c.getPlayer().addFishingJF(amount)

    def openWeb(self, web: str) -> None:
        self.c.getSession().write(MaplePacketCreator.openWeb(web))

    def getBossLog(self, bossid: str) -> int:
        return self.getPlayer().getBossLog(bossid)

    def getBossLogType(self, bossid: str) -> int:
        return self.getPlayer().getBossLogType(bossid)

    def setBossLog(self, bossid: str) -> None:
        self.getPlayer().setBossLog(bossid)

    def setBossLog_bossid_type(self, bossid: str, type: int) -> None:
        self.getPlayer().setBossLog(bossid, type)

    def resetBossLog(self, bossid: str) -> None:
        self.getPlayer().resetBossLog(bossid)

    def givePartyBossLog(self, bossid: str) -> None:
        if self.getPlayer().getParty() is None || self.getPlayer().getParty().getMembers() == 1:
            self.setBossLog(bossid)
            return
        for chr in self.getPlayer().getParty().getMembers():
            curChar = self.getMap().getCharacterById(chr.getId())
            if curChar is not None:
                curChar.setBossLog(bossid)

    def getOneTimeLog(self, bossid: str) -> int:
        return self.getPlayer().getOneTimeLog(bossid)

    def setOneTimeLog(self, bossid: str) -> None:
        self.getPlayer().setOneTimeLog(bossid)

    def resetAp(self) -> None:
        beginner = self.getPlayer().getJob() == 0 || self.getPlayer().getJob() == 1000 || self.getPlayer().getJob() == 2001
        self.getPlayer().resetStatsByJob(beginner)

    def displayGuide(self, guide: int) -> None:
        self.c.getSession().write(MaplePacketCreator.displayGuide(guide))

    def lockUI(self) -> None:
        self.c.getPlayer()
        MapleCharacter.tutorial = True
        self.c.getSession().write(UIPacket.IntroLock(True))
        self.c.getSession().write(UIPacket.IntroDisableUI(True))

    def unlockUI(self) -> None:
        self.c.getPlayer()
        MapleCharacter.tutorial = False
        self.c.getSession().write(UIPacket.IntroLock(False))
        self.c.getSession().write(UIPacket.IntroDisableUI(False))

    def MarrageChecking(self) -> int:
        if self.getPlayer().getParty() is None:
            return -1
        if self.getPlayer().getMarriageId() > 0:
            return 0
        if self.getPlayer().getParty().getMembers() != 2:
            return 1
        if self.getPlayer().getGender() == 0 && !self.getPlayer().haveItem(1050121) && !self.getPlayer().haveItem(1050122) && !self.getPlayer().haveItem(1050113):
            return 5
        if self.getPlayer().getGender() == 1 && !self.getPlayer().haveItem(1051129) && !self.getPlayer().haveItem(1051130) && !self.getPlayer().haveItem(1051114):
            return 5
        if !self.getPlayer().haveItem(1112001):
            return 6
        for chr in self.getPlayer().getParty().getMembers():
            if chr.getId() == self.getPlayer().getId():
                continue
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is None:
                return 2
            if curChar.getMarriageId() > 0:
                return 3
            if curChar.getGender() == self.getPlayer().getGender():
                return 4
            if curChar.getGender() == 0 && !curChar.haveItem(1050121) && !curChar.haveItem(1050122) && !curChar.haveItem(1050113):
                return 5
            if curChar.getGender() == 1 && !curChar.haveItem(1051129) && !curChar.haveItem(1051130) && !curChar.haveItem(1051114):
                return 5
            if !curChar.haveItem(1112001):
                return 6
        return 9

    def getPartyFormID(self) -> int:
        curCharID = -1
        if self.getPlayer().getParty() is None:
            curCharID = -1
        elif self.getPlayer().getMarriageId() > 0:
            curCharID = -2
        elif self.getPlayer().getParty().getMembers() != 2:
            curCharID = -3
        for chr in self.getPlayer().getParty().getMembers():
            if chr.getId() == self.getPlayer().getId():
                continue
            curChar = self.getChannelServer().getPlayerStorage().getCharacterById(chr.getId())
            if curChar is None:
                curCharID = -4
            else:
                curCharID = chr.getId()
        return curCharID

    def warpByName(self, mapid: int, chrname: str) -> None:
        chr = self.c.getChannelServer().getPlayerStorage().getCharacterByName(chrname)
        if chr is None:
            self.c.getPlayer().dropMessage(1, "找不到这个角色。")
            self.c.getSession().write(MaplePacketCreator.enableActions())
            return
        mapz = self.getWarpMap(mapid)
        try:
            chr.changeMap(mapz, mapz.getPortal(Randomizer.nextInt(mapz.getPortals())))
            chr.getClient().removeClickedNPC()
            NPCScriptManager.getInstance().dispose(chr.getClient())
            chr.getClient().getSession().write(MaplePacketCreator.enableActions())
        except Exception as e:
            chr.changeMap(mapz, mapz.getPortal(0))
            chr.getClient().removeClickedNPC()
            NPCScriptManager.getInstance().dispose(chr.getClient())
            chr.getClient().getSession().write(MaplePacketCreator.enableActions())

    def mapChangeTimer(self, map: int, nextmap: int, time: int, notice: bool) -> None:
        current = self.c.getChannelServer().getMapFactory().getMap(map).getCharacters()
        self.c.getChannelServer().getMapFactory().getMap(map).broadcastMessage(MaplePacketCreator.getClock(time))
        if notice:
            self.c.getChannelServer().getMapFactory().getMap(map).startMapEffect("当计时器结束时，您将被移出地图。", 5120041)
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                if current is not None:
                    for chrs in current:
                        chrs.changeMap(nextmap, 0)

    def run(self) -> None:
        if current is not None:
            for chrs in current:
                chrs.changeMap(nextmap, 0)

    def hideNpc(self, npcId: int) -> None:
        self.c.getPlayer().getMap().hideNpc(npcId)

    def respawn(self, force: bool) -> None:
        self.c.getPlayer().getMap().respawn(force)

    def touzhu(self, type: int, nx: int, num: int) -> bool:
        flage = False
        if nx >= 50:
            cherryMSLottery = CherryMScustomEventFactory.getInstance().getCherryMSLottery()
            self.getPlayer().setTouzhuType(type)
            self.getPlayer().setTouzhuNX(nx)
            self.getPlayer().setTouzhuNum(num)
            self.getPlayer().modifyCSPoints(1, -nx)
            cherryMSLottery.addChar(self.getPlayer())
            flage = True
        else:
            flage = False
        return flage

    def seeTouzhuByType(self, type: int) -> int:
        return CherryMScustomEventFactory.getInstance().getCherryMSLottery().getTouNumbyType(type)

    def seeAlltouzhu(self) -> int:
        return CherryMScustomEventFactory.getInstance().getCherryMSLottery().getAlltouzhu()

    def seeAllpeichu(self) -> int:
        return CherryMScustomEventFactory.getInstance().getCherryMSLottery().getAllpeichu()

    def getItemsByType(self, type: int) -> list:
        items = []
        itemtype = MapleInventoryType.getByType(type)
        mi = self.getPlayer().getInventory(itemtype)
        if mi is not None:
            for item in mi.list():
                items.add(item)
        return items

    def translated_获取当前星期(self) -> int:
        return Calendar.getInstance().get(7)

    def getServerName(self) -> str:
        return ServerProperties.getProperty("RoyMS.ServerName")

    def translated_获取最高玩家等级(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高等级玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `level` FROM characters WHERE gm = 0 ORDER BY `level` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("level")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家人气(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高人气玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `fame` FROM characters WHERE gm = 0 ORDER BY `fame` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("fame")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家金币(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高金币玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `meso` FROM characters WHERE gm = 0 ORDER BY `meso` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("meso")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def translated_获取最高玩家在线(self) -> int:
        data = 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXas DATA FROM characters WHERE gm = 0")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    data = rs.getInt("DATA")
            ps.close()
        except Exception as Ex:
            print("获取最高玩家等级出错 - 数据库查询失败：" + Ex)
        return data

    def translated_获取最高在线玩家名字(self) -> str:
        name = ""
        level = ""
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `totalOnlineTime` FROM characters WHERE gm = 0 ORDER BY `totalOnlineTime` DESC LIMIT 1")
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    name = rs.getString("name")
                    level = rs.getString("totalOnlineTime")
            ps.close()
        except Exception as Ex:
            print("获取家族名称出错 - 数据库查询失败：" + Ex)
        return String.format("%s", name)

    def getBossRankPointsTop(self, bossname: str) -> list:
        return BossRankManager.getInstance().getRank(bossname, 1)

    def getBossRankCountTop(self, bossname: str) -> list:
        return BossRankManager.getInstance().getRank(bossname, 2)

    def getBossRankTop(self, bossname: str, type: int) -> list:
        return BossRankManager.getInstance().getRank(bossname, type)

    def setBossRankPoints(self, bossname: str) -> int:
        return self.setBossRank(self.getPlayer().getId(), self.getPlayer().getName(), bossname, 1, 1)

    def setBossRankCount(self, bossname: str) -> int:
        return self.setBossRank(self.getPlayer().getId(), self.getPlayer().getName(), bossname, 2, 1)

    def setBossRankPoints_bossname_add(self, bossname: str, add: int) -> int:
        return self.setBossRank(self.getPlayer().getId(), self.getPlayer().getName(), bossname, 1, add)

    def setBossRankCount_bossname_add(self, bossname: str, add: int) -> int:
        return self.setBossRank(self.getPlayer().getId(), self.getPlayer().getName(), bossname, 2, add)

    def setBossRank(self, bossname: str, type: int, add: int) -> int:
        return self.setBossRank(self.getPlayer().getId(), self.getPlayer().getName(), bossname, type, add)

    def setBossRank_cid_cname_bossname_type_add(self, cid: int, cname: str, bossname: str, type: int, add: int) -> int:
        return BossRankManager.getInstance().setLog(cid, cname, bossname, type, add)

    def getBossRankPoints(self, bossname: str) -> int:
        return self.getBossRank(bossname, 1)

    def getBossRankCount(self, bossname: str) -> int:
        return self.getBossRank(bossname, 2)

    def getBossRank(self, bossname: str, type: int) -> int:
        return self.getBossRank(self.getPlayer().getId(), bossname, type)

    def getBossRank_cid_bossname_type(self, cid: int, bossname: str, type: int) -> int:
        ret = -1
        info = BossRankManager.getInstance().getInfo(cid, bossname)
        if None == info:
            return ret
        # switch (type):
            # case 1:
                ret = info.getPoints()
                break
            # case 2:
                ret = info.getCount()
                break
        return ret

    def auction_putIn(self, source: Any, quantity: int) -> int:
        return AuctionManager.getInstance().putInt(self.getPlayer(), source, quantity)

    def auction_takeOutAuctionItem(self, id: int) -> int:
        return AuctionManager.getInstance().takeOutAuctionItem(self.getPlayer(), id)

    def auction_setPutaway(self, id: int, price: int) -> int:
        return AuctionManager.getInstance().setPutaway(id, price)

    def auction_soldOut(self, id: int) -> int:
        return AuctionManager.getInstance().soldOut(id)

    def auction_buy(self, id: int) -> int:
        return AuctionManager.getInstance().buy(self.getPlayer(), id)

    def auction_getAuctionPoint(self) -> Any:
        return AuctionManager.getInstance().getAuctionPoint(self.getPlayer().getId())

    def auction_getAuctionPoint_characterid(self, characterid: int) -> Any:
        return AuctionManager.getInstance().getAuctionPoint(characterid)

    def auction_addPoint(self, point: int) -> int:
        return AuctionManager.getInstance().addPoint(self.getPlayer().getId(), point)

    def auction_findById(self, id: int) -> Any:
        return AuctionManager.getInstance().findById(id)

    def auction_findByCharacterId(self) -> list:
        return AuctionManager.getInstance().findByCharacterId(self.getPlayer().getId())

    def auction_findByCharacterId_characterid(self, characterid: int) -> list:
        return AuctionManager.getInstance().findByCharacterId(characterid)

    def auction_findByItemType(self, inventorytype: int) -> list:
        return AuctionManager.getInstance().findByItemType(inventorytype)

    def auction_deletePlayerSold(self) -> int:
        return AuctionManager.getInstance().deletePlayerSold(self.getPlayer().getId())

    def itemQuantity(self, itemid: int) -> int:
        return self.getPlayer().itemQuantity(itemid)

    def debug(self, s: str) -> None:
        print(s)

