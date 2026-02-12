"""
BuddyList - Converted from Java source
Original: client/BuddyList.java
Package: client
"""

from enum import Enum, IntEnum
from pymysql import Connection
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from database import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes


class BuddyList:
    """
    Class BuddyList
    Implements: Serializable
    """

    def __init__(self, capacity: int):
        self.buddies = {}
        self.capacity = 0
        self.pendingReqs = None
        self.changed = False
        self.pendingReqs = []
        self.changed = False
        self.buddies = {}
        self.capacity = capacity

    # Static initializer
    # BuddyList.DEFAULT_GROUP = "其他"


    def getBuddyCount(self, chrId: int, pending: int) -> int:
        count = 0
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT COUNT(*) as buddyCount FROM buddies WHERE characterid = ? AND pending = ?")
        try:
            ps.setInt(1, chrId)
            ps.setInt(2, pending)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if not rs.next():
                    raise RuntimeError("BuddyListHandler: getBuudyCount From DB is Error.")
                count = rs.getInt("buddyCount")
        except Exception as ex:
            ex.printStackTrace()
        return count

    def getBuddyCapacity(self, charId: int) -> int:
        capacity = -1
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT buddyCapacity FROM characters WHERE id = ?")
        try:
            ps.setInt(1, charId)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    capacity = rs.getInt("buddyCapacity")
        except Exception as ex:
            ex.printStackTrace()
        return capacity

    def getBuddyPending(self, chrId: int, buddyId: int) -> int:
        pending = -1
        con = DatabaseConnection.getConnection()
        # try-with-resources: final PreparedStatement ps = con.prepareStatement("SELECT pending FROM buddies WHERE characterid = ? AND buddyid = ?")
        try:
            ps.setInt(1, chrId)
            ps.setInt(2, buddyId)
            # try-with-resources: final ResultSet rs = ps.executeQuery()
            try:
                if rs.next():
                    pending = rs.getInt("pending")
        except Exception as ex:
            ex.printStackTrace()
        return pending

    def addBuddyToDB(self, player: Any, buddy: Any) -> None:
        try:
            con = DatabaseConnection.getConnection()
            # try-with-resources: final PreparedStatement ps = con.prepareStatement("INSERT INTO buddies (`characterid`, `buddyid`, `groupname`, `pending`) VALUES (?, ?, ?, 1)")
            try:
                ps.setInt(1, buddy.getCharacterId())
                ps.setInt(2, player.getId())
                ps.setString(3, buddy.getGroup())
                ps.executeUpdate()
        except Exception as ex:
            ex.printStackTrace()

    def contains(self, characterId: int) -> bool:
        return (characterId in self.buddies)

    def containsVisible(self, charId: int) -> bool:
        ble = self.buddies.get(charId)
        return ble is not None and ble.isVisible()

    def getCapacity(self) -> int:
        return self.capacity

    def setCapacity(self, newCapacity: int) -> None:
        self.capacity = newCapacity

    def get(self, characterId: int) -> Any:
        return self.buddies.get(characterId)

    def get_characterName(self, characterName: str) -> Any:
        searchName = characterName.lower()
        for ble in self.buddies.values():
            if ble.getName().lower() == (searchName):
                return ble
        return None

    def put(self, newEntry: Any) -> None:
        self.buddies.put(newEntry.getCharacterId(), newEntry)
        self.changed = True

    def remove(self, characterId: int) -> None:
        self.buddies.remove(characterId)
        self.changed = True

    def getBuddies(self) -> list:
        return self.buddies.values()

    def isFull(self) -> bool:
        return self.buddies >= self.capacity

    def getBuddiesIds(self) -> list:
        return self.buddies.keys()

    def loadFromTransfer(self, data: dict) -> None:
        for (final Map.Entry<BuddyEntry, Boolean> qs : data.items())
            buddyid = qs.getKey()
            pair = qs.getValue()
            if not pair:
                self.pendingReqs.push(buddyid)
            else:
                self.put(BuddyEntry(buddyid.getName(), buddyid.getCharacterId(), buddyid.getGroup(), -1, True, buddyid.getLevel(), buddyid.getJob()))

    def loadFromDb(self, characterId: int) -> None:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("SELECT b.buddyid, b.pending, c.name as buddyname, c.job as buddyjob, c.level as buddylevel, b.groupname FROM buddies as b, characters as c WHERE c.id = b.buddyid AND b.characterid = ?")
        ps.setInt(1, characterId)
        rs = ps.executeQuery()
        while rs.next():
            buddyid = rs.getInt("buddyid")
            buddyname = rs.getString("buddyname")
            if rs.getInt("pending") == 1:
                self.pendingReqs.push(BuddyEntry(buddyname, buddyid, rs.getString("groupname"), -1, False, rs.getInt("buddylevel"), rs.getInt("buddyjob")))
            else:
                self.put(BuddyEntry(buddyname, buddyid, rs.getString("groupname"), -1, True, rs.getInt("buddylevel"), rs.getInt("buddyjob")))
        rs.close()
        ps.close()
        ps = con.prepareStatement("DELETE FROM buddies WHERE pending = 1 AND characterid = ?")
        ps.setInt(1, characterId)
        ps.executeUpdate()
        ps.close()

    def pollPendingRequest(self) -> Any:
        return self.pendingReqs.pollLast()

    def addBuddyRequest(self, client: Any, buddyId: int, buddyName: str, buddyChannel: int, buddyLevel: int, buddyJob: int) -> None:
        self.put(BuddyEntry(buddyName, buddyId, BuddyList.DEFAULT_GROUP, buddyChannel, False, buddyLevel, buddyJob))
        if self.pendingReqs == 0:
            client.sendPacket(MaplePacketCreator.requestBuddylistAdd(buddyId, buddyName, buddyLevel, buddyJob))
        else:
            newPair = BuddyEntry(buddyName, buddyId, BuddyList.DEFAULT_GROUP, -1, False, buddyJob, buddyLevel)
            self.pendingReqs.push(newPair)

    def setChanged(self, v: bool) -> None:
        self.changed = v

    def changed(self) -> bool:
        return self.changed


# Inner class from Java (originally nested)
class BuddyOperation(Enum):
    """Enum BuddyOperation"""

    ADDED = 0
    DELETED = 1


# Inner class from Java (originally nested)
class BuddyAddResult(Enum):
    """Enum BuddyAddResult"""

    BUDDYLIST_FULL = 0
    ALREADY_ON_LIST = 1
    OK = 2

