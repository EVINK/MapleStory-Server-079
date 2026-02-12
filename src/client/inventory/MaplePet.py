"""
MaplePet - Converted from Java source
Original: client/inventory/MaplePet.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Iterator
from typing import List
from typing import Optional, Any
import logging
import pymysql

# Internal module imports
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.movement.LifeMovement import *  # TODO: import specific classes
# from server.movement.LifeMovementFragment import *  # TODO: import specific classes


class MaplePet:
    """
    Class MaplePet
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, petitemid: int, uniqueid: int):
        self.name = ""
        self.Fh = 0
        self.stance = 0
        self.uniqueid = 0
        self.petitemid = 0
        self.secondsLeft = 0
        self.pos = None
        self.fullness = 100
        self.level = 1
        self.summoned = 0
        self.inventorypos = 0
        self.closeness = 0
        self.flags = 0
        self.changed = False
        self.i = None
        self.item = None
        self.remove = None
        self.petitemid = petitemid
        self.uniqueid = uniqueid


    def loadFromDb(self, itemid: int, petid: int, inventorypos: int) -> Any:
        try:
            ret = MaplePet(itemid, petid, inventorypos)
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM pets WHERE petid = ?")
            ps.setInt(1, petid)
            rs = ps.executeQuery()
            if !rs.next():
                rs.close()
                ps.close()
                return None
            ret.setName(rs.getString("name"))
            ret.setCloseness(rs.getShort("closeness"))
            ret.setLevel(rs.getByte("level"))
            ret.setFullness(rs.getByte("fullness"))
            ret.setSecondsLeft(rs.getInt("seconds"))
            ret.setFlags(rs.getShort("flags"))
            ret.changed = False
            rs.close()
            ps.close()
            return ret
        except SQLException as ex:
            Logger.getLogger(MaplePet.class.getName()).log(Level.SEVERE, None, ex)
            return None

    def createPet(self, itemid: int, uniqueid: int) -> Any:
        return createPet(itemid, MapleItemInformationProvider.getInstance().getName(itemid), 1, 0, 100, uniqueid, (itemid == 5000054) ? 18000 : 0)

    def createPet_itemid_name_level_closeness_fullness_uniqueid_secondsLeft(self, itemid: int, name: str, level: int, closeness: int, fullness: int, uniqueid: int, secondsLeft: int) -> Any:
        if uniqueid <= -1:
        uniqueid = MapleInventoryIdentifier.getInstance()
        ret1 = MapleItemInformationProvider.getInstance().getPetFlagInfo(itemid)
        try:
            pse = DatabaseConnection.getConnection().prepareStatement("INSERT INTO pets (petid, name, level, closeness, fullness, seconds, flags) VALUES (?, ?, ?, ?, ?, ?, ?)")
            pse.setInt(1, uniqueid)
            pse.setString(2, name)
            pse.setByte(3, level)
            pse.setShort(4, closeness)
            pse.setByte(5, fullness)
            pse.setInt(6, secondsLeft)
            pse.setShort(7, ret1)
            pse.executeUpdate()
            pse.close()
        except SQLException as ex:
            ex.printStackTrace()
            return None
        pet = MaplePet(itemid, uniqueid)
        pet.setName(name)
        pet.setLevel(level)
        pet.setFullness(fullness)
        pet.setCloseness(closeness)
        pet.setFlags(ret1)
        pet.setSecondsLeft(secondsLeft)
        return pet

    def saveToDb(self) -> None:
        if !self.changed:
        return
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("UPDATE pets SET name = ?, level = ?, closeness = ?, fullness = ?, seconds = ?, flags = ? WHERE petid = ?")
            ps.setString(1, self.name)
            ps.setByte(2, self.level)
            ps.setShort(3, self.closeness)
            ps.setByte(4, self.fullness)
            ps.setInt(5, self.secondsLeft)
            ps.setShort(6, self.flags)
            ps.setInt(7, self.uniqueid)
            ps.executeUpdate()
            ps.close()
            self.changed = False
        except SQLException as ex:
            ex.printStackTrace()

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name
        self.changed = True

    def getSummoned(self) -> bool:
        return (self.summoned > 0)

    def getSummonedValue(self) -> int:
        return self.summoned

    def setSummoned(self, summoned: int) -> None:
        self.summoned = summoned

    def getInventoryPosition(self) -> int:
        return self.inventorypos

    def setInventoryPosition(self, inventorypos: int) -> None:
        self.inventorypos = inventorypos

    def getUniqueId(self) -> int:
        return self.uniqueid

    def getCloseness(self) -> int:
        return self.closeness

    def setCloseness(self, closeness: int) -> None:
        if closeness >= Integer.MAX_VALUE || closeness <= 0:
        closeness = 1
        self.closeness = closeness
        self.changed = True

    def getLevel(self) -> int:
        return self.level

    def setLevel(self, level: int) -> None:
        self.level = level
        self.changed = True

    def getFullness(self) -> int:
        return self.fullness

    def setFullness(self, fullness: int) -> None:
        self.fullness = fullness
        self.changed = True

    def getFlags(self) -> int:
        return self.flags

    def setFlags(self, fffh: int) -> None:
        self.flags = fffh
        self.changed = True

    def getFh(self) -> int:
        return self.Fh

    def setFh(self, Fh: int) -> None:
        self.Fh = Fh

    def getPos(self) -> Any:
        return self.pos

    def setPos(self, pos: Any) -> None:
        self.pos = pos

    def getStance(self) -> int:
        return self.stance

    def setStance(self, stance: int) -> None:
        self.stance = stance

    def getPetItemId(self) -> int:
        return self.petitemid

    def canConsume(self, itemId: int) -> bool:
        mii = MapleItemInformationProvider.getInstance()
        Iterator<Integer> iterator = mii.petsCanConsume(itemId).iterator()
        while iterator.hasNext():
            petId = (iterator.next())
            if petId == self.petitemid:
            return True
        return False

    def updatePosition(self, movement: list) -> None:
        for move in movement:
            if isinstance(move, LifeMovement):
                if isinstance(move, server).movement.AbsoluteLifeMovement:
                setPos((move).getPosition())
                setStance((move).getNewstate())

    def getSecondsLeft(self) -> int:
        return self.secondsLeft

    def setSecondsLeft(self, sl: int) -> None:
        self.secondsLeft = sl
        self.changed = True

    def getValue(self) -> int:
        return self.i

    def check(self, flag: int) -> bool:
        return ((flag & self.i) == self.i)

    def getByAddId(self, itemId: int) -> Any:
        for flag in values():
            if flag.item == itemId:
            return flag
        return None

    def getByDelId(self, itemId: int) -> Any:
        for flag in values():
            if flag.remove == itemId:
            return flag
        return None


# Inner class from Java (originally nested)
class PetFlag(Enum):
    """Enum PetFlag"""

    ITEM_PICKUP = (1, 5190000, 5191000)
    EXPAND_PICKUP = (2, 5190002, 5191002)
    AUTO_PICKUP = (4, 5190003, 5191003)
    UNPICKABLE = (8, 5190005, -1)
    LEFTOVER_PICKUP = (16, 5190004, 5191004)
    HP_CHARGE = (32, 5190001, 5191001)
    MP_CHARGE = (64, 5190006, -1)
    PET_BUFF = (128, -1, -1)
    PET_DRAW = (256, 5190007, -1)
    PET_DIALOGUE = (512, 5190008, -1)

    def getValue(self) -> int:
        return self.i

    def check(self, flag: int) -> bool:
        return ((flag & self.i) == self.i)

    def getByAddId(self, itemId: int) -> Any:
        for flag in values():
            if flag.item == itemId:
            return flag
        return None

    def getByDelId(self, itemId: int) -> Any:
        for flag in values():
            if flag.remove == itemId:
            return flag
        return None

