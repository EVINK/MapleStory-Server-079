"""
MapleInventoryIdentifier - Converted from Java source
Original: client/inventory/MapleInventoryIdentifier.java
Package: client.inventory
"""

from pymysql import Connection
from typing import List
from typing import Optional, Any
import pymysql
import threading

# Internal module imports
# from database import *  # TODO: import specific classes


class MapleInventoryIdentifier:
    """
    Class MapleInventoryIdentifier
    Implements: Serializable
    """

    serialVersionUID = 21830921831301

    def __init__(self):
        self.runningUID = None
        self.rwl = None
        self.readLock = None
        self.writeLock = None
        self.rwl = ReentrantReadWriteLock()
        self.readLock = self.rwl.readLock()
        self.writeLock = self.rwl.writeLock()
        self.runningUID = AtomicInteger(0)
        self.getNextUniqueId()

    # Static initializer
    # instance = MapleInventoryIdentifier()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getNextUniqueId(self) -> int:
        if self.grabRunningUID() <= 0:
            self.setRunningUID(self.initUID())
        self.incrementRunningUID()
        return self.grabRunningUID()

    def grabRunningUID(self) -> int:
        self.readLock.lock()
        try:
            return self.runningUID.get()
        finally:
            self.readLock.unlock()

    def incrementRunningUID(self) -> None:
        self.setRunningUID(self.grabRunningUID() + 1)

    def setRunningUID(self, rUID: int) -> None:
        if rUID < self.grabRunningUID():
            return
        self.writeLock.lock()
        try:
            self.runningUID.set(rUID)
        finally:
            self.writeLock.unlock()

    def initUID(self) -> int:
        ret = 0
        if self.grabRunningUID() > 0:
            return self.grabRunningUID()
        try:
            ids = new int[4]
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT MAXFROM inventoryitems")
            rs = ps.executeQuery()
            if rs.next():
                ids[0] = rs.getInt(1) + 1
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT MAXFROM pets")
            rs = ps.executeQuery()
            if rs.next():
                ids[1] = rs.getInt(1) + 1
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT MAXFROM rings")
            rs = ps.executeQuery()
            if rs.next():
                ids[2] = rs.getInt(1) + 1
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT MAXFROM rings")
            rs = ps.executeQuery()
            if rs.next():
                ids[3] = rs.getInt(1) + 1
            rs.close()
            ps.close()
            for i in range(4):
                if ids[i] > ret:
                    ret = ids[i]
        except Exception as e:
            e.printStackTrace()
        return ret

