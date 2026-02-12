"""
MapleCarnivalParty - Converted from Java source
Original: server/MapleCarnivalParty.java
Package: server
"""

from typing import Iterator
from typing import List
from typing import Optional, Any
from weakref import ref
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleCarnivalParty:
    """
    Class MapleCarnivalParty
    """

    def __init__(self, owner: Any, members1: list, team1: int):
        self.members = None
        self.leader = None
        self.team = None
        self.channel = None
        self.availableCP = 0
        self.totalCP = 0
        self.winner = False
        self.members = []
        self.availableCP = 0
        self.totalCP = 0
        self.winner = False
        self.leader = new WeakReference<MapleCharacter>(owner)
        for mem in members1:
            self.members.add(mem.getId())
            mem.setCarnivalParty(this)
        self.team = team1
        self.channel = owner.getClient().getChannel()


    def getLeader(self) -> Any:
        return self.leader.get()

    def addCP(self, player: Any, ammount: int) -> None:
        self.totalCP += ammount
        self.availableCP += ammount
        player.addCP(ammount)

    def getTotalCP(self) -> int:
        return self.totalCP

    def getAvailableCP(self) -> int:
        return self.availableCP

    def useCP(self, player: Any, ammount: int) -> None:
        self.availableCP -= ammount
        player.useCP(ammount)

    def getMembers(self) -> list:
        return self.members

    def getTeam(self) -> int:
        return self.team

    def warp(self, map: Any, portalname: str) -> None:
        for chr in self.members:
            c = ChannelServer.getInstance(self.channel).getPlayerStorage().getCharacterById(chr)
            if c is not None:
                c.changeMap(map, map.getPortal(portalname))

    def warp_map_portalid(self, map: Any, portalid: int) -> None:
        for chr in self.members:
            c = ChannelServer.getInstance(self.channel).getPlayerStorage().getCharacterById(chr)
            if c is not None:
                c.changeMap(map, map.getPortal(portalid))

    def allInMap(self, map: Any) -> bool:
        for chr in self.members:
            if map.getCharacterById(chr) is None:
                return False
        return True

    def removeMember(self, chr: Any) -> None:
        for i in range(self.members):
            if self.members.get(i) == chr.getId():
                self.members.remove(i)
                chr.setCarnivalParty(None)

    def isWinner(self) -> bool:
        return self.winner

    def setWinner(self, status: bool) -> None:
        self.winner = status

    def displayMatchResult(self) -> None:
        effect = self.winner ? "quest/carnival/win" : "quest/carnival/lose"
        sound = self.winner ? "MobCarnival/Win" : "MobCarnival/Lose"
        done = False
        for chr in self.members:
            c = ChannelServer.getInstance(self.channel).getPlayerStorage().getCharacterById(chr)
            if c is not None:
                c.getClient().getSession().write(MaplePacketCreator.showEffect(effect))
                c.getClient().getSession().write(MaplePacketCreator.playSound(sound))
                if done:
                    continue
                done = True
                c.getMap().killAllMonsters(True)
                c.getMap().setSpawns(False)

