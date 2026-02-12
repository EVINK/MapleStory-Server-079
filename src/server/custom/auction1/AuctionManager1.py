"""
AuctionManager1 - Converted from Java source
Original: server/custom/auction1/AuctionManager1.java
Package: server.custom.auction1
"""

from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import logging
import pymysql

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.IEquip import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.Item import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryIdentifier import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from client.inventory.MaplePet import *  # TODO: import specific classes
# from client.inventory.MapleRing import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.OtherSettings import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class AuctionManager1:
    """
    Class AuctionManager1
    """

    def __init__(self):
        pass
        pass

    # Static initializer
    # instance = AuctionManager1()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def gainItem(self, item: Any, quantity: int, cg: Any) -> None:
        if quantity >= 0:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(item.getItemId())
            if !MapleInventoryManipulator.checkSpace(cg, item.getItemId(), quantity, ""):
                return
            if type == (MapleInventoryType.EQUIP) && !GameConstants.isThrowingStar(item.getItemId()) && !GameConstants.isBullet(item.getItemId()):
                equip = item
                name = ii.getName(item.getItemId())
                if item.getItemId() / 10000 == 114 && name is not None && name > 0:
                    msg = "你已获得称号 <" + name + ">"
                    cg.getPlayer().dropMessage(5, msg)
                    cg.getPlayer().dropMessage(5, msg)
                MapleInventoryManipulator.addbyItem(cg, equip.copy())
            else:
                MapleInventoryManipulator.addbyItem(cg, item.copy())
        else:
            MapleInventoryManipulator.removeById(cg, GameConstants.getInventoryType(item.getItemId()), item.getItemId(), -quantity, True, False)
        cg.getSession().write(MaplePacketCreator.getShowItemGain(item.getItemId(), quantity, True))

    def putInt(self, player: Any, source: Any, quantity: int) -> int:
        ret = 1
        if player is None || source is None:
            return -4
        ii = MapleItemInformationProvider.getInstance()
        if source.getExpiration() > 0:
            return -5
        flag = source.getFlag()
        if quantity > source.getQuantity() || quantity < 1:
            return -6
        itemtype = self.getItemTypeByItemId(source.getItemId())
        if ItemFlag.LOCK.check(flag) || (quantity != 1 && itemtype == MapleInventoryType.EQUIP):
            return -7
        item_id = OtherSettings()
        itemgy_id = item_id.getItempb_id()
        for i in range(len(itemgy_id)):
            if source.getItemId() == int(itemgy_id[i]):
                return -8
        AuctionItem1 = AuctionItem1()
        AuctionItem1.setAuctionState(AuctionState1.下架)
        AuctionItem1.setCharacterid(player.getId())
        AuctionItem1.setCharacterName(player.getName())
        AuctionItem1.setQuantity(quantity)
        AuctionItem1.setItem(source.copy())
        id = self.add(AuctionItem1)
        if id < 1:
            return id
        AuctionItem1.setId(id)
        if GameConstants.isThrowingStar(source.getItemId()) || GameConstants.isBullet(source.getItemId()):
            quantity = source.getQuantity()
        MapleInventoryManipulator.removeFromSlot(player.getClient(), itemtype, source.getPosition(), quantity, False)
        return ret

    def takeOutAuctionItem(self, player: Any, id: int) -> int:
        AuctionItem1 = self.findById(id)
        if AuctionItem1 is None:
            return -5
        return self.takeOutAuctionItem(player, id, AuctionItem1.getQuantity())

    def takeOutAuctionItem_player_id_count(self, player: Any, id: int, count: int) -> int:
        AuctionItem1 = self.findById(id)
        if AuctionItem1 is None:
            return -5
        return self.takeOutAuctionItem(player, AuctionItem1, count)

    def takeOutAuctionItem_player_AuctionItem1_count(self, player: Any, AuctionItem1: Any, count: int) -> int:
        if AuctionItem1 is None:
            return -5
        if AuctionItem1.getCharacterid() != player.getId():
            return -6
        if AuctionState1.下架 != AuctionItem1.getAuctionState():
            return -7
        if count > AuctionItem1.getQuantity() || count < 1:
            return -8
        if !MapleInventoryManipulator.checkSpace(player.getClient(), AuctionItem1.getItem().getItemId(), count, ""):
            return -9
        ret = 1
        if count < AuctionItem1.getQuantity() && !GameConstants.isThrowingStar(AuctionItem1.getItem().getItemId()) && !GameConstants.isBullet(AuctionItem1.getItem().getItemId()):
            AuctionItem1.setQuantity(AuctionItem1.getQuantity() - count)
            ret = getInstance().update(AuctionItem1)
        else:
            ret = getInstance().deleteById(AuctionItem1.getId())
        if ret > 0:
            self.gainItem(AuctionItem1.getItem(), count, player.getClient())
        return ret

    def buy(self, player: Any, id: int) -> int:
        AuctionItem1 = self.findById(id)
        if AuctionItem1 is None:
            return -5
        return self.buy(player, AuctionItem1)

    def buy_player_AuctionItem1(self, player: Any, AuctionItem1: Any) -> int:
        ret = -1
        if AuctionItem1 is None:
            return -5
        if AuctionState1.上架 != AuctionItem1.getAuctionState():
            return -6
        AuctionPoint1 = self.getAuctionPoint(player.getId())
        if AuctionPoint1 is None:
            return -7
        if AuctionPoint1.getPoint1() < AuctionItem1.getPrice():
            return -8
        if !MapleInventoryManipulator.checkSpace(player.getClient(), AuctionItem1.getItem().getItemId(), AuctionItem1.getQuantity(), ""):
            return -9
        AuctionItem1.setAuctionState(AuctionState1.已售)
        AuctionItem1.setBuyer(player.getId())
        AuctionItem1.setBuyerName(player.getName())
        ret = self.update(AuctionItem1)
        if ret > 0:
            addpc = self.addPoint(player.getId(), -AuctionItem1.getPrice())
            if addpc > 0:
                addp = self.addPoint(AuctionItem1.getCharacterid(), AuctionItem1.getPrice())
                if addp > 0:
                    if AuctionItem1.getCharacterid() != player.getId():
                        self.addPointSell(AuctionItem1.getCharacterid(), AuctionItem1.getPrice())
                        self.addPointBuy(player.getId(), AuctionItem1.getPrice())
                    self.gainItem(AuctionItem1.getItem(), AuctionItem1.getQuantity(), player.getClient())
        return ret

    def setPutaway(self, id: int, price: int) -> int:
        AuctionItem1 = self.findById(id)
        if AuctionItem1 is None:
            return -5
        AuctionItem1.setPrice(price)
        return self.setPutaway(AuctionItem1)

    def setPutaway_AuctionItem1(self, AuctionItem1: Any) -> int:
        if AuctionState1.下架 != AuctionItem1.getAuctionState():
            return -6
        if AuctionItem1.getPrice() < 1:
            return -7
        AuctionItem1.setAuctionState(AuctionState1.上架)
        return self.update(AuctionItem1)

    def soldOut(self, id: int) -> int:
        AuctionItem1 = self.findById(id)
        if AuctionItem1 is None:
            return -5
        return self.soldOut(AuctionItem1)

    def soldOut_AuctionItem1(self, AuctionItem1: Any) -> int:
        if AuctionState1.上架 != AuctionItem1.getAuctionState():
            return -6
        AuctionItem1.setAuctionState(AuctionState1.下架)
        AuctionItem1.setPrice(0)
        return self.update(AuctionItem1)

    def getAuctionPoint(self, characterid: int) -> Any:
        AuctionPoint1 = None
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from AuctionPoint1 where characterid = ?")
            ps.setInt(1, characterid)
            rs = ps.executeQuery()
            if rs.next():
                AuctionPoint1 = AuctionPoint1()
                AuctionPoint1.setCharacterid(rs.getInt("characterid"))
                AuctionPoint1.setPoint(rs.getInt("point"))
                AuctionPoint1.setPoint1_sell(rs.getInt("point_sell"))
                AuctionPoint1.setPoint1_buy(rs.getInt("point_buy"))
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return None
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return None
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return None
        return AuctionPoint1

    def addPoint(self, characterid: int, point: int) -> int:
        return self.addPoint(characterid, point, 1)

    def addPointSell(self, characterid: int, point: int) -> int:
        return self.addPoint(characterid, point, 2)

    def addPointBuy(self, characterid: int, point: int) -> int:
        return self.addPoint(characterid, point, 3)

    def addPoint_characterid_point_type(self, characterid: int, point: int, type: int) -> int:
        ret = -1
        update = False
        dbPoint = self.getAuctionPoint(characterid)
        if dbPoint is None:
            dbPoint = AuctionPoint1()
            dbPoint.setCharacterid(characterid)
        else:
            update = True
        # switch (type):
            # case 1:
                dbPoint.setPoint(dbPoint.getPoint1() + point)
                break
            # case 2:
                dbPoint.setPoint1_sell(dbPoint.getPoint1_sell() + point)
                break
            # case 3:
                dbPoint.setPoint1_buy(dbPoint.getPoint1_buy() + point)
                break
        ps = None
        try:
            if update:
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `AuctionPoint1` SET point = ? , point_sell = ? , point_buy = ? WHERE characterid = ? ")
                ps.setLong(1, dbPoint.getPoint1())
                ps.setLong(2, dbPoint.getPoint1_sell())
                ps.setLong(3, dbPoint.getPoint1_buy())
                ps.setInt(4, dbPoint.getCharacterid())
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `AuctionPoint1` VALUES (?, ?, ?, ?)")
                ps.setInt(1, dbPoint.getCharacterid())
                ps.setLong(2, dbPoint.getPoint1())
                ps.setLong(3, dbPoint.getPoint1_sell())
                ps.setLong(4, dbPoint.getPoint1_buy())
            ret = ps.executeUpdate()
            try:
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def add(self, AuctionItem1: Any) -> int:
        ret = -1
        itemtype = self.getItemTypeByItemId(AuctionItem1.getItem().getItemId())
        ps = None
        rs = None
        try:
            if itemtype == (MapleInventoryType.EQUIP) || itemtype == (MapleInventoryType.EQUIPPED):
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `auctionitems` VALUES (None, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 1)
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `auctionitems` (characterid,characterName,AuctionState1,buyer,buyerName,price,itemid,inventorytype,quantity,owner,GM_Log,uniqueid,flag,expiredate,sender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 1)
            self.mapSavePs(ps, AuctionItem1)
            ps.executeUpdate()
            rs = ps.getGeneratedKeys()
            if rs is not None && rs.next():
                ret = rs.getInt(1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def update(self, AuctionItem1: Any) -> int:
        ret = -1
        itemtype = self.getItemTypeByItemId(AuctionItem1.getItem().getItemId())
        ps = None
        rs = None
        try:
            if itemtype == (MapleInventoryType.EQUIP) || itemtype == (MapleInventoryType.EQUIPPED):
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `auctionitems` SET characterid = ? ,characterName = ? ,AuctionState1 = ?,buyer = ?,buyerName = ? ,price = ?,itemid = ?,inventorytype = ?,quantity = ?,owner = ?,GM_Log = ?,uniqueid = ?,flag = ?,expiredate = ?,sender = ?,upgradeslots = ?,level = ?,str = ?,dex = ?,_int = ?,luk = ?,hp = ?,mp = ?,watk = ?,matk = ?,wdef = ?,mdef = ?,acc = ?,avoid = ?,hands = ?,speed = ?,jump = ?,ViciousHammer = ?,itemEXP = ?,durability = ?,enhance = ?,potential1 = ?,potential2 = ?,potential3 = ?,hpR = ?,mpR = ?,itemlevel = ? where id = ?")
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `auctionitems` SET characterid = ?, characterName = ? ,AuctionState1 = ?,buyer = ?,buyerName = ? ,price = ?,itemid = ?,inventorytype = ?,quantity = ?,owner = ?,GM_Log = ?,uniqueid = ?,flag = ?,expiredate = ?,sender = ? where id = ?")
            self.mapSavePs(ps, AuctionItem1)
            if itemtype == (MapleInventoryType.EQUIP) || itemtype == (MapleInventoryType.EQUIPPED):
                ps.setLong(43, AuctionItem1.getId())
            else:
                ps.setLong(16, AuctionItem1.getId())
            ret = ps.executeUpdate()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def deleteById(self, id: int) -> int:
        ret = -1
        ps_del = None
        try:
            ps_del = DatabaseConnection.getConnection().prepareStatement("DELETE  FROM auctionItems where id = ?")
            ps_del.setLong(1, id)
            ret = ps_del.executeUpdate()
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def deletePlayerSold(self, characterid: int) -> int:
        ret = -1
        ps_del = None
        try:
            ps_del = DatabaseConnection.getConnection().prepareStatement("DELETE  FROM auctionItems where characterid = ? and AuctionState1 = ?")
            ps_del.setInt(1, characterid)
            ps_del.setInt(2, AuctionState1.已售.getState1())
            ret = ps_del.executeUpdate()
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def findById(self, id: int) -> Any:
        AuctionItem1 = None
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where id = ?")
            ps.setLong(1, id)
            rs = ps.executeQuery()
            if rs.next():
                AuctionItem1 = self.mapLoadRs(rs)
        except Exception as e1:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
        return AuctionItem1

    def findByCharacterId(self, characterid: int) -> list:
        ret = []
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where characterid = ?")
            ps.setInt(1, characterid)
            rs = ps.executeQuery()
            while rs.next():
                AuctionItem1 = self.mapLoadRs(rs)
                if AuctionItem1 is not None:
                    ret.add(AuctionItem1)
        except Exception as e1:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
        return ret

    def findByItemType(self, inventorytype: int) -> list:
        ret = []
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where inventorytype = ? and AuctionState1 = 1 order by itemid desc")
            ps.setInt(1, inventorytype)
            rs = ps.executeQuery()
            while rs.next():
                AuctionItem1 = self.mapLoadRs(rs)
                if AuctionItem1 is not None:
                    ret.add(AuctionItem1)
        except Exception as e1:
            Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager1.class.getName()).log(Level.SEVERE, None, ex2)
        return ret

    def getItemTypeByItemId(self, itemid: int) -> Any:
        return MapleInventoryType.getByType((byte)(itemid / 1000000))

    def mapSavePs(self, ps: Any, auctionItem1: Any) -> None:
        itemtype = self.getItemTypeByItemId(auctionItem1.getItem().getItemId())
        item = auctionItem1.getItem()
        ps.setInt(1, auctionItem1.getCharacterid())
        ps.setString(2, auctionItem1.getCharacterName())
        ps.setInt(3, auctionItem1.getAuctionState().getState1())
        ps.setInt(4, auctionItem1.getBuyer())
        ps.setString(5, auctionItem1.getBuyerName())
        ps.setInt(6, auctionItem1.getPrice())
        ps.setInt(7, item.getItemId())
        ps.setInt(8, itemtype.getType())
        ps.setInt(9, auctionItem1.getQuantity())
        ps.setString(10, item.getOwner())
        ps.setString(11, item.getGMLog())
        ps.setInt(12, item.getUniqueId())
        ps.setByte(13, item.getFlag())
        ps.setLong(14, item.getExpiration())
        ps.setString(15, item.getGiftFrom())
        if itemtype == (MapleInventoryType.EQUIP) || itemtype == (MapleInventoryType.EQUIPPED):
            equip = item
            ps.setInt(16, equip.getUpgradeSlots())
            ps.setInt(17, equip.getLevel())
            ps.setInt(18, equip.getStr())
            ps.setInt(19, equip.getDex())
            ps.setInt(20, equip.getInt())
            ps.setInt(21, equip.getLuk())
            ps.setInt(22, equip.getHp())
            ps.setInt(23, equip.getMp())
            ps.setInt(24, equip.getWatk())
            ps.setInt(25, equip.getMatk())
            ps.setInt(26, equip.getWdef())
            ps.setInt(27, equip.getMdef())
            ps.setInt(28, equip.getAcc())
            ps.setInt(29, equip.getAvoid())
            ps.setInt(30, equip.getHands())
            ps.setInt(31, equip.getSpeed())
            ps.setInt(32, equip.getJump())
            ps.setInt(33, equip.getViciousHammer())
            ps.setInt(34, equip.getItemEXP())
            ps.setInt(35, equip.getDurability())
            ps.setByte(36, equip.getEnhance())
            ps.setInt(37, equip.getPotential1())
            ps.setInt(38, equip.getPotential2())
            ps.setInt(39, equip.getPotential3())
            ps.setInt(40, equip.getHpR())
            ps.setInt(41, equip.getMpR())
            ps.setByte(42, equip.getEquipLevel())

    def mapLoadRs(self, rs: Any) -> Any:
        id = rs.getLong("id")
        characterid = rs.getInt("characterid")
        characterName = rs.getString("characterName")
        AuctionState1 = rs.getByte("AuctionState1")
        buyer = rs.getInt("buyer")
        buyerName = rs.getString("buyerName")
        price = rs.getInt("price")
        itemid = rs.getInt("itemid")
        inventorytype = rs.getInt("inventorytype")
        quantity = rs.getShort("quantity")
        owner = rs.getString("owner")
        GM_Log = rs.getString("GM_Log")
        uniqueid = rs.getInt("uniqueid")
        flag = rs.getByte("flag")
        expiredate = rs.getLong("expiredate")
        sender = rs.getString("sender")
        upgradeslots = rs.getByte("upgradeslots")
        level = rs.getByte("level")
        str = rs.getShort("str")
        dex = rs.getShort("dex")
        _int = rs.getShort("_int")
        luk = rs.getShort("luk")
        hp = rs.getShort("hp")
        mp = rs.getShort("mp")
        watk = rs.getShort("watk")
        matk = rs.getShort("matk")
        wdef = rs.getShort("wdef")
        mdef = rs.getShort("mdef")
        acc = rs.getShort("acc")
        avoid = rs.getShort("avoid")
        hands = rs.getShort("hands")
        speed = rs.getShort("speed")
        jump = rs.getShort("jump")
        ViciousHammer = rs.getByte("ViciousHammer")
        itemEXP = rs.getInt("itemEXP")
        durability = rs.getInt("durability")
        enhance = rs.getByte("enhance")
        potential1 = rs.getShort("potential1")
        potential2 = rs.getShort("potential2")
        potential3 = rs.getShort("potential3")
        hpR = rs.getShort("hpR")
        mpR = rs.getShort("mpR")
        itemlevel = rs.getByte("itemlevel")
        mit = MapleInventoryType.getByType(inventorytype)
        if characterid < 1 || mit is None:
            return None
        auctionItem1 = AuctionItem1()
        auctionItem1.setPrice(price)
        auctionItem1.setBuyer(buyer)
        auctionItem1.setBuyerName(buyerName)
        auctionItem1.setCharacterid(characterid)
        auctionItem1.setCharacterName(characterName)
        auctionItem1.setQuantity(quantity)
        if mit == (MapleInventoryType.EQUIP) || mit == (MapleInventoryType.EQUIPPED):
            equip = Equip(itemid, 0, uniqueid, flag)
            equip.setQuantity(1)
            equip.setOwner(owner)
            equip.setExpiration(expiredate)
            equip.setUpgradeSlots(upgradeslots)
            equip.setLevel(level)
            equip.setStr(str)
            equip.setDex(dex)
            equip.setInt(_int)
            equip.setLuk(luk)
            equip.setHp(hp)
            equip.setMp(mp)
            equip.setWatk(watk)
            equip.setMatk(matk)
            equip.setWdef(wdef)
            equip.setMdef(mdef)
            equip.setAcc(acc)
            equip.setAvoid(avoid)
            equip.setHands(hands)
            equip.setSpeed(speed)
            equip.setJump(jump)
            equip.setViciousHammer(ViciousHammer)
            equip.setItemEXP(itemEXP)
            equip.setGMLog(GM_Log)
            equip.setDurability(durability)
            equip.setEnhance(enhance)
            equip.setPotential1(potential1)
            equip.setPotential2(potential2)
            equip.setPotential3(potential3)
            equip.setHpR(hpR)
            equip.setMpR(mpR)
            equip.setGiftFrom(sender)
            equip.setEquipLevel(itemlevel)
            if equip.getUniqueId() > -1 && GameConstants.isEffectRing(itemid):
                ring = MapleRing.loadFromDb(equip.getUniqueId(), mit == (MapleInventoryType.EQUIPPED))
                if ring is not None:
                    equip.setRing(ring)
            auctionItem1.setItem(equip.copy())
        else:
            item = Item(itemid, 0, quantity, flag)
            item.setUniqueId(uniqueid)
            item.setOwner(owner)
            item.setExpiration(expiredate)
            item.setGMLog(GM_Log)
            item.setGiftFrom(sender)
            if GameConstants.isPet(item.getItemId()):
                if item.getUniqueId() > -1:
                    pet = MaplePet.loadFromDb(item.getItemId(), item.getUniqueId(), item.getPosition())
                    if pet is not None:
                        item.setPet(pet)
                else:
                    new_unique = MapleInventoryIdentifier.getInstance()
                    item.setUniqueId(new_unique)
                    item.setPet(MaplePet.createPet(item.getItemId(), new_unique))
            auctionItem1.setItem(item.copy())
        return auctionItem1


# Inner class from Java (originally nested)
class InstanceHolder1:
    """
    Class InstanceHolder1
    """

    # Static initializer
    # instance = AuctionManager1()

    pass

