"""
CashShop - Converted from Java source
Original: server/CashShop.java
Package: server
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import pymysql
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class CashShop:
    """
    Class CashShop
    Implements: Serializable
    """

    serialVersionUID = 231541893513373579

    def __init__(self, accountId: int, characterId: int, jobType: int):
        self.accountId = None
        self.characterId = None
        self.factory = None
        self.inventory = None
        self.uniqueids = None
        self.inventory = []
        self.uniqueids = []
        self.accountId = accountId
        self.characterId = characterId
        self.factory = ItemLoader.CASHSHOP_EXPLORER
        for item in self.factory.loadItems(False, accountId).values():
            self.inventory.add(item.getLeft())


    def getItemsSize(self) -> int:
        return self.inventory

    def getInventory(self) -> list:
        return self.inventory

    def findByCashId(self, cashId: int) -> Any:
        for item in self.inventory:
            if item.getUniqueId() == cashId:
                return item
        return None

    def checkExpire(self, c: Any) -> None:
        toberemove = []
        for item in self.inventory:
            if item is not None && !GameConstants.isPet(item.getItemId()) && item.getExpiration() > 0 && item.getExpiration() < int(time.time() * 1000):
                toberemove.add(item)
        if toberemove > 0:
            for item in toberemove:
                self.removeFromInventory(item)
                c.getSession().write(MTSCSPacket.cashItemExpired(item.getUniqueId()))
            toberemove.clear()

    def toItemA(self, cItem: Any) -> Any:
        return self.toItemA(cItem, MapleInventoryManipulator.getUniqueId(cItem.getId(), None), "")

    def toItemA_cItem_gift(self, cItem: Any, gift: str) -> Any:
        return self.toItemA(cItem, MapleInventoryManipulator.getUniqueId(cItem.getId(), None), gift)

    def toItemA_cItem_uniqueid(self, cItem: Any, uniqueid: int) -> Any:
        return self.toItemA(cItem, uniqueid, "")

    def toItemA_cItem_uniqueid_gift(self, cItem: Any, uniqueid: int, gift: str) -> Any:
        if uniqueid <= 0:
            uniqueid = MapleInventoryIdentifier.getInstance()
        period = cItem.getPeriod()
        if period <= 0 || GameConstants.isPet(cItem.getId()):
            period = 45
        ret = None
        if GameConstants.getInventoryType(cItem.getId()) == MapleInventoryType.EQUIP:
            eq = MapleItemInformationProvider.getInstance().getEquipById(cItem.getId())
            eq.setUniqueId(uniqueid)
            eq.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
            eq.setGiftFrom(gift)
            if GameConstants.isEffectRing(cItem.getId()) && uniqueid > 0:
                ring = MapleRing.loadFromDb(uniqueid)
                if ring is not None:
                    eq.setRing(ring)
            ret = eq.copy()
        else:
            item = Item(cItem.getId(), 0, cItem.getCount(), 0, uniqueid)
            item.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
            item.setGiftFrom(gift)
            if GameConstants.isPet(cItem.getId()):
                pet = MaplePet.createPet(cItem.getId(), uniqueid)
                if pet is not None:
                    item.setPet(pet)
            ret = item.copy()
        return ret

    def toItem(self, cItem: Any) -> Any:
        return self.toItem(cItem, MapleInventoryManipulator.getUniqueId(cItem.getId(), None), "")

    def toItem_cItem_gift(self, cItem: Any, gift: str) -> Any:
        return self.toItem(cItem, MapleInventoryManipulator.getUniqueId(cItem.getId(), None), gift)

    def toItem_cItem_uniqueid(self, cItem: Any, uniqueid: int) -> Any:
        return self.toItem(cItem, uniqueid, "")

    def toItem_cItem_uniqueid_gift(self, cItem: Any, uniqueid: int, gift: str) -> Any:
        if uniqueid <= 0:
            uniqueid = MapleInventoryIdentifier.getInstance()
        period = cItem.getPeriod()
        if GameConstants.isPet(cItem.getId()):
            period = 90
        elif cItem.getId() < 5210000 || cItem.getId() > 5360099 || cItem.getId() == 5220007 || cItem.getId() == 5220008:
            period = 0
        ret = None
        if GameConstants.getInventoryType(cItem.getId()) == MapleInventoryType.EQUIP:
            eq = MapleItemInformationProvider.getInstance().getEquipById(cItem.getId())
            eq.setUniqueId(uniqueid)
            if GameConstants.isPet(cItem.getId()) || period > 0:
                eq.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
            eq.setGiftFrom(gift)
            if GameConstants.isEffectRing(cItem.getId()) && uniqueid > 0:
                ring = MapleRing.loadFromDb(uniqueid)
                if ring is not None:
                    eq.setRing(ring)
            ret = eq.copy()
        else:
            item = Item(cItem.getId(), 0, cItem.getCount(), 0, uniqueid)
            if period > 0:
                item.setExpiration(int(time.time() * 1000) + period * 24 * 60 * 60 * 1000)
            if cItem.getId() == 5211047 || cItem.getId() == 5360014:
                item.setExpiration(int(time.time() * 1000) + 10800000)
            item.setGiftFrom(gift)
            if GameConstants.isPet(cItem.getId()):
                pet = MaplePet.createPet(cItem.getId(), uniqueid)
                if pet is not None:
                    item.setPet(pet)
            ret = item.copy()
        return ret

    def addToInventory(self, item: Any) -> None:
        self.inventory.add(item)

    def removeFromInventory(self, item: Any) -> None:
        self.inventory.remove(item)

    def gift(self, recipient: int, from: str, message: str, sn: int) -> None:
        self.gift(recipient, from, message, sn, 0)

    def gift_recipient_from_message_sn_uniqueid(self, recipient: int, from: str, message: str, sn: int, uniqueid: int) -> None:
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `gifts` VALUES (DEFAULT, ?, ?, ?, ?, ?)")
            ps.setInt(1, recipient)
            ps.setString(2, from)
            ps.setString(3, message)
            ps.setInt(4, sn)
            ps.setInt(5, uniqueid)
            ps.executeUpdate()
            ps.close()
        except Exception as sqle:
            sqle.printStackTrace()

    def loadGifts(self) -> list:
        gifts = new ArrayList<Pair<IItem, String>>()
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM `gifts` WHERE `recipient` = ?")
            ps.setInt(1, self.characterId)
            rs = ps.executeQuery()
            while rs.next():
                cItem = CashItemFactory.getInstance().getItem(rs.getInt("sn"))
                item = self.toItem(cItem, rs.getInt("uniqueid"), rs.getString("from"))
                gifts.add(new Pair<IItem, String>(item, rs.getString("message")))
                self.uniqueids.add(item.getUniqueId())
                packages = CashItemFactory.getInstance().getPackageItems(cItem.getId())
                if packages is not None && packages > 0:
                    for packageItem in packages:
                        self.addToInventory(self.toItem(packageItem, rs.getString("from")))
                else:
                    self.addToInventory(item)
            rs.close()
            ps.close()
            ps = con.prepareStatement("DELETE FROM `gifts` WHERE `recipient` = ?")
            ps.setInt(1, self.characterId)
            ps.executeUpdate()
            ps.close()
            self.save()
        except Exception as sqle:
            sqle.printStackTrace()
        return gifts

    def canSendNote(self, uniqueid: int) -> bool:
        return (uniqueid in self.uniqueids)

    def sendedNote(self, uniqueid: int) -> None:
        for i in range(self.uniqueids):
            if self.uniqueids.get(i) == uniqueid:
                self.uniqueids.remove(i)

    def save(self) -> None:
        itemsWithType = new ArrayList<Pair<IItem, MapleInventoryType>>()
        for item in self.inventory:
            itemsWithType.add(new Pair<IItem, MapleInventoryType>(item, GameConstants.getInventoryType(item.getItemId())))
        self.factory.saveItems(itemsWithType, self.accountId)

    def toItem_cItem_chr_uniqueid_gift(self, cItem: Any, chr: Any, uniqueid: int, gift: str) -> Any:
        if uniqueid <= 0:
            uniqueid = MapleInventoryIdentifier.getInstance()
        ret = None
        if GameConstants.getInventoryType(cItem.getId()) == MapleInventoryType.EQUIP:
            eq = MapleItemInformationProvider.getInstance().getEquipById(cItem.getId())
            eq.setUniqueId(uniqueid)
            eq.setGiftFrom(gift)
            if GameConstants.isEffectRing(cItem.getId()) && uniqueid > 0:
                ring = MapleRing.loadFromDb(uniqueid)
                if ring is not None:
                    eq.setRing(ring)
            ret = eq.copy()
        else:
            item = Item(cItem.getId(), 0, cItem.getCount(), 0, uniqueid)
            item.setGiftFrom(gift)
            if GameConstants.isPet(cItem.getId()):
                pet = MaplePet.createPet(cItem.getId(), uniqueid)
                if pet is not None:
                    item.setPet(pet)
            ret = item.copy()
        return ret

