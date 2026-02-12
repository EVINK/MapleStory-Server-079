"""
AuctionManager - Converted from Java source
Original: server/custom/auction/AuctionManager.java
Package: server.custom.auction
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


class AuctionManager:
    """
    Class AuctionManager
    """

    def __init__(self):
        pass
        pass

    # Static initializer
    # instance = AuctionManager()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def gainItem(self, item: Any, quantity: int, cg: Any) -> None:
        if quantity >= 0:
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(item.getItemId())
            if not MapleInventoryManipulator.checkSpace(cg, item.getItemId(), quantity, ""):
                return
            if type == (MapleInventoryType.EQUIP) and not GameConstants.isThrowingStar(item.getItemId()) and not GameConstants.isBullet(item.getItemId()):
                equip = item
                name = ii.getName(item.getItemId())
                if item.getItemId() / 10000 == 114 and name is not None and name > 0:
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
        if player is None or source is None:
            return -4
        ii = MapleItemInformationProvider.getInstance()
        if source.getExpiration() > 0:
            return -5
        flag = source.getFlag()
        if quantity > source.getQuantity() or quantity < 1:
            return -6
        itemtype = self.getItemTypeByItemId(source.getItemId())
        if ItemFlag.LOCK.check(flag) or ItemFlag.UNTRADEABLE.check(flag) or (quantity != 1 and itemtype == MapleInventoryType.EQUIP):
            return -7
        item_id = OtherSettings()
        itemgy_id = item_id.getItempb_id()
        for i in range(len(itemgy_id)):
            if source.getItemId() == int(itemgy_id[i]):
                return -8
        auctionItem = AuctionItem()
        auctionItem.setAuctionState(AuctionState.下架)
        auctionItem.setCharacterid(player.getId())
        auctionItem.setCharacterName(player.getName())
        auctionItem.setQuantity(quantity)
        auctionItem.setItem(source.copy())
        id = self.add(auctionItem)
        if id < 1:
            return id
        auctionItem.setId(id)
        if GameConstants.isThrowingStar(source.getItemId()) or GameConstants.isBullet(source.getItemId()):
            quantity = source.getQuantity()
        MapleInventoryManipulator.removeFromSlot(player.getClient(), itemtype, source.getPosition(), quantity, False)
        return ret

    def takeOutAuctionItem(self, player: Any, id: int) -> int:
        auctionItem = self.findById(id)
        if auctionItem is None:
            return -5
        return self.takeOutAuctionItem(player, id, auctionItem.getQuantity())

    def takeOutAuctionItem_player_id_count(self, player: Any, id: int, count: int) -> int:
        auctionItem = self.findById(id)
        if auctionItem is None:
            return -5
        return self.takeOutAuctionItem(player, auctionItem, count)

    def takeOutAuctionItem_player_auctionItem_count(self, player: Any, auctionItem: Any, count: int) -> int:
        if auctionItem is None:
            return -5
        if auctionItem.getCharacterid() != player.getId():
            return -6
        if AuctionState.下架 != auctionItem.getAuctionState():
            return -7
        if count > auctionItem.getQuantity() or count < 1:
            return -8
        if not MapleInventoryManipulator.checkSpace(player.getClient(), auctionItem.getItem().getItemId(), count, ""):
            return -9
        ret = 1
        if count < auctionItem.getQuantity() and not GameConstants.isThrowingStar(auctionItem.getItem().getItemId()) and not GameConstants.isBullet(auctionItem.getItem().getItemId()):
            auctionItem.setQuantity(auctionItem.getQuantity() - count)
            ret = getInstance().update(auctionItem)
        else:
            ret = getInstance().deleteById(auctionItem.getId())
        if ret > 0:
            self.gainItem(auctionItem.getItem(), count, player.getClient())
        return ret

    def buy(self, player: Any, id: int) -> int:
        auctionItem = self.findById(id)
        if auctionItem is None:
            return -5
        return self.buy(player, auctionItem)

    def buy_player_auctionItem(self, player: Any, auctionItem: Any) -> int:
        ret = -1
        if auctionItem is None:
            return -5
        if AuctionState.上架 != auctionItem.getAuctionState():
            return -6
        auctionPoint = self.getAuctionPoint(player.getId())
        if auctionPoint is None:
            return -7
        if auctionPoint.getPoint() < auctionItem.getPrice():
            return -8
        if not MapleInventoryManipulator.checkSpace(player.getClient(), auctionItem.getItem().getItemId(), auctionItem.getQuantity(), ""):
            return -9
        auctionItem.setAuctionState(AuctionState.已售)
        auctionItem.setBuyer(player.getId())
        auctionItem.setBuyerName(player.getName())
        ret = self.update(auctionItem)
        if ret > 0:
            addpc = self.addPoint(player.getId(), -auctionItem.getPrice())
            if addpc > 0:
                addp = self.addPoint(auctionItem.getCharacterid(), auctionItem.getPrice())
                if addp > 0:
                    if auctionItem.getCharacterid() != player.getId():
                        self.addPointSell(auctionItem.getCharacterid(), auctionItem.getPrice())
                        self.addPointBuy(player.getId(), auctionItem.getPrice())
                    self.gainItem(auctionItem.getItem(), auctionItem.getQuantity(), player.getClient())
        return ret

    def setPutaway(self, id: int, price: int) -> int:
        auctionItem = self.findById(id)
        if auctionItem is None:
            return -5
        auctionItem.setPrice(price)
        return self.setPutaway(auctionItem)

    def setPutaway_auctionItem(self, auctionItem: Any) -> int:
        if AuctionState.下架 != auctionItem.getAuctionState():
            return -6
        if auctionItem.getPrice() < 1:
            return -7
        auctionItem.setAuctionState(AuctionState.上架)
        return self.update(auctionItem)

    def soldOut(self, id: int) -> int:
        auctionItem = self.findById(id)
        if auctionItem is None:
            return -5
        return self.soldOut(auctionItem)

    def soldOut_auctionItem(self, auctionItem: Any) -> int:
        if AuctionState.上架 != auctionItem.getAuctionState():
            return -6
        auctionItem.setAuctionState(AuctionState.下架)
        auctionItem.setPrice(0)
        return self.update(auctionItem)

    def getAuctionPoint(self, characterid: int) -> Any:
        auctionPoint = None
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionPoint where characterid = ?")
            ps.setInt(1, characterid)
            rs = ps.executeQuery()
            if rs.next():
                auctionPoint = AuctionPoint()
                auctionPoint.setCharacterid(rs.getInt("characterid"))
                auctionPoint.setPoint(rs.getInt("point"))
                auctionPoint.setPoint_sell(rs.getInt("point_sell"))
                auctionPoint.setPoint_buy(rs.getInt("point_buy"))
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return None
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return None
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return None
        return auctionPoint

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
            dbPoint = AuctionPoint()
            dbPoint.setCharacterid(characterid)
        else:
            update = True
        # switch (type):
            # case 1:
                dbPoint.setPoint(dbPoint.getPoint() + point)
                break
            # case 2:
                dbPoint.setPoint_sell(dbPoint.getPoint_sell() + point)
                break
            # case 3:
                dbPoint.setPoint_buy(dbPoint.getPoint_buy() + point)
                break
        ps = None
        try:
            if update:
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `auctionPoint` SET point = ? , point_sell = ? , point_buy = ? WHERE characterid = ? ")
                ps.setLong(1, dbPoint.getPoint())
                ps.setLong(2, dbPoint.getPoint_sell())
                ps.setLong(3, dbPoint.getPoint_buy())
                ps.setInt(4, dbPoint.getCharacterid())
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `auctionPoint` VALUES (?, ?, ?, ?)")
                ps.setInt(1, dbPoint.getCharacterid())
                ps.setLong(2, dbPoint.getPoint())
                ps.setLong(3, dbPoint.getPoint_sell())
                ps.setLong(4, dbPoint.getPoint_buy())
            ret = ps.executeUpdate()
            try:
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def add(self, auctionItem: Any) -> int:
        ret = -1
        itemtype = self.getItemTypeByItemId(auctionItem.getItem().getItemId())
        ps = None
        rs = None
        try:
            if itemtype == (MapleInventoryType.EQUIP) or itemtype == (MapleInventoryType.EQUIPPED):
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `auctionitems` VALUES (None, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 1)
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("INSERT INTO `auctionitems` (characterid,characterName,auctionState,buyer,buyerName,price,itemid,inventorytype,quantity,owner,GM_Log,uniqueid,flag,expiredate,sender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 1)
            self.mapSavePs(ps, auctionItem)
            ps.executeUpdate()
            rs = ps.getGeneratedKeys()
            if rs is not None and rs.next():
                ret = rs.getInt(1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def update(self, auctionItem: Any) -> int:
        ret = -1
        itemtype = self.getItemTypeByItemId(auctionItem.getItem().getItemId())
        ps = None
        rs = None
        try:
            if itemtype == (MapleInventoryType.EQUIP) or itemtype == (MapleInventoryType.EQUIPPED):
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `auctionitems` SET characterid = ? ,characterName = ? ,auctionState = ?,buyer = ?,buyerName = ? ,price = ?,itemid = ?,inventorytype = ?,quantity = ?,owner = ?,GM_Log = ?,uniqueid = ?,flag = ?,expiredate = ?,sender = ?,upgradeslots = ?,level = ?,str = ?,dex = ?,_int = ?,luk = ?,hp = ?,mp = ?,watk = ?,matk = ?,wdef = ?,mdef = ?,acc = ?,avoid = ?,hands = ?,speed = ?,jump = ?,ViciousHammer = ?,itemEXP = ?,durability = ?,enhance = ?,potential1 = ?,potential2 = ?,potential3 = ?,hpR = ?,mpR = ?,itemlevel = ? where id = ?")
            else:
                ps = DatabaseConnection.getConnection().prepareStatement("UPDATE `auctionitems` SET characterid = ?, characterName = ? ,auctionState = ?,buyer = ?,buyerName = ? ,price = ?,itemid = ?,inventorytype = ?,quantity = ?,owner = ?,GM_Log = ?,uniqueid = ?,flag = ?,expiredate = ?,sender = ? where id = ?")
            self.mapSavePs(ps, auctionItem)
            if itemtype == (MapleInventoryType.EQUIP) or itemtype == (MapleInventoryType.EQUIPPED):
                ps.setLong(43, auctionItem.getId())
            else:
                ps.setLong(16, auctionItem.getId())
            ret = ps.executeUpdate()
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def deleteById(self, id: int) -> int:
        ret = -1
        ps_del = None
        try:
            ps_del = DatabaseConnection.getConnection().prepareStatement("DELETE FROM auctionItems where id = ?")
            ps_del.setLong(1, id)
            ret = ps_del.executeUpdate()
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def deletePlayerSold(self, characterid: int) -> int:
        ret = -1
        ps_del = None
        try:
            ps_del = DatabaseConnection.getConnection().prepareStatement("DELETE FROM auctionItems where characterid = ? and auctionState = ?")
            ps_del.setInt(1, characterid)
            ps_del.setInt(2, AuctionState.已售.getState())
            ret = ps_del.executeUpdate()
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
                return -2
        except Exception as ex:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
            return -2
        finally:
            try:
                if ps_del is not None:
                    ps_del.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
                return -2
        return ret

    def findById(self, id: int) -> Any:
        auctionItem = None
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where id = ?")
            ps.setLong(1, id)
            rs = ps.executeQuery()
            if rs.next():
                auctionItem = self.mapLoadRs(rs)
        except Exception as e1:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
        return auctionItem

    def findByCharacterId(self, characterid: int) -> list:
        ret = []
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where characterid = ?")
            ps.setInt(1, characterid)
            rs = ps.executeQuery()
            while rs.next():
                auctionItem = self.mapLoadRs(rs)
                if auctionItem is not None:
                    ret.add(auctionItem)
        except Exception as e1:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
        return ret

    def findByItemType(self, inventorytype: int) -> list:
        ret = []
        ps = None
        rs = None
        try:
            ps = DatabaseConnection.getConnection().prepareStatement("select * from auctionitems where inventorytype = ? and auctionState = 1 order by itemid desc")
            ps.setInt(1, inventorytype)
            rs = ps.executeQuery()
            while rs.next():
                auctionItem = self.mapLoadRs(rs)
                if auctionItem is not None:
                    ret.add(auctionItem)
        except Exception as e1:
            Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, e1)
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex)
        finally:
            try:
                if rs is not None:
                    rs.close()
                if ps is not None:
                    ps.close()
            except Exception as ex2:
                Logger.getLogger(AuctionManager.class.getName()).log(Level.SEVERE, None, ex2)
        return ret

    def getItemTypeByItemId(self, itemid: int) -> Any:
        return MapleInventoryType.getByType((byte)(itemid / 1000000))

    def mapSavePs(self, ps: Any, auctionItem: Any) -> None:
        itemtype = self.getItemTypeByItemId(auctionItem.getItem().getItemId())
        item = auctionItem.getItem()
        ps.setInt(1, auctionItem.getCharacterid())
        ps.setString(2, auctionItem.getCharacterName())
        ps.setInt(3, auctionItem.getAuctionState().getState())
        ps.setInt(4, auctionItem.getBuyer())
        ps.setString(5, auctionItem.getBuyerName())
        ps.setInt(6, auctionItem.getPrice())
        ps.setInt(7, item.getItemId())
        ps.setInt(8, itemtype.getType())
        ps.setInt(9, auctionItem.getQuantity())
        ps.setString(10, item.getOwner())
        ps.setString(11, item.getGMLog())
        ps.setInt(12, item.getUniqueId())
        ps.setByte(13, item.getFlag())
        ps.setLong(14, item.getExpiration())
        ps.setString(15, item.getGiftFrom())
        if itemtype == (MapleInventoryType.EQUIP) or itemtype == (MapleInventoryType.EQUIPPED):
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
        auctionState = rs.getByte("auctionState")
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
        if characterid < 1 or mit is None:
            return None
        auctionItem = AuctionItem()
        auctionItem.setId(id)
        auctionItem.setAuctionState(AuctionState.getState(auctionState))
        auctionItem.setPrice(price)
        auctionItem.setBuyer(buyer)
        auctionItem.setBuyerName(buyerName)
        auctionItem.setCharacterid(characterid)
        auctionItem.setCharacterName(characterName)
        auctionItem.setQuantity(quantity)
        if mit == (MapleInventoryType.EQUIP) or mit == (MapleInventoryType.EQUIPPED):
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
            if equip.getUniqueId() > -1 and GameConstants.isEffectRing(itemid):
                ring = MapleRing.loadFromDb(equip.getUniqueId(), mit == (MapleInventoryType.EQUIPPED))
                if ring is not None:
                    equip.setRing(ring)
            auctionItem.setItem(equip.copy())
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
            auctionItem.setItem(item.copy())
        return auctionItem


# Inner class from Java (originally nested)
class InstanceHolder:
    """
    Class InstanceHolder
    """

    # Static initializer
    # instance = AuctionManager()

    pass

