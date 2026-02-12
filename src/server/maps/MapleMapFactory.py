"""
MapleMapFactory - Converted from Java source
Original: server/maps/MapleMapFactory.java
Package: server.maps
"""

from pathlib import Path
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import RLock
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import os
import pymysql
import sys
import threading

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from provider.MapleData import *  # TODO: import specific classes
# from provider.MapleDataProvider import *  # TODO: import specific classes
# from provider.MapleDataProviderFactory import *  # TODO: import specific classes
# from provider.MapleDataTool import *  # TODO: import specific classes
# from server.PortalFactory import *  # TODO: import specific classes
# from server.life.AbstractLoadedMapleLife import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes


class MapleMapFactory:
    """
    Class MapleMapFactory
    """

    def __init__(self, channel: int):
        self.maps = None
        self.DeStorymaps = None
        self.instanceMap = None
        self.lock = None
        self.channel = 0
        self.maps = {}
        self.DeStorymaps = {} {}
        self.instanceMap = {}
        self.lock = ReentrantLock(True)
        self.channel = channel

    # Static initializer
    # source = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/Map.wz"))
    # nameData = MapleDataProviderFactory.getDataProvider(File(os.environ.get("wzPath") + "/String.wz")).getData("Map.img")
    # mapInfos = {}
    # customLife = new HashMap<Integer, List<AbstractLoadedMapleLife>>()


    def loadLife(self, id: int, f: int, hide: bool, fh: int, cy: int, rx0: int, rx1: int, x: int, y: int, type: str, mtime: int) -> Any:
        myLife = MapleLifeFactory.getLife(id, type)
        if myLife is None:
            print("载入 npc " + id + " 异常...")
            return None
        myLife.setCy(cy)
        myLife.setF(f)
        myLife.setFh(fh)
        myLife.setRx0(rx0)
        myLife.setRx1(rx1)
        myLife.setPosition(Point(x, y))
        myLife.setHide(hide)
        myLife.setMTime(mtime)
        myLife.setCType(type)
        return myLife

    def loadCustomLife(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT * FROM `wz_customlife`"
            try:
            rs = ps.executeQuery())
                while rs.next():
                    mapid = rs.getInt("mid")
                    myLife = loadLife(rs.getInt("dataid"), rs.getInt("f"), rs.getByte("hide") > 0, rs.getInt("fh"), rs.getInt("cy"), rs.getInt("rx0"), rs.getInt("rx1"), rs.getInt("x"), rs.getInt("y"), rs.getString("type"), rs.getInt("mobtime"))
                    if myLife is None:
                        continue
                    entries = MapleMapFactory.customLife.get(mapid)
                    collections = []
                    if entries is None:
                        collections.add(myLife)
                        MapleMapFactory.customLife.put(mapid, collections)
                    else:
                        collections.addAll(entries)
                        collections.add(myLife)
                        MapleMapFactory.customLife.put(mapid, collections)
        except Exception as e:
            print("Error loading custom life..." + e)

    def getMap(self, mapid: int) -> Any:
        return self.getMap(mapid, True, True, True)

    def getMap_mapid_respawns_npcs(self, mapid: int, respawns: bool, npcs: bool) -> Any:
        return self.getMap(mapid, respawns, npcs, True)

    def getMap_mapid_respawns_npcs_reactors(self, mapid: int, respawns: bool, npcs: bool, reactors: bool) -> Any:
        omapid = mapid
        map = self.maps.get(omapid)
        if map is None:
            self.lock.lock()
            try:
                if self.DeStorymaps.get(omapid) is not None:
                    return None
                map = self.maps.get(omapid)
                if map is not None:
                    return map
                mapData = MapleMapFactory.source.getData(self.getMapName(mapid))
                link = mapData.getChildByPath("info/link")
                if link is not None:
                    mapData = MapleMapFactory.source.getData(self.getMapName(MapleDataTool.getIntConvert("info/link", mapData)))
                monsterRate = 0.0
                if respawns:
                    mobRate = mapData.getChildByPath("info/mobRate")
                    if mobRate is not None:
                        monsterRate = mobRate.getData()
                map = MapleMap(mapid, self.channel, MapleDataTool.getInt("info/returnMap", mapData), monsterRate)
                portalFactory = PortalFactory()
                for portal in mapData.getChildByPath("portal"):
                    map.addPortal(portalFactory.makePortal(MapleDataTool.getInt(portal.getChildByPath("pt")), portal))
                allFootholds = []
                lBound = Point()
                uBound = Point()
                for footRoot in mapData.getChildByPath("foothold"):
                    for footCat in footRoot:
                        for footHold in footCat:
                            fh = MapleFoothold(Point(MapleDataTool.getInt(footHold.getChildByPath("x1")), MapleDataTool.getInt(footHold.getChildByPath("y1"))), Point(MapleDataTool.getInt(footHold.getChildByPath("x2")), MapleDataTool.getInt(footHold.getChildByPath("y2"))), int(footHold.getName()))
                            fh.setPrev(MapleDataTool.getInt(footHold.getChildByPath("prev")))
                            fh.setNext(MapleDataTool.getInt(footHold.getChildByPath("next")))
                            if fh.getX1() < lBound.x:
                                lBound.x = fh.getX1()
                            if fh.getX2() > uBound.x:
                                uBound.x = fh.getX2()
                            if fh.getY1() < lBound.y:
                                lBound.y = fh.getY1()
                            if fh.getY2() > uBound.y:
                                uBound.y = fh.getY2()
                            allFootholds.add(fh)
                fTree = MapleFootholdTree(lBound, uBound)
                for foothold in allFootholds:
                    fTree.insert(foothold)
                map.setFootholds(fTree)
                bossid = -1
                msg = None
                if mapData.getChildByPath("info/timeMob") is not None:
                    bossid = MapleDataTool.getInt(mapData.getChildByPath("info/timeMob/id"), 0)
                    msg = MapleDataTool.getString(mapData.getChildByPath("info/timeMob/message"), None)
                for life in mapData.getChildByPath("life"):
                    type = MapleDataTool.getString(life.getChildByPath("type"))
                    if npcs or not type == ("n"):
                        myLife = self.loadLife(life, MapleDataTool.getString(life.getChildByPath("id")), type, mapid)
                        if myLife is None:
                            continue
                        if isinstance(myLife, MapleMonster):
                            mob = myLife
                            map.addMonsterSpawn(mob, MapleDataTool.getInt("mobTime", life, 0), MapleDataTool.getInt("team", life, -1), (mob.getId() == bossid) ? msg : None)
                        else:
                            if myLife is None:
                                continue
                            map.addMapObject(myLife)
                custom = MapleMapFactory.customLife.get(mapid)
                if custom is not None:
                    for n in custom:
                        cType = n.getCType()
                        # switch (cType):
                            # case "n":
                                map.addMapObject(n)
                                continue
                            # case "m":
                                monster = n
                                map.addMonsterSpawn(monster, n.getMTime(), (byte)(-1), None)
                                continue
                self.addAreaBossSpawn(map)
                map.setCreateMobInterval(MapleDataTool.getInt(mapData.getChildByPath("info/createMobInterval"), 9000))
                map.loadMonsterRate(True)
                map.setNodes(self.loadNodes(mapid, mapData))
                if reactors and mapData.getChildByPath("reactor") is not None:
                    for reactor in mapData.getChildByPath("reactor"):
                        id = MapleDataTool.getString(reactor.getChildByPath("id"))
                        if id is not None:
                            map.spawnReactor(self.loadReactor(reactor, id, MapleDataTool.getInt(reactor.getChildByPath("f"), 0)))
                try:
                    map.setMapName(MapleDataTool.getString("mapName", MapleMapFactory.nameData.getChildByPath(self.getMapStringName(omapid)), ""))
                    map.setStreetName(MapleDataTool.getString("streetName", MapleMapFactory.nameData.getChildByPath(self.getMapStringName(omapid)), ""))
                except Exception as e:
                    map.setMapName("")
                    map.setStreetName("")
                map.setClock(mapData.getChildByPath("clock") is not None)
                map.setEverlast(MapleDataTool.getInt(mapData.getChildByPath("info/everlast"), 0) > 0)
                map.setTown(MapleDataTool.getInt(mapData.getChildByPath("info/town"), 0) > 0)
                map.setSoaring(MapleDataTool.getInt(mapData.getChildByPath("info/needSkillForFly"), 0) > 0)
                map.setPersonalShop(MapleDataTool.getInt(mapData.getChildByPath("info/personalShop"), 0) > 0)
                map.setForceMove(MapleDataTool.getInt(mapData.getChildByPath("info/lvForceMove"), 0))
                map.setHPDec(MapleDataTool.getInt(mapData.getChildByPath("info/decHP"), 0))
                map.setHPDecInterval(MapleDataTool.getInt(mapData.getChildByPath("info/decHPInterval"), 10000))
                map.setHPDecProtect(MapleDataTool.getInt(mapData.getChildByPath("info/protectItem"), 0))
                map.setForcedReturnMap(MapleDataTool.getInt(mapData.getChildByPath("info/forcedReturn"), 999999999))
                map.setTimeLimit(MapleDataTool.getInt(mapData.getChildByPath("info/timeLimit"), -1))
                map.setFieldLimit(MapleDataTool.getInt(mapData.getChildByPath("info/fieldLimit"), 0))
                map.setFieldType(MapleDataTool.getInt(mapData.getChildByPath("info/fieldType"), 0))
                map.setFirstUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onFirstUserEnter"), ""))
                map.setUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onUserEnter"), ""))
                map.setRecoveryRate(MapleDataTool.getFloat(mapData.getChildByPath("info/recovery"), 1.0))
                map.setFixedMob(MapleDataTool.getInt(mapData.getChildByPath("info/fixedMobCapacity"), 0))
                map.setConsumeItemCoolTime(MapleDataTool.getInt(mapData.getChildByPath("info/consumeItemCoolTime"), 0))
                map.setOnUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onUserEnter"), str(mapid)))
                if mapData.getChildByPath("shipObj") is not None:
                    map.setBoat(True)
                else:
                    map.setBoat(False)
                self.maps.put(omapid, map)
            finally:
                self.lock.unlock()
        return map

    def HealMap(self, mapid: int) -> None:
        with self.maps:  # synchronized
            if (mapid in self.DeStorymaps):
                self.DeStorymaps.remove(mapid)

    def destroyMap(self, mapid: int, Remove: bool) -> bool:
        with self.maps:  # synchronized
            if (mapid in self.maps):
                if Remove:
                    self.DeStorymaps.put(mapid, 0)
                    self.maps.remove(mapid)
                return self.maps.remove(mapid) is not None
        return False

    def destroyMap_mapid(self, mapid: int) -> bool:
        return self.destroyMap(mapid, False)

    def getInstanceMap(self, instanceid: int) -> Any:
        return self.instanceMap.get(instanceid)

    def removeInstanceMap(self, instanceid: int) -> None:
        if self.isInstanceMapLoaded(instanceid):
            self.getInstanceMap(instanceid).checkStates("")
            self.instanceMap.remove(instanceid)

    def removeMap(self, instanceid: int) -> None:
        if self.isMapLoaded(instanceid):
            self.getMap(instanceid).checkStates("")
            self.maps.remove(instanceid)

    def CreateInstanceMap(self, mapid: int, respawns: bool, npcs: bool, reactors: bool, instanceid: int) -> Any:
        if self.isInstanceMapLoaded(instanceid):
            return self.getInstanceMap(instanceid)
        mapData = MapleMapFactory.source.getData(self.getMapName(mapid))
        link = mapData.getChildByPath("info/link")
        if link is not None:
            mapData = MapleMapFactory.source.getData(self.getMapName(MapleDataTool.getIntConvert("info/link", mapData)))
        monsterRate = 0.0
        if respawns:
            mobRate = mapData.getChildByPath("info/mobRate")
            if mobRate is not None:
                monsterRate = mobRate.getData()
        map = MapleMap(mapid, self.channel, MapleDataTool.getInt("info/returnMap", mapData), monsterRate)
        portalFactory = PortalFactory()
        for portal in mapData.getChildByPath("portal"):
            map.addPortal(portalFactory.makePortal(MapleDataTool.getInt(portal.getChildByPath("pt")), portal))
        allFootholds = []
        lBound = Point()
        uBound = Point()
        for footRoot in mapData.getChildByPath("foothold"):
            for footCat in footRoot:
                for footHold in footCat:
                    fh = MapleFoothold(Point(MapleDataTool.getInt(footHold.getChildByPath("x1")), MapleDataTool.getInt(footHold.getChildByPath("y1"))), Point(MapleDataTool.getInt(footHold.getChildByPath("x2")), MapleDataTool.getInt(footHold.getChildByPath("y2"))), int(footHold.getName()))
                    fh.setPrev(MapleDataTool.getInt(footHold.getChildByPath("prev")))
                    fh.setNext(MapleDataTool.getInt(footHold.getChildByPath("next")))
                    if fh.getX1() < lBound.x:
                        lBound.x = fh.getX1()
                    if fh.getX2() > uBound.x:
                        uBound.x = fh.getX2()
                    if fh.getY1() < lBound.y:
                        lBound.y = fh.getY1()
                    if fh.getY2() > uBound.y:
                        uBound.y = fh.getY2()
                    allFootholds.add(fh)
        fTree = MapleFootholdTree(lBound, uBound)
        for fh2 in allFootholds:
            fTree.insert(fh2)
        map.setFootholds(fTree)
        bossid = -1
        msg = None
        if mapData.getChildByPath("info/timeMob") is not None:
            bossid = MapleDataTool.getInt(mapData.getChildByPath("info/timeMob/id"), 0)
            msg = MapleDataTool.getString(mapData.getChildByPath("info/timeMob/message"), None)
        for life in mapData.getChildByPath("life"):
            type = MapleDataTool.getString(life.getChildByPath("type"))
            if npcs or not type == ("n"):
                myLife = self.loadLife(life, MapleDataTool.getString(life.getChildByPath("id")), type, mapid)
                if myLife is None:
                    continue
                if isinstance(myLife, MapleMonster):
                    mob = myLife
                    map.addMonsterSpawn(mob, MapleDataTool.getInt("mobTime", life, 0), MapleDataTool.getInt("team", life, -1), (mob.getId() == bossid) ? msg : None)
                else:
                    map.addMapObject(myLife)
        self.addAreaBossSpawn(map)
        map.setCreateMobInterval(MapleDataTool.getInt(mapData.getChildByPath("info/createMobInterval"), 9000))
        map.loadMonsterRate(True)
        map.setNodes(self.loadNodes(mapid, mapData))
        if reactors and mapData.getChildByPath("reactor") is not None:
            for reactor in mapData.getChildByPath("reactor"):
                id = MapleDataTool.getString(reactor.getChildByPath("id"))
                if id is not None:
                    map.spawnReactor(self.loadReactor(reactor, id, MapleDataTool.getInt(reactor.getChildByPath("f"), 0)))
        try:
            map.setMapName(MapleDataTool.getString("mapName", MapleMapFactory.nameData.getChildByPath(self.getMapStringName(mapid)), ""))
            map.setStreetName(MapleDataTool.getString("streetName", MapleMapFactory.nameData.getChildByPath(self.getMapStringName(mapid)), ""))
        except Exception as e:
            map.setMapName("")
            map.setStreetName("")
        map.setClock(MapleDataTool.getInt(mapData.getChildByPath("info/clock"), 0) > 0)
        map.setEverlast(MapleDataTool.getInt(mapData.getChildByPath("info/everlast"), 0) > 0)
        map.setTown(MapleDataTool.getInt(mapData.getChildByPath("info/town"), 0) > 0)
        map.setSoaring(MapleDataTool.getInt(mapData.getChildByPath("info/needSkillForFly"), 0) > 0)
        map.setForceMove(MapleDataTool.getInt(mapData.getChildByPath("info/lvForceMove"), 0))
        map.setHPDec(MapleDataTool.getInt(mapData.getChildByPath("info/decHP"), 0))
        map.setHPDecInterval(MapleDataTool.getInt(mapData.getChildByPath("info/decHPInterval"), 10000))
        map.setHPDecProtect(MapleDataTool.getInt(mapData.getChildByPath("info/protectItem"), 0))
        map.setForcedReturnMap(MapleDataTool.getInt(mapData.getChildByPath("info/forcedReturn"), 999999999))
        map.setTimeLimit(MapleDataTool.getInt(mapData.getChildByPath("info/timeLimit"), -1))
        map.setFieldType(MapleDataTool.getInt(mapData.getChildByPath("info/fieldType"), 0))
        map.setFieldLimit(MapleDataTool.getInt(mapData.getChildByPath("info/fieldLimit"), 0))
        map.setFirstUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onFirstUserEnter"), ""))
        map.setUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onUserEnter"), ""))
        map.setRecoveryRate(MapleDataTool.getFloat(mapData.getChildByPath("info/recovery"), 1.0))
        map.setFixedMob(MapleDataTool.getInt(mapData.getChildByPath("info/fixedMobCapacity"), 0))
        map.setConsumeItemCoolTime(MapleDataTool.getInt(mapData.getChildByPath("info/consumeItemCoolTime"), 0))
        map.setOnUserEnter(MapleDataTool.getString(mapData.getChildByPath("info/onUserEnter"), str(mapid)))
        if mapData.getChildByPath("shipObj") is not None:
            map.setBoat(True)
        else:
            map.setBoat(False)
        self.instanceMap.put(instanceid, map)
        return map

    def getLoadedMaps(self) -> int:
        return self.maps

    def isMapLoaded(self, mapId: int) -> bool:
        return (mapId in self.maps)

    def isInstanceMapLoaded(self, instanceid: int) -> bool:
        return (instanceid in self.instanceMap)

    def clearLoadedMap(self) -> None:
        self.maps.clear()

    def getAllMaps(self) -> list:
        return self.maps.values()

    def getAllInstanceMaps(self) -> list:
        return self.instanceMap.values()

    def loadLife_life_id_type_mapid(self, life: Any, id: str, type: str, mapid: int) -> Any:
        pb_map = { 910000000 }
        pb_npc = { 9310059, 9310022 }
        myLife = MapleLifeFactory.getLife(int(id), type)
        if myLife is None:
            return None
        for m in range(len(pb_map)):
            if mapid == pb_map[m]:
                for i in range(len(pb_npc)):
                    if int(id) == pb_npc[i]:
                        return None
        myLife.setCy(MapleDataTool.getInt(life.getChildByPath("cy")))
        dF = life.getChildByPath("f")
        if dF is not None:
            myLife.setF(MapleDataTool.getInt(dF))
        myLife.setFh(MapleDataTool.getInt(life.getChildByPath("fh")))
        myLife.setRx0(MapleDataTool.getInt(life.getChildByPath("rx0")))
        myLife.setRx1(MapleDataTool.getInt(life.getChildByPath("rx1")))
        myLife.setPosition(Point(MapleDataTool.getInt(life.getChildByPath("x")), MapleDataTool.getInt(life.getChildByPath("y"))))
        if MapleDataTool.getInt("hide", life, 0) == 1 and isinstance(myLife, MapleNPC):
            myLife.setHide(True)
        return myLife

    def loadReactor(self, reactor: Any, id: str, FacingDirection: int) -> Any:
        stats = MapleReactorFactory.getReactor(int(id))
        myReactor = MapleReactor(stats, int(id))
        stats.setFacingDirection(FacingDirection)
        myReactor.setPosition(Point(MapleDataTool.getInt(reactor.getChildByPath("x")), MapleDataTool.getInt(reactor.getChildByPath("y"))))
        myReactor.setDelay(MapleDataTool.getInt(reactor.getChildByPath("reactorTime")) * 1000)
        myReactor.setState(0)
        myReactor.setName(MapleDataTool.getString(reactor.getChildByPath("name"), ""))
        return myReactor

    def getMapName(self, mapid: int) -> str:
        mapName = StringUtil.getLeftPaddedStr(Integer.toString(mapid), '0', 9)
        builder = ""
        builder.append(mapid / 100000000)
        builder.append("/")
        builder.append(mapName)
        builder.append(".img")
        mapName = builder
        return mapName

    def getMapStringName(self, mapid: int) -> str:
        builder = ""
        if mapid < 100000000:
            builder.append("maple")
        elif (mapid >= 100000000 and mapid < 200000000) or mapid / 100000 == 5540:
            builder.append("victoria")
        elif mapid >= 200000000 and mapid < 300000000:
            builder.append("ossyria")
        elif mapid >= 300000000 and mapid < 400000000:
            builder.append("elin")
        elif mapid >= 500000000 and mapid < 510000000:
            builder.append("thai")
        elif mapid >= 540000000 and mapid < 600000000:
            builder.append("SG")
        elif mapid >= 600000000 and mapid < 620000000:
            builder.append("MasteriaGL")
        elif (mapid >= 670000000 and mapid < 677000000) or (mapid >= 678000000 and mapid < 682000000):
            builder.append("global")
        elif mapid >= 677000000 and mapid < 678000000:
            builder.append("Episode1GL")
        elif mapid >= 682000000 and mapid < 683000000:
            builder.append("HalloweenGL")
        elif mapid >= 683000000 and mapid < 684000000:
            builder.append("event")
        elif mapid >= 684000000 and mapid < 685000000:
            builder.append("event_5th")
        elif mapid >= 700000000 and mapid < 700000300:
            builder.append("wedding")
        elif mapid >= 701000000 and mapid < 701020000:
            builder.append("china")
        elif mapid >= 800000000 and mapid < 900000000:
            builder.append("jp")
        elif mapid >= 700000000 and mapid < 782000002:
            builder.append("chinese")
        else:
            builder.append("etc")
        builder.append("/")
        builder.append(mapid)
        return builder

    def setChannel(self, channel: int) -> None:
        self.channel = channel

    def addAreaBossSpawn(self, map: Any) -> None:
        monsterid = -1
        mobtime = -1
        msg = None
        pos1 = None
        pos2 = None
        pos3 = None
        # switch (map.getId()):
            # case 104000400:
                mobtime = 240
                monsterid = 2220000
                msg = "红蜗牛王出现了"
                pos1 = Point(439, 185)
                pos2 = Point(301, -85)
                pos3 = Point(107, -355)
                break
            # case 101030404:
                mobtime = 240
                monsterid = 3220000
                msg = "树妖王出现了,小心被他的树枝插到丁丁"
                pos1 = Point(867, 1282)
                pos2 = Point(810, 1570)
                pos3 = Point(838, 2197)
                break
            # case 110040000:
                mobtime = 240
                monsterid = 5220001
                msg = "巨居蟹出现了,小心你的丁丁被他夹断"
                pos1 = Point(-355, 179)
                pos2 = Point(-1283, -113)
                pos3 = Point(-571, -593)
                break
            # case 250010304:
                mobtime = 240
                monsterid = 7220000
                msg = "流浪熊出现了,我他妈会放雷电啊"
                pos1 = Point(-210, 33)
                pos2 = Point(-234, 393)
                pos3 = Point(-654, 33)
                break
            # case 200010300:
                mobtime = 240
                monsterid = 8220000
                msg = "艾利杰出现了"
                pos1 = Point(665, 83)
                pos2 = Point(672, -217)
                pos3 = Point(-123, -217)
                break
            # case 250010503:
                mobtime = 240
                monsterid = 7220002
                msg = "喵仙怪人出现了,小心被他CC到死喔"
                pos1 = Point(-303, 543)
                pos2 = Point(227, 543)
                pos3 = Point(719, 543)
                break
            # case 222010310:
                mobtime = 240
                monsterid = 7220001
                msg = "九尾妖狐出现了"
                pos1 = Point(-169, -147)
                pos2 = Point(-517, 93)
                pos3 = Point(247, 93)
                break
            # case 107000300:
                mobtime = 240
                monsterid = 6220000
                msg = "沼泽巨鳄大大了"
                pos1 = Point(710, 118)
                pos2 = Point(95, 119)
                pos3 = Point(-535, 120)
                break
            # case 100040105:
                mobtime = 240
                monsterid = 5220002
                msg = "僵尸猴王出现了"
                pos1 = Point(1000, 278)
                pos2 = Point(557, 278)
                pos3 = Point(95, 278)
                break
            # case 100040106:
                mobtime = 240
                monsterid = 5220002
                msg = "The blue fog became darker when Faust appeared."
                pos1 = Point(1000, 278)
                pos2 = Point(557, 278)
                pos3 = Point(95, 278)
                break
            # case 220050100:
                mobtime = 240
                monsterid = 5220003
                msg = "Click clock! Timer has appeared with an irregular clock sound."
                pos1 = Point(-467, 1032)
                pos2 = Point(532, 1032)
                pos3 = Point(-47, 1032)
                break
            # case 221040301:
                mobtime = 240
                monsterid = 6220001
                msg = "葛雷金刚出现了"
                pos1 = Point(-4134, 416)
                pos2 = Point(-4283, 776)
                pos3 = Point(-3292, 776)
                break
            # case 240040401:
                mobtime = 240
                monsterid = 8220003
                msg = "寒霜冰龙出现了"
                pos1 = Point(-15, 2481)
                pos2 = Point(127, 1634)
                pos3 = Point(159, 1142)
                break
            # case 260010201:
                mobtime = 240
                monsterid = 3220001
                msg = "仙人長老出現了"
                pos1 = Point(-215, 275)
                pos2 = Point(298, 275)
                pos3 = Point(592, 275)
                break
            # case 261030000:
                mobtime = 240
                monsterid = 8220002
                msg = "奇美拉出现了,小心他的BB弹"
                pos1 = Point(-1094, -405)
                pos2 = Point(-772, -116)
                pos3 = Point(-108, 181)
                break
            # case 230020100:
                mobtime = 240
                monsterid = 4220000
                msg = "火蚌壳出现了"
                pos1 = Point(-291, -20)
                pos2 = Point(-272, -500)
                pos3 = Point(-462, 640)
                break
            # default:
                return
        if monsterid > 0:
            map.addAreaMonsterSpawn(MapleLifeFactory.getMonster(monsterid), pos1, pos2, pos3, mobtime, msg)

    def loadNodes(self, mapid: int, mapData: Any) -> Any:
        nodeInfo = MapleMapFactory.mapInfos.get(mapid)
        if nodeInfo is None:
            nodeInfo = MapleNodes(mapid)
            if mapData.getChildByPath("nodeInfo") is not None:
                for node in mapData.getChildByPath("nodeInfo"):
                    try:
                        if node.getName() == ("start"):
                            nodeInfo.setNodeStart(MapleDataTool.getInt(node, 0))
                        elif node.getName() == ("end"):
                            nodeInfo.setNodeEnd(MapleDataTool.getInt(node, 0))
                        else:
                            edges = []
                            if node.getChildByPath("edge") is not None:
                                for edge in node.getChildByPath("edge"):
                                    edges.add(MapleDataTool.getInt(edge, -1))
                            final MapleNodes.MapleNodeInfo mni = new MapleNodes.MapleNodeInfo(int(node.getName()), MapleDataTool.getIntConvert("key", node, 0), MapleDataTool.getIntConvert("x", node, 0), MapleDataTool.getIntConvert("y", node, 0), MapleDataTool.getIntConvert("attr", node, 0), edges)
                            nodeInfo.addNode(mni)
                    except NumberFormatException as ex:
                        pass
                nodeInfo.sortNodes()
            for i in range(1, = 7):
                if mapData.getChildByPath(str(i)) is not None and mapData.getChildByPath(i + "/obj") is not None:
                    for node2 in mapData.getChildByPath(i + "/obj"):
                        sn_count = MapleDataTool.getIntConvert("SN_count", node2, 0)
                        name = MapleDataTool.getString("name", node2, "")
                        speed = MapleDataTool.getIntConvert("speed", node2, 0)
                        if sn_count > 0 and speed > 0:
                            if name == (""):
                                continue
                            SN = []
                            for x in range(sn_count):
                                SN.add(MapleDataTool.getIntConvert("SN" + x, node2, 0))
                            final MapleNodes.MaplePlatform mni2 = new MapleNodes.MaplePlatform(name, MapleDataTool.getIntConvert("start", node2, 2), speed, MapleDataTool.getIntConvert("x1", node2, 0), MapleDataTool.getIntConvert("y1", node2, 0), MapleDataTool.getIntConvert("x2", node2, 0), MapleDataTool.getIntConvert("y2", node2, 0), MapleDataTool.getIntConvert("r", node2, 0), SN)
                            nodeInfo.addPlatform(mni2)
            if mapData.getChildByPath("area") is not None:
                for area in mapData.getChildByPath("area"):
                    x2 = MapleDataTool.getInt(area.getChildByPath("x1"))
                    y1 = MapleDataTool.getInt(area.getChildByPath("y1"))
                    x3 = MapleDataTool.getInt(area.getChildByPath("x2"))
                    y2 = MapleDataTool.getInt(area.getChildByPath("y2"))
                    mapArea = Rectangle(x2, y1, x3 - x2, y2 - y1)
                    nodeInfo.addMapleArea(mapArea)
            if mapData.getChildByPath("monsterCarnival") is not None:
                mc = mapData.getChildByPath("monsterCarnival")
                if mc.getChildByPath("mobGenPos") is not None:
                    for area2 in mc.getChildByPath("mobGenPos"):
                        nodeInfo.addMonsterPoint(MapleDataTool.getInt(area2.getChildByPath("x")), MapleDataTool.getInt(area2.getChildByPath("y")), MapleDataTool.getInt(area2.getChildByPath("fh")), MapleDataTool.getInt(area2.getChildByPath("cy")), MapleDataTool.getInt("team", area2, -1))
                if mc.getChildByPath("mob") is not None:
                    for area2 in mc.getChildByPath("mob"):
                        nodeInfo.addMobSpawn(MapleDataTool.getInt(area2.getChildByPath("id")), MapleDataTool.getInt(area2.getChildByPath("spendCP")))
                if mc.getChildByPath("guardianGenPos") is not None:
                    for area2 in mc.getChildByPath("guardianGenPos"):
                        nodeInfo.addGuardianSpawn(Point(MapleDataTool.getInt(area2.getChildByPath("x")), MapleDataTool.getInt(area2.getChildByPath("y"))), MapleDataTool.getInt("team", area2, -1))
                if mc.getChildByPath("skill") is not None:
                    for area2 in mc.getChildByPath("skill"):
                        nodeInfo.addSkillId(MapleDataTool.getInt(area2))
            MapleMapFactory.mapInfos.put(mapid, nodeInfo)
        return nodeInfo

    def getAllLoadedMaps(self) -> list:
        ret = []
        self.lock.lock()
        try:
            ret.addAll(self.maps.values())
            ret.addAll(self.instanceMap.values())
        finally:
            self.lock.unlock()
        return ret

