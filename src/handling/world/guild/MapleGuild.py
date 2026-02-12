"""
MapleGuild - Converted from Java source
Original: handling/world/guild/MapleGuild.java
Package: handling.world.guild
"""

from enum import Enum, IntEnum
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
import math
import pymysql
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.StringUtil import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes
# from tools.packet.UIPacket import *  # TODO: import specific classes


class MapleGuild:
    """
    Class MapleGuild
    Implements: Serializable
    """

    def __init__(self, guildid: int):
        self.members = []
        self.name = ""
        self.notice = ""
        self.id = 0
        self.gp = 0
        self.logo = 0
        self.logoColor = 0
        self.leader = 0
        self.capacity = 0
        self.logoBG = 0
        self.logoBGColor = 0
        self.signature = 0
        self.bDirty = False
        self.proper = False
        self.allianceid = 0
        self.invitedid = 0
        self.bbs = {}
        self.lock = None
        self.rL = None
        self.wL = None
        self.init = False
        self.members = []
        self.rankTitles = new String[5]
        self.bDirty = True
        self.proper = True
        self.allianceid = 0
        self.invitedid = 0
        self.bbs = {}
        self.lock = ReentrantReadWriteLock()
        self.rL = self.lock.readLock()
        self.wL = self.lock.writeLock()
        self.init = False
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM guilds WHERE guildid = ?")
            ps.setInt(1, guildid)
            rs = ps.executeQuery()
            if !rs.first():
                rs.close()
                ps.close()
                self.id = -1
                return
            self.id = guildid
            self.name = rs.getString("name")
            self.gp = rs.getInt("GP")
            self.logo = rs.getInt("logo")
            self.logoColor = rs.getInt("logoColor")
            self.logoBG = rs.getInt("logoBG")
            self.logoBGColor = rs.getInt("logoBGColor")
            self.capacity = rs.getInt("capacity")
            self.rankTitles[0] = rs.getString("rank1title")
            self.rankTitles[1] = rs.getString("rank2title")
            self.rankTitles[2] = rs.getString("rank3title")
            self.rankTitles[3] = rs.getString("rank4title")
            self.rankTitles[4] = rs.getString("rank5title")
            self.leader = rs.getInt("leader")
            self.notice = rs.getString("notice")
            self.signature = rs.getInt("signature")
            self.allianceid = rs.getInt("alliance")
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT id, name, level, job, guildrank, alliancerank FROM characters WHERE guildid = ? ORDER BY guildrank ASC, name ASC")
            ps.setInt(1, guildid)
            rs = ps.executeQuery()
            if !rs.first():
                print("No members in guild " + self.id + ".  Impossible... guild is disbanding")
                rs.close()
                ps.close()
                self.proper = False
                return
            leaderCheck = False
            while True:
                if rs.getInt("id") == self.leader:
                    leaderCheck = True
                self.members.add(MapleGuildCharacter(rs.getInt("id"), rs.getShort("level"), rs.getString("name"), (byte)(-1), rs.getInt("job"), rs.getByte("guildrank"), guildid, rs.getByte("alliancerank"), False))
            rs.close()
            ps.close()
            if !leaderCheck:
                print("Leader " + self.leader + " isn't in guild " + self.id + ".  Impossible... guild is disbanding.")
                self.proper = False
                return
            ps = con.prepareStatement("SELECT * FROM bbs_threads WHERE guildid = ? ORDER BY localthreadid DESC")
            ps.setInt(1, guildid)
            rs = ps.executeQuery()
            while rs.next():
                thread = MapleBBSThread(rs.getInt("localthreadid"), rs.getString("name"), rs.getString("startpost"), rs.getLong("timestamp"), guildid, rs.getInt("postercid"), rs.getInt("icon"))
                pse = con.prepareStatement("SELECT * FROM bbs_replies WHERE threadid = ?")
                pse.setInt(1, rs.getInt("threadid"))
                rse = pse.executeQuery()
                while rse.next():
                    thread.replies.put(thread.replies, new MapleBBSThread.MapleBBSReply(thread.replies, rse.getInt("postercid"), rse.getString("content"), rse.getLong("timestamp")))
                rse.close()
                pse.close()
                self.bbs.put(rs.getInt("localthreadid"), thread)
            rs.close()
            ps.close()
        except Exception as se:
            print("unable to read guild information from sql")
            se.printStackTrace()

    # Static initializer
    # MapleGuild.serialVersionUID = 6322150443228168192


    def displayGuildRanks(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `GP`, `logoBG`, `logoBGColor`, `logo`, `logoColor` FROM guilds ORDER BY `GP` DESC LIMIT 50")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.showGuildRanks(npcid, rs))
            ps.close()
            rs.close()
        catch (SQLException ex) {}

    def meso(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`,`meso`,`vip`, `level`FROM characters ORDER BY `meso` DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.showMesoRanks(npcid, rs))
            ps.close()
            rs.close()
        catch (SQLException ex) {}

    def translated_战斗力排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            rs = None
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("select `name`, ((`level` * 15) + CASE WHEN fame < 0 THEN 0 ELSE fame END + (maxhp / 50) + (maxmp / 50) + str + dex + luk + `int`) AS `data`, `level`, meso from characters order by `data` desc LIMIT 100")
            try:
                rs = ps.executeQuery()
                c.getSession().write(MaplePacketCreator.showCustomRanks(npcid, rs))
            rs.close()
        except Exception as e:
            print("战斗力排行出错！")

    def translated_破攻排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            rs = None
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("select `name`, `PGMaxDamage` AS `data`, `level`, meso from characters order by `data` desc LIMIT 100")
            try:
                rs = ps.executeQuery()
                c.getSession().write(MaplePacketCreator.showCustomRanks(npcid, rs))
            rs.close()
        except Exception as e:
            print("破攻排行出错！")

    def translated_总在线时间排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            rs = None
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("select `name`, totalOnlineTime AS `data`, `level`, meso from characters order by `data` desc LIMIT 100")
            try:
                rs = ps.executeQuery()
                c.getSession().write(MaplePacketCreator.showCustomRanks(npcid, rs))
            rs.close()
        except Exception as e:
            print("总在线时间排行出错！")

    def displayLevelRanks(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `vip`, `level`, `meso` FROM characters ORDER BY `level` DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.showLevelRanks(npcid, rs))
            ps.close()
            rs.close()
        catch (SQLException ex) {}

    def translated_豆豆排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            rs = None
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("select `name`, beans AS `data`, `level`, meso from characters order by `data` desc LIMIT 100")
            try:
                rs = ps.executeQuery()
                c.getSession().write(MaplePacketCreator.showCustomRanks(npcid, rs))
            rs.close()
        except Exception as e:
            print("豆豆排行出错！")

    def translated_VIP排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `vip`, `level`, `meso` FROM characters ORDER BY `vip` DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.showVipRanks(npcid, rs))
            ps.close()
            rs.close()
        catch (SQLException ex) {}

    def MapleMSpvpdeaths(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `pvpdeaths`, `str`, `dex`, `int`, `luk` FROM characters ORDER BY `pvpdeaths` DESC LIMIT 20")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.MapleMSpvpdeaths(npcid, rs))
            ps.close()
            rs.close()
        except Exception as e:
            print("failed to display guild ranks." + e)

    def MapleMSpvpkills(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `pvpkills`, `str`, `dex`, `int`, `luk` FROM characters ORDER BY `pvpkills` WHERE gm < 1  DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.MapleMSpvpkills(npcid, rs))
            ps.close()
            rs.close()
        except Exception as e:
            print("failed to display guild ranks." + e)

    def translated_人气排行(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `fame`, `level`, `meso` FROM characters ORDER BY `fame` DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.showRQRanks(npcid, rs))
            ps.close()
            rs.close()
        catch (SQLException ex) {}

    def loadAll(self) -> list:
        ret = []
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT guildid FROM guilds")
            rs = ps.executeQuery()
            while rs.next():
                g = MapleGuild(rs.getInt("guildid"))
                if g.getId() > 0:
                    ret.add(g)
            rs.close()
            ps.close()
        except Exception as se:
            print("unable to read guild information from sql")
            se.printStackTrace()
        return ret

    def createGuild(self, leaderId: int, name: str) -> int:
        if name > 12:
            return 0
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT guildid FROM guilds WHERE name = ?")
            ps.setString(1, name)
            rs = ps.executeQuery()
            if rs.first():
                rs.close()
                ps.close()
                return 0
            ps.close()
            rs.close()
            ps = con.prepareStatement("INSERT INTO guilds (`leader`, `name`, `signature`, `alliance`) VALUES (?, ?, ?, 0)", 1)
            ps.setInt(1, leaderId)
            ps.setString(2, name)
            ps.setInt(3, (int)(int(time.time() * 1000) / 1000))
            ps.execute()
            rs = ps.getGeneratedKeys()
            ret = 0
            if rs.next():
                ret = rs.getInt(1)
            rs.close()
            ps.close()
            return ret
        except Exception as se:
            print("SQL THROW")
            se.printStackTrace()
            return 0

    def sendInvite(self, c: Any, targetName: str) -> Any:
        mc = c.getChannelServer().getPlayerStorage().getCharacterByName(targetName)
        if mc is None:
            return MapleGuildResponse.NOT_IN_CHANNEL
        if mc.getGuildId() > 0:
            return MapleGuildResponse.ALREADY_IN_GUILD
        mc.getClient().getSession().write(MaplePacketCreator.guildInvite(c.getPlayer().getGuildId(), c.getPlayer().getName(), c.getPlayer().getLevel(), c.getPlayer().getJob()))
        return None

    def setOfflineGuildStatus(self, guildid: int, guildrank: int, alliancerank: int, cid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE characters SET guildid = ?, guildrank = ?, alliancerank = ? WHERE id = ?")
            ps.setInt(1, guildid)
            ps.setInt(2, guildrank)
            ps.setInt(3, alliancerank)
            ps.setInt(4, cid)
            ps.execute()
            ps.close()
        except Exception as se:
            print("SQLException: " + se.getLocalizedMessage())
            se.printStackTrace()

    def isProper(self) -> bool:
        return self.proper

    def writeGPToDB(self) -> None:
        try:
            con = DatabaseConnection.getConnection()
            buf = ""
            buf.append(" WHERE guildid = ?")
            ps = con.prepareStatement(buf)
            ps.setInt(1, self.gp)
            ps.setInt(2, self.id)
            ps.execute()
            ps.close()
        except Exception as se:
            print("Error saving guildGP to SQL")
            se.printStackTrace()

    def writeToDB(self, bDisband: bool) -> None:
        try:
            con = DatabaseConnection.getConnection()
            if !bDisband:
                buf = ""
                for i in range(1, 6):
                    buf.append("rank").append(i).append("title = ?, ")
                buf.append("capacity = ?, notice = ?, alliance = ? WHERE guildid = ?")
                ps = con.prepareStatement(buf)
                ps.setInt(1, self.gp)
                ps.setInt(2, self.logo)
                ps.setInt(3, self.logoColor)
                ps.setInt(4, self.logoBG)
                ps.setInt(5, self.logoBGColor)
                ps.setString(6, self.rankTitles[0])
                ps.setString(7, self.rankTitles[1])
                ps.setString(8, self.rankTitles[2])
                ps.setString(9, self.rankTitles[3])
                ps.setString(10, self.rankTitles[4])
                ps.setInt(11, self.capacity)
                ps.setString(12, self.notice)
                ps.setInt(13, self.allianceid)
                ps.setInt(14, self.id)
                ps.execute()
                ps.close()
                ps = con.prepareStatement("DELETE FROM bbs_threads WHERE guildid = ?")
                ps.setInt(1, self.id)
                ps.execute()
                ps.close()
                ps = con.prepareStatement("DELETE FROM bbs_replies WHERE guildid = ?")
                ps.setInt(1, self.id)
                ps.execute()
                ps.close()
                ps = con.prepareStatement("INSERT INTO bbs_threads(`postercid`, `name`, `timestamp`, `icon`, `startpost`, `guildid`, `localthreadid`) VALUES(?, ?, ?, ?, ?, ?, ?)", 1)
                ps.setInt(6, self.id)
                for bb in self.bbs.values():
                    ps.setInt(1, bb.ownerID)
                    ps.setString(2, bb.name)
                    ps.setLong(3, bb.timestamp)
                    ps.setInt(4, bb.icon)
                    ps.setString(5, bb.text)
                    ps.setInt(7, bb.localthreadID)
                    ps.executeUpdate()
                    rs = ps.getGeneratedKeys()
                    if !rs.next():
                        rs.close()
                    else:
                        pse = con.prepareStatement("INSERT INTO bbs_replies (`threadid`, `postercid`, `timestamp`, `content`, `guildid`) VALUES (?, ?, ?, ?, ?)")
                        pse.setInt(5, self.id)
                        for (final MapleBBSThread.MapleBBSReply r : bb.replies.values())
                            pse.setInt(1, rs.getInt(1))
                            pse.setInt(2, r.ownerID)
                            pse.setLong(3, r.timestamp)
                            pse.setString(4, r.content)
                            pse.execute()
                        pse.close()
                        rs.close()
                ps.close()
            else:
                ps2 = con.prepareStatement("UPDATE characters SET guildid = 0, guildrank = 5, alliancerank = 5 WHERE guildid = ?")
                ps2.setInt(1, self.id)
                ps2.execute()
                ps2.close()
                ps2 = con.prepareStatement("DELETE FROM bbs_threads WHERE guildid = ?")
                ps2.setInt(1, self.id)
                ps2.execute()
                ps2.close()
                ps2 = con.prepareStatement("DELETE FROM bbs_replies WHERE guildid = ?")
                ps2.setInt(1, self.id)
                ps2.execute()
                ps2.close()
                ps2 = con.prepareStatement("DELETE FROM guilds WHERE guildid = ?")
                ps2.setInt(1, self.id)
                ps2.execute()
                ps2.close()
                if self.allianceid > 0:
                    alliance = World.Alliance.getAlliance(self.allianceid)
                    if alliance is not None:
                        alliance.removeGuild(self.id, False)
                self.broadcast(MaplePacketCreator.guildDisband(self.id))
        except Exception as se:
            print("Error saving guild to SQL")
            se.printStackTrace()

    def translated_杀怪排行榜(self, c: Any, npcid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT `name`, `shaguai`, `str`, `dex`, `int`, `luk` FROM characters ORDER BY `shaguai` DESC LIMIT 100")
            rs = ps.executeQuery()
            c.getSession().write(MaplePacketCreator.杀怪排行榜(npcid, rs))
            ps.close()
            rs.close()
        except Exception as e:
            print("获取杀怪排行出错" + e)

    def getId(self) -> int:
        return self.id

    def getLeaderId(self) -> int:
        return self.leader

    def getLeader(self, c: Any) -> Any:
        return c.getChannelServer().getPlayerStorage().getCharacterById(self.leader)

    def getGP(self) -> int:
        return self.gp

    def getLogo(self) -> int:
        return self.logo

    def setLogo(self, l: int) -> None:
        self.logo = l

    def getLogoColor(self) -> int:
        return self.logoColor

    def setLogoColor(self, c: int) -> None:
        self.logoColor = c

    def getLogoBG(self) -> int:
        return self.logoBG

    def setLogoBG(self, bg: int) -> None:
        self.logoBG = bg

    def getLogoBGColor(self) -> int:
        return self.logoBGColor

    def setLogoBGColor(self, c: int) -> None:
        self.logoBGColor = c

    def getNotice(self) -> str:
        if self.notice is None:
            return ""
        return self.notice

    def getName(self) -> str:
        return self.name

    def getCapacity(self) -> int:
        return self.capacity

    def getSignature(self) -> int:
        return self.signature

    def broadcast(self, packet: Any) -> None:
        self.broadcast(packet, -1, BCOp.NONE)

    def broadcast_packet_exception(self, packet: Any, exception: int) -> None:
        self.broadcast(packet, exception, BCOp.NONE)

    def broadcast_packet_exceptionId_bcop(self, packet: Any, exceptionId: int, bcop: Any) -> None:
        self.wL.lock()
        try:
            self.buildNotifications()
        finally:
            self.wL.unlock()
        self.rL.lock()
        try:
            for mgc in self.members:
                if bcop == BCOp.DISBAND:
                    if mgc.isOnline():
                        World.Guild.setGuildAndRank(mgc.getId(), 0, 5, 5)
                    else:
                        setOfflineGuildStatus(0, 5, 5, mgc.getId())
                else:
                    if !mgc.isOnline() || mgc.getId() == exceptionId:
                        continue
                    if bcop == BCOp.EMBELMCHANGE:
                        World.Guild.changeEmblem(self.id, mgc.getId(), MapleGuildSummary(this))
                    else:
                        World.Broadcast.sendGuildPacket(mgc.getId(), packet, exceptionId, self.id)
        finally:
            self.rL.unlock()

    def buildNotifications(self) -> None:
        if !self.bDirty:
            return
        mem = []
        for mgc in self.members:
            if !mgc.isOnline():
                continue
            if (mgc.getId( in mem)) || mgc.getGuildId() != self.id:
                self.members.remove(mgc)
            else:
                mem.add(mgc.getId())
        self.bDirty = False

    def setOnline(self, cid: int, online: bool, channel: int) -> None:
        bBroadcast = True
        for mgc in self.members:
            if mgc.getGuildId() == self.id && mgc.getId() == cid:
                if mgc.isOnline() == online:
                    bBroadcast = False
                mgc.setOnline(online)
                mgc.setChannel(channel)
                break
        if bBroadcast:
            self.broadcast(MaplePacketCreator.guildMemberOnline(self.id, cid, online), cid)
            if self.allianceid > 0:
                World.Alliance.sendGuild(MaplePacketCreator.allianceMemberOnline(self.allianceid, self.id, cid, online), self.id, self.allianceid)
        self.bDirty = True
        self.init = True

    def guildChat(self, name: str, cid: int, msg: str) -> None:
        self.broadcast(MaplePacketCreator.multiChat(name, msg, 2), cid)

    def allianceChat(self, name: str, cid: int, msg: str) -> None:
        self.broadcast(MaplePacketCreator.multiChat(name, msg, 3), cid)

    def getRankTitle(self, rank: int) -> str:
        return self.rankTitles[rank - 1]

    def getAllianceId(self) -> int:
        return self.allianceid

    def getInvitedId(self) -> int:
        return self.invitedid

    def setInvitedId(self, iid: int) -> None:
        self.invitedid = iid

    def setAllianceId(self, a: int) -> None:
        self.allianceid = a
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE guilds SET alliance = ? WHERE guildid = ?")
            ps.setInt(1, a)
            ps.setInt(2, self.id)
            ps.execute()
            ps.close()
        except Exception as e:
            print("Saving allianceid ERROR" + e)

    def addGuildMember(self, mgc: Any) -> int:
        self.wL.lock()
        try:
            if self.members >= self.capacity:
                return 0
            i = self.members - 1
            while i >= 0:
                if self.members.get(i).getGuildRank() < 5 || self.members.get(i).getName().compareTo(mgc.getName()) < 0:
                    self.members.add(i + 1, mgc)
                    self.bDirty = True
                    break
        finally:
            self.wL.unlock()
        self.gainGP(50)
        self.broadcast(MaplePacketCreator.newGuildMember(mgc))
        if self.allianceid > 0:
            World.Alliance.sendGuild(self.allianceid)
        return 1

    def leaveGuild(self, mgc: Any) -> None:
        self.broadcast(MaplePacketCreator.memberLeft(mgc, False))
        self.gainGP(-50)
        self.wL.lock()
        try:
            self.bDirty = True
            self.members.remove(mgc)
            if mgc.isOnline():
                World.Guild.setGuildAndRank(mgc.getId(), 0, 5, 5)
            else:
                setOfflineGuildStatus(0, 5, 5, mgc.getId())
            if self.allianceid > 0:
                World.Alliance.sendGuild(self.allianceid)
        finally:
            self.wL.unlock()

    def expelMember(self, initiator: Any, name: str, cid: int) -> None:
        self.wL.lock()
        try:
            for mgc in self.members:
                if mgc.getId() == cid && initiator.getGuildRank() < mgc.getGuildRank():
                    self.broadcast(MaplePacketCreator.memberLeft(mgc, True))
                    self.bDirty = True
                    self.gainGP(-50)
                    if self.allianceid > 0:
                        World.Alliance.sendGuild(self.allianceid)
                    if mgc.isOnline():
                        World.Guild.setGuildAndRank(cid, 0, 5, 5)
                    else:
                        MapleCharacterUtil.sendNote(mgc.getName(), initiator.getName(), "You have been expelled from the guild.", 0)
                        setOfflineGuildStatus(0, 5, 5, cid)
                    self.members.remove(mgc)
                    break
        finally:
            self.wL.unlock()

    def changeARank(self) -> None:
        self.changeARank(False)

    def changeARank_leader(self, leader: bool) -> None:
        for mgc in self.members:
            if self.leader == mgc.getId():
                self.changeARank(mgc.getId(), leader ? 1 : 2)
            else:
                self.changeARank(mgc.getId(), 3)

    def changeARank_newRank(self, newRank: int) -> None:
        for mgc in self.members:
            self.changeARank(mgc.getId(), newRank)

    def changeARank_cid_newRank(self, cid: int, newRank: int) -> None:
        if self.allianceid <= 0:
            return
        for mgc in self.members:
            if cid == mgc.getId():
                if mgc.isOnline():
                    World.Guild.setGuildAndRank(cid, self.id, mgc.getGuildRank(), newRank)
                else:
                    setOfflineGuildStatus(self.id, mgc.getGuildRank(), newRank, cid)
                mgc.setAllianceRank(newRank)
                World.Alliance.sendGuild(self.allianceid)
                return
        print("INFO: unable to find the correct id for changeRank({" + cid + "}, {" + newRank + "})")

    def changeRank(self, cid: int, newRank: int) -> None:
        for mgc in self.members:
            if cid == mgc.getId():
                if mgc.isOnline():
                    World.Guild.setGuildAndRank(cid, self.id, newRank, mgc.getAllianceRank())
                else:
                    setOfflineGuildStatus(self.id, newRank, mgc.getAllianceRank(), cid)
                mgc.setGuildRank(newRank)
                self.broadcast(MaplePacketCreator.changeRank(mgc))
                return
        print("INFO: unable to find the correct id for changeRank({" + cid + "}, {" + newRank + "})")

    def setGuildNotice(self, notice: str) -> None:
        self.notice = notice
        self.broadcast(MaplePacketCreator.guildNotice(self.id, notice))

    def memberLevelJobUpdate(self, mgc: Any) -> None:
        for member in self.members:
            if member.getId() == mgc.getId():
                old_level = member.getLevel()
                old_job = member.getJobId()
                member.setJobId(mgc.getJobId())
                member.setLevel(mgc.getLevel())
                if mgc.getLevel() > old_level:
                    self.gainGP((mgc.getLevel() - old_level) * mgc.getLevel() / 10, False)
                if (old_level != mgc.getLevel()) {}
                if (old_job != mgc.getJobId()) {}
                self.broadcast(MaplePacketCreator.guildMemberLevelJobUpdate(mgc))
                if self.allianceid > 0:
                    World.Alliance.sendGuild(MaplePacketCreator.updateAlliance(mgc, self.allianceid), self.id, self.allianceid)
                    break
                break

    def changeRankTitle(self, ranks: list) -> None:
        for i in range(5):
            self.rankTitles[i] = ranks[i]
        self.broadcast(MaplePacketCreator.rankTitleChange(self.id, ranks))

    def disbandGuild(self) -> None:
        self.writeToDB(True)
        self.broadcast(None, -1, BCOp.DISBAND)

    def setGuildEmblem(self, bg: int, bgcolor: int, logo: int, logocolor: int) -> None:
        self.logoBG = bg
        self.logoBGColor = bgcolor
        self.logo = logo
        self.logoColor = logocolor
        self.broadcast(None, -1, BCOp.EMBELMCHANGE)
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE guilds SET logo = ?, logoColor = ?, logoBG = ?, logoBGColor = ? WHERE guildid = ?")
            ps.setInt(1, logo)
            ps.setInt(2, self.logoColor)
            ps.setInt(3, self.logoBG)
            ps.setInt(4, self.logoBGColor)
            ps.setInt(5, self.id)
            ps.execute()
            ps.close()
        except Exception as e:
            print("Saving guild logo / BG colo ERROR")
            e.printStackTrace()

    def getMGC(self, cid: int) -> Any:
        for mgc in self.members:
            if mgc.getId() == cid:
                return mgc
        return None

    def increaseCapacity(self) -> bool:
        if self.capacity >= 100 || self.capacity + 5 > 100:
            return False
        self.capacity += 5
        self.broadcast(MaplePacketCreator.guildCapacityChange(self.id, self.capacity))
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE guilds SET capacity = ? WHERE guildid = ?")
            ps.setInt(1, self.capacity)
            ps.setInt(2, self.id)
            ps.execute()
            ps.close()
        except Exception as e:
            print("Saving guild capacity ERROR")
            e.printStackTrace()
        return True

    def gainGP(self, amount: int) -> None:
        self.gainGP(amount, True)

    def gainGP_amount_broadcast(self, amount: int, broadcast: bool) -> None:
        if amount == 0:
            return
        if amount + self.gp < 0:
            amount = -self.gp
        self.gp += amount
        self.broadcast(MaplePacketCreator.updateGP(self.id, self.gp))
        if broadcast:
            self.broadcast(UIPacket.getGPMsg(amount))

    def addMemberData(self, mplew: Any) -> None:
        mplew.write(self.members)
        for mgc in self.members:
            mplew.writeInt(mgc.getId())
        for mgc in self.members:
            mplew.writeAsciiString(StringUtil.getRightPaddedStr(mgc.getName(), '\0', 13))
            mplew.writeInt(mgc.getJobId())
            mplew.writeInt(mgc.getLevel())
            mplew.writeInt(mgc.getGuildRank())
            mplew.writeInt(mgc.isOnline() ? 1 : 0)
            mplew.writeInt(self.signature)
            mplew.writeInt(mgc.getAllianceRank())

    def getMembers(self) -> list:
        return Collections.unmodifiableCollection((Collection<? extends MapleGuildCharacter>)self.members)

    def isInit(self) -> bool:
        return self.init

    def getBBS(self) -> list:
        ret = [])
        Collections.sort(ret, new MapleBBSThread.ThreadComparator())
        return ret

    def addBBSThread(self, title: str, text: str, icon: int, bNotice: bool, posterID: int) -> int:
        add = (self.bbs.get(0) is None) ? 1 : 0
        ret = bNotice ? 0 : max(1, self.bbs + add)
        self.bbs.put(ret, MapleBBSThread(ret, title, text, int(time.time() * 1000), self.id, posterID, icon))
        return ret

    def editBBSThread(self, localthreadid: int, title: str, text: str, icon: int, posterID: int, guildRank: int) -> None:
        thread = self.bbs.get(localthreadid)
        if thread is not None && (thread.ownerID == posterID || guildRank <= 2):
            self.bbs.put(localthreadid, MapleBBSThread(localthreadid, title, text, int(time.time() * 1000), self.id, thread.ownerID, icon))

    def deleteBBSThread(self, localthreadid: int, posterID: int, guildRank: int) -> None:
        thread = self.bbs.get(localthreadid)
        if thread is not None && (thread.ownerID == posterID || guildRank <= 2):
            self.bbs.remove(localthreadid)

    def addBBSReply(self, localthreadid: int, text: str, posterID: int) -> None:
        thread = self.bbs.get(localthreadid)
        if thread is not None:
            thread.replies.put(thread.replies, new MapleBBSThread.MapleBBSReply(thread.replies, posterID, text, int(time.time() * 1000)))

    def deleteBBSReply(self, localthreadid: int, replyid: int, posterID: int, guildRank: int) -> None:
        thread = self.bbs.get(localthreadid)
        if thread is not None:
            final MapleBBSThread.MapleBBSReply reply = thread.replies.get(replyid)
            if reply is not None && (reply.ownerID == posterID || guildRank <= 2):
                thread.replies.remove(replyid)

    def getPrefix(self, chr: Any) -> int:
        return chr.getPrefix()


# Inner class from Java (originally nested)
class BCOp(Enum):
    """Enum BCOp"""

    NONE = 0
    DISBAND = 1
    EMBELMCHANGE = 2

