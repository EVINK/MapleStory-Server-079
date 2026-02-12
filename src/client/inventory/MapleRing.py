"""
MapleRing - Converted from Java source
Original: client/inventory/MapleRing.java
Package: client.inventory
"""

from pymysql import Connection
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from database import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from server import *  # TODO: import specific classes


class MapleRing:
    """
    Class MapleRing
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738579

    def __init__(self, id: int, id2: int, partnerId: int, itemid: int, partnerName: str):
        self.ringId = None
        self.ringId2 = None
        self.partnerId = None
        self.itemId = None
        self.partnerName = ""
        self.equipped = False
        self.equipped = False
        self.ringId = id
        self.ringId2 = id2
        self.partnerId = partnerId
        self.itemId = itemid
        self.partnerName = partnerName


    def loadFromDb(self, ring: Any) -> Any:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM rings WHERE ringid = ?")
            ps.setInt(1, ring.getUniqueId())
            rs = ps.executeQuery()
            rs.next()
            ret = MapleRing(ring.getItemId(), rs.getInt("partnerRingId"), rs.getInt("partnerChrId"), rs.getInt("itemid"), rs.getString("partnerName"))
            ret.setEquipped(False)
            eq = Equip(ring.getItemId(), ring.getPosition(), ring.getUniqueId(), ring.getFlag())
            rs.close()
            ps.close()
            return eq
        except Exception as ex:
            return None

    def loadFromDb_ringId(self, ringId: int) -> Any:
        return loadFromDb(ringId, False)

    def loadFromDb_ringId_equipped(self, ringId: int, equipped: bool) -> Any:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM rings WHERE ringId = ?")
            ps.setInt(1, ringId)
            rs = ps.executeQuery()
            ret = None
            if rs.next():
                ret = MapleRing(ringId, rs.getInt("partnerRingId"), rs.getInt("partnerChrId"), rs.getInt("itemid"), rs.getString("partnerName"))
                ret.setEquipped(equipped)
            rs.close()
            ps.close()
            return ret
        except Exception as ex:
            ex.printStackTrace()
            return None

    def addToDB(self, itemid: int, chr: Any, player: str, id: int, ringId: list) -> None:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("INSERT INTO rings (ringId, itemid, partnerChrId, partnerName, partnerRingId) VALUES (?, ?, ?, ?, ?)")
        ps.setInt(1, ringId[0])
        ps.setInt(2, itemid)
        ps.setInt(3, chr.getId())
        ps.setString(4, chr.getName())
        ps.setInt(5, ringId[1])
        ps.executeUpdate()
        ps.close()
        ps = con.prepareStatement("INSERT INTO rings (ringId, itemid, partnerChrId, partnerName, partnerRingId) VALUES (?, ?, ?, ?, ?)")
        ps.setInt(1, ringId[1])
        ps.setInt(2, itemid)
        ps.setInt(3, id)
        ps.setString(4, player)
        ps.setInt(5, ringId[0])
        ps.executeUpdate()
        ps.close()

    def createRing(self, itemid: int, partner1: Any, partner2: str, msg: str, id2: int, sn: int) -> int:
        try:
            if partner1 is None:
                return -2
            if id2 <= 0:
                return -1
            return makeRing(itemid, partner1, partner2, id2, msg, sn)
        except Exception as ex:
            ex.printStackTrace()
            return 0

    def makeRing(self, itemid: int, partner1: Any, partner2: str, id2: int, msg: str, sn: int) -> int:
        ringID = { MapleInventoryIdentifier.getInstance(), MapleInventoryIdentifier.getInstance() }
        try:
            addToDB(itemid, partner1, partner2, id2, ringID)
        except MySQLIntegrityConstraintViolationException as mslcve:
            return 0
        MapleInventoryManipulator.addRing(partner1, itemid, ringID[1], sn)
        partner1.getCashInventory().gift(id2, partner1.getName(), msg, sn, ringID[0])
        return 1

    def removeRingFromDb(self, player: Any) -> None:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM rings WHERE partnerChrId = ?")
            ps.setInt(1, player.getId())
            rs = ps.executeQuery()
            if not rs.next():
                ps.close()
                rs.close()
                return
            otherId = rs.getInt("partnerRingId")
            otherotherId = rs.getInt("ringId")
            rs.close()
            ps.close()
            ps = con.prepareStatement("DELETE FROM rings WHERE ringId = ? OR ringId = ?")
            ps.setInt(1, otherotherId)
            ps.setInt(2, otherId)
            ps.executeUpdate()
            ps.close()
        except Exception as sex:
            sex.printStackTrace()

    def getRingId(self) -> int:
        return self.ringId

    def getPartnerRingId(self) -> int:
        return self.ringId2

    def getPartnerChrId(self) -> int:
        return self.partnerId

    def getItemId(self) -> int:
        return self.itemId

    def isEquipped(self) -> bool:
        return self.equipped

    def setEquipped(self, equipped: bool) -> None:
        self.equipped = equipped

    def getPartnerName(self) -> str:
        return self.partnerName

    def setPartnerName(self, partnerName: str) -> None:
        self.partnerName = partnerName

    def equals(self, o: Any) -> bool:
        return isinstance(o, MapleRing) and (o).getRingId() == self.getRingId()

    def hashCode(self) -> int:
        hash = 5
        hash = 53 * hash + self.ringId
        return hash

    def compare(self, o1: Any, o2: Any) -> int:
        if o1.ringId < o2.ringId:
            return -1
        if o1.ringId == o2.ringId:
            return 0
        return 1


# Inner class from Java (originally nested)
class RingComparator(Comparator):
    """
    Class RingComparator
    Implements: Comparator<MapleRing>, Serializable
    """


    def compare(self, o1: Any, o2: Any) -> int:
        if o1.ringId < o2.ringId:
            return -1
        if o1.ringId == o2.ringId:
            return 0
        return 1

