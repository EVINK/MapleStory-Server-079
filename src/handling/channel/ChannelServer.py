"""
ChannelServer - Converted from Java source
Original: handling/channel/ChannelServer.java
Package: handling.channel
"""

from enum import Enum
from socket import socket
from threading import RLock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
from typing import Set
import asyncio
import os
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.ByteArrayMaplePacket import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.MapleServerHandler import *  # TODO: import specific classes
# from handling.cashshop.CashShopServer import *  # TODO: import specific classes
# from handling.login.LoginServer import *  # TODO: import specific classes
# from handling.mina.MapleCodecFactory import *  # TODO: import specific classes
# from handling.world.CheaterData import *  # TODO: import specific classes
# from scripting.EventScriptManager import *  # TODO: import specific classes
# from server.MapleSquad import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.events.MapleCoconut import *  # TODO: import specific classes
# from server.events.MapleEvent import *  # TODO: import specific classes
# from server.events.MapleEventType import *  # TODO: import specific classes
# from server.events.MapleFitness import *  # TODO: import specific classes
# from server.events.MapleOla import *  # TODO: import specific classes
# from server.events.MapleOxQuiz import *  # TODO: import specific classes
# from server.events.MapleSnowball import *  # TODO: import specific classes
# from server.life.PlayerNPC import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.shops.HiredMerchant import *  # TODO: import specific classes
# from tools.CollectionUtil import *  # TODO: import specific classes
# from tools.ConcurrentEnumMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class ChannelServer:
    """
    Class ChannelServer
    Implements: Serializable
    """

    DEFAULT_PORT = 2524

    def __init__(self, channel: int):
        self.expRate = 0
        self.mesoRate = 0
        self.dropRate = 0
        self.cashRate = 0
        self.BossdropRate = 0
        self.doubleExp = 0
        self.doubleMeso = 0
        self.doubleDrop = 0
        self.port = 0
        self.channel = None
        self.running_MerchantID = 0
        self.flags = 0
        self.serverMessage = ""
        self.key = ""
        self.ip = ""
        self.serverName = ""
        self.shutdown = False
        self.finishedShutdown = False
        self.MegaphoneMuteState = False
        self.adminOnly = False
        self.players = None
        self.serverHandler = None
        self.acceptor = None
        self.mapFactory = None
        self.eventSM = None
        self.merchants = None
        self.playerNPCs = None
        self.merchLock = None
        self.squadLock = None
        self.eventmap = 0
        self.events = None
        self.debugMode = False
        self.instanceId = 0
        self.warpcsshop = False
        self.warpmts = False
        self.BossdropRate = 1
        self.doubleExp = 1
        self.doubleMeso = 1
        self.doubleDrop = 1
        self.port = 2524
        self.running_MerchantID = 0
        self.flags = 0
        self.shutdown = False
        self.finishedShutdown = False
        self.MegaphoneMuteState = False
        self.adminOnly = False
        self.mapleSquads = new ConcurrentEnumMap<MapleSquad.MapleSquadType, MapleSquad>(MapleSquad.MapleSquadType.class)
        self.merchants = {}
        self.playerNPCs = {}
        self.merchLock = ReentrantReadWriteLock()
        self.squadLock = ReentrantReadWriteLock()
        self.eventmap = -1
        self.events = new EnumMap<MapleEventType, MapleEvent>(MapleEventType.class)
        self.instanceId = 0
        self.channel = channel
        self.mapFactory = MapleMapFactory(channel)
        self.merchLock = ReentrantReadWriteLock(True)

    # Static initializer
    # instances = {}


    def getAllInstance(self) -> set:
        return set())

    def newInstance(self, channel: int) -> Any:
        return ChannelServer(channel)

    @classmethod
    def get_instance(cls, channel: int) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getAllInstances(self) -> list:
        return Collections.unmodifiableCollection((Collection<? extends ChannelServer>)ChannelServer.instances.values())

    def startChannel_Main(self) -> None:
        ChannelServer.serverStartTime = int(time.time() * 1000)
        ch = int(ServerProperties.getProperty("RoyMS.Count", "0"))
        if ch > 10:
            ch = 10
        for i in range(ch):
            newInstance(i + 1).run_startup_configurations()

    def startChannel(self, channel: int) -> None:
        ChannelServer.serverStartTime = int(time.time() * 1000)
        for i in range(int(ServerProperties.getProperty("RoyMS.Count", "0"))):
            if channel == i + 1:
                newInstance(i + 1).run_startup_configurations()
                break

    def getChannelServer(self) -> set:
        return set())

    def getChannelCount(self) -> int:
        return ChannelServer.instances

    def getChannelLoad(self) -> dict:
        ret = {}
        for cs in ChannelServer.instances.values():
            ret.put(cs.getChannel(), cs.getConnectedClients())
        return ret

    def forceRemovePlayerByCharName(self, Name: str) -> bool:
        for ch in getAllInstances():
            chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
            for c in chrs:
                if c.getName().lower() == Name.lower():
                    try:
                        if c.getMap() is not None:
                            c.getMap().removePlayer(c)
                        if c.getClient() is not None:
                            c.getClient().disconnect(True, False, False)
                            c.getClient().getSession().close(True)
                    except Exception as ex:
                        pass
                    chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
                    if (c in chrs):
                        ch.removePlayer(c)
                        return True
                    continue
        return False

    def forceRemovePlayerByAccId(self, c: Any, accid: int) -> None:
        for ch in getAllInstances():
            chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
            for chr in chrs:
                if chr.getAccountID() == accid:
                    try:
                        if chr.getClient() is not None and chr.getClient() != c:
                            chr.getClient().disconnect(True, False, False)
                    except Exception as ex:
                        pass
                    chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
                    if chr.getClient() == c:
                        continue
                    if (chr in chrs):
                        ch.removePlayer(chr)
                    if chr.getMap() is None:
                        continue
                    chr.getMap().removePlayer(chr)
        try:
            chrs2 = CashShopServer.getPlayerStorage().getAllCharactersThreadSafe()
            for chr2 in chrs2:
                if chr2.getAccountID() == accid:
                    try:
                        if chr2.getClient() is None or chr2.getClient() == c:
                            continue
                        chr2.getClient().disconnect(True, False, False)
                    except Exception as ex2:
                        pass
        except Exception as ex3:
            pass

    def forceRemovePlayerByAccId_accid(self, accid: int) -> None:
        for ch in getAllInstances():
            chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
            for c in chrs:
                if c.getAccountID() == accid:
                    try:
                        if c.getClient() is not None:
                            c.getClient().disconnect(True, False, False)
                    except Exception as ex:
                        pass
                    chrs = ch.getPlayerStorage().getAllCharactersThreadSafe()
                    if (c in chrs):
                        ch.removePlayer(c)
                    if c.getMap() is None:
                        continue
                    c.getMap().removePlayer(c)

    def loadEvents(self) -> None:
        if self.events != 0:
            return
        self.events.put(MapleEventType.打椰子比赛, MapleCoconut(self.channel, MapleEventType.打椰子比赛.mapids))
        self.events.put(MapleEventType.打瓶盖比赛, MapleCoconut(self.channel, MapleEventType.打瓶盖比赛.mapids))
        self.events.put(MapleEventType.向高地, MapleFitness(self.channel, MapleEventType.向高地.mapids))
        self.events.put(MapleEventType.上楼上楼, MapleOla(self.channel, MapleEventType.上楼上楼.mapids))
        self.events.put(MapleEventType.快速0X猜题, MapleOxQuiz(self.channel, MapleEventType.快速0X猜题.mapids))
        self.events.put(MapleEventType.雪球赛, MapleSnowball(self.channel, MapleEventType.雪球赛.mapids))

    def run_startup_configurations(self) -> None:
        self.setChannel(self.channel)
        try:
            self.expRate = int(ServerProperties.getProperty("RoyMS.Exp"))
            self.mesoRate = int(ServerProperties.getProperty("RoyMS.Meso"))
            self.dropRate = int(ServerProperties.getProperty("RoyMS.Drop"))
            self.BossdropRate = int(ServerProperties.getProperty("RoyMS.BDrop"))
            self.cashRate = int(ServerProperties.getProperty("RoyMS.Cash"))
            self.serverMessage = ServerProperties.getProperty("RoyMS.EventMessage")
            self.serverName = ServerProperties.getProperty("RoyMS.ServerName")
            self.flags = int(ServerProperties.getProperty("RoyMS.WFlags", "0"))
            self.adminOnly = bool(ServerProperties.getProperty("RoyMS.Admin", "False"))
            self.eventSM = EventScriptManager(this, ServerProperties.getProperty("RoyMS.Events").split(","))
            self.port = Short.parseShort(ServerProperties.getProperty("RoyMS.Port" + self.channel, str(2524 + self.channel)))
            self.warpcsshop = bool(ServerProperties.getProperty("RoyMS.warpcsshop", "False"))
            self.warpmts = bool(ServerProperties.getProperty("RoyMS.warpmts", "False"))
            self.ip = ServerProperties.getProperty("RoyMS.IP") +":"+ self.port
            # this.ip = "49.235.142.128:"+ this.port;
        except ValueError as e:
            raise RuntimeError(e)
        # switch (GameConstants.game) {
        # case 0: {
        # this.ip = "127.0.0.1:" + this.port;
        # break;
        # }
        # default: {
        # this.ip = "127.0.0.1:" + this.port;
        # break;
        # }
        # }
        IoBuffer.setUseDirectBuffer(False)
        IoBuffer.setAllocator(SimpleBufferAllocator())
        self.acceptor = NioSocketAcceptor()
        self.acceptor.getFilterChain().addLast("codec", ProtocolCodecFilter(MapleCodecFactory()))
        self.players = PlayerStorage(self.channel)
        self.loadEvents()
        tMan = Timer.TimerManager.getInstance()
        try:
            self.acceptor.setHandler(MapleServerHandler(self.channel, False))
            self.acceptor.bind(InetSocketAddress(self.port))
            (self.acceptor.getSessionConfig()).setTcpNoDelay(True)
            print("频道 " + self.channel + ": 启动端口 " + self.port + ": 服务器IP " + self.ip + "")
            self.eventSM.init()
        except IOError as e2:
            print("Binding to port " + self.port + " failed (ch: " + self.getChannel() + ")" + e2)

    def shutdown(self, threadToNotify: Any) -> None:
        if self.finishedShutdown:
            return
        self.broadcastPacket(MaplePacketCreator.serverNotice(0, "这个频道正在关闭中."))
        self.shutdown = True
        print("频道 " + self.channel + " 正在清理活动脚本...")
        self.eventSM.cancel()
        print("频道 " + self.channel + ", 正在保存所有角色数据...")
        print("频道 " + self.channel + ", Saving characters...")
        print("频道 " + self.channel + ", 解除绑定端口...")
        ChannelServer.instances.remove(self.channel)
        LoginServer.removeChannel(self.channel)
        self.setFinishShutdown()

    def hasFinishedShutdown(self) -> bool:
        return self.finishedShutdown

    def getMapFactory(self) -> Any:
        return self.mapFactory

    def addPlayer(self, chr: Any) -> None:
        self.getPlayerStorage().registerPlayer(chr)
        chr.getClient().getSession().write(MaplePacketCreator.serverMessage(self.serverMessage))

    def getPlayerStorage(self) -> Any:
        if self.players is None:
            self.players = PlayerStorage(self.channel)
        return self.players

    def removePlayer(self, chr: Any) -> None:
        self.getPlayerStorage().deregisterPlayer(chr)

    def removePlayer_idz_namez(self, idz: int, namez: str) -> None:
        self.getPlayerStorage().deregisterPlayer(idz, namez)

    def getServerMessage(self) -> str:
        return self.serverMessage

    def setServerMessage(self, newMessage: str) -> None:
        self.serverMessage = newMessage
        self.broadcastPacket(MaplePacketCreator.serverMessage(self.serverMessage))

    def broadcastPacket(self, data: Any) -> None:
        self.getPlayerStorage().broadcastPacket(data)

    def broadcastSmegaPacket(self, data: Any) -> None:
        self.getPlayerStorage().broadcastSmegaPacket(data)

    def broadcastGMPacket(self, data: Any) -> None:
        self.getPlayerStorage().broadcastGMPacket(data)

    def getExpRate(self) -> int:
        return self.expRate * self.doubleExp

    def setExpRate(self, expRate: int) -> None:
        self.expRate = expRate

    def getCashRate(self) -> int:
        return self.cashRate

    def setCashRate(self, cashRate: int) -> None:
        self.cashRate = cashRate

    def getChannel(self) -> int:
        return self.channel

    def setChannel(self, channel: int) -> None:
        ChannelServer.instances.put(channel, this)
        LoginServer.addChannel(channel)

    def getSocket(self) -> str:
        return self.ip

    def getIP(self) -> str:
        return self.ip

    def getIPA(self) -> str:
        return self.ip

    def isShutdown(self) -> bool:
        return self.shutdown

    def getLoadedMaps(self) -> int:
        return self.mapFactory.getLoadedMaps()

    def getEventSM(self) -> Any:
        return self.eventSM

    def reloadEvents(self) -> None:
        self.eventSM.cancel()
        (self.eventSM = EventScriptManager(this, ServerProperties.getProperty("RoyMS.Events").split(","))).init()

    def getBossDropRate(self) -> int:
        return self.BossdropRate

    def setBossDropRate(self, dropRate: int) -> None:
        self.BossdropRate = dropRate

    def getMesoRate(self) -> int:
        return self.mesoRate * self.doubleMeso

    def setMesoRate(self, mesoRate: int) -> None:
        self.mesoRate = mesoRate

    def getDropRate(self) -> int:
        return self.dropRate * self.doubleDrop

    def setDropRate(self, dropRate: int) -> None:
        self.dropRate = dropRate

    def getDoubleExp(self) -> int:
        if self.doubleExp < 0 or self.doubleExp > 2:
            return 1
        return self.doubleExp

    def setDoubleExp(self, doubleExp: int) -> None:
        if doubleExp < 0 or doubleExp > 2:
            self.doubleExp = 1
        else:
            self.doubleExp = doubleExp

    def getDoubleMeso(self) -> int:
        if self.doubleMeso < 0 or self.doubleMeso > 2:
            return 1
        return self.doubleMeso

    def setDoubleMeso(self, doubleMeso: int) -> None:
        if doubleMeso < 0 or doubleMeso > 2:
            self.doubleMeso = 1
        else:
            self.doubleMeso = doubleMeso

    def getDoubleDrop(self) -> int:
        if self.doubleDrop < 0 or self.doubleDrop > 2:
            return 1
        return self.doubleDrop

    def setDoubleDrop(self, doubleDrop: int) -> None:
        if doubleDrop < 0 or doubleDrop > 2:
            self.doubleDrop = 1
        else:
            self.doubleDrop = doubleDrop

    def getAllSquads(self) -> dict:
        return Collections.unmodifiableMap((Map<? extends MapleSquad.MapleSquadType, ? extends MapleSquad>)self.mapleSquads)

    def getMapleSquad(self, type: str) -> Any:
        return self.getMapleSquad(MapleSquad.MapleSquadType.valueOf(type.lower()))

    def getMapleSquad_type(self, type: Any) -> Any:
        return self.mapleSquads.get(type)

    def addMapleSquad(self, squad: Any, type: str) -> bool:
        final MapleSquad.MapleSquadType types = MapleSquad.MapleSquadType.valueOf(type.lower())
        if types is not None and not (types in self.mapleSquads):
            self.mapleSquads.put(types, squad)
            squad.scheduleRemoval()
            return True
        return False

    def removeMapleSquad(self, squad: Any, type: Any) -> bool:
        if type is not None and (type in self.mapleSquads) and self.mapleSquads.get(type) == squad:
            self.mapleSquads.remove(type)
            return True
        return False

    def removeMapleSquad_types(self, types: Any) -> bool:
        if types is not None and (types in self.mapleSquads):
            self.mapleSquads.remove(types)
            return True
        return False

    def closeAllMerchant(self) -> int:
        ret = 0
        self.merchLock.writeLock().lock()
        try:
            Iterator<Map.Entry<Integer, HiredMerchant>> merchants_ = self.merchants.items().iterator()
            while merchants_.hasNext():
                hm = (HiredMerchant)((Map.Entry)merchants_.next()).getValue()
                hm.closeShop(True, False)
                hm.getMap().removeMapObject(hm)
                merchants_.remove()
                ret += 1
        finally:
            self.merchLock.writeLock().unlock()
        return ret

    def addMerchant(self, hMerchant: Any) -> int:
        self.merchLock.writeLock().lock()
        runningmer = 0
        try:
            runningmer = self.running_MerchantID
            self.merchants.put(self.running_MerchantID, hMerchant)
            self.running_MerchantID += 1
        finally:
            self.merchLock.writeLock().unlock()
        return runningmer

    def removeMerchant(self, hMerchant: Any) -> None:
        self.merchLock.writeLock().lock()
        try:
            self.merchants.remove(hMerchant.getStoreId())
        finally:
            self.merchLock.writeLock().unlock()

    def containsMerchant(self, accid: int) -> bool:
        contains = False
        self.merchLock.readLock().lock()
        try:
            itr = self.merchants.values().iterator()
            while itr.hasNext():
                if (itr.next()).getOwnerAccId() == accid:
                    contains = True
                    break
        finally:
            self.merchLock.readLock().unlock()
        return contains

    def searchMerchant(self, itemSearch: int) -> list:
        list = []
        self.merchLock.readLock().lock()
        try:
            itr = self.merchants.values().iterator()
            while itr.hasNext():
                hm = itr.next()
                if hm.searchItem(itemSearch) > 0:
                list.add(hm)
        finally:
            self.merchLock.readLock().unlock()
        return list

    def toggleMegaphoneMuteState(self) -> None:
        self.MegaphoneMuteState = not self.MegaphoneMuteState

    def getMegaphoneMuteState(self) -> bool:
        return self.MegaphoneMuteState

    def getEvent(self) -> int:
        return self.eventmap

    def setEvent(self, ze: int) -> None:
        self.eventmap = ze

    def getEvent_t(self, t: Any) -> Any:
        return self.events.get(t)

    def getAllPlayerNPC(self) -> list:
        return self.playerNPCs.values()

    def getPlayerNPC(self, id: int) -> Any:
        return self.playerNPCs.get(id)

    def addPlayerNPC(self, npc: Any) -> None:
        if (npc.getId( in self.playerNPCs)):
            self.removePlayerNPC(npc)
        self.playerNPCs.put(npc.getId(), npc)
        self.getMapFactory().getMap(npc.getMapId()).addMapObject(npc)

    def removePlayerNPC(self, npc: Any) -> None:
        if (npc.getId( in self.playerNPCs)):
            self.playerNPCs.remove(npc.getId())
            self.getMapFactory().getMap(npc.getMapId()).removeMapObject(npc)

    def getServerName(self) -> str:
        return self.serverName

    def setServerName(self, sn: str) -> None:
        self.serverName = sn

    def getPort(self) -> int:
        return self.port

    def setShutdown(self) -> None:
        self.shutdown = True
        print("频道 " + self.channel + " 已开始关闭.")

    def setFinishShutdown(self) -> None:
        self.finishedShutdown = True
        print("频道 " + self.channel + " 已关闭完成.")

    def isAdminOnly(self) -> bool:
        return self.adminOnly

    def getServerHandler(self) -> Any:
        return self.serverHandler

    def getTempFlag(self) -> int:
        return self.flags

    def getConnectedClients(self) -> int:
        return self.getPlayerStorage().getConnectedClients()

    def getCheaters(self) -> list:
        cheaters = self.getPlayerStorage().getCheaters()
        Collections.sort(cheaters)
        return CollectionUtil.copyFirst(cheaters, 20)

    def broadcastMessage(self, message: bytes) -> None:
        self.broadcastPacket(ByteArrayMaplePacket(message))

    def broadcastMessage_message(self, message: Any) -> None:
        self.broadcastPacket(message)

    def broadcastSmega(self, message: bytes) -> None:
        self.broadcastSmegaPacket(ByteArrayMaplePacket(message))

    def broadcastGMMessage(self, message: bytes) -> None:
        self.broadcastGMPacket(ByteArrayMaplePacket(message))

    def saveAll(self) -> None:
        ppl = 0
        for chr in self.players.getAllCharactersThreadSafe():
            if chr is not None:
                ppl += 1
                chr.saveToDB(False, False)
        print("[自动存档] 已经将频道 " + self.channel + " 的 " + ppl + " 个玩家保存到数据中.")

    def AutoNx(self, dy: int) -> None:
        self.mapFactory.getMap(741000208).AutoNx(dy)
        self.mapFactory.getMap(910000000).AutoNx(dy)
        self.mapFactory.getMap(209080100).AutoNx(dy)

    def AutoTime(self, dy: int) -> None:
        try:
            for chan in getAllInstances():
                for chr in chan.getPlayerStorage().getAllCharacters():
                    if chr is None:
                        continue
                    chr.gainGamePoints(1)
                    if chr.getGamePoints() >= 5:
                        continue
                    chr.resetGamePointsPD()
        except Exception as ex:
            pass

    def getInstanceId(self) -> int:
        return self.instanceId

    def addInstanceId(self) -> None:
        self.instanceId += 1

    def WarpCSShop(self) -> bool:
        return self.warpcsshop

    def WarpMTS(self) -> bool:
        return self.warpmts

    def closeAllMerchants(self) -> None:
        ret = 0
        Start = int(time.time() * 1000)
        self.merchLock.writeLock().lock()
        try:
            Iterator<Map.Entry<Integer, HiredMerchant>> hmit = self.merchants.items().iterator()
            while hmit.hasNext():
                ((HiredMerchant)((Map.Entry)hmit.next()).getValue()).closeShop(True, False)
                hmit.remove()
                ret += 1
        except Exception as e:
            print("关闭雇佣商店出现错误..." + e)
        finally:
            self.merchLock.writeLock().unlock()
        print("频道 " + self.channel + " 共保存雇佣商店: " + ret + " | 耗时: " + (int(time.time() * 1000) - Start) + " 毫秒.")

    def isConnected(self, name: str) -> bool:
        return self.getPlayerStorage().getCharacterByName(name) is not None

