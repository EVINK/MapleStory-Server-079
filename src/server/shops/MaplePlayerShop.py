"""
MaplePlayerShop - Converted from Java source
Original: server/shops/MaplePlayerShop.java
Package: server.shops
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.maps.MapleMapObject import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class MaplePlayerShop(AbstractPlayerStore):
    """
    Class MaplePlayerShop
    Extends: AbstractPlayerStore
    """

    def __init__(self, owner: Any, itemId: int, desc: str):
        self.boughtnumber = 0
        self.bannedList = None
        super(owner, itemId, desc, "", 3)
        self.boughtnumber = 0
        self.bannedList = []


    def buy(self, c: Any, item: int, quantity: int) -> None:
        pItem = self.items.get(item)
        if pItem.bundles > 0:
            newItem = pItem.item.copy()
            newItem.setQuantity((short)(quantity * newItem.getQuantity()))
            flag = newItem.getFlag()
            if ItemFlag.KARMA_EQ.check(flag):
                newItem.setFlag((byte)(flag - ItemFlag.KARMA_EQ.getValue()))
            elif ItemFlag.KARMA_USE.check(flag):
                newItem.setFlag((byte)(flag - ItemFlag.KARMA_USE.getValue()))
            gainmeso = pItem.price * quantity
            if c.getPlayer().getMeso() >= gainmeso:
                if self.getMCOwner().getMeso() + gainmeso > 0 && MapleInventoryManipulator.checkSpace(c, newItem.getItemId(), newItem.getQuantity(), newItem.getOwner()) && MapleInventoryManipulator.addFromDrop(c, newItem, False):
                    maplePlayerShopItem = pItem
                    maplePlayerShopItem.bundles -= quantity
                    self.bought.add(BoughtItem(newItem.getItemId(), quantity, gainmeso, c.getPlayer().getName()))
                    c.getPlayer().gainMeso(-gainmeso, False)
                    self.getMCOwner().gainMeso(gainmeso, False)
                    if pItem.bundles <= 0:
                        self.boughtnumber += 1
                        if self.boughtnumber == self.items:
                            self.closeShop(True, True)
                            return
                else:
                    c.getPlayer().dropMessage(1, "你的背包已满.")
            else:
                c.getPlayer().dropMessage(1, "You do not have enough mesos.")
            self.getMCOwner().getClient().getSession().write(PlayerShopPacket.shopItemUpdate(this))

    def getShopType(self) -> int:
        return 2

    def closeShop(self, saveItems: bool, remove: bool) -> None:
        owner = self.getMCOwner()
        self.removeAllVisitors(10, 1)
        self.getMap().removeMapObject(this)
        for items in self.getItems():
            if items.bundles > 0:
                newItem = items.item.copy()
                newItem.setQuantity((short)(items.bundles * newItem.getQuantity()))
                if !MapleInventoryManipulator.addFromDrop(owner.getClient(), newItem, False):
                    self.saveItems()
                    break
                items.bundles = 0
        owner.setPlayerShop(None)
        self.update()
        self.getMCOwner().getClient().getSession().write(PlayerShopPacket.shopErrorMessage(10, 1))

    def banPlayer(self, name: str) -> None:
        if !(name in self.bannedList):
            self.bannedList.add(name)
        for i in range(3):
            chr = self.getVisitor(i)
            if chr.getName() == (name):
                chr.getClient().getSession().write(PlayerShopPacket.shopErrorMessage(5, 1))
                chr.setPlayerShop(None)
                self.removeVisitor(chr)

    def isBanned(self, name: str) -> bool:
        return (name in self.bannedList)

