"""
MTSStorage - Converted from Java source
Original: server/MTSStorage.java
Package: server
"""

from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from threading import Lock
from threading import RLock
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import pymysql
import threading
import time

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class MTSStorage:
    """
    Class MTSStorage
    """

    serialVersionUID = 231541893513228

    def __init__(self):
        self.lastUpdate = 0
        self.idToCart = None
        self.packageId = None
        self.buyNow = None
        self.end = False
        self.mutex = None
        self.cart_mutex = None
        self.price = None
        self.item = None
        self.seller = None
        self.id = None
        self.cid = None
        self.date = None
        self.lastUpdate = int(time.time() * 1000)
        self.end = False
        print("Loading MTSStorage :::")
        self.idToCart = {}
        self.buyNow = {}
        self.packageId = AtomicInteger(1)
        self.mutex = ReentrantReadWriteLock()
        self.cart_mutex = ReentrantReadWriteLock()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self) -> None:
        if MTSStorage.instance is None:
            (MTSStorage.instance = MTSStorage()).loadBuyNow()

    def check(self, packageid: int) -> bool:
        return self.getSingleItem(packageid) is not None

    def checkCart(self, packageid: int, charID: int) -> bool:
        item = self.getSingleItem(packageid)
        return item is not None and item.getCharacterId() != charID

    def getSingleItem(self, packageid: int) -> Any:
        self.mutex.readLock().lock()
        try:
            return self.buyNow.get(packageid)
        finally:
            self.mutex.readLock().unlock()

    def addToBuyNow(self, cart: Any, item: Any, price: int, cid: int, seller: str, expiration: int) -> None:
        self.mutex.writeLock().lock()
        id = None
        try:
            id = self.packageId.incrementAndGet()
            self.buyNow.put(id, MTSItemInfo(price, item, seller, id, cid, expiration))
        finally:
            self.mutex.writeLock().unlock()
        cart.addToNotYetSold(id)

    def removeFromBuyNow(self, id: int, cidBought: int, check: bool) -> bool:
        item = None
        self.mutex.writeLock().lock()
        try:
            if (id in self.buyNow):
                r = self.buyNow.get(id)
                if not check or r.getCharacterId() == cidBought:
                    item = r.getItem()
                    self.buyNow.remove(id)
        finally:
            self.mutex.writeLock().unlock()
        if item is not None:
            self.cart_mutex.readLock().lock()
            try:
                for (final Map.Entry<Integer, MTSCart> c : self.idToCart.items())
                    c.getValue().removeFromCart(id)
                    c.getValue().removeFromNotYetSold(id)
                    if c.getKey() == cidBought:
                        c.getValue().addToInventory(item)
            finally:
                self.cart_mutex.readLock().unlock()
        return item is not None

    def loadBuyNow(self) -> None:
        lastPackage = 0
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM mts_items WHERE tab = 1")
            rs = ps.executeQuery()
            while rs.next():
                lastPackage = rs.getInt("id")
                cId = rs.getInt("characterid")
                if not (cId in self.idToCart):
                    self.idToCart.put(cId, MTSCart(cId))
                items = ItemLoader.MTS.loadItems(False, lastPackage)
                if items is not None and items > 0:
                    for i in items.values():
                        self.buyNow.put(lastPackage, MTSItemInfo(rs.getInt("price"), i.getLeft(), rs.getString("seller"), lastPackage, cId, rs.getLong("expiration")))
            rs.close()
            ps.close()
        except Exception as e:
            e.printStackTrace()
        self.packageId.set(lastPackage)

    def saveBuyNow(self, isShutDown: bool) -> None:
        if self.end:
            return
        self.end = isShutDown
        if isShutDown:
            print("Saving MTS...")
        expire = new HashMap<Integer, ArrayList<IItem>>()
        toRemove = []
        now = int(time.time() * 1000)
        items = new HashMap<Integer, ArrayList<Pair<IItem, MapleInventoryType>>>()
        con = DatabaseConnection.getConnection()
        self.mutex.writeLock().lock()
        try:
            ps = con.prepareStatement("DELETE FROM mts_items WHERE tab = 1")
            ps.execute()
            ps.close()
            ps = con.prepareStatement("INSERT INTO mts_items VALUES (?, ?, ?, ?, ?, ?)")
            for m in self.buyNow.values():
                if now > m.getEndingDate():
                    if not (m.getCharacterId( in expire)):
                        expire.put(m.getCharacterId(), [])
                    expire.get(m.getCharacterId()).add(m.getItem())
                    toRemove.add(m.getId())
                    items.put(m.getId(), None)
                else:
                    ps.setInt(1, m.getId())
                    ps.setByte(2, 1)
                    ps.setInt(3, m.getPrice())
                    ps.setInt(4, m.getCharacterId())
                    ps.setString(5, m.getSeller())
                    ps.setLong(6, m.getEndingDate())
                    ps.executeUpdate()
                    if not (m.getId( in items)):
                        items.put(m.getId(), new ArrayList<Pair<IItem, MapleInventoryType>>())
                    items.get(m.getId()).add(new Pair<IItem, MapleInventoryType>(m.getItem(), GameConstants.getInventoryType(m.getItem().getItemId())))
            for i in toRemove:
                self.buyNow.remove(i)
            ps.close()
        except Exception as e:
            e.printStackTrace()
        finally:
            self.mutex.writeLock().unlock()
        if isShutDown:
            print("Saving MTS items...")
        try:
            for (final Map.Entry<Integer, ArrayList<Pair<IItem, MapleInventoryType>>> ite : items.items())
                ItemLoader.MTS.saveItems(ite.getValue(), ite.getKey())
        except Exception as e:
            e.printStackTrace()
        if isShutDown:
            print("Saving MTS carts...")
        self.cart_mutex.writeLock().lock()
        try:
            for (final Map.Entry<Integer, MTSCart> c : self.idToCart.items())
                for j in toRemove:
                    c.getValue().removeFromCart(j)
                    c.getValue().removeFromNotYetSold(j)
                if (c.getKey( in expire)):
                    for item in expire.get(c.getKey()):
                        c.getValue().addToInventory(item)
                c.getValue().save()
        except Exception as e:
            e.printStackTrace()
        finally:
            self.cart_mutex.writeLock().unlock()
        self.lastUpdate = int(time.time() * 1000)

    def checkExpirations(self) -> None:
        if int(time.time() * 1000) - self.lastUpdate > 3600000:
            self.saveBuyNow(False)

    def getCart(self, characterId: int) -> Any:
        self.cart_mutex.readLock().lock()
        ret = None
        try:
            ret = self.idToCart.get(characterId)
        finally:
            self.cart_mutex.readLock().unlock()
        if ret is None:
            self.cart_mutex.writeLock().lock()
            try:
                ret = MTSCart(characterId)
                self.idToCart.put(characterId, ret)
            except Exception as e:
                e.printStackTrace()
            finally:
                self.cart_mutex.writeLock().unlock()
        return ret

    def getCurrentMTS(self, cart: Any) -> Any:
        self.mutex.readLock().lock()
        try:
            # switch (cart.getTab()):
                # case 1:
                    return MTSCSPacket.sendMTS(self.getBuyNow(cart.getType(), cart.getPage()), cart.getTab(), cart.getType(), cart.getPage(), self.buyNow / 16 + ((self.buyNow % 16 > 0) ? 1 : 0))
                # case 4:
                    return MTSCSPacket.sendMTS(self.getCartItems(cart), cart.getTab(), cart.getType(), cart.getPage(), 0)
                # default:
                    return MTSCSPacket.sendMTS([], cart.getTab(), cart.getType(), cart.getPage(), 0)
        finally:
            self.mutex.readLock().unlock()

    def getCurrentNotYetSold(self, cart: Any) -> Any:
        self.mutex.readLock().lock()
        try:
            nys = []
            nyss = [])
            for i in nyss:
                r = self.buyNow.get(i)
                if r is None:
                    cart.removeFromNotYetSold(i)
                else:
                    nys.add(r)
            return MTSCSPacket.getNotYetSoldInv(nys)
        finally:
            self.mutex.readLock().unlock()

    def getCurrentTransfer(self, cart: Any, changed: bool) -> Any:
        return MTSCSPacket.getTransferInventory(cart.getInventory(), changed)

    def getBuyNow(self, type: int, page: int) -> list:
        size = self.buyNow / 16 + ((self.buyNow % 16 > 0) ? 1 : 0)
        ret = []
        rett = [])
        if page > size:
            page = 0
        i = page * 16
        while i < page * 16 + 16 and self.buyNow >= i + 1:
            r = rett.get(i)
            if r is not None and (type == 0 or GameConstants.getInventoryType(r.getItem().getItemId()).getType() == type):
                ret.add(r)
        return ret

    def getCartItems(self, cart: Any) -> list:
        ret = []
        cartt = [])
        for i in cartt:
            r = self.buyNow.get(i)
            if r is None:
                cart.removeFromCart(i)
            else:
                if cart.getType() != 0 and GameConstants.getInventoryType(r.getItem().getItemId()).getType() != cart.getType():
                    continue
                ret.add(r)
        return ret

    def getItem(self) -> Any:
        return self.item

    def getPrice(self) -> int:
        return self.price

    def getRealPrice(self) -> int:
        return self.price + self.getTaxes()

    def getTaxes(self) -> int:
        return ServerConstants.MTS_BASE + self.price * ServerConstants.MTS_TAX / 100

    def getId(self) -> int:
        return self.id

    def getCharacterId(self) -> int:
        return self.cid

    def getEndingDate(self) -> int:
        return self.date

    def getSeller(self) -> str:
        return self.seller


# Inner class from Java (originally nested)
class MTSItemInfo:
    """
    Class MTSItemInfo
    """

    def __init__(self, price: int, item: Any, seller: str, id: int, cid: int, date: int):
        self.price = None
        self.item = None
        self.seller = None
        self.id = None
        self.cid = None
        self.date = None
        self.item = item
        self.price = price
        self.seller = seller
        self.id = id
        self.cid = cid
        self.date = date


    def getItem(self) -> Any:
        return self.item

    def getPrice(self) -> int:
        return self.price

    def getRealPrice(self) -> int:
        return self.price + self.getTaxes()

    def getTaxes(self) -> int:
        return ServerConstants.MTS_BASE + self.price * ServerConstants.MTS_TAX / 100

    def getId(self) -> int:
        return self.id

    def getCharacterId(self) -> int:
        return self.cid

    def getEndingDate(self) -> int:
        return self.date

    def getSeller(self) -> str:
        return self.seller

