"""
MapleGuildAlliance - Converted from Java source
Original: handling/world/guild/MapleGuildAlliance.java
Package: handling.world.guild
"""

from enum import Enum, IntEnum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Collection
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleGuildAlliance:
    """
    Class MapleGuildAlliance
    Implements: Serializable
    """

    def __init__(self, id: int):
        self.allianceid = 0
        self.leaderid = 0
        self.capacity = 0
        self.name = ""
        self.notice = ""
        self.guilds = new int[5]
        self.ranks = new String[5]
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM alliances WHERE id = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if !rs.first():
                rs.close()
                ps.close()
                self.allianceid = -1
                return
            self.allianceid = id
            self.name = rs.getString("name")
            self.capacity = rs.getInt("capacity")
            for i in range(1, 6):
                self.guilds[i - 1] = rs.getInt("guild" + i)
                self.ranks[i - 1] = rs.getString("rank" + i)
            self.leaderid = rs.getInt("leaderid")
            self.notice = rs.getString("notice")
            rs.close()
            ps.close()
        except Exception as se:
            print("unable to read guild information from sql")
            se.printStackTrace()

    # Static initializer
    # MapleGuildAlliance.serialVersionUID = 24081985245
    # MapleGuildAlliance.CHANGE_CAPACITY_COST = 10000000


    def loadAll(self) -> list:
        ret = []
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT id FROM alliances")
            rs = ps.executeQuery()
            while rs.next():
                g = MapleGuildAlliance(rs.getInt("id"))
                if g.getId() > 0:
                    ret.add(g)
            rs.close()
            ps.close()
        except Exception as se:
            print("unable to read guild information from sql")
            se.printStackTrace()
        return ret

    def createToDb(self, leaderId: int, name: str, guild1: int, guild2: int) -> int:
        ret = -1
        if name > 12:
            return ret
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT id FROM alliances WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if rs.first():
                rs.close()
                ps.close()
                return ret
            ps.close()
            rs.close()
            ps = con.prepareStatement("insert into alliances (name, guild1, guild2, leaderid) VALUES (?, ?, ?, ?)", 1)
            ps.setString(1, name)
            ps.setInt(2, guild1)
            ps.setInt(3, guild2)
            ps.setInt(4, leaderId)
            ps.execute()
            rs = ps.getGeneratedKeys()
            if rs.next():
                ret = rs.getInt(1)
            rs.close()
            ps.close()
        except Exception as SE:
            print("SQL THROW")
            SE.printStackTrace()
        return ret

    def getNoGuilds(self) -> int:
        ret = 0
        for i in range(self.capacity):
            if self.guilds[i] > 0:
                ret += 1
        return ret

    def deleteAlliance(self) -> bool:
        try:
            con = DatabaseConnection.getConnection()
            for i in range(self.getNoGuilds()):
                ps = con.prepareStatement("UPDATE characters SET alliancerank = 5 WHERE guildid = ?")
                ps.setInt(1, self.guilds[i])
                ps.execute()
                ps.close()
            ps = con.prepareStatement("delete from alliances where id = ?")
            ps.setInt(1, self.allianceid)
            ps.execute()
            ps.close()
        except Exception as SE:
            print("SQL THROW" + SE)
            return False
        return True

    def broadcast(self, packet: Any) -> None:
        self.broadcast(packet, -1, GAOp.NONE, False)

    def broadcast_packet_exception(self, packet: Any, exception: int) -> None:
        self.broadcast(packet, exception, GAOp.NONE, False)

    def broadcast_packet_exceptionId_op_expelled(self, packet: Any, exceptionId: int, op: Any, expelled: bool) -> None:
        if None != op:
            # switch (op):
                # case DISBAND:
                    World.Alliance.setOldAlliance(exceptionId, expelled, self.allianceid)
                    break
                # case NEWGUILD:
                    World.Alliance.setNewAlliance(exceptionId, self.allianceid)
                    break
                # default:
                    World.Alliance.sendGuild(packet, exceptionId, self.allianceid)
                    break

    def disband(self) -> bool:
        ret = self.deleteAlliance()
        if ret:
            self.broadcast(None, -1, GAOp.DISBAND, False)
        return ret

    def saveToDb(self) -> None:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("UPDATE alliances set guild1 = ?, guild2 = ?, guild3 = ?, guild4 = ?, guild5 = ?, rank1 = ?, rank2 = ?, rank3 = ?, rank4 = ?, rank5 = ?, capacity = ?, leaderid = ?, notice = ? where id = ?")
            for i in range(5):
                ps.setInt(i + 1, (self.guilds[i] < 0) ? 0 : self.guilds[i])
                ps.setString(i + 6, self.ranks[i])
            ps.setInt(11, self.capacity)
            ps.setInt(12, self.leaderid)
            ps.setString(13, self.notice)
            ps.setInt(14, self.allianceid)
            ps.executeUpdate()
            ps.close()
        except Exception as SE:
            print("SQL THROW")
            SE.printStackTrace()

    def setRank(self, ranks: list) -> None:
        self.ranks = ranks
        self.broadcast(MaplePacketCreator.getAllianceUpdate(this))
        self.saveToDb()

    def getRank(self, rank: int) -> str:
        return self.ranks[rank - 1]

    def getRanks(self) -> list:
        return self.ranks

    def getNotice(self) -> str:
        return self.notice

    def setNotice(self, newNotice: str) -> None:
        self.notice = newNotice
        self.broadcast(MaplePacketCreator.getAllianceUpdate(this))
        self.broadcast(MaplePacketCreator.serverNotice(5, "聯盟公告事項 : " + newNotice))
        self.saveToDb()

    def getGuildId(self, i: int) -> int:
        return self.guilds[i]

    def getId(self) -> int:
        return self.allianceid

    def getName(self) -> str:
        return self.name

    def getCapacity(self) -> int:
        return self.capacity

    def setCapacity(self) -> bool:
        if self.capacity >= 5:
            return False
        self.capacity += 1
        self.broadcast(MaplePacketCreator.getAllianceUpdate(this))
        self.saveToDb()
        return True

    def addGuild(self, guildid: int) -> bool:
        if self.getNoGuilds() >= self.getCapacity():
            return False
        self.guilds[self.getNoGuilds()] = guildid
        self.saveToDb()
        self.broadcast(None, guildid, GAOp.NEWGUILD, False)
        return True

    def removeGuild(self, guildid: int, expelled: bool) -> bool:
        i = 0
        while i < self.getNoGuilds():
            if self.guilds[i] == guildid:
                self.broadcast(None, guildid, GAOp.DISBAND, expelled)
                if i > 0 && i != self.getNoGuilds() - 1:
                    x = i + 1
                    while x < self.getNoGuilds():
                        if self.guilds[x] > 0:
                            self.guilds[x - 1] = self.guilds[x]
                            if x == self.getNoGuilds() - 1:
                                self.guilds[x] = -1
                else:
                    self.guilds[i] = -1
                if i == 0:
                    return self.disband()
                self.broadcast(MaplePacketCreator.getAllianceUpdate(this))
                self.broadcast(MaplePacketCreator.getGuildAlliance(this))
                self.saveToDb()
                return True
            else:
                i += 1
        return False

    def getLeaderId(self) -> int:
        return self.leaderid

    def setLeaderId(self, c: int) -> bool:
        if self.leaderid == c:
            return False
        g = -1
        leaderName = None
        for i in range(self.getNoGuilds()):
            g_ = World.Guild.getGuild(self.guilds[i])
            if g_ is not None:
                newLead = g_.getMGC(c)
                oldLead = g_.getMGC(self.leaderid)
                if newLead is not None && oldLead is not None:
                    return False
                if newLead is not None && newLead.getGuildRank() == 1 && newLead.getAllianceRank() == 2:
                    g_.changeARank(c, 1)
                    g = i
                    leaderName = newLead.getName()
                elif oldLead is not None && oldLead.getGuildRank() == 1 && oldLead.getAllianceRank() == 1:
                    g_.changeARank(self.leaderid, 2)
                elif oldLead is not None || newLead is not None:
                    return False
        if g == -1:
            return False
        oldGuild = self.guilds[g]
        self.guilds[g] = self.guilds[0]
        self.guilds[0] = oldGuild
        if leaderName is not None:
            self.broadcast(MaplePacketCreator.serverNotice(5, leaderName + " has become the leader of the alliance."))
        self.broadcast(MaplePacketCreator.changeAllianceLeader(self.allianceid, self.leaderid, c))
        self.broadcast(MaplePacketCreator.updateAllianceLeader(self.allianceid, self.leaderid, c))
        self.broadcast(MaplePacketCreator.getAllianceUpdate(this))
        self.broadcast(MaplePacketCreator.getGuildAlliance(this))
        self.leaderid = c
        self.saveToDb()
        return True

    def changeAllianceRank(self, cid: int, change: int) -> bool:
        if self.leaderid == cid || change < 0 || change > 1:
            return False
        for i in range(self.getNoGuilds()):
            g_ = World.Guild.getGuild(self.guilds[i])
            if g_ is not None:
                chr = g_.getMGC(cid)
                if chr is not None && chr.getAllianceRank() > 2:
                    if (change == 0 && chr.getAllianceRank() >= 5) || (change == 1 && chr.getAllianceRank() <= 3):
                        return False
                    g_.changeARank(cid, chr.getAllianceRank() + ((change == 0) ? 1 : -1))
                    return True
        return False


# Inner class from Java (originally nested)
class GAOp(Enum):
    """Enum GAOp"""

    NONE = 0
    DISBAND = 1
    NEWGUILD = 2

