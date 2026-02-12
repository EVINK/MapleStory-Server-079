"""
MapleSquad - Converted from Java source
Original: server/MapleSquad.java
Package: server
"""

from concurrent.futures import Future
from enum import Enum, IntEnum
from typing import Dict
from typing import List
from typing import Optional, Any
from weakref import ref
import sched
import threading
import time
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleSquad:
    """
    Class MapleSquad
    """

    def __init__(self, ch: int, type: str, leader: Any, expiration: int, toSay: str):
        self.leader = None
        self.leaderName = None
        self.toSay = None
        self.members = None
        self.bannedMembers = None
        self.ch = None
        self.startTime = None
        self.expiration = None
        self.beginMapId = None
        self.type = None
        self.status = 0
        self.c = None
        self.i = 0
        self.queuedPlayers = {}
        self.queue = {}
        self.members = {}
        self.bannedMembers = {}
        self.status = 0
        self.leader = new WeakReference<MapleCharacter>(leader)
        self.members.put(leader.getName(), MapleCarnivalChallenge.getJobBasicNameById(leader.getJob()))
        self.leaderName = leader.getName()
        self.ch = ch
        self.toSay = toSay
        self.type = MapleSquadType.valueOf(type.lower())
        self.status = 1
        self.beginMapId = leader.getMapId()
        leader.getMap().setSquad(self.type)
        if self.type.queue.get(ch) is None:
            self.type.queue.put(ch, new ArrayList<Pair<String, Long>>())
            self.type.queuedPlayers.put(ch, new ArrayList<Pair<String, String>>())
        self.startTime = int(time.time() * 1000)
        self.expiration = expiration


    def copy(self) -> None:
        while self.type.queue.get(self.ch) > 0 && ChannelServer.getInstance(self.ch).getMapleSquad(self.type) is None:
            index = 0
            lowest = 0
            for i in range(self.type.queue.get(self.ch)):
                if lowest == 0 || self.type.queue.get(self.ch).get(i).right < lowest:
                    index = i
                    lowest = self.type.queue.get(self.ch).get(i).right
            nextPlayerId = self.type.queue.get(self.ch).remove(index).left
            theirCh = World.Find.findChannel(nextPlayerId)
            if theirCh > 0:
                lead = ChannelServer.getInstance(theirCh).getPlayerStorage().getCharacterByName(nextPlayerId)
                if lead is not None && lead.getMapId() == self.beginMapId && lead.getClient().getChannel() == self.ch:
                    squad = MapleSquad(self.ch, self.type.name(), lead, self.expiration, self.toSay)
                    if ChannelServer.getInstance(self.ch).addMapleSquad(squad, self.type.name()):
                        self.getBeginMap().broadcastMessage(MaplePacketCreator.getClock(self.expiration / 1000))
                        self.getBeginMap().broadcastMessage(MaplePacketCreator.serverNotice(6, nextPlayerId + self.toSay))
                        self.type.queuedPlayers.get(self.ch).add(new Pair<String, String>(nextPlayerId, "Success"))
                        break
                    squad.clear()
                    self.type.queuedPlayers.get(self.ch).add(new Pair<String, String>(nextPlayerId, "Skipped"))
                    break
                else:
                    if lead is not None:
                        lead.dropMessage(6, "Your squad has been skipped due to you not being in the right channel and map.")
                    self.getBeginMap().broadcastMessage(MaplePacketCreator.serverNotice(6, nextPlayerId + "'s squad has been skipped due to the player not being in the right channel and map."))
                    self.type.queuedPlayers.get(self.ch).add(new Pair<String, String>(nextPlayerId, "Not in map"))
            else:
                self.getBeginMap().broadcastMessage(MaplePacketCreator.serverNotice(6, nextPlayerId + "'s squad has been skipped due to the player not being online."))
                self.type.queuedPlayers.get(self.ch).add(new Pair<String, String>(nextPlayerId, "Not online"))

    def getBeginMap(self) -> Any:
        return ChannelServer.getInstance(self.ch).getMapFactory().getMap(self.beginMapId)

    def clear(self) -> None:
        if self.removal is not None:
            self.removal.cancel(False)
            self.removal = None
        self.members.clear()
        self.bannedMembers.clear()
        self.leader = None
        ChannelServer.getInstance(self.ch).removeMapleSquad(self.type)
        self.status = 0

    def getChar(self, name: str) -> Any:
        return ChannelServer.getInstance(self.ch).getPlayerStorage().getCharacterByName(name)

    def getTimeLeft(self) -> int:
        return self.expiration - (int(time.time() * 1000) - self.startTime)

    def scheduleRemoval(self) -> None:
        self.removal = Timer.EtcTimer.getInstance().schedule(Runnable()
            public void run()
                if MapleSquad.self.status != 0 && MapleSquad.self.leader is not None && (MapleSquad.self.getLeader() is None || MapleSquad.self.status == 1):
                    MapleSquad.self.clear()
                    MapleSquad.self.copy()

    def run(self) -> None:
        if MapleSquad.self.status != 0 && MapleSquad.self.leader is not None && (MapleSquad.self.getLeader() is None || MapleSquad.self.status == 1):
            MapleSquad.self.clear()
            MapleSquad.self.copy()

    def getLeaderName(self) -> str:
        return self.leaderName

    def getAllNextPlayer(self) -> list:
        return self.type.queue.get(self.ch)

    def getNextPlayer(self) -> str:
        sb = ""
        sb.append("#b").append(self.type.queue.get(self.ch)).append(" #k ").append("与远征队名单 : \n\r ")
        i = 0
        for chr in self.type.queue.get(self.ch):
            i += 1
            sb.append(i).append(" : ").append(chr.left)
            sb.append(" \n\r ")
        sb.append("你是否想要 #e当下一个#n 在远征队排队中\u3000或者 #e移除#n 在远征队? 如果你想的话...")
        return sb

    def setNextPlayer(self, i: str) -> None:
        toRemove = None
        for s in self.type.queue.get(self.ch):
            if s.left == (i):
                toRemove = s
                break
        if toRemove is not None:
            self.type.queue.get(self.ch).remove(toRemove)
            return
        for v in self.type.queue.values():
            for s2 in v:
                if s2.left == (i):
                    return
        self.type.queue.get(self.ch).add(new Pair<String, Long>(i, int(time.time() * 1000)))

    def getLeader(self) -> Any:
        if self.leader is None || self.leader.get() is None:
            if self.members <= 0 || self.getChar(self.leaderName) is None:
                if self.status != 0:
                    self.clear()
                return None
            self.leader = new WeakReference<MapleCharacter>(self.getChar(self.leaderName))
        return self.leader.get()

    def containsMember(self, member: Any) -> bool:
        for mmbr in self.members.keys():
            if mmbr.lower() == member.getName(.lower()):
                return True
        return False

    def getMembers(self) -> list:
        return [])

    def getBannedMembers(self) -> list:
        return [])

    def getSquadSize(self) -> int:
        return self.members

    def isBanned(self, member: Any) -> bool:
        return (member.getName( in self.bannedMembers))

    def addMember(self, member: Any, join: bool) -> int:
        if self.getLeader() is None:
            return -1
        job = MapleCarnivalChallenge.getJobBasicNameById(member.getJob())
        if join:
            if self.containsMember(member) || self.getAllNextPlayer().__contains__(member.getName()):
                return -1
            if self.members <= 30:
                self.members.put(member.getName(), job)
                self.getLeader().dropMessage(6, member.getName() + " (" + job + ") 加入远征队!")
                return 1
            return 2
        else:
            if self.containsMember(member):
                self.members.remove(member.getName())
                self.getLeader().dropMessage(6, member.getName() + " (" + job + ") 离开了远征队.")
                return 1
            return -1

    def acceptMember(self, pos: int) -> None:
        if pos < 0 || pos >= self.bannedMembers:
            return
        membersAsList = self.getBannedMembers()
        toadd = membersAsList.get(pos)
        if toadd is not None && self.getChar(toadd) is not None:
            self.members.put(toadd, self.bannedMembers.get(toadd))
            self.bannedMembers.remove(toadd)
            self.getChar(toadd).dropMessage(5, self.getLeaderName() + " 允许你从新回来远征队")

    def reAddMember(self, chr: Any) -> None:
        self.removeMember(chr)
        self.members.put(chr.getName(), MapleCarnivalChallenge.getJobBasicNameById(chr.getJob()))

    def removeMember(self, chr: Any) -> None:
        if (chr.getName( in self.members)):
            self.members.remove(chr.getName())

    def removeMember_chr(self, chr: str) -> None:
        if (chr in self.members):
            self.members.remove(chr)

    def banMember(self, pos: int) -> None:
        if pos <= 0 || pos >= self.members:
            return
        membersAsList = self.getMembers()
        toban = membersAsList.get(pos)
        if toban is not None && self.getChar(toban) is not None:
            self.bannedMembers.put(toban, self.members.get(toban))
            self.members.remove(toban)
            self.getChar(toban).dropMessage(5, self.getLeaderName() + " 从远征队中删除了您.")

    def setStatus(self, status: int) -> None:
        self.status = status
        if status == 2 && self.removal is not None:
            self.removal.cancel(False)
            self.removal = None

    def getStatus(self) -> int:
        return self.status

    def getBannedMemberSize(self) -> int:
        return self.bannedMembers

    def getSquadMemberString(self, type: int) -> str:
        # switch (type):
            # case 0:
                sb = ""
                sb.append("#b").append(self.members).append(" #k ").append("与成员名单 : \n\r ")
                i = 0
                for (final Map.Entry<String, String> chr : self.members.items())
                    i += 1
                    sb.append(i).append(" : ").append(chr.getKey()).append(" (").append(chr.getValue()).append(") ")
                    if i == 1:
                        sb.append("(远征队领袖)")
                    sb.append(" \n\r ")
                while i < 30:
                    i += 1
                    sb.append(i).append(" : ").append(" \n\r ")
                return sb
            # case 1:
                sb = ""
                sb.append("#b").append(self.members).append(" #n ").append("与成员名单 : \n\r ")
                i = 0
                selection = 0
                for (final Map.Entry<String, String> chr2 : self.members.items())
                    i += 1
                    sb.append("#b#L").append(selection).append("#")
                    selection += 1
                    sb.append(i).append(" : ").append(chr2.getKey()).append(" (").append(chr2.getValue()).append(") ")
                    if i == 1:
                        sb.append("(远征队领袖)")
                    sb.append("#l").append(" \n\r ")
                while i < 30:
                    i += 1
                    sb.append(i).append(" : ").append(" \n\r ")
                return sb
            # case 2:
                sb = ""
                sb.append("#b").append(self.members).append(" #n ").append("与成员名单 : \n\r ")
                i = 0
                selection = 0
                for (final Map.Entry<String, String> chr2 : self.bannedMembers.items())
                    i += 1
                    sb.append("#b#L").append(selection).append("#")
                    selection += 1
                    sb.append(i).append(" : ").append(chr2.getKey()).append(" (").append(chr2.getValue()).append(") ")
                    sb.append("#l").append(" \n\r ")
                while i < 30:
                    i += 1
                    sb.append(i).append(" : ").append(" \n\r ")
                return sb
            # case 3:
                sb = ""
                jobs = self.getJobs()
                for (final Map.Entry<String, Integer> chr3 : jobs.items())
                    sb.append("\r\n").append(chr3.getKey()).append(" : ").append(chr3.getValue())
                return sb
            # default:
                return None

    def getType(self) -> Any:
        return self.type

    def getJobs(self) -> dict:
        jobs = {}
        for (final Map.Entry<String, String> chr : self.members.items())
            if (chr.getValue( in jobs)):
                jobs.put(chr.getValue(), jobs.get(chr.getValue()) + 1)
            else:
                jobs.put(chr.getValue(), 1)
        return jobs


# Inner class from Java (originally nested)
class MapleSquadType(Enum):
    """Enum MapleSquadType"""

    bossbalrog = (1)
    zak = (1)
    chaoszak = (3)
    horntail = (1)
    chaosht = (3)
    pinkbean = (3)
    nmm_squad = (2)
    vergamot = (2)
    dunas = (2)
    nibergen_squad = (2)
    dunas2 = (2)
    core_blaze = (2)
    aufheben = (2)
    cwkpq = (10)
    tokyo_2095 = (2)
    vonleon = (3)
    scartar = (2)
    ARIANT1 = (3)
    ARIANT2 = (4)
    ARIANT3 = (5)
    cygnus = (3)

