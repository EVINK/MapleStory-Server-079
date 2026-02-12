"""
MapleMount - Converted from Java source
Original: client/inventory/MapleMount.java
Package: client.inventory
"""

from pymysql import Connection
from typing import Optional, Any
from weakref import ref
import pymysql
import time
import weakref

# Internal module imports
# from database import *  # TODO: import specific classes
# from client import *  # TODO: import specific classes
# from server import *  # TODO: import specific classes
# from tools import *  # TODO: import specific classes


class MapleMount:
    """
    Class MapleMount
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, owner: Any, id: int, skillid: int, fatigue: int, level: int, exp: int):
        self.itemid = 0
        self.skillid = None
        self.exp = 0
        self.fatigue = 0
        self.level = 0
        self.changed = None
        self.lastFatigue = 0
        self.owner = None
        self.changed = False
        self.lastFatigue = 0
        self.itemid = id
        self.skillid = skillid
        self.fatigue = fatigue
        self.level = level
        self.exp = exp
        self.owner = new WeakReference<MapleCharacter>(owner)


    def saveMount(self, charid: int) -> None:
        if !self.changed:
            return
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("UPDATE mountdata set `Level` = ?, `Exp` = ?, `Fatigue` = ? WHERE characterid = ?")
        ps.setByte(1, self.level)
        ps.setInt(2, self.exp)
        ps.setByte(3, self.fatigue)
        ps.setInt(4, charid)
        ps.executeUpdate()
        ps.close()

    def getItemId(self) -> int:
        return self.itemid

    def getSkillId(self) -> int:
        return self.skillid

    def getFatigue(self) -> int:
        return self.fatigue

    def getExp(self) -> int:
        return self.exp

    def getLevel(self) -> int:
        return self.level

    def setItemId(self, c: int) -> None:
        self.changed = True
        self.itemid = c

    def setFatigue(self, amount: int) -> None:
        self.changed = True
        self.fatigue += amount
        if self.fatigue < 0:
            self.fatigue = 0

    def setExp(self, c: int) -> None:
        self.changed = True
        self.exp = c

    def setLevel(self, c: int) -> None:
        self.changed = True
        self.level = c

    def increaseFatigue(self) -> None:
        self.changed = True
        self.fatigue += 1
        self.fatigue = 0
        if self.fatigue > 100 && self.owner.get() is not None:
            self.owner.get().cancelEffectFromBuffStat(MapleBuffStat.骑兽技能)
        self.update()

    def canTire(self, now: int) -> bool:
        return self.lastFatigue > 0 && self.lastFatigue + 30000 < now

    def startSchedule(self) -> None:
        self.lastFatigue = int(time.time() * 1000)

    def cancelSchedule(self) -> None:
        self.lastFatigue = 0

    def increaseExp(self) -> None:
        e = None
        if self.level >= 1 && self.level <= 7:
            e = Randomizer.nextInt(10) + 15
        elif self.level >= 8 && self.level <= 15:
            e = Randomizer.nextInt(13) + 7
        elif self.level >= 16 && self.level <= 24:
            e = Randomizer.nextInt(23) + 9
        else:
            e = Randomizer.nextInt(28) + 12
        self.setExp(self.exp + e)

    def update(self) -> None:
        chr = self.owner.get()
        if chr is not None:
            chr.getMap().broadcastMessage(MaplePacketCreator.updateMount(chr, False))

