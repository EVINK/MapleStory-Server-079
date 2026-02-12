"""
AbstractPlayerStore - Converted from Java source
Original: server/shops/AbstractPlayerStore.java
Package: server.shops
"""

from pymysql import Connection
from pymysql.cursors import Cursor
from threading import Lock
from typing import List
from typing import Optional, Any
from weakref import ref
import pymysql
import time
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.maps.AbstractMapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class AbstractPlayerStore(AbstractMapleMapObject, IMaplePlayerShop):
    """
    Class AbstractPlayerStore
    Extends: AbstractMapleMapObject
    Implements: IMaplePlayerShop
    """

    def __init__(self, owner: Any, itemId: int, desc: str, pass: str, slots: int):
        self.open = False
        self.available = False
        self.ownerName = ""
        self.des = ""
        self.pass = ""
        self.ownerId = 0
        self.owneraccount = 0
        self.itemId = 0
        self.channel = 0
        self.map = 0
        self.meso = None
        self.visitors = []
        self.bought = []
        self.items = []
        self.id = 0
        self.quantity = 0
        self.totalPrice = 0
        self.buyer = ""
        self.open = False
        self.available = False
        self.meso = AtomicInteger(0)
        self.visitors = []
        self.bought = []
        self.items = []
        self.setPosition(owner.getPosition())
        self.ownerName = owner.getName()
        self.ownerId = owner.getId()
        self.owneraccount = owner.getAccountID()
        self.itemId = itemId
        self.des = desc
        self.pass = pass
        self.map = owner.getMapId()
        self.channel = owner.getClient().getChannel()
        self.chrs = (WeakReference<MapleCharacter>[])new WeakReference[slots]
        for i in range(self.len(chrs)):
            self.chrs[i] = new WeakReference<MapleCharacter>(None)


    def getMapId(self) -> int:
        return self.map

    def getChannel(self) -> int:
        return self.channel

    def getMaxSize(self) -> int:
        return self.len(chrs) + 1

    def getSize(self) -> int:
        return (self.getFreeSlot() == -1) ? self.getMaxSize() : self.getFreeSlot()

    def broadcastToVisitors(self, packet: Any) -> None:
        self.broadcastToVisitors(packet, True)

    def broadcastToVisitors_packet_owner(self, packet: Any, owner: bool) -> None:
        for chr in self.chrs:
            if chr is not None && chr.get() is not None:
                chr.get().getClient().getSession().write(packet)
        if self.getShopType() != 1 && owner && self.getMCOwner() is not None:
            self.getMCOwner().getClient().getSession().write(packet)

    def broadcastToVisitors_packet_exception(self, packet: Any, exception: int) -> None:
        for chr in self.chrs:
            if chr is not None && chr.get() is not None && self.getVisitorSlot(chr.get()) != exception:
                chr.get().getClient().getSession().write(packet)
        if self.getShopType() != 1 && self.getMCOwner() is not None && exception != self.ownerId:
            self.getMCOwner().getClient().getSession().write(packet)

    def getMeso(self) -> int:
        return self.meso.get()

    def setMeso(self, meso: int) -> None:
        self.meso.set(meso)

    def setOpen(self, open: bool) -> None:
        self.open = open

    def isOpen(self) -> bool:
        return self.open

    def saveItems(self) -> bool:
        if self.getShopType() != 1:
            return False
        con = DatabaseConnection.getConnection()
        try:
            ps = None
            ps2 = None
            ps = con.prepareStatement("select * from hiredmerch where accountid = ? and characterid = ?")
            ps.setInt(1, self.owneraccount)
            ps.setInt(2, self.ownerId)
            rs = ps.executeQuery()
            packageid = 0
            if rs.next():
                ps2 = con.prepareStatement("update hiredmerch set Mesos = ? where accountid = ? and characterid = ?")
                ps2.setInt(1, self.meso.get())
                ps2.setInt(2, self.owneraccount)
                ps2.setInt(3, self.ownerId)
                ps2.executeUpdate()
                ps2.close()
                packageid = rs.getInt("PackageId")
            else:
                ps2 = con.prepareStatement("INSERT INTO hiredmerch (characterid, accountid, Mesos, map, channel, time) VALUES (?, ?, ?, ?, ?, ?)", 1)
                ps2.setInt(1, self.ownerId)
                ps2.setInt(2, self.owneraccount)
                ps2.setInt(3, self.meso.get())
                ps2.setInt(4, self.map)
                ps2.setInt(5, self.channel)
                ps2.setLong(6, int(time.time() * 1000))
                ps2.executeUpdate()
                rs2 = ps2.getGeneratedKeys()
                if !rs2.next():
                    ps.close()
                    rs.close()
                    rs2.close()
                    ps2.close()
                    print("[SaveItems] 保存雇佣商店信息出错 - 1")
                    raise RuntimeError("保存雇佣商店信息出错.")
                packageid = rs2.getInt(1)
                rs2.close()
            rs.close()
            ps.close()
            if packageid == 0:
                print("[SaveItems] 保存雇佣商店信息出错 - 1")
                raise RuntimeError("保存雇佣商店信息出错.")
            iters = new ArrayList<Pair<IItem, MapleInventoryType>>()
            for pItems in self.items:
                if pItems.item is not None && pItems.bundles > 0:
                    if pItems.item.getQuantity() <= 0 && !GameConstants.isRechargable(pItems.item.getItemId()):
                        continue
                    item = pItems.item.copy()
                    item.setQuantity((short)(item.getQuantity() * pItems.bundles))
                    iters.add(new Pair<IItem, MapleInventoryType>(item, GameConstants.getInventoryType(item.getItemId())))
            ItemLoader.HIRED_MERCHANT.saveItems(iters, packageid, self.owneraccount, self.ownerId)
            return True
        except Exception as e:
            e.printStackTrace()
            print("[SaveItems] 保存雇佣商店信息出错 - 2 " + e)
            return False

    def getVisitor(self, num: int) -> Any:
        return self.chrs[num].get()

    def update(self) -> None:
        if self.isAvailable():
            if self.getShopType() == 1:
                self.getMap().broadcastMessage(PlayerShopPacket.updateHiredMerchant(this))
            elif self.getMCOwner() is not None:
                self.getMap().broadcastMessage(PlayerShopPacket.sendPlayerShopBox(self.getMCOwner()))

    def addVisitor(self, visitor: Any) -> None:
        i = self.getFreeSlot()
        if i > 0:
            if self.getShopType() >= 3:
                self.broadcastToVisitors(PlayerShopPacket.getMiniGameNewVisitor(visitor, i, this))
            else:
                self.broadcastToVisitors(PlayerShopPacket.shopVisitorAdd(visitor, i))
            self.chrs[i - 1] = new WeakReference<MapleCharacter>(visitor)
            if !self.isOwner(visitor):
                self.visitors.add(visitor.getName())
            if i == 3:
                self.update()

    def removeVisitor(self, visitor: Any) -> None:
        slot = self.getVisitorSlot(visitor)
        shouldUpdate = self.getFreeSlot() == -1
        if slot > 0:
            self.broadcastToVisitors(PlayerShopPacket.shopVisitorLeave(slot), slot)
            self.chrs[slot - 1] = new WeakReference<MapleCharacter>(None)
            if shouldUpdate:
                self.update()

    def getVisitorSlot(self, visitor: Any) -> int:
        i = 0
        while i < self.len(chrs):
            if self.chrs[i] is not None && self.chrs[i].get() is not None && self.chrs[i].get().getId() == visitor.getId():
                return (byte)(i + 1)
        if visitor.getId() == self.ownerId:
            return 0
        return -1

    def removeAllVisitors(self, error: int, type: int) -> None:
        for i in range(self.len(chrs)):
            visitor = self.getVisitor(i)
            if visitor is not None:
                if type != -1:
                    visitor.getClient().getSession().write(PlayerShopPacket.shopErrorMessage(error, type))
                self.broadcastToVisitors(PlayerShopPacket.shopVisitorLeave(self.getVisitorSlot(visitor)), self.getVisitorSlot(visitor))
                visitor.setPlayerShop(None)
                self.chrs[i] = new WeakReference<MapleCharacter>(None)
        self.update()

    def getOwnerName(self) -> str:
        return self.ownerName

    def getOwnerId(self) -> int:
        return self.ownerId

    def getOwnerAccId(self) -> int:
        return self.owneraccount

    def getDescription(self) -> str:
        if self.des is None:
            return ""
        return self.des

    def getVisitors(self) -> list:
        chrz = new LinkedList<Pair<Byte, MapleCharacter>>()
        i = 0
        while i < self.len(chrs):
            if self.chrs[i] is not None && self.chrs[i].get() is not None:
                chrz.add(new Pair<Byte, MapleCharacter>((byte)(i + 1), self.chrs[i].get()))
        return chrz

    def getItems(self) -> list:
        return self.items

    def addItem(self, item: Any) -> None:
        self.items.add(item)

    def removeItem(self, item: int) -> bool:
        return False

    def removeFromSlot(self, slot: int) -> None:
        self.items.remove(slot)

    def getFreeSlot(self) -> int:
        i = 0
        while i < self.len(chrs):
            if self.chrs[i] is None || self.chrs[i].get() is None:
                return (byte)(i + 1)
        return -1

    def getItemId(self) -> int:
        return self.itemId

    def isOwner(self, chr: Any) -> bool:
        return chr.getId() == self.ownerId && chr.getName() == (self.ownerName)

    def getPassword(self) -> str:
        if self.pass is None:
            return ""
        return self.pass

    def sendDestroyData(self, client: Any) -> None:
        pass

    def sendSpawnData(self, client: Any) -> None:
        pass

    def getType(self) -> Any:
        return MapleMapObjectType.SHOP

    def getMCOwner(self) -> Any:
        return self.getMap().getCharacterById(self.ownerId)

    def getMCOwnerWorld(self) -> Any:
        ourChannel = World.Find.findChannel(self.ownerId)
        if ourChannel <= 0:
            return None
        return ChannelServer.getInstance(ourChannel).getPlayerStorage().getCharacterById(self.ownerId)

    def getMap(self) -> Any:
        return ChannelServer.getInstance(self.channel).getMapFactory().getMap(self.map)

    def getGameType(self) -> int:
        if self.getShopType() == 1:
            return 5
        if self.getShopType() == 2:
            return 4
        if self.getShopType() == 3:
            return 1
        if self.getShopType() == 4:
            return 2
        return 0

    def isAvailable(self) -> bool:
        return self.available

    def setAvailable(self, b: bool) -> None:
        self.available = b

    def getBoughtItems(self) -> list:
        return self.bought


# Inner class from Java (originally nested)
class BoughtItem:
    """
    Class BoughtItem
    """

    def __init__(self, id: int, quantity: int, totalPrice: int, buyer: str):
        self.id = 0
        self.quantity = 0
        self.totalPrice = 0
        self.buyer = ""
        self.id = id
        self.quantity = quantity
        self.totalPrice = totalPrice
        self.buyer = buyer


