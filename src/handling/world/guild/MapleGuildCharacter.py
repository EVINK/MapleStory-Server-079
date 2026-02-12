"""
MapleGuildCharacter - Converted from Java source
Original: handling/world/guild/MapleGuildCharacter.java
Package: handling.world.guild
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes


class MapleGuildCharacter:
    """
    Class MapleGuildCharacter
    Implements: Serializable
    """

    def __init__(self, c: Any):
        self.channel = 0
        self.guildrank = 0
        self.allianceRank = 0
        self.level = 0
        self.id = 0
        self.jobid = 0
        self.guildid = 0
        self.online = False
        self.name = ""
        self.channel = -1
        self.name = c.getName()
        self.level = c.getLevel()
        self.id = c.getId()
        self.channel = c.getClient().getChannel()
        self.jobid = c.getJob()
        self.guildrank = c.getGuildRank()
        self.guildid = c.getGuildId()
        self.allianceRank = c.getAllianceRank()
        self.online = True

    # Static initializer
    # MapleGuildCharacter.serialVersionUID = 2058609046116597760


    def getLevel(self) -> int:
        return self.level

    def setLevel(self, l: int) -> None:
        self.level = l

    def getId(self) -> int:
        return self.id

    def setChannel(self, ch: int) -> None:
        self.channel = ch

    def getChannel(self) -> int:
        return self.channel

    def getJobId(self) -> int:
        return self.jobid

    def setJobId(self, job: int) -> None:
        self.jobid = job

    def getGuildId(self) -> int:
        return self.guildid

    def setGuildId(self, gid: int) -> None:
        self.guildid = gid

    def setGuildRank(self, rank: int) -> None:
        self.guildrank = rank

    def getGuildRank(self) -> int:
        return self.guildrank

    def isOnline(self) -> bool:
        return self.online

    def getName(self) -> str:
        return self.name

    def setOnline(self, f: bool) -> None:
        self.online = f

    def setAllianceRank(self, rank: int) -> None:
        self.allianceRank = rank

    def getAllianceRank(self) -> int:
        return self.allianceRank

