"""
Item - Converted from Java source
Original: client/inventory/Item.java
Package: client.inventory
"""

from typing import Optional, Any
import math
import threading

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes


class Item(IItem):
    """
    Class Item
    Implements: IItem, Serializable
    """

    def __init__(self, id: int, position: int, quantity: int, flag: int, uniqueid: int):
        self.id = 0
        self.position = 0
        self.quantity = 0
        self.flag = 0
        self.expiration = 0
        self.pet = None
        self.uniqueid = 0
        self.equipOnlyId = 0
        self.owner = ""
        self.GameMaster_log = ""
        self.giftFrom = ""
        self.ring = None
        self.itemLevel = 0
        self.expiration = -1
        self.pet = None
        self.uniqueid = -1
        self.equipOnlyId = -1
        self.owner = ""
        self.GameMaster_log = None
        self.giftFrom = ""
        self.ring = None
        self.id = id
        self.position = position
        self.quantity = quantity
        self.flag = flag
        self.uniqueid = uniqueid
        self.equipOnlyId = -1


    def copy(self) -> Any:
        ret = Item(self.id, self.position, self.quantity, self.flag, self.uniqueid)
        ret.pet = self.pet
        ret.owner = self.owner
        ret.GameMaster_log = self.GameMaster_log
        ret.expiration = self.expiration
        ret.giftFrom = self.giftFrom
        ret.equipOnlyId = self.equipOnlyId
        return ret

    def setPosition(self, position: int) -> None:
        self.position = position
        if self.pet is not None:
            self.pet.setInventoryPosition(position)

    def setQuantity(self, quantity: int) -> None:
        self.quantity = quantity

    def getItemId(self) -> int:
        return self.id

    def getPosition(self) -> int:
        return self.position

    def getFlag(self) -> int:
        return self.flag

    def getLocked(self) -> bool:
        return self.flag == ItemFlag.LOCK.getValue()

    def getQuantity(self) -> int:
        return self.quantity

    def getType(self) -> int:
        return 2

    def getOwner(self) -> str:
        return self.owner

    def setOwner(self, owner: str) -> None:
        self.owner = owner

    def setFlag(self, flag: int) -> None:
        self.flag = flag

    def setLocked(self, flag: int) -> None:
        if flag == 1:
            self.setFlag(ItemFlag.LOCK.getValue())
        elif flag == 0:
            self.setFlag((byte)(self.getFlag() - ItemFlag.LOCK.getValue()))

    def getExpiration(self) -> int:
        return self.expiration

    def setExpiration(self, expire: int) -> None:
        self.expiration = expire

    def getGMLog(self) -> str:
        return self.GameMaster_log

    def setGMLog(self, GameMaster_log: str) -> None:
        self.GameMaster_log = GameMaster_log

    def getUniqueId(self) -> int:
        return self.uniqueid

    def setUniqueId(self, id: int) -> None:
        self.uniqueid = id

    def getPet(self) -> Any:
        return self.pet

    def setPet(self, pet: Any) -> None:
        self.pet = pet

    def setGiftFrom(self, gf: str) -> None:
        self.giftFrom = gf

    def getGiftFrom(self) -> str:
        return self.giftFrom

    def setEquipLevel(self, gf: int) -> None:
        self.itemLevel = gf

    def getEquipLevel(self) -> int:
        return self.itemLevel

    def compareTo(self, other: Any) -> int:
        if abs(self.position) < abs(other.getPosition()):
            return -1
        if abs(self.position) == abs(other.getPosition()):
            return 0
        return 1

    def equals(self, obj: Any) -> bool:
        if not (isinstance(obj, IItem)):
            return False
        ite = obj
        return self.uniqueid == ite.getUniqueId() and self.id == ite.getItemId() and self.quantity == ite.getQuantity() and abs(self.position) == abs(ite.getPosition())

    def toString(self) -> str:
        return "Item: " + self.id + " quantity: " + self.quantity

    def getRing(self) -> Any:
        if not GameConstants.isEffectRing(self.id) or self.getUniqueId() <= 0:
            return None
        if self.ring is None:
            self.ring = MapleRing.loadFromDb(self.getUniqueId(), self.position < 0)
        return self.ring

    def setRing(self, ring: Any) -> None:
        self.ring = ring

    def hasSetOnlyId(self) -> bool:
        ii = MapleItemInformationProvider.getInstance()
        return self.equipOnlyId <= 0

    def getEquipOnlyId(self) -> int:
        return self.equipOnlyId

    def setEquipOnlyId(self, OnlyId: int) -> None:
        self.equipOnlyId = OnlyId

