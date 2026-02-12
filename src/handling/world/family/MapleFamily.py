"""
MapleFamily - Converted from Java source
Original: handling/world/family/MapleFamily.java
Package: handling.world.family
"""

from enum import Enum, IntEnum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from typing import Collection
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.FamilyPacket import *  # TODO: import specific classes


class MapleFamily:
    """
    Class MapleFamily
    Implements: Serializable
    """

    def __init__(self, fid: int):
        self.members = {}
        self.leadername = ""
        self.notice = ""
        self.id = 0
        self.leaderid = 0
        self.generations = 0
        self.proper = False
        self.bDirty = False
        self.changed = False
        self.members = {}
        self.leadername = None
        self.generations = 0
        self.proper = True
        self.bDirty = False
        self.changed = False
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM families WHERE familyid = ?")
            ps.setInt(1, fid)
            rs = ps.executeQuery()
            if not rs.first():
                rs.close()
                ps.close()
                self.id = -1
                return
            self.id = fid
            self.leaderid = rs.getInt("leaderid")
            self.notice = rs.getString("notice")
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT id, name, level, job, seniorid, junior1, junior2, currentrep, totalrep FROM characters WHERE familyid = ?")
            ps.setInt(1, fid)
            rs = ps.executeQuery()
            while rs.next():
                if rs.getInt("id") == self.leaderid:
                    self.leadername = rs.getString("name")
                self.members.put(rs.getInt("id"), MapleFamilyCharacter(rs.getInt("id"), rs.getShort("level"), rs.getString("name"), -1, rs.getInt("job"), fid, rs.getInt("seniorid"), rs.getInt("junior1"), rs.getInt("junior2"), rs.getInt("currentrep"), rs.getInt("totalrep"), False))
            rs.close()
            ps.close()
            if self.leadername is None or self.members < 2:
                print("Leader " + self.leaderid + " isn't in family " + self.id + ". Impossible... family is disbanding.")
                self.proper = False
                return
            for mfc in self.members.values():
                if mfc.getJunior1() > 0 and (self.getMFC(mfc.getJunior1()) is None or mfc.getId() == mfc.getJunior1()):
                    mfc.setJunior1(0)
                if mfc.getJunior2() > 0 and (self.getMFC(mfc.getJunior2()) is None or mfc.getId() == mfc.getJunior2() or mfc.getJunior1() == mfc.getJunior2()):
                    mfc.setJunior2(0)
                if mfc.getSeniorId() > 0 and (self.getMFC(mfc.getSeniorId()) is None or mfc.getId() == mfc.getSeniorId()):
                    mfc.setSeniorId(0)
                if mfc.getJunior2() > 0 and mfc.getJunior1() <= 0:
                    mfc.setJunior1(mfc.getJunior2())
                    mfc.setJunior2(0)
                if mfc.getJunior1() > 0:
                    mfc2 = self.getMFC(mfc.getJunior1())
                    if mfc2.getJunior1() == mfc.getId():
                        mfc2.setJunior1(0)
                    if mfc2.getJunior2() == mfc.getId():
                        mfc2.setJunior2(0)
                    if mfc2.getSeniorId() != mfc.getId():
                        mfc2.setSeniorId(mfc.getId())
                if mfc.getJunior2() > 0:
                    mfc2 = self.getMFC(mfc.getJunior2())
                    if mfc2.getJunior1() == mfc.getId():
                        mfc2.setJunior1(0)
                    if mfc2.getJunior2() == mfc.getId():
                        mfc2.setJunior2(0)
                    if mfc2.getSeniorId() == mfc.getId():
                        continue
                    mfc2.setSeniorId(mfc.getId())
            self.resetPedigree()
            self.resetDescendants()
            self.resetGens()
        except Exception as se:
            print("unable to read family information from sql")
            se.printStackTrace()

    # Static initializer
    # MapleFamily.serialVersionUID = 6322150443228168192


    def loadAll(self) -> list:
        ret = []
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT familyid FROM families")
            rs = ps.executeQuery()
            while rs.next():
                g = MapleFamily(rs.getInt("familyid"))
                if g.getId() > 0:
                    ret.add(g)
            rs.close()
            ps.close()
        except Exception as se:
            print("unable to read family information from sql")
            se.printStackTrace()
        return ret

    def setOfflineFamilyStatus(self, familyid: int, seniorid: int, junior1: int, junior2: int, currentrep: int, totalrep: int, cid: int) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE characters SET familyid = ?, seniorid = ?, junior1 = ?, junior2 = ?, currentrep = ?, totalrep = ? WHERE id = ?")
            ps.setInt(1, familyid)
            ps.setInt(2, seniorid)
            ps.setInt(3, junior1)
            ps.setInt(4, junior2)
            ps.setInt(5, currentrep)
            ps.setInt(6, totalrep)
            ps.setInt(7, cid)
            ps.execute()
            ps.close()
        except Exception as se:
            print("SQLException: " + se.getLocalizedMessage())
            se.printStackTrace()

    def createFamily(self, leaderId: int) -> int:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("INSERT INTO families (`leaderid`) VALUES (?)", 1)
            ps.setInt(1, leaderId)
            ps.executeUpdate()
            rs = ps.getGeneratedKeys()
            if not rs.next():
                rs.close()
                ps.close()
                return 0
            ret = rs.getInt(1)
            rs.close()
            ps.close()
            return ret
        except Exception as e:
            e.printStackTrace()
            return 0

    def mergeFamily(self, newfam: Any, oldfam: Any) -> None:
        for mgc in oldfam.members.values():
            mgc.setFamilyId(newfam.getId())
            if mgc.isOnline():
                World.Family.setFamily(newfam.getId(), mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
            else:
                setOfflineFamilyStatus(newfam.getId(), mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
            newfam.members.put(mgc.getId(), mgc)
            newfam.setOnline(mgc.getId(), mgc.isOnline(), mgc.getChannel())
        newfam.resetPedigree()
        World.Family.disbandFamily(oldfam.getId())

    def getGens(self) -> int:
        return self.generations

    def resetPedigree(self) -> None:
        for mfc in self.members.values():
            mfc.resetPedigree(this)
        self.bDirty = True

    def resetGens(self) -> None:
        mfc = self.getMFC(self.leaderid)
        if mfc is not None:
            self.generations = mfc.resetGenerations(this)
        self.bDirty = True

    def resetDescendants(self) -> None:
        mfc = self.getMFC(self.leaderid)
        if mfc is not None:
            mfc.resetDescendants(this)
        self.bDirty = True

    def isProper(self) -> bool:
        return self.proper

    def writeToDB(self, bDisband: bool) -> None:
        try:
            con = DatabaseConnection.getConnection()
            if not bDisband:
                if self.changed:
                    ps = con.prepareStatement("UPDATE families SET notice = ? WHERE familyid = ?")
                    ps.setString(1, self.notice)
                    ps.setInt(2, self.id)
                    ps.execute()
                    ps.close()
                self.changed = False
            else:
                ps = con.prepareStatement("DELETE FROM families WHERE familyid = ?")
                ps.setInt(1, self.id)
                ps.execute()
                ps.close()
        except Exception as se:
            print("Error saving family to SQL")
            se.printStackTrace()

    def getId(self) -> int:
        return self.id

    def getLeaderId(self) -> int:
        return self.leaderid

    def getNotice(self) -> str:
        if self.notice is None:
            return ""
        return self.notice

    def getLeaderName(self) -> str:
        return self.leadername

    def broadcast(self, packet: Any, cids: list) -> None:
        self.broadcast(packet, -1, FCOp.NONE, cids)

    def broadcast_packet_exception_cids(self, packet: Any, exception: int, cids: list) -> None:
        self.broadcast(packet, exception, FCOp.NONE, cids)

    def broadcast_packet_exceptionId_bcop_cids(self, packet: Any, exceptionId: int, bcop: Any, cids: list) -> None:
        self.buildNotifications()
        if self.members < 2:
            self.bDirty = True
            return
        for mgc in self.members.values():
            if cids is None or (mgc.getId( in cids)):
                if bcop == FCOp.DISBAND:
                    if mgc.isOnline():
                        World.Family.setFamily(0, 0, 0, 0, mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
                    else:
                        setOfflineFamilyStatus(0, 0, 0, 0, mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
                else:
                    if not mgc.isOnline() or mgc.getId() == exceptionId:
                        continue
                    World.Broadcast.sendFamilyPacket(mgc.getId(), packet, exceptionId, self.id)

    def buildNotifications(self) -> None:
        if not self.bDirty:
            return
        final Iterator<Map.Entry<Integer, MapleFamilyCharacter>> toRemove = self.members.items().iterator()
        while toRemove.hasNext():
            mfc = toRemove.next().getValue()
            if mfc.getJunior1() > 0 and self.getMFC(mfc.getJunior1()) is None:
                mfc.setJunior1(0)
            if mfc.getJunior2() > 0 and self.getMFC(mfc.getJunior2()) is None:
                mfc.setJunior2(0)
            if mfc.getSeniorId() > 0 and self.getMFC(mfc.getSeniorId()) is None:
                mfc.setSeniorId(0)
            if mfc.getFamilyId() != self.id:
                toRemove.remove()
        if self.members < 2 and World.Family.getFamily(self.id) is not None:
            World.Family.disbandFamily(self.id)
        self.bDirty = False

    def setOnline(self, cid: int, online: bool, channel: int) -> None:
        mgc = self.getMFC(cid)
        if mgc is not None and mgc.getFamilyId() == self.id:
            if mgc.isOnline() != online:
                self.broadcast(FamilyPacket.familyLoggedIn(online, mgc.getName()), cid, (mgc.getId() == self.leaderid) ? None : mgc.getPedigree())
            mgc.setOnline(online)
            mgc.setChannel(channel)
        self.bDirty = True

    def setRep(self, cid: int, addrep: int, oldLevel: int) -> int:
        mgc = self.getMFC(cid)
        if mgc is not None and mgc.getFamilyId() == self.id:
            if oldLevel > mgc.getLevel():
                addrep /= 2
            if mgc.isOnline():
                dummy = []
                dummy.add(mgc.getId())
                self.broadcast(FamilyPacket.changeRep(addrep), -1, dummy)
                World.Family.setFamily(self.id, mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep() + addrep, mgc.getTotalRep() + addrep, mgc.getId())
            else:
                setOfflineFamilyStatus(self.id, mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep() + addrep, mgc.getTotalRep() + addrep, mgc.getId())
            return mgc.getSeniorId()
        return 0

    def addFamilyMemberInfo(self, mc: Any, seniorid: int, junior1: int, junior2: int) -> Any:
        ret = MapleFamilyCharacter(mc, self.id, seniorid, junior1, junior2)
        self.members.put(mc.getId(), ret)
        ret.resetPedigree(this)
        self.bDirty = True
        toRemove = []
        for i in range(ret.getPedigree()):
            if ret.getPedigree().get(i) != ret.getId():
                mfc = self.getMFC(ret.getPedigree().get(i))
                if mfc is None:
                    toRemove.add(i)
                else:
                    mfc.resetPedigree(this)
        for j in toRemove:
            ret.getPedigree().remove(j)
        return ret

    def addFamilyMember(self, mgc: Any) -> int:
        mgc.setFamilyId(self.id)
        self.members.put(mgc.getId(), mgc)
        mgc.resetPedigree(this)
        self.bDirty = True
        for i in mgc.getPedigree():
            self.getMFC(i).resetPedigree(this)
        return 1

    def leaveFamily(self, id: int) -> None:
        self.leaveFamily(self.getMFC(id), True)

    def leaveFamily_mgc_skipLeader(self, mgc: Any, skipLeader: bool) -> None:
        self.bDirty = True
        if mgc.getId() == self.leaderid and not skipLeader:
            self.leadername = None
            World.Family.disbandFamily(self.id)
        else:
            if mgc.getJunior1() > 0:
                j = self.getMFC(mgc.getJunior1())
                if j is not None:
                    j.setSeniorId(0)
                    self.splitFamily(j.getId(), j)
            if mgc.getJunior2() > 0:
                j = self.getMFC(mgc.getJunior2())
                if j is not None:
                    j.setSeniorId(0)
                    self.splitFamily(j.getId(), j)
            if mgc.getSeniorId() > 0:
                mfc = self.getMFC(mgc.getSeniorId())
                if mfc is not None:
                    if mfc.getJunior1() == mgc.getId():
                        mfc.setJunior1(0)
                    else:
                        mfc.setJunior2(0)
            dummy = []
            dummy.add(mgc.getId())
            self.broadcast(None, -1, FCOp.DISBAND, dummy)
            self.resetPedigree()
        self.members.remove(mgc.getId())
        self.bDirty = True

    def memberLevelJobUpdate(self, mgc: Any) -> None:
        member = self.getMFC(mgc.getId())
        if member is not None:
            old_level = member.getLevel()
            old_job = member.getJobId()
            member.setJobId(mgc.getJob())
            member.setLevel(mgc.getLevel())
            if old_level != mgc.getLevel():
                self.broadcast(MaplePacketCreator.sendLevelup(True, mgc.getLevel(), mgc.getName()), mgc.getId(), (mgc.getId() == self.leaderid) ? None : member.getPedigree())
            if old_job != mgc.getJob():
                self.broadcast(MaplePacketCreator.sendJobup(True, mgc.getJob(), mgc.getName()), mgc.getId(), (mgc.getId() == self.leaderid) ? None : member.getPedigree())

    def disbandFamily(self) -> None:
        self.writeToDB(True)

    def getMFC(self, cid: int) -> Any:
        return self.members.get(cid)

    def getMemberSize(self) -> int:
        return self.members

    def splitFamily(self, splitId: int, def: Any) -> bool:
        leader = self.getMFC(splitId)
        if leader is None:
            leader = def
            if leader is None:
                return False
        try:
            all = leader.getAllJuniors(this)
            if all <= 1:
                self.leaveFamily(leader, False)
                return True
            newId = createFamily(leader.getId())
            if newId <= 0:
                return False
            for mgc in all:
                mgc.setFamilyId(newId)
                setOfflineFamilyStatus(newId, mgc.getSeniorId(), mgc.getJunior1(), mgc.getJunior2(), mgc.getCurrentRep(), mgc.getTotalRep(), mgc.getId())
                self.members.remove(mgc.getId())
            newfam = World.Family.getFamily(newId)
            for mgc2 in all:
                if mgc2.isOnline():
                    World.Family.setFamily(newId, mgc2.getSeniorId(), mgc2.getJunior1(), mgc2.getJunior2(), mgc2.getCurrentRep(), mgc2.getTotalRep(), mgc2.getId())
                newfam.setOnline(mgc2.getId(), mgc2.isOnline(), mgc2.getChannel())
            if self.members <= 1:
                World.Family.disbandFamily(self.id)
                return True
        finally:
            if self.members <= 1:
                World.Family.disbandFamily(self.id)
                return True
        self.bDirty = True
        return False

    def setNotice(self, notice: str) -> None:
        self.changed = True
        self.notice = notice


# Inner class from Java (originally nested)
class FCOp(Enum):
    """Enum FCOp"""

    NONE = 0
    DISBAND = 1

