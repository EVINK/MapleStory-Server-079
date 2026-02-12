"""
MapleEquipOnlyId - Converted from Java source
Original: client/inventory/MapleEquipOnlyId.java
Package: client.inventory
"""

from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class MapleEquipOnlyId:
    """
    Class MapleEquipOnlyId
    """

    instance = MapleEquipOnlyId()

    def __init__(self):
        self.runningId = None
        self.runningId = AtomicInteger(0)


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getNextEquipOnlyId(self) -> int:
        if self.runningId.get() <= 0:
            self.runningId.set(initOnlyId())
        else:
            self.runningId.set(self.runningId.get() + 1)
        return self.runningId.get()

    def initOnlyId(self) -> int:
        ret = 0
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("SELECT MAXFROM inventoryitems WHERE equipOnlyId > 0")
            rs = ps.executeQuery()
            if rs.next():
            ret = rs.getInt(1) + 1
            rs.close()
            ps.close()
        except SQLException as e:
            e.printStackTrace()
        return ret


# Inner class from Java (originally nested)
class SingletonHolder:
    """
    Class SingletonHolder
    """

    instance = MapleEquipOnlyId()


