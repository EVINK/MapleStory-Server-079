"""
MapleShop - Converted from Java source
Original: server/MapleShop.java
Package: server
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
from typing import Set
import math
import os
import pymysql
import sys

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.life.MapleLifeFactory import *  # TODO: import specific classes
# from server.life.MapleNPC import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleShop:
    """
    Class MapleShop
    """

    def __init__(self, id: int, npcId: int):
        self.id = None
        self.npcId = None
        self.items = None
        self.id = id
        self.npcId = npcId
        self.items = []

    # Static initializer
    # (rechargeableItems = new LinkedHashSet<Integer>()).add(2070000)
    # MapleShop.rechargeableItems.add(2070001)
    # MapleShop.rechargeableItems.add(2070002)
    # MapleShop.rechargeableItems.add(2070003)
    # MapleShop.rechargeableItems.add(2070004)
    # MapleShop.rechargeableItems.add(2070005)
    # MapleShop.rechargeableItems.add(2070006)
    # MapleShop.rechargeableItems.add(2070007)
    # MapleShop.rechargeableItems.add(2070008)
    # MapleShop.rechargeableItems.add(2070009)
    # MapleShop.rechargeableItems.add(2070010)
    # MapleShop.rechargeableItems.add(2070011)
    # MapleShop.rechargeableItems.add(2070012)
    # MapleShop.rechargeableItems.add(2070013)
    # MapleShop.rechargeableItems.add(2070015)
    # MapleShop.rechargeableItems.add(2070016)
    # MapleShop.rechargeableItems.add(2070019)
    # MapleShop.rechargeableItems.add(2070020)
    # MapleShop.rechargeableItems.add(2070021)
    # MapleShop.rechargeableItems.add(2070023)
    # MapleShop.rechargeableItems.add(2070024)
    # MapleShop.rechargeableItems.add(2070025)
    # MapleShop.rechargeableItems.add(2070026)
    # MapleShop.rechargeableItems.add(2330000)
    # MapleShop.rechargeableItems.add(2330001)
    # MapleShop.rechargeableItems.add(2330002)
    # MapleShop.rechargeableItems.add(2330003)
    # MapleShop.rechargeableItems.add(2330004)
    # MapleShop.rechargeableItems.add(2330005)
    # MapleShop.rechargeableItems.add(2330006)
    # MapleShop.rechargeableItems.add(2331000)
    # MapleShop.rechargeableItems.add(2332000)


    def createFromDB(self, id: int, isShopId: bool) -> Any:
        ret = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement(isShopId ? "SELECT * FROM shops WHERE shopid = ?" : "SELECT * FROM shops WHERE npcid = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if !rs.next():
                rs.close()
                ps.close()
                return None
            shopId = rs.getInt("shopid")
            ret = MapleShop(shopId, rs.getInt("npcid"))
            rs.close()
            ps.close()
            ps = con.prepareStatement("SELECT * FROM shopitems WHERE shopid = ? ORDER BY position ASC")
            ps.setInt(1, shopId)
            rs = ps.executeQuery()
            recharges = []
            while rs.next():
                if GameConstants.is飞镖道具(rs.getInt("itemid")) || GameConstants.is子弹道具(rs.getInt("itemid")):
                    starItem = MapleShopItem(1, rs.getInt("itemid"), rs.getInt("price"))
                    ret.addItem(starItem)
                    if !(starItem.getItemId( in MapleShop.rechargeableItems)):
                        # continue;
                        recharges.remove(starItem.getItemId())
                else:
                    ret.addItem(MapleShopItem(1000, rs.getInt("itemid"), rs.getInt("price")))
            for recharge in recharges:
                ret.addItem(MapleShopItem(1000, recharge, 0))
            rs.close()
            ps.close()
        except Exception as e:
            print("Could not load shop" + e)
        return ret

    def addItem(self, item: Any) -> None:
        self.items.add(item)

    def sendShop(self, c: Any) -> None:
        npc = MapleLifeFactory.getNPC(self.getNpcId())
        if npc is None || npc.getName() == ("MISSINGNO"):
            c.getPlayer().dropMessage(1, "商店" + self.id + "找不到此代码为" + self.getNpcId() + "的Npc")
            return
        if c.getPlayer().isAdmin():
            c.getPlayer().dropMessage("您已建立与商店" + self.id + "的连接")
        c.getPlayer().setShop(this)
        c.getSession().write(MaplePacketCreator.getNPCShop(c, self.getNpcId(), self.items))

    def buy(self, c: Any, itemId: int, quantity: int) -> None:
        if quantity <= 0:
            AutobanManager.getInstance().addPoints(c, 1000, 0, "购买道具数量 " + quantity + " 道具: " + itemId)
            return
        if c.getPlayer().getMapId() != 809030000 && self.getId() == 9100109:
            c.getPlayer().dropMessage(5, "无法正常操作A！" + c.getPlayer().getMapId() + "/" + self.getId())
        elif c.getPlayer().getMapId() == 809030000 && self.getId() == 9100109:
            item = self.findById(itemId)
            if item is not None && item.getPrice() > 0:
                price = GameConstants.isRechargable(itemId) ? item.getPrice() : (item.getPrice() * quantity)
                if price >= 0 && c.getPlayer().getddj() >= price:
                    if MapleInventoryManipulator.checkSpace(c, itemId, quantity, ""):
                        c.getPlayer().gainddj(-price)
                        if GameConstants.isPet(itemId):
                            MapleInventoryManipulator.addById(c, itemId, quantity, "", MaplePet.createPet(itemId, MapleInventoryIdentifier.getInstance()), -1, 0)
                        else:
                            ii = MapleItemInformationProvider.getInstance()
                            if GameConstants.isRechargable(itemId):
                                quantity = ii.getSlotMax(c, item.getItemId())
                            MapleInventoryManipulator.addById(c, itemId, quantity, 0)
                        c.getPlayer().dropMessage(1, "购买成功.\r\n消费：" + price + os.environ.get("server_name")+"中奖次数！\r\n剩余：" + c.getPlayer().getddj() + "豆豆中奖次数！")
                    else:
                        c.getPlayer().dropMessage(1, "请留出足够的背包空间！")
                    c.getSession().write(MaplePacketCreator.confirmShopTransaction(0))
                else:
                    c.getPlayer().dropMessage(1, "你的豆豆机中奖次数不足!\r\n请继续打豆豆中奖!\r\n中奖次数够了以后才能\r\n当前豆豆中奖次数：" + c.getPlayer().getddj())
        elif c.getPlayer().getMapId() != 809030000 && self.getId() == 9120104:
            c.getPlayer().dropMessage(5, "无法正常操作A！" + c.getPlayer().getMapId() + "/" + self.getId())
        elif c.getPlayer().getMapId() == 809030000 && self.getId() == 9120104:
            item = self.findById(itemId)
            if item is not None && item.getPrice() > 0:
                price = GameConstants.isRechargable(itemId) ? item.getPrice() : (item.getPrice() * quantity)
                if price >= 0 && c.getPlayer().getBeans() >= price:
                    if MapleInventoryManipulator.checkSpace(c, itemId, quantity, ""):
                        c.getPlayer().gainBeans(-price)
                        if GameConstants.isPet(itemId):
                            MapleInventoryManipulator.addById(c, itemId, quantity, "", MaplePet.createPet(itemId, MapleInventoryIdentifier.getInstance()), -1, 0)
                        else:
                            ii = MapleItemInformationProvider.getInstance()
                            if GameConstants.isRechargable(itemId):
                                quantity = ii.getSlotMax(c, item.getItemId())
                            MapleInventoryManipulator.addById(c, itemId, quantity, 0)
                        c.getPlayer().dropMessage(1, "购买成功.\r\n消费：" + price + "豆豆！\r\n剩余：" + c.getPlayer().getBeans() + "豆豆！")
                    else:
                        c.getPlayer().dropMessage(1, "请留出足够的背包空间！")
                    c.getSession().write(MaplePacketCreator.confirmShopTransaction(0))
                else:
                    c.getPlayer().dropMessage(1, "你的豆豆数量不足!\r\n请去商城购买!")
        else:
            item = self.findById(itemId)
            if item is not None && item.getPrice() > 0:
                price = GameConstants.isRechargable(itemId) ? item.getPrice() : (item.getPrice() * quantity)
                if price >= 0 && c.getPlayer().getMeso() >= price:
                    if MapleInventoryManipulator.checkSpace(c, itemId, quantity, ""):
                        c.getPlayer().gainMeso(-price, False)
                        if GameConstants.isPet(itemId):
                            MapleInventoryManipulator.addById(c, itemId, quantity, "", MaplePet.createPet(itemId, MapleInventoryIdentifier.getInstance()), -1, 0)
                        else:
                            ii = MapleItemInformationProvider.getInstance()
                            if GameConstants.isRechargable(itemId):
                                quantity = ii.getSlotMax(c, item.getItemId())
                            MapleInventoryManipulator.addById(c, itemId, quantity, 0)
                    else:
                        c.getPlayer().dropMessage(1, "你的背包已满")
                    c.getSession().write(MaplePacketCreator.confirmShopTransaction(0))

    def sell(self, c: Any, type: Any, slot: int, quantity: int) -> None:
        if quantity == 65535 || quantity == 0:
            quantity = 1
        item = c.getPlayer().getInventory(type).getItem(slot)
        if item is None:
            return
        if GameConstants.is飞镖道具(item.getItemId()) || GameConstants.is子弹道具(item.getItemId()):
            quantity = item.getQuantity()
        if quantity < 0:
            AutobanManager.getInstance().addPoints(c, 1000, 0, "Selling " + quantity + " " + item.getItemId() + " (" + type.name() + "/" + slot + ")")
            return
        iQuant = item.getQuantity()
        if iQuant == 65535:
            iQuant = 1
        ii = MapleItemInformationProvider.getInstance()
        if ii.cantSell(item.getItemId()):
            return
        if quantity <= iQuant && iQuant > 0:
            MapleInventoryManipulator.removeFromSlot(c, type, slot, quantity, False)
            price = None
            if GameConstants.is飞镖道具(item.getItemId()) || GameConstants.is子弹道具(item.getItemId()):
                price = ii.getWholePrice(item.getItemId()) / ii.getSlotMax(c, item.getItemId())
            else:
                price = ii.getPrice(item.getItemId())
            recvMesos = max(math.ceil(price * quantity), 0.0)
            if price != -1.0 && recvMesos > 0:
                c.getPlayer().gainMeso(recvMesos, False)
            c.getSession().write(MaplePacketCreator.confirmShopTransaction(8))

    def recharge(self, c: Any, slot: int) -> None:
        item = c.getPlayer().getInventory(MapleInventoryType.USE).getItem(slot)
        if item is None || (!GameConstants.is飞镖道具(item.getItemId()) && !GameConstants.is子弹道具(item.getItemId())):
            return
        ii = MapleItemInformationProvider.getInstance()
        slotMax = ii.getSlotMax(c, item.getItemId())
        skill = GameConstants.getMasterySkill(c.getPlayer().getJob())
        if skill != 0:
            slotMax += (short)(c.getPlayer().getSkillLevel(SkillFactory.getSkill(skill)) * 10)
        if item.getQuantity() < slotMax:
            price = Math.round(ii.getPrice(item.getItemId()) * (slotMax - item.getQuantity()))
            if c.getPlayer().getMeso() >= price:
                item.setQuantity(slotMax)
                c.getSession().write(MaplePacketCreator.updateInventorySlot(MapleInventoryType.USE, item, False))
                c.getPlayer().gainMeso(-price, False, True, False)
                c.getSession().write(MaplePacketCreator.confirmShopTransaction(8))
            else:
                c.getSession().write(MaplePacketCreator.confirmShopTransaction(2))

    def findById(self, itemId: int) -> Any:
        for item in self.items:
            if item.getItemId() == itemId:
                return item
        return None

    def getNpcId(self) -> int:
        return self.npcId

    def getId(self) -> int:
        return self.id

