"""
EventManager - Converted from Java source
Original: scripting/EventManager.java
Package: scripting
"""

from concurrent.futures import Future
from configparser import ConfigParser
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Collection
from typing import Dict
from typing import List
from typing import Optional, Any
import json
import logging
import pymysql
import sched
import threading
import tkinter

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from server.MapleSquad import *  # TODO: import specific classes
# from server.Randomizer import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.events.MapleEvent import *  # TODO: import specific classes
# from server.events.MapleEventType import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.OverrideMonsterStats import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class EventManager:
    """
    Class EventManager
    """

    def __init__(self, cserv: Any, iv: Any, name: str):
        self.iv = None
        self.channel = 0
        self.instances = {}
        self.props = None
        self.name = ""
        self.instances = new WeakHashMap<String, EventInstanceManager>()
        self.props = Properties()
        self.iv = iv
        self.channel = cserv.getChannel()
        self.name = name

    # Static initializer
    # EventManager.eventChannel = new int[2]


    def cancel(self) -> None:
        try:
            self.iv.invokeFunction("cancelSchedule", None)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : cancelSchedule:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : cancelSchedule:\n" + ex)

    def schedule(self, methodName: str, delay: int) -> Any:
        return Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                try:
                    EventManager.self.iv.invokeFunction(methodName, None)
                except Exception as ex:
                    print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)
                    FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)

    def run(self) -> None:
        try:
            EventManager.self.iv.invokeFunction(methodName, None)
        except Exception as ex:
            print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)

    def schedule_methodName_delay_eim(self, methodName: str, delay: int, eim: Any) -> Any:
        return Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                try:
                    EventManager.self.iv.invokeFunction(methodName, eim)
                except Exception as ex:
                    print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)
                    FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)

    def schedule_methodName_eim_delay(self, methodName: str, eim: Any, delay: int) -> Any:
        return Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                try:
                    EventManager.self.iv.invokeFunction(methodName, eim)
                except Exception as ex:
                    print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)
                    FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)

    def scheduleAtTimestamp(self, methodName: str, timestamp: int) -> Any:
        return Timer.EventTimer.getInstance().scheduleAtTimestamp(Runnable()
            public void run()
                try:
                    EventManager.self.iv.invokeFunction(methodName, None)
                except ScriptException as ex:
                    print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex)
                except NoSuchMethodException as ex2:
                    print("Event name : " + EventManager.self.name + ", method Name : " + methodName + ":\n" + ex2)

    def getChannel(self) -> int:
        return self.channel

    def getChannelServer(self) -> Any:
        return ChannelServer.getInstance(self.channel)

    @classmethod
    def get_instance(cls, name: str) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getInstances(self) -> list:
        return Collections.unmodifiableCollection((Collection<? extends EventInstanceManager>)self.instances.values())

    def newInstance(self, name: str) -> Any:
        ret = EventInstanceManager(this, name, self.channel)
        self.instances.put(name, ret)
        return ret

    def disposeInstance(self, name: str) -> None:
        self.instances.remove(name)
        if self.getProperty("state") is not None && self.instances == 0:
            self.setProperty("state", "0")
        if self.getProperty("leader") is not None && self.instances == 0 && self.getProperty("leader") == ("False"):
            self.setProperty("leader", "True")
        if self.name == ("CWKPQ"):
            squad = ChannelServer.getInstance(self.channel).getMapleSquad("CWKPQ")
            if squad is not None:
                squad.clear()

    def getIv(self) -> Any:
        return self.iv

    def setProperty(self, key: str, value: str) -> None:
        self.props.setProperty(key, value)

    def getProperty(self, key: str) -> str:
        return self.props.getProperty(key)

    def getProperties(self) -> Any:
        return self.props

    def getName(self) -> str:
        return self.name

    def startInstance(self) -> None:
        try:
            self.iv.invokeFunction("setup", None)
        except Exception as ex:
            ex.printStackTrace()
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup:\n" + ex)

    def startInstance_mapid_chr(self, mapid: str, chr: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", mapid)
            eim.registerCarnivalParty(chr, chr.getMap(), 0)
        except Exception as ex:
            ex.printStackTrace()
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup:\n" + ex)

    def startInstance_Party(self, mapid: str, chr: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", mapid)
            eim.registerParty(chr.getParty(), chr.getMap())
        except Exception as ex:
            ex.printStackTrace()
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup:\n" + ex)

    def startInstance_character_leader(self, character: Any, leader: str) -> None:
        try:
            eim = self.iv.invokeFunction("setup", None)
            eim.registerPlayer(character)
            eim.setProperty("leader", leader)
            eim.setProperty("guildid", str(character.getGuildId()))
            self.setProperty("guildid", str(character.getGuildId()))
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-Guild:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-Guild:\n" + ex)

    def startInstance_CharID(self, character: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", character.getId())
            eim.registerPlayer(character)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-CharID:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-CharID:\n" + ex)

    def startInstance_character(self, character: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", None)
            eim.registerPlayer(character)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-character:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-character:\n" + ex)

    def startInstance_party_map(self, party: Any, map: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", party.getId())
            eim.registerParty(party, map)
        except ScriptException as ex:
            print("Event name : " + self.name + ", method Name : setup-partyid:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-partyid:\n" + ex)
        except Exception as ex2:
            self.startInstance_NoID(party, map, ex2)

    def startInstance_NoID(self, party: Any, map: Any) -> None:
        self.startInstance_NoID(party, map, None)

    def startInstance_NoID_party_map_old(self, party: Any, map: Any, old: Any) -> None:
        try:
            eim = self.iv.invokeFunction("setup", None)
            eim.registerParty(party, map)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-party:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-party:\n" + ex + "\n" + ((old is None) ? "no old exception" : old))

    def startInstance_eim_leader(self, eim: Any, leader: str) -> None:
        try:
            self.iv.invokeFunction("setup", eim)
            eim.setProperty("leader", leader)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-leader:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-leader:\n" + ex)

    def startInstance_squad_map(self, squad: Any, map: Any) -> None:
        self.startInstance(squad, map, -1)

    def startInstance_squad_map_questID(self, squad: Any, map: Any, questID: int) -> None:
        if squad.getStatus() == 0:
            return
        if !squad.getLeader().isGM():
            if squad.getMembers() < squad.getType().i:
                squad.getLeader().dropMessage(5, "这个远征队至少要有 " + squad.getType().i + " 人以上才可以开战.")
                return
            if self.name == ("CWKPQ") && squad.getJobs() < 5:
                squad.getLeader().dropMessage(5, "The squad requires members from every type of job.")
                return
        try:
            eim = self.iv.invokeFunction("setup", squad.getLeaderName())
            eim.registerSquad(squad, map, questID)
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-squad:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name : " + self.name + ", method Name : setup-squad:\n" + ex)

    def startInstance_squad_map_bossid(self, squad: Any, map: Any, bossid: str) -> None:
        if squad.getStatus() == 0:
            return
        if !squad.getLeader().isGM():
            mapid = map.getId()
            chrSize = 0
            for chr in squad.getMembers():
                player = squad.getChar(chr)
                if player is not None && player.getMapId() == mapid:
                    chrSize += 1
            if chrSize < squad.getType().i:
                squad.getLeader().dropMessage(5, "远征队中人员少于 " + squad.getType().i + " 人，无法开始远征任务。注意必须队伍中的角色在线且在同一地图。当前人数: " + chrSize)
                return
            if self.name == ("CWKPQ") && squad.getJobs() < 5:
                squad.getLeader().dropMessage(5, "远征队中成员职业的类型小于5种，无法开始远征任务。")
                return
        try:
            eim = self.iv.invokeFunction("setup", squad.getLeaderName())
            eim.registerSquad(squad, map, int(bossid))
        except Exception as ex:
            print("Event name : " + self.name + ", method Name : setup-squad:\n" + ex)
            FileoutputUtil.log("logs/Script_Except.log", "Event name : " + self.name + ", method Name : setup-squad:\n" + ex)

    def warpAllPlayer(self, from: int, to: int) -> None:
        tomap = self.getMapFactory().getMap(to)
        frommap = self.getMapFactory().getMap(from)
        list = frommap.getCharactersThreadsafe()
        if tomap is not None && frommap is not None && list is not None && frommap.getCharactersSize() > 0:
            for mmo in list:
                (mmo).changeMap(tomap, tomap.getPortal(0))

    def setAllPlayerBossLog(self, map: int, bosslog: str, type: int) -> None:
        frommap = self.getMapFactory().getMap(map)
        list = frommap.getCharactersThreadsafe()
        if frommap is not None && list is not None && frommap.getCharactersSize() > 0:
            for mmo in list:
                (mmo).setBossLog(bosslog, type)

    def online(self) -> int:
        con = DatabaseConnection.getConnection()
        count = 0
        try:
            ps = con.prepareStatement("SELECT count(*) as cc FROM accounts WHERE loggedin = 2")
            re = ps.executeQuery()
            while re.next():
                count = re.getInt("cc")
        except Exception as ex:
            Logger.getLogger(EventInstanceManager.class.getName()).log(Level.SEVERE, None, ex)
        return count

    def getMapFactory(self) -> Any:
        return self.getChannelServer().getMapFactory()

    def newMonsterStats(self) -> Any:
        return OverrideMonsterStats()

    def newCharList(self) -> list:
        return []

    def getMonster(self, id: int) -> Any:
        return MapleLifeFactory.getMonster(id)

    def broadcastShip(self, mapid: int, effect: int) -> None:
        self.getMapFactory().getMap(mapid).broadcastMessage(MaplePacketCreator.boatPacket(effect))

    def broadcastChangeMusic(self, mapid: int) -> None:
        self.getMapFactory().getMap(mapid).broadcastMessage(MaplePacketCreator.musicChange("Bgm04/ArabPirate"))

    def broadcastYellowMsg(self, msg: str) -> None:
        pass

    def broadcastServerMsg(self, type: int, msg: str, weather: bool) -> None:
        if !weather:
            self.getChannelServer().broadcastPacket(MaplePacketCreator.serverNotice(type, msg))
        else:
            for load in self.getMapFactory().getAllMaps():
                if load.getCharactersSize() > 0:
                    load.startMapEffect(msg, type)

    def scheduleRandomEvent(self) -> bool:
        omg = False
        for i in range(EventManager.len(eventChannel)):
            omg |= self.scheduleRandomEventInChannel(EventManager.eventChannel[i])
        return omg

    def scheduleRandomEventInChannel(self, chz: int) -> bool:
        cs = ChannelServer.getInstance(chz)
        if cs is None || cs.getEvent() > -1:
            return False
        t = None
        x = None
        = None
        while t is None:
            values = MapleEventType.values()
            length = len(values), i = 0
            while i < length:
                x = values[i]
                if Randomizer.nextInt(MapleEventType.values().length) == 0:
                    break
        msg = MapleEvent.scheduleEvent(t, cs)
        if msg > 0:
            self.broadcastYellowMsg(msg)
            return False
        Timer.EventTimer.getInstance().schedule(Runnable()
            public void run()
                if cs.getEvent() >= 0:
                    MapleEvent.setEvent(cs, True)
        return True

    def setWorldEvent(self) -> None:
        for i in range(EventManager.len(eventChannel)):
            EventManager.eventChannel[i] = Randomizer.nextInt(ChannelServer.getAllInstances()) + i

