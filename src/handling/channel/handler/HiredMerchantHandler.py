"""
HiredMerchantHandler - Converted from Java source
Original: handling/channel/handler/HiredMerchantHandler.java
Package: handling.channel.handler
"""

from datetime import datetime, timezone, timedelta
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MerchItemPackage import *  # TODO: import specific classes
# from tools.FileoutputUtil import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes
# from tools.packet.PlayerShopPacket import *  # TODO: import specific classes


class HiredMerchantHandler:
    """
    Class HiredMerchantHandler
    """


    def UseHiredMerchant(self, slea: Any, c: Any) -> None:
        if c.getPlayer().getMap().allowPersonalShop():
            state = checkExistance(c.getPlayer().getAccountID(), c.getPlayer().getId())
            # switch (state):
                # case 1:
                    c.getPlayer().dropMessage(1, "请先去领取你之前摆摊的东西")
                    break
                # case 0:
                    merch = World.hasMerchant(c.getPlayer().getAccountID())
                    if not merch:
                        c.getSession().write(PlayerShopPacket.sendTitleBox())
                        break
                    c.getPlayer().dropMessage(1, "请换个地方开或者是你已经有开店了")
                    break
                # default:
                    c.getPlayer().dropMessage(1, "发生未知错误.")
                    break
        else:
            c.getSession().close()

    def checkExistance(self, accid: int, charid: int) -> int:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * from hiredmerch where accountid = ? OR characterid = ?")
            ps.setInt(1, accid)
            ps.setInt(2, charid)
            rs = ps.executeQuery()
            if rs.next():
                ps.close()
                rs.close()
                return 1
            rs.close()
            ps.close()
            return 0
        except Exception as se:
            return -1

    def MerchantItemStore(self, slea: Any, c: Any) -> None:
        chr = c.getPlayer()
        if chr is None:
            return
        operation = slea.readByte()
        # switch (operation):
            # case 20:
                slea.readMapleAsciiString()
                conv = c.getPlayer().getConversation()
                merch = World.hasMerchant(c.getPlayer().getAccountID())
                if merch:
                    c.getPlayer().dropMessage(1, "请关闭商店后再试一次.")
                    c.getPlayer().setConversation(0)
                    break
                if conv == 3:
                    pack = loadItemFrom_Database(c.getPlayer().getId(), c.getPlayer().getAccountID(), chr)
                    if pack is None:
                        c.getPlayer().dropMessage(1, "你没有物品可以领取!")
                        deletePackage(c.getPlayer().getId(), c.getPlayer().getAccountID())
                        c.getPlayer().setConversation(0)
                    elif pack.getItems() <= 0:
                        if not check(c.getPlayer(), pack):
                            c.getSession().write(PlayerShopPacket.merchItem_Message(33))
                            return
                        if deletePackage(c.getPlayer().getId(), c.getPlayer().getAccountID(), pack.getPackageid()):
                            FileoutputUtil.logToFile_chr(c.getPlayer(), "logs/Log_雇佣金币领取记录.txt", " 领回金币 " + pack.getMesos())
                            c.getPlayer().gainMeso(pack.getMesos(), False)
                            c.getPlayer().setConversation(0)
                            c.getPlayer().dropMessage("领取金币" + pack.getMesos())
                        else:
                            c.getPlayer().dropMessage(1, "发生未知错误。")
                        c.getPlayer().setConversation(0)
                        c.getSession().write(MaplePacketCreator.enableActions())
                    else:
                        c.getSession().write(PlayerShopPacket.merchItemStore_ItemData(pack))
                    break
                break
            # case 25:
                if c.getPlayer().getConversation() != 3:
                    return
                c.getSession().write(PlayerShopPacket.merchItemStore(36))
                break
            # case 26:
                if c.getPlayer().getConversation() != 3:
                    c.getPlayer().dropMessage(1, "发生未知错误1.")
                    c.getSession().write(MaplePacketCreator.enableActions())
                    return
                pack2 = loadItemFrom_Database(c.getPlayer().getId(), c.getPlayer().getAccountID(), chr)
                if pack2 is None:
                    c.getPlayer().dropMessage(1, "发生未知错误。\r\n你没有物品可以领取！")
                    return
                if not check(c.getPlayer(), pack2):
                    c.getPlayer().dropMessage(1, "因为背包空间不足，无法领取道具.")
                    c.getSession().write(PlayerShopPacket.merchItem_Message(33))
                    return
                if deletePackage(c.getPlayer().getId(), c.getPlayer().getAccountID(), pack2.getPackageid()):
                    if pack2.getMesos() > 0:
                        c.getPlayer().gainMeso(pack2.getMesos(), False)
                        if chr.isGM():
                            chr.dropMessage(6, "[雇佣] " + chr.getName() + " 雇佣取回获得金币: " + pack2.getMesos() + " 时间: " + FileoutputUtil.CurrentReadable_Date())
                        print("[雇佣] " + chr.getName() + " 雇佣取回获得金币: " + pack2.getMesos() + " 时间: " + FileoutputUtil.CurrentReadable_Date())
                        FileoutputUtil.hiredMerchLog(chr.getName(), "雇佣取回获得金币: " + pack2.getMesos())
                    for item in pack2.getItems():
                        MapleInventoryManipulator.addFromDrop(c, item, False)
                        if chr.isGM():
                            chr.dropMessage(6, "名称：" + chr.getName() + "雇佣取回 获得道具：" + item.getItemId() + " - " + MapleItemInformationProvider.getInstance().getName(item.getItemId()) + " 数量：" + item.getQuantity())
                        FileoutputUtil.hiredMerchLog(chr.getName(), "雇佣取回获得道具: " + item.getItemId() + " - " + MapleItemInformationProvider.getInstance().getName(item.getItemId()) + " 数量: " + item.getQuantity())
                    c.getSession().write(PlayerShopPacket.merchItem_Message(29))
                    break
                c.getPlayer().dropMessage(1, "发生未知错误.")
                break
            # case 27:
                c.getPlayer().setConversation(0)
                break
            # default:
                print("弗兰德里：雇佣商店未知的操作类型 " + operation)
                break

    def getShopItem(self, c: Any) -> None:
        if c.getPlayer().getConversation() != 3:
            return
        pack = loadItemFrom_Database(c.getPlayer().getId(), c.getPlayer().getAccountID(), c.getPlayer())
        if pack is None:
            c.getPlayer().dropMessage(1, "发生未知错误。")
            return
        if not check(c.getPlayer(), pack):
            c.getPlayer().dropMessage(1, "你背包格子不够。")
            return
        if deletePackage(c.getPlayer().getId(), c.getPlayer().getAccountID(), pack.getPackageid()):
            c.getPlayer().gainMeso(pack.getMesos(), False)
            for item in pack.getItems():
                MapleInventoryManipulator.addFromDrop(c, item, False)
            c.getPlayer().dropMessage(5, "领取成功。")
        else:
            c.getPlayer().dropMessage(1, "发生未知错误。")

    def check(self, chr: Any, pack: Any) -> bool:
        if chr.getMeso() + pack.getMesos() < 0:
            print("[雇佣] " + chr.getName() + " 雇佣取回道具金币检测错误 时间: " + FileoutputUtil.CurrentReadable_Date())
            FileoutputUtil.hiredMerchLog(chr.getName(), "雇佣取回道具金币检测错误")
            return False
        eq = 0
        use = 0
        setup = 0
        etc = 0
        cash = 0
        for item in pack.getItems():
            invtype = GameConstants.getInventoryType(item.getItemId())
            if None != invtype:
                # switch (invtype):
                    # case EQUIP:
                        eq += 1
                        break
                    # case USE:
                        use += 1
                        break
                    # case SETUP:
                        setup += 1
                        break
                    # case ETC:
                        etc += 1
                        break
                    # case CASH:
                        cash += 1
                        break
            if MapleItemInformationProvider.getInstance().isPickupRestricted(item.getItemId()) and chr.haveItem(item.getItemId(), 1):
                print("[雇佣] " + chr.getName() + " 雇佣取回道具是否可以捡取错误 时间: " + FileoutputUtil.CurrentReadable_Date())
                FileoutputUtil.hiredMerchLog(chr.getName(), "雇佣取回道具是否可以捡取错误")
                return False
        if chr.getInventory(MapleInventoryType.EQUIP).getNumFreeSlot() < eq or chr.getInventory(MapleInventoryType.USE).getNumFreeSlot() < use or chr.getInventory(MapleInventoryType.SETUP).getNumFreeSlot() < setup or chr.getInventory(MapleInventoryType.ETC).getNumFreeSlot() < etc or chr.getInventory(MapleInventoryType.CASH).getNumFreeSlot() < cash:
            print("[雇佣] " + chr.getName() + " 雇佣取回道具背包空间不够 时间: " + FileoutputUtil.CurrentReadable_Date())
            FileoutputUtil.hiredMerchLog(chr.getName(), "雇佣取回道具背包空间不够")
            return False
        return True

    def deletePackage(self, charid: int, accid: int, packageid: int) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("DELETE from hiredmerch where characterid = ? OR accountid = ? OR packageid = ?")
            ps.setInt(1, charid)
            ps.setInt(2, accid)
            ps.setInt(3, packageid)
            ps.execute()
            ps.close()
            ItemLoader.HIRED_MERCHANT.saveItems(None, packageid, accid, charid)
            return True
        except Exception as e:
            print("删除弗洛兰德道具信息出错" + e)
            return False

    def deletePackage_charid_accid(self, charid: int, accid: int) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("DELETE from hiredmerch where characterid = ? OR accountid = ?")
            ps.setInt(1, charid)
            ps.setInt(2, accid)
            ps.execute()
            ps.close()
            return True
        except Exception as e:
            print("删除弗洛兰德道具信息出错" + e)
            return False

    def loadItemFrom_Database(self, charid: int, accountid: int, chr: Any) -> Any:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * from hiredmerch where characterid = ? OR accountid = ?")
            ps.setInt(1, charid)
            ps.setInt(2, accountid)
            rs = ps.executeQuery()
            if not rs.next():
                ps.close()
                rs.close()
                return None
            packageid = rs.getInt("PackageId")
            pack = MerchItemPackage()
            pack.setPackageid(packageid)
            pack.setSentTime(rs.getLong("time"))
            ps.close()
            rs.close()
            items = ItemLoader.HIRED_MERCHANT.loadItems_hm(packageid, accountid)
            mesos = chr.getMerchantMeso()
            if mesos == 0 and items == 0:
                FileoutputUtil.hiredMerchLog(chr.getName(), "加载弗洛兰德道具信息 金币 " + mesos + " 是否有道具 " + items)
                return None
            pack.setMesos(mesos)
            if not items == 0:
                iters = []
                for z in items.values():
                    iters.add(z.left)
                pack.setItems(iters)
            FileoutputUtil.hiredMerchLog(chr.getName(), "弗洛兰德取回最后返回 金币: " + mesos + " 道具数量: " + items)
            return pack
        except Exception as e:
            print("加载弗洛兰德道具信息出错" + e)
            return None

