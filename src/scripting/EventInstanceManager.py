"""
EventInstanceManager - Converted from Java source
Original: scripting/EventInstanceManager.java
Package: scripting
"""

from concurrent.futures import Future
from configparser import ConfigParser
from threading import Lock
from threading import RLock
from typing import Dict
from typing import List
from typing import Optional, Any
import json
import sched
import threading
import time
import tkinter

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleQuestStatus import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.MapleParty import *  # TODO: import specific classes
# from handling.world.MaplePartyCharacter import *  # TODO: import specific classes
# from server.MapleCarnivalParty import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleSquad import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.UIPacket import *  # TODO: import specific classes


class EventInstanceManager:
    """
    Class EventInstanceManager
    """

    def __init__(self, em: Any, name: str, channel: int):
        self.chars = []
        self.dced = []
        self.mobs = []
        self.killCount = {}
        self.em = None
        self.channel = 0
        self.name = ""
        self.props = None
        self.timeStarted = 0
        self.eventTime = 0
        self.mapIds = []
        self.isInstanced = []
        self.mutex = None
        self.rL = None
        self.wL = None
        self.disposed = False
        self.chars = []
        self.dced = []
        self.mobs = []
        self.killCount = {}
        self.props = Properties()
        self.timeStarted = 0
        self.eventTime = 0
        self.mapIds = []
        self.isInstanced = []
        self.mutex = ReentrantReadWriteLock()
        self.rL = self.mutex.readLock()
        self.wL = self.mutex.writeLock()
        self.disposed = False
        self.em = em
        self.name = name
        self.channel = channel


    def registerPlayer(self, chr: Any) -> None:
        if self.disposed or chr is None:
            return
        try:
            self.wL.lock()
            try:
                self.chars.add(chr)
            finally:
                self.wL.unlock()
            chr.setEventInstance(this)
            self.em.getIv().invokeFunction("playerEntry", this, chr)
        except TypeError as ex:
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex)
            ex.printStackTrace()
        except Exception as ex2:
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerEntry:\n" + ex2)
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerEntry:\n" + ex2)

    def changedMap(self, chr: Any, mapid: int) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("changedMap", this, chr, mapid)
        except NullPointerException as ex2:
            pass
        except Exception as ex:
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "副本名称" + self.em.getName() + ", 实例名称 : " + self.name + ", 方法名称 : changedMap:\n" + ex)
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : changedMap:\n" + ex)

    def timeOut(self, delay: int, eim: Any) -> None:
        def _task_1():
            if EventInstanceManager.self.disposed or eim is None or EventInstanceManager.self.em is None:
                return
            try:
                EventInstanceManager.self.em.getIv().invokeFunction("scheduledTimeout", eim)
            except Exception as ex:
                FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name : scheduledTimeout:\n" + ex)
                print("Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name : scheduledTimeout:\n" + ex)

        if self.disposed or eim is None:
            return
        self.eventTimer = Timer.EventTimer.getInstance().schedule(_task_1, delay)

    def run(self) -> None:
        if EventInstanceManager.self.disposed or eim is None or EventInstanceManager.self.em is None:
            return
        try:
            EventInstanceManager.self.em.getIv().invokeFunction("scheduledTimeout", eim)
        except Exception as ex:
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name : scheduledTimeout:\n" + ex)
            print("Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name : scheduledTimeout:\n" + ex)

    def forceRemovePlayerByCharName(self, name: str) -> None:
        ChannelServer.forceRemovePlayerByCharName(name)

    def stopEventTimer(self) -> None:
        self.eventTime = 0
        self.timeStarted = 0
        if self.eventTimer is not None:
            self.eventTimer.cancel(False)

    def restartEventTimer(self, time: int) -> None:
        try:
            if self.disposed:
                return
            self.timeStarted = int(time.time() * 1000)
            self.eventTime = time
            if self.eventTimer is not None:
                self.eventTimer.cancel(False)
            self.eventTimer = None
            timesend = time / 1000
            for chr in self.getPlayers():
                chr.getClient().getSession().write(MaplePacketCreator.getClock(timesend))
            self.timeOut(time, this)
        except Exception as ex:
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex)
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : restartEventTimer:\n")
            ex.printStackTrace()

    def isSquadLeader(self, tt: Any, ttt: Any) -> bool:
        return tt.getClient().getChannelServer().getMapleSquad(ttt).getLeader() == (tt)

    def startEventTimer(self, time: int) -> None:
        self.restartEventTimer(time)

    def getInstanceId(self) -> int:
        return ChannelServer.getInstance(1).getInstanceId()

    def addInstanceId(self) -> None:
        ChannelServer.getInstance(1).addInstanceId()

    def isTimerStarted(self) -> bool:
        return self.eventTime > 0 and self.timeStarted > 0

    def getTimeLeft(self) -> int:
        return self.eventTime - (int(time.time() * 1000) - self.timeStarted)

    def registerParty(self, party: Any, map: Any) -> None:
        if self.disposed:
            return
        for pc in party.getMembers():
            c = map.getCharacterById(pc.getId())
            self.registerPlayer(c)

    def unregisterPlayer(self, chr: Any) -> None:
        if self.disposed:
            chr.setEventInstance(None)
            return
        self.wL.lock()
        try:
            self.unregisterPlayer_NoLock(chr)
        finally:
            self.wL.unlock()

    def unregisterPlayer_NoLock(self, chr: Any) -> bool:
        if self.name == ("CWKPQ"):
            squad = ChannelServer.getInstance(self.channel).getMapleSquad("CWKPQ")
            if squad is not None:
                squad.removeMember(chr.getName())
                if squad.getLeaderName() == (chr.getName()):
                    self.em.setProperty("leader", "False")
        chr.setEventInstance(None)
        if self.disposed:
            return False
        if (chr in self.chars):
            self.chars.remove(chr)
            return True
        return False

    def disposeIfPlayerBelow(self, size: int, towarp: int) -> bool:
        if self.disposed:
            return True
        map = None
        if towarp > 0:
            map = self.getMapFactory().getMap(towarp)
        self.wL.lock()
        try:
            if self.chars <= size:
                chrs = []
                for chr in chrs:
                    self.unregisterPlayer_NoLock(chr)
                    if towarp > 0:
                        chr.changeMap(map, map.getPortal(0))
                self.dispose_NoLock()
                return True
        finally:
            self.wL.unlock()
        return False

    def saveBossQuest(self, points: int) -> None:
        if self.disposed:
            return
        for chr in self.getPlayers():
            record = chr.getQuestNAdd(MapleQuest.getInstance(150001))
            if record.getCustomData() is not None:
                record.setCustomData(str(points + int(record.getCustomData())))
            else:
                record.setCustomData(str(points))

    def getPlayers(self) -> list:
        if self.disposed:
            return Collections.emptyList()
        self.rL.lock()
        try:
            return []
        finally:
            self.rL.unlock()

    def getDisconnected(self) -> list:
        return self.dced

    def getPlayerCount(self) -> int:
        if self.disposed:
            return 0
        return self.chars

    def registerMonster(self, mob: Any) -> None:
        if self.disposed:
            return
        self.mobs.add(mob)
        mob.setEventInstance(this)

    def unregisterMonster(self, mob: Any) -> None:
        mob.setEventInstance(None)
        if self.disposed:
            return
        self.mobs.remove(mob)
        if self.mobs == 0:
            try:
                self.em.getIv().invokeFunction("allMonstersDead", this)
            except Exception as ex:
                FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : allMonstersDead:\n" + ex)
                print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : allMonstersDead:\n" + ex)

    def playerKilled(self, chr: Any) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("playerDead", this, chr)
        except Exception as ex:
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerDead:\n" + ex)
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerDead:\n" + ex)

    def revivePlayer(self, chr: Any) -> bool:
        if self.disposed:
            return False
        try:
            b = self.em.getIv().invokeFunction("playerRevive", this, chr)
            if isinstance(b, Boolean):
                return b
        except Exception as ex:
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerRevive:\n" + ex)
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerRevive:\n" + ex)
        return True

    def playerDisconnected(self, chr: Any, idz: int) -> None:
        if self.disposed:
            return
        ret = None
        try:
            ret = (self.em.getIv().invokeFunction("playerDisconnected", this, chr)).byteValue()
        except Exception as e:
            ret = 0
        self.wL.lock()
        try:
            if self.disposed:
                return
            self.dced.add(idz)
            if chr is not None:
                self.unregisterPlayer_NoLock(chr)
            if ret == 0:
                if self.getPlayerCount() <= 0:
                    self.dispose_NoLock()
            elif (ret > 0 and self.getPlayerCount() < ret) or (ret < 0 and (self.isLeader(chr) or self.getPlayerCount() < ret * -1)):
                chrs = []
                for player in chrs:
                    if player.getId() != idz:
                        self.removePlayer(player)
                self.dispose_NoLock()
        except Exception as ex:
            ex.printStackTrace()
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex)
        finally:
            self.wL.unlock()

    def monsterKilled(self, chr: Any, mob: Any) -> None:
        if self.disposed:
            return
        try:
            kc = self.killCount.get(chr.getId())
            inc = (self.em.getIv().invokeFunction("monsterValue", this, mob.getId()))
            if self.disposed:
                return
            if kc is None:
                kc = inc
            else:
                kc += inc
            self.killCount.put(chr.getId(), kc)
            if chr.getCarnivalParty() is not None and (mob.getStats().getPoint() > 0 or mob.getStats().getCP() > 0):
                self.em.getIv().invokeFunction("monsterKilled", this, chr, (mob.getStats().getCP() > 0) ? mob.getStats().getCP() : mob.getStats().getPoint())
        except ScriptException as ex:
            print("Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex)
        except NoSuchMethodException as ex2:
            print("Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex2)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex2)
        except Exception as ex3:
            ex3.printStackTrace()
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex3)

    def monsterDamaged(self, chr: Any, mob: Any, damage: int) -> None:
        if self.disposed or mob.getId() != 9700037:
            return
        try:
            self.em.getIv().invokeFunction("monsterDamaged", this, chr, mob.getId(), damage)
        except ScriptException as ex:
            print("Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex)
        except NoSuchMethodException as ex2:
            print("Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex2)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + ((self.em is None) ? "None" : self.em.getName()) + ", Instance name : " + self.name + ", method Name : monsterValue:\n" + ex2)
        except Exception as ex3:
            ex3.printStackTrace()
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex3)

    def getKillCount(self, chr: Any) -> int:
        if self.disposed:
            return 0
        kc = self.killCount.get(chr.getId())
        if kc is None:
            return 0
        return kc

    def dispose_NoLock(self) -> None:
        if self.disposed or self.em is None:
            return
        emN = self.em.getName()
        try:
            self.disposed = True
            for chr in self.chars:
                chr.setEventInstance(None)
            self.chars.clear()
            self.chars = None
            for mob in self.mobs:
                mob.setEventInstance(None)
            self.mobs.clear()
            self.mobs = None
            self.killCount.clear()
            self.killCount = None
            self.dced.clear()
            self.dced = None
            self.timeStarted = 0
            self.eventTime = 0
            self.props.clear()
            self.props = None
            for i in range(self.mapIds):
                if self.isInstanced.get(i):
                    self.getMapFactory().removeInstanceMap(self.mapIds.get(i))
            self.mapIds.clear()
            self.mapIds = None
            self.isInstanced.clear()
            self.isInstanced = None
            self.em.disposeInstance(self.name)
        except Exception as e:
            print("Caused by : " + emN + " instance name: " + self.name + " method: dispose: " + e)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + emN + ", Instance name : " + self.name + ", method Name : dispose:\n" + e)

    def dispose(self) -> None:
        self.wL.lock()
        try:
            self.dispose_NoLock()
        finally:
            self.wL.unlock()

    def getChannelServer(self) -> Any:
        return ChannelServer.getInstance(self.channel)

    def getMobs(self) -> list:
        return self.mobs

    def broadcastPlayerMsg(self, type: int, msg: str) -> None:
        if self.disposed:
            return
        for chr in self.getPlayers():
            chr.getClient().getSession().write(MaplePacketCreator.serverNotice(type, msg))

    def createInstanceMap(self, mapid: int) -> Any:
        if self.disposed:
            return None
        assignedid = self.getChannelServer().getEventSM().getNewInstanceMapId()
        self.mapIds.add(assignedid)
        self.isInstanced.add(True)
        return self.getMapFactory().CreateInstanceMap(mapid, True, True, True, assignedid)

    def createInstanceMapS(self, mapid: int) -> Any:
        if self.disposed:
            return None
        assignedid = self.getChannelServer().getEventSM().getNewInstanceMapId()
        self.mapIds.add(assignedid)
        self.isInstanced.add(True)
        return self.getMapFactory().CreateInstanceMap(mapid, False, False, False, assignedid)

    def setInstanceMap(self, mapid: int) -> Any:
        if self.disposed:
            return self.getMapFactory().getMap(mapid)
        self.mapIds.add(mapid)
        self.isInstanced.add(False)
        return self.getMapFactory().getMap(mapid)

    def getMapFactory(self) -> Any:
        return self.getChannelServer().getMapFactory()

    def getMapInstance(self, args: int) -> Any:
        if self.disposed:
            return None
        try:
            instanced = False
            trueMapID = -1
            if args >= self.mapIds:
                trueMapID = args
            else:
                trueMapID = self.mapIds.get(args)
                instanced = self.isInstanced.get(args)
            map = None
            if not instanced:
                map = self.getMapFactory().getMap(trueMapID)
                if map is None:
                    return None
                if map.getCharactersSize() == 0 and self.em.getProperty("shuffleReactors") is not None and self.em.getProperty("shuffleReactors") == ("True"):
                    map.shuffleReactors()
            else:
                map = self.getMapFactory().getInstanceMap(trueMapID)
                if map is None:
                    return None
                if map.getCharactersSize() == 0 and self.em.getProperty("shuffleReactors") is not None and self.em.getProperty("shuffleReactors") == ("True"):
                    map.shuffleReactors()
            return map
        except TypeError as ex:
            FileoutputUtil.outputFileError(FileoutputUtil.ScriptEx_Log, ex)
            ex.printStackTrace()
            return None

    def schedule(self, methodName: str, delay: int) -> None:
        def _task_1():
            if EventInstanceManager.self.disposed or EventInstanceManager.this is None or EventInstanceManager.self.em is None:
                return
            try:
                EventInstanceManager.self.em.getIv().invokeFunction(methodName, EventInstanceManager.this)
            except NullPointerException as ex2:
                pass
            except Exception as ex:
                print("Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name : " + methodName + ":\n" + ex)
                FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + EventInstanceManager.self.em.getName() + ", Instance name : " + EventInstanceManager.self.name + ", method Name(schedule) : " + methodName + " :\n" + ex)

        if self.disposed:
            return
        Timer.EventTimer.getInstance().schedule(_task_1, delay)

    def getName(self) -> str:
        return self.name

    def setProperty(self, key: str, value: str) -> None:
        if self.disposed:
            return
        self.props.setProperty(key, value)

    def setProperty_key_value_prev(self, key: str, value: str, prev: bool) -> Any:
        if self.disposed:
            return None
        return self.props.setProperty(key, value)

    def getProperty(self, key: str) -> str:
        if self.disposed:
            return ""
        return self.props.getProperty(key)

    def getProperties(self) -> Any:
        return self.props

    def leftParty(self, chr: Any) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("leftParty", this, chr)
        except Exception as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : leftParty:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : leftParty:\n" + ex)

    def disbandParty(self) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("disbandParty", this)
        except Exception as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : disbandParty:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : disbandParty:\n" + ex)

    def finishPQ(self) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("clearPQ", this)
        except Exception as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : clearPQ:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : clearPQ:\n" + ex)

    def removePlayer(self, chr: Any) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("playerExit", this, chr)
        except Exception as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerExit:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : playerExit:\n" + ex)

    def registerCarnivalParty(self, leader: Any, map: Any, team: int) -> None:
        if self.disposed:
            return
        leader.clearCarnivalRequests()
        characters = []
        party = leader.getParty()
        if party is None:
            return
        for pc in party.getMembers():
            c = map.getCharacterById(pc.getId())
            if c is not None:
                characters.add(c)
                self.registerPlayer(c)
                c.resetCP()
        carnivalParty = MapleCarnivalParty(leader, characters, team)
        try:
            self.em.getIv().invokeFunction("registerCarnivalParty", this, carnivalParty)
        except ScriptException as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : registerCarnivalParty:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : registerCarnivalParty:\n" + ex)
        except NoSuchMethodException as ex2:
            pass

    def onMapLoad(self, chr: Any) -> None:
        if self.disposed:
            return
        try:
            self.em.getIv().invokeFunction("onMapLoad", this, chr)
        except ScriptException as ex:
            print("Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : onMapLoad:\n" + ex)
            FileoutputUtil.log(FileoutputUtil.ScriptEx_Log, "Event name" + self.em.getName() + ", Instance name : " + self.name + ", method Name : onMapLoad:\n" + ex)
        except NoSuchMethodException as ex2:
            pass

    def isLeader(self, chr: Any) -> bool:
        return chr is not None and chr.getParty() is not None and chr.getParty().getLeader().getId() == chr.getId()

    def registerSquad(self, squad: Any, map: Any, questID: int) -> None:
        if self.disposed:
            return
        mapid = map.getId()
        for chr in squad.getMembers():
            player = squad.getChar(chr)
            if player is not None and player.getMapId() == mapid:
                if questID > 0:
                    player.getQuestNAdd(MapleQuest.getInstance(questID)).setCustomData(str(int(time.time() * 1000)))
                self.registerPlayer(player)
        squad.setStatus(2)

    def isDisconnected(self, chr: Any) -> bool:
        return not self.disposed and (chr.getId( in self.dced))

    def removeDisconnected(self, id: int) -> None:
        if self.disposed:
            return
        self.dced.remove(id)

    def getEventManager(self) -> Any:
        return self.em

    def applyBuff(self, chr: Any, id: int) -> None:
        MapleItemInformationProvider.getInstance().getItemEffect(id).applyTo(chr)
        chr.getClient().getSession().write(UIPacket.getStatusMsg(id))

    def check(self) -> bool:
        for chr in self.getPlayers():
            if chr.getLevel() < 30 or chr.getLevel() > 50:
                return False
        return True

    def check1(self) -> bool:
        for chr in self.getPlayers():
            if chr.getLevel() < 51 or chr.getLevel() > 120:
                return False
        return True

