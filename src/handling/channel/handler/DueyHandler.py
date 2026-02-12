"""
DueyHandler - Converted from Java source
Original: handling/channel/handler/DueyHandler.java
Package: handling.channel.handler
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
import pymysql
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleCharacterUtil import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.MapleDueyActions import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes
# from tools.data.input.SeekableLittleEndianAccessor import *  # TODO: import specific classes


class DueyHandler:
    """
    Class DueyHandler
    """


    def DueyOperation(self, slea: Any, c: Any) -> None:
        operation = slea.readByte()
        # switch (operation):
            # case 1:
                AS13Digit = slea.readMapleAsciiString()
                conv = c.getPlayer().getConversation()
                if conv == 2:
                    c.getSession().write(MaplePacketCreator.sendDuey(10, loadItems(c.getPlayer())))
                    break
                break
            # case 3:
                if c.getPlayer().getConversation() != 2:
                    return
                inventId = slea.readByte()
                itemPos = slea.readShort()
                amount = slea.readShort()
                mesos = slea.readInt()
                recipient = slea.readMapleAsciiString()
                quickdelivery = slea.readByte() > 0
                finalcost = mesos + GameConstants.getTaxAmount(mesos) + (quickdelivery ? 0 : 5000)
                if mesos >= 0 && mesos <= 100000000 && c.getPlayer().getMeso() >= finalcost:
                    accid = MapleCharacterUtil.getIdByName(recipient)
                    if accid != -1:
                        if accid != c.getAccID():
                            recipientOn = False
                            if inventId > 0:
                                inv = MapleInventoryType.getByType(inventId)
                                item = c.getPlayer().getInventory(inv).getItem(itemPos)
                                if item is None:
                                    c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                                    return
                                flag = item.getFlag()
                                if ItemFlag.UNTRADEABLE.check(flag) || ItemFlag.LOCK.check(flag):
                                    c.getSession().write(MaplePacketCreator.enableActions())
                                    return
                                if c.getPlayer().getItemQuantity(item.getItemId(), False) >= amount:
                                    ii = MapleItemInformationProvider.getInstance()
                                    if !ii.isDropRestricted(item.getItemId()) && !ii.isAccountShared(item.getItemId()):
                                        if addItemToDB(item, amount, mesos, c.getPlayer().getName(), accid, recipientOn):
                                            if GameConstants.is飞镖道具(item.getItemId()) || GameConstants.is子弹道具(item.getItemId()):
                                                MapleInventoryManipulator.removeFromSlot(c, inv, itemPos, item.getQuantity(), True)
                                            else:
                                                MapleInventoryManipulator.removeFromSlot(c, inv, itemPos, amount, True, False)
                                            c.getPlayer().gainMeso(-finalcost, False)
                                            c.getSession().write(MaplePacketCreator.sendDuey(19, None))
                                        else:
                                            c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                                    else:
                                        c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                                else:
                                    c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                            elif addMesoToDB(mesos, c.getPlayer().getName(), accid, recipientOn):
                                c.getPlayer().gainMeso(-finalcost, False)
                                c.getSession().write(MaplePacketCreator.sendDuey(19, None))
                            else:
                                c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                        else:
                            c.getSession().write(MaplePacketCreator.sendDuey(15, None))
                    else:
                        c.getSession().write(MaplePacketCreator.sendDuey(14, None))
                    break
                c.getSession().write(MaplePacketCreator.sendDuey(12, None))
                break
            # case 5:
                if c.getPlayer().getConversation() != 2:
                    return
                packageid = slea.readInt()
                dp = loadSingleItem(packageid, c.getPlayer().getId())
                if dp is None:
                    return
                if dp.getItem() is not None && !MapleInventoryManipulator.checkSpace(c, dp.getItem().getItemId(), dp.getItem().getQuantity(), dp.getItem().getOwner()):
                    c.getSession().write(MaplePacketCreator.sendDuey(16, None))
                    return
                if dp.getMesos() < 0 || dp.getMesos() + c.getPlayer().getMeso() < 0:
                    c.getSession().write(MaplePacketCreator.sendDuey(17, None))
                    return
                removeItemFromDB(packageid, c.getPlayer().getId())
                if dp.getItem() is not None:
                    MapleInventoryManipulator.addFromDrop(c, dp.getItem(), False)
                if dp.getMesos() != 0:
                    c.getPlayer().gainMeso(dp.getMesos(), False)
                c.getSession().write(MaplePacketCreator.removeItemFromDuey(False, packageid))
                break
            # case 6:
                if c.getPlayer().getConversation() != 2:
                    return
                packageid = slea.readInt()
                removeItemFromDB(packageid, c.getPlayer().getId())
                c.getSession().write(MaplePacketCreator.removeItemFromDuey(True, packageid))
                break
            # case 8:
                c.getPlayer().setConversation(0)
                break
            # default:
                print("Unhandled Duey operation : " + slea)
                break

    def addMesoToDB(self, mesos: int, sName: str, recipientID: int, isOn: bool) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("INSERT INTO dueypackages (RecieverId, SenderName, Mesos, TimeStamp, Checked, Type) VALUES (?, ?, ?, ?, ?, ?)")
            ps.setInt(1, recipientID)
            ps.setString(2, sName)
            ps.setInt(3, mesos)
            ps.setLong(4, int(time.time() * 1000))
            ps.setInt(5, isOn ? 0 : 1)
            ps.setInt(6, 3)
            ps.executeUpdate()
            ps.close()
            return True
        except Exception as se:
            se.printStackTrace()
            return False

    def addItemToDB(self, item: Any, quantity: int, mesos: int, sName: str, recipientID: int, isOn: bool) -> bool:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("INSERT INTO dueypackages (RecieverId, SenderName, Mesos, TimeStamp, Checked, Type) VALUES (?, ?, ?, ?, ?, ?)", 1)
            ps.setInt(1, recipientID)
            ps.setString(2, sName)
            ps.setInt(3, mesos)
            ps.setLong(4, int(time.time() * 1000))
            ps.setInt(5, isOn ? 0 : 1)
            ps.setInt(6, item.getType())
            ps.executeUpdate()
            rs = ps.getGeneratedKeys()
            if rs.next():
                ItemLoader.DUEY.saveItems(Collections.singletonList(new Pair<IItem, MapleInventoryType>(item, GameConstants.getInventoryType(item.getItemId()))), rs.getInt(1))
            rs.close()
            ps.close()
            return True
        except Exception as se:
            se.printStackTrace()
            return False

    def loadItems(self, chr: Any) -> list:
        packages = []
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM dueypackages WHERE RecieverId = ?")
            ps.setInt(1, chr.getId())
            rs = ps.executeQuery()
            while rs.next():
                dueypack = getItemByPID(rs.getInt("packageid"))
                dueypack.setSender(rs.getString("SenderName"))
                dueypack.setMesos(rs.getInt("Mesos"))
                dueypack.setSentTime(rs.getLong("TimeStamp"))
                packages.add(dueypack)
            rs.close()
            ps.close()
            return packages
        except Exception as se:
            se.printStackTrace()
            return None

    def loadSingleItem(self, packageid: int, charid: int) -> Any:
        packages = []
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("SELECT * FROM dueypackages WHERE PackageId = ? and RecieverId = ?")
            ps.setInt(1, packageid)
            ps.setInt(2, charid)
            rs = ps.executeQuery()
            if rs.next():
                dueypack = getItemByPID(packageid)
                dueypack.setSender(rs.getString("SenderName"))
                dueypack.setMesos(rs.getInt("Mesos"))
                dueypack.setSentTime(rs.getLong("TimeStamp"))
                packages.add(dueypack)
                rs.close()
                ps.close()
                return dueypack
            rs.close()
            ps.close()
            return None
        except Exception as se:
            return None

    def reciveMsg(self, c: Any, recipientId: int) -> None:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("UPDATE dueypackages SET Checked = 0 where RecieverId = ?")
            ps.setInt(1, recipientId)
            ps.executeUpdate()
            ps.close()
        except Exception as se:
            se.printStackTrace()

    def removeItemFromDB(self, packageid: int, charid: int) -> None:
        con = DatabaseConnection.getConnection()
        try:
            ps = con.prepareStatement("DELETE FROM dueypackages WHERE PackageId = ? and RecieverId = ?")
            ps.setInt(1, packageid)
            ps.setInt(2, charid)
            ps.executeUpdate()
            ps.close()
        except Exception as se:
            se.printStackTrace()

    def getItemByPID(self, packageid: int) -> Any:
        try:
            iter = ItemLoader.DUEY.loadItems(False, packageid)
            if iter is not None && iter > 0:
                iterator = iter.values().iterator()
                if iterator.hasNext():
                    i = iterator.next()
                    return MapleDueyActions(packageid, i.getLeft())
        except Exception as se:
            se.printStackTrace()
        return MapleDueyActions(packageid)

