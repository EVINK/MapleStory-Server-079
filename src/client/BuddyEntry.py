"""
BuddyEntry - Converted from Java source
Original: client/BuddyEntry.java
Package: client
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Optional, Any
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes


class BuddyEntry:
    """
    Class BuddyEntry
    """

    def __init__(self, name: str, characterId: int, group: str, channel: int, visible: bool, level: int, job: int):
        self.name = None
        self.group = ""
        self.characterId = None
        self.level = None
        self.job = None
        self.visible = False
        self.channel = 0
        self.name = name
        self.characterId = characterId
        self.group = group
        self.channel = channel
        self.visible = visible
        self.level = level
        self.job = job


    def getByNameFromDB(self, buddyName: str) -> Any:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT id, name, level, job FROM characters WHERE name = ?")
            ps.setString(1, buddyName)
            rs = ps.executeQuery()
            if rs.next():
                return BuddyEntry(rs.getString("name"), rs.getInt("id"), BuddyList.DEFAULT_GROUP, -1, False, rs.getInt("level"), rs.getInt("job"))
            return None
        except Exception as ex:
            ex.printStackTrace()
            return None

    def getByIdfFromDB(self, buddyCharId: int) -> Any:
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT id, name, level, job FROM characters WHERE id = ?")
            ps.setInt(1, buddyCharId)
            rs = ps.executeQuery()
            if rs.next():
                return BuddyEntry(rs.getString("name"), rs.getInt("id"), BuddyList.DEFAULT_GROUP, -1, True, rs.getInt("level"), rs.getInt("job"))
            return None
        except Exception as ex:
            ex.printStackTrace()
            return None

    def getChannel(self) -> int:
        return self.channel

    def setChannel(self, channel: int) -> None:
        self.channel = channel

    def isOnline(self) -> bool:
        return self.channel >= 0

    def setOffline(self) -> None:
        self.channel = -1

    def getName(self) -> str:
        return self.name

    def getCharacterId(self) -> int:
        return self.characterId

    def getLevel(self) -> int:
        return self.level

    def getJob(self) -> int:
        return self.job

    def setVisible(self, visible: bool) -> None:
        self.visible = visible

    def isVisible(self) -> bool:
        return self.visible

    def getGroup(self) -> str:
        return self.group

    def setGroup(self, newGroup: str) -> None:
        self.group = newGroup

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + self.characterId
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        other = obj
        return self.characterId == other.characterId

