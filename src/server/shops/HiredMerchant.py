"""
HiredMerchant - Converted from Java source
Original: server/shops/HiredMerchant.java
Package: server.shops
"""

from concurrent.futures import Future
from typing import List
from typing import Optional, Any
import sched
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.maps.MapleMap import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class HiredMerchant(AbstractPlayerStore):
    """
    Class HiredMerchant
    Extends: AbstractPlayerStore
    """

    def __init__(self, owner: Any, itemId: int, desc: str):
        self.blacklist = None
        self.storeid = 0
        self.start = None
        super(owner, itemId, desc, "", 3)
        self.start = int(time.time() * 1000)
        self.blacklist = []
        self.schedule = Timer.EtcTimer.getInstance().schedule(Runnable()
            public void run()
                HiredMerchant.self.closeShop(True, True)


    def run(self) -> None:
        HiredMerchant.self.closeShop(True, True)

    def getShopType(self) -> int:
        return 1

    def setStoreid(self, storeid: int) -> None:
        self.storeid = storeid

    def searchItem(self, itemSearch: int) -> list:
        itemz = []
        for item in self.items:
            if item.item.getItemId() == itemSearch && item.bundles > 0:
                itemz.add(item)
        return itemz

    def buy(self, c: Any, item: int, quantity: int) -> None:
        pItem = self.items.get(item)
        shopItem = pItem.item
        newItem = shopItem.copy()
        perbundle = newItem.getQuantity()
        theQuantity = pItem.price * quantity
        newItem.setQuantity((short)(quantity * perbundle))
        flag = newItem.getFlag()
        if ItemFlag.KARMA_EQ.check(flag):
            newItem.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
        elif ItemFlag.KARMA_USE.check(flag):
            newItem.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
        if !c.getPlayer().canHold(newItem.getItemId()):
            c.getPlayer().dropMessage(1, "背包已满")
            c.sendPacket(MaplePacketCreator.enableActions())
            return
        if MapleInventoryManipulator.checkSpace(c, newItem.getItemId(), newItem.getQuantity(), newItem.getOwner()):
            gainmeso = self.getMeso() + theQuantity - GameConstants.EntrustedStoreTax(theQuantity)
            if gainmeso > 0:
                self.setMeso(gainmeso)
                tmp167_165 = pItem
                tmp167_165.bundles -= quantity
                MapleInventoryManipulator.addFromDrop(c, newItem, False)
                self.bought.add(BoughtItem(newItem.getItemId(), quantity, theQuantity, c.getPlayer().getName()))
                c.getPlayer().gainMeso(-theQuantity, False)
                self.saveItems()
                chr = self.getMCOwnerWorld()
                itemText = MapleItemInformationProvider.getInstance().getName(newItem.getItemId()) + " (" + perbundle + ") x " + quantity + " 已经被卖出。 剩余数量: " + pItem.bundles + " 购买者: " + c.getPlayer().getName()
                if chr is not None:
                    chr.dropMessage(-5, "您雇佣商店里面的道具: " + itemText)
                print("[雇佣] " + ((chr is not None) ? chr.getName() : self.getOwnerName()) + " 雇佣商店卖出: " + newItem.getItemId() + " - " + itemText + " 价格: " + theQuantity)
            else:
                c.getPlayer().dropMessage(1, "金币不足.")
                c.getSession().write(MaplePacketCreator.enableActions())
        else:
            c.getPlayer().dropMessage(1, "背包已满\r\n请留1格以上位置\r\n在进行购买物品\r\n防止非法复制")
            c.getSession().write(MaplePacketCreator.enableActions())

    def closeShop(self, saveItems: bool, remove: bool) -> None:
        if self.schedule is not None:
            self.schedule.cancel(False)
        if saveItems:
            self.saveItems()
            self.items.clear()
        if remove:
            ChannelServer.getInstance(self.channel).removeMerchant(this)
            self.getMap().broadcastMessage(PlayerShopPacket.destroyHiredMerchant(self.getOwnerId()))
        self.getMap().removeMapObject(this)
        try:
            for ch in ChannelServer.getAllInstances():
                map = None
                for i in range(910000001, = 910000022):
                    map = ch.getMapFactory().getMap(i)
                    if map is not None:
                        HMS = map.getMapObjectsInRange(Point(0, 0), Double.POSITIVE_INFINITY, Arrays.asList(MapleMapObjectType.HIRED_MERCHANT))
                        for HM in HMS:
                            HMM = HM
                            if HMM.getOwnerId() == self.getOwnerId():
                                map.removeMapObject(this)
        catch (Exception ex) {}
        self.schedule = None

    def getTimeLeft(self) -> int:
        return (int)((int(time.time() * 1000) - self.start) / 1000)

    def getStoreId(self) -> int:
        return self.storeid

    def getType(self) -> Any:
        return MapleMapObjectType.HIRED_MERCHANT

    def sendDestroyData(self, client: Any) -> None:
        if self.isAvailable():
            client.getSession().write(PlayerShopPacket.destroyHiredMerchant(self.getOwnerId()))

    def sendSpawnData(self, client: Any) -> None:
        if self.isAvailable():
            client.getSession().write(PlayerShopPacket.spawnHiredMerchant(this))

    def isInBlackList(self, bl: str) -> bool:
        return (bl in self.blacklist)

    def addBlackList(self, bl: str) -> None:
        self.blacklist.add(bl)

    def removeBlackList(self, bl: str) -> None:
        self.blacklist.remove(bl)

    def sendBlackList(self, c: Any) -> None:
        c.getSession().write(PlayerShopPacket.MerchantBlackListView(self.blacklist))

    def sendVisitor(self, c: Any) -> None:
        c.getSession().write(PlayerShopPacket.MerchantVisitorView(self.visitors))

    def getMapId(self) -> int:
        return self.map

