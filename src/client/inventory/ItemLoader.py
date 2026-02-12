"""
ItemLoader - Converted from Java source
Original: client/inventory/ItemLoader.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class ItemLoader(Enum):
    """Enum ItemLoader"""

    装备道具 = ("inventoryitems", "inventoryequipment", 0, new String[])
    STORAGE = ("inventoryitems", "inventoryequipment", 1, new String[])
    CASHSHOP_EXPLORER = ("csitems", "csequipment", 2, new String[])
    CASHSHOP_CYGNUS = ("csitems", "csequipment", 3, new String[])
    CASHSHOP_ARAN = ("csitems", "csequipment", 4, new String[])
    HIRED_MERCHANT = ("hiredmerchitems", "hiredmerchequipment", 5, new String[])
    DUEY = ("dueyitems", "dueyequipment", 6, new String[])
    CASHSHOP_EVAN = ("csitems", "csequipment", 7, new String[])
    MTS = ("mtsitems", "mtsequipment", 8, new String[])
    MTS_TRANSFER = ("mtstransfer", "mtstransferequipment", 9, new String[])
    CASHSHOP_DB = ("csitems", "csequipment", 10, new String[])
    CASHSHOP_RESIST = ("csitems", "csequipment", 11, new String[])

    def getValue(self) -> int:
        return self.value

    def loadItems_hm(self, packageid: int, accountid: int) -> dict:
        items = {}
        query = ""
        query.append("SELECT * FROM `hiredmerchitems` LEFT JOIN `hiredmerchequipment` USING(`inventoryitemid`) WHERE `type` = ? AND `accountid` = ? ")
        ps = DatabaseConnection.getConnection().prepareStatement(query)
        ps.setInt(1, self.value)
        ps.setInt(2, accountid)
        rs = ps.executeQuery()
        while rs.next():
            mit = MapleInventoryType.getByType(rs.getByte("inventorytype"))
            if mit == (MapleInventoryType.EQUIP) || mit == (MapleInventoryType.EQUIPPED):
                equip = Equip(rs.getInt("itemid"), rs.getShort("position"), rs.getInt("uniqueid"), rs.getByte("flag"))
                equip.setQuantity(1)
                equip.setOwner(rs.getString("owner"))
                equip.setExpiration(rs.getLong("expiredate"))
                equip.setUpgradeSlots(rs.getByte("upgradeslots"))
                equip.setLevel(rs.getByte("level"))
                equip.setStr(rs.getShort("str"))
                equip.setDex(rs.getShort("dex"))
                equip.setInt(rs.getShort("int"))
                equip.setLuk(rs.getShort("luk"))
                equip.setHp(rs.getShort("hp"))
                equip.setMp(rs.getShort("mp"))
                equip.setWatk(rs.getShort("watk"))
                equip.setMatk(rs.getShort("matk"))
                equip.setWdef(rs.getShort("wdef"))
                equip.setMdef(rs.getShort("mdef"))
                equip.setAcc(rs.getShort("acc"))
                equip.setAvoid(rs.getShort("avoid"))
                equip.setHands(rs.getShort("hands"))
                equip.setSpeed(rs.getShort("speed"))
                equip.setJump(rs.getShort("jump"))
                equip.setViciousHammer(rs.getByte("ViciousHammer"))
                equip.setItemEXP(rs.getInt("itemEXP"))
                equip.setGMLog(rs.getString("GM_Log"))
                equip.setDurability(rs.getInt("durability"))
                equip.setEnhance(rs.getByte("enhance"))
                equip.setPotential1(rs.getShort("potential1"))
                equip.setPotential2(rs.getShort("potential2"))
                equip.setPotential3(rs.getShort("potential3"))
                equip.setHpR(rs.getShort("hpR"))
                equip.setMpR(rs.getShort("mpR"))
                equip.setGiftFrom(rs.getString("sender"))
                equip.setEquipLevel(rs.getByte("itemlevel"))
                equip.setEquipOnlyId(rs.getInt("equipOnlyId"))
                if (equip.getUniqueId() > -1 &&
                GameConstants.isEffectRing(rs.getInt("itemid")))
                    ring = MapleRing.loadFromDb(equip.getUniqueId(), mit == (MapleInventoryType.EQUIPPED))
                    if ring is not None:
                    equip.setRing(ring)
                items.put(Integer.valueOf(rs.getInt("inventoryitemid")), Pair(equip.copy(), mit))
                continue
            item = Item(rs.getInt("itemid"), rs.getShort("position"), rs.getShort("quantity"), rs.getByte("flag"))
            item.setUniqueId(rs.getInt("uniqueid"))
            item.setOwner(rs.getString("owner"))
            item.setExpiration(rs.getLong("expiredate"))
            item.setEquipOnlyId(rs.getInt("equipOnlyId"))
            item.setGMLog(rs.getString("GM_Log"))
            item.setGiftFrom(rs.getString("sender"))
            if GameConstants.isPet(item.getItemId()):
            if item.getUniqueId() > -1:
                pet = MaplePet.loadFromDb(item.getItemId(), item.getUniqueId(), item.getPosition())
                if pet is not None:
                item.setPet(pet)
            else:
                new_unique = MapleInventoryIdentifier.getInstance()
                item.setUniqueId(new_unique)
                item.setPet(MaplePet.createPet(item.getItemId(), new_unique))
            items.put(Integer.valueOf(rs.getInt("inventoryitemid")), Pair(item.copy(), mit))
        rs.close()
        ps.close()
        return items

    def loadItems(self, login: bool, id: int) -> dict:
        lulz = Arrays.asList(id)
        items = {}
        if lulz != self.arg:
        return items
        query = ""
        query.append("SELECT * FROM `")
        query.append(self.table)
        query.append("` LEFT JOIN `")
        query.append(self.table_equip)
        query.append("` USING(`inventoryitemid`) WHERE `type` = ?")
        for g in self.arg:
            query.append(" AND `")
            query.append(g)
            query.append("` = ?")
        if login:
            query.append(" AND `inventorytype` = ")
            query.append(MapleInventoryType.EQUIPPED.getType())
        ps = DatabaseConnection.getConnection().prepareStatement(query)
        ps.setInt(1, self.value)
        for i in range(lulz):
        ps.setInt(i + 2, (lulz.get(i)))
        rs = ps.executeQuery()
        while rs.next():
            mit = MapleInventoryType.getByType(rs.getByte("inventorytype"))
            if mit == (MapleInventoryType.EQUIP) || mit == (MapleInventoryType.EQUIPPED):
                equip = Equip(rs.getInt("itemid"), rs.getShort("position"), rs.getInt("uniqueid"), rs.getByte("flag"))
                if !login:
                    equip.setQuantity(1)
                    equip.setOwner(rs.getString("owner"))
                    equip.setExpiration(rs.getLong("expiredate"))
                    equip.setUpgradeSlots(rs.getByte("upgradeslots"))
                    equip.setLevel(rs.getByte("level"))
                    equip.setStr(rs.getShort("str"))
                    equip.setDex(rs.getShort("dex"))
                    equip.setInt(rs.getShort("int"))
                    equip.setLuk(rs.getShort("luk"))
                    equip.setHp(rs.getShort("hp"))
                    equip.setMp(rs.getShort("mp"))
                    equip.setWatk(rs.getShort("watk"))
                    equip.setMatk(rs.getShort("matk"))
                    equip.setWdef(rs.getShort("wdef"))
                    equip.setMdef(rs.getShort("mdef"))
                    equip.setAcc(rs.getShort("acc"))
                    equip.setAvoid(rs.getShort("avoid"))
                    equip.setHands(rs.getShort("hands"))
                    equip.setSpeed(rs.getShort("speed"))
                    equip.setJump(rs.getShort("jump"))
                    equip.setViciousHammer(rs.getByte("ViciousHammer"))
                    equip.setItemEXP(rs.getInt("itemEXP"))
                    equip.setGMLog(rs.getString("GM_Log"))
                    equip.setDurability(rs.getInt("durability"))
                    equip.setEnhance(rs.getByte("enhance"))
                    equip.setPotential1(rs.getShort("potential1"))
                    equip.setPotential2(rs.getShort("potential2"))
                    equip.setPotential3(rs.getShort("potential3"))
                    equip.setHpR(rs.getShort("hpR"))
                    equip.setMpR(rs.getShort("mpR"))
                    equip.setGiftFrom(rs.getString("sender"))
                    equip.setEquipLevel(rs.getByte("itemlevel"))
                    equip.setEquipOnlyId(rs.getInt("equipOnlyId"))
                    if (equip.getUniqueId() > -1 &&
                    GameConstants.isEffectRing(rs.getInt("itemid")))
                        ring = MapleRing.loadFromDb(equip.getUniqueId(), mit == (MapleInventoryType.EQUIPPED))
                        if ring is not None:
                        equip.setRing(ring)
                items.put(Integer.valueOf(rs.getInt("inventoryitemid")), Pair(equip.copy(), mit))
                continue
            item = Item(rs.getInt("itemid"), rs.getShort("position"), rs.getShort("quantity"), rs.getByte("flag"))
            item.setUniqueId(rs.getInt("uniqueid"))
            item.setOwner(rs.getString("owner"))
            item.setExpiration(rs.getLong("expiredate"))
            item.setEquipOnlyId(rs.getInt("equipOnlyId"))
            item.setGMLog(rs.getString("GM_Log"))
            item.setGiftFrom(rs.getString("sender"))
            if GameConstants.isPet(item.getItemId()):
            if item.getUniqueId() > -1:
                pet = MaplePet.loadFromDb(item.getItemId(), item.getUniqueId(), item.getPosition())
                if pet is not None:
                item.setPet(pet)
            else:
                new_unique = MapleInventoryIdentifier.getInstance()
                item.setUniqueId(new_unique)
                item.setPet(MaplePet.createPet(item.getItemId(), new_unique))
            items.put(Integer.valueOf(rs.getInt("inventoryitemid")), Pair(item.copy(), mit))
        rs.close()
        ps.close()
        return items

    def saveItems(self, items: list, id: int) -> None:
        con = DatabaseConnection.getConnection()
        saveItems(items, con, id)

    def saveItems(self, items: list, con: Any, id: int) -> None:
        lulz = Arrays.asList(id)
        if lulz != self.arg:
        return
        if items is None:
        return
        querySelectNeedDelete = ""
        querySelectNeedDelete.append("SELECT * FROM `")
        querySelectNeedDelete.append(self.table)
        querySelectNeedDelete.append("` WHERE `type` = ? AND (`")
        querySelectNeedDelete.append(self.arg.get(0))
        querySelectNeedDelete.append("` = ?")
        if self.arg > 1:
        for j in range(1, self.arg):
            querySelectNeedDelete.append(" OR `")
            querySelectNeedDelete.append(self.arg.get(j))
            querySelectNeedDelete.append("` = ?")
        querySelectNeedDelete.append(")")
        ps = con.prepareStatement(querySelectNeedDelete)
        ps.setInt(1, self.value)
        for i in range(lulz):
        ps.setInt(i + 2, (lulz.get(i)))
        rs = ps.executeQuery()
        equipOnlyIds = []
        checkItems = {}
        while rs.next():
            itemId = rs.getInt("itemId")
            equipOnlyId = rs.getInt("equipOnlyId")
            if equipOnlyId > 0:
            if (Integer.valueOf(equipOnlyId in checkItems)):
                if (checkItems.get(Integer.valueOf(equipOnlyId))) == itemId:
                equipOnlyIds.add(Integer.valueOf(equipOnlyId))
            else:
                checkItems.put(Integer.valueOf(equipOnlyId), Integer.valueOf(itemId))
            find = False
            for item in items:
                if (item.getLeft()).getEquipOnlyId() == equipOnlyId && (item.getLeft()).getItemId() == itemId:
                    find = True
                    break
            if !find || (Integer.valueOf(equipOnlyId in equipOnlyIds)):
                queryDelete = ""
                queryDelete.append("DELETE FROM `")
                queryDelete.append(self.table)
                queryDelete.append("` WHERE `type` = ? AND `itemId` = " + itemId + " AND `equipOnlyId` = " + equipOnlyId + " AND (`")
                queryDelete.append(self.arg.get(0))
                queryDelete.append("` = ?")
                if self.arg > 1:
                for j in range(1, self.arg):
                    queryDelete.append(" OR `")
                    queryDelete.append(self.arg.get(j))
                    queryDelete.append("` = ?")
                queryDelete.append(")")
                ps2 = con.prepareStatement(queryDelete)
                try:
                    ps2.setInt(1, self.value)
                    for j in range(lulz):
                    ps2.setInt(j + 2, (lulz.get(j)))
                    ps2.executeUpdate()
                except SQLException as ex:
                    print("Delete Item Error: " + itemId + " equipOnlyId : " + equipOnlyId + " " + ex)
                ps2.close()
        checkItems.clear()
        equipOnlyIds.clear()
        rs.close()
        ps.close()
        querySelectNeedInsert = ""
        querySelectNeedInsert.append("SELECT * FROM `")
        querySelectNeedInsert.append(self.table)
        querySelectNeedInsert.append("` WHERE `type` = ? AND `itemId` = ? AND `equipOnlyId` = ? AND (`")
        querySelectNeedInsert.append(self.arg.get(0))
        querySelectNeedInsert.append("` = ?")
        if self.arg > 1:
        for j in range(1, self.arg):
            querySelectNeedInsert.append(" OR `")
            querySelectNeedInsert.append(self.arg.get(j))
            querySelectNeedInsert.append("` = ?")
        querySelectNeedInsert.append(") LIMIT 1")
        ps = con.prepareStatement(querySelectNeedInsert)
        for item in items:
            itemId = (item.getLeft()).getItemId()
            equipOnlyId = (item.getLeft()).getEquipOnlyId()
            ps.setInt(1, self.value)
            ps.setInt(2, itemId)
            ps.setInt(3, equipOnlyId)
            for j in range(lulz):
            ps.setInt(j + 4, (lulz.get(j)))
            rs = ps.executeQuery()
            if rs.next():
                queryItemUpdate = ""
                queryItemUpdate.append(self.table)
                queryItemUpdate.append("` SET ")
                queryItemUpdate.append("`itemid` = ?, `inventorytype` = ?, `position` = ?, `quantity` = ?, `owner` = ?, `GM_Log` = ?, `uniqueid` = ?, `expiredate` = ?, `flag` = ?, `type` = ?, `sender` = ?  WHERE `equipOnlyId` = ? and (`")
                queryItemUpdate.append(self.arg.get(0))
                queryItemUpdate.append("` = ?")
                if self.arg > 1:
                for k in range(1, self.arg):
                    queryItemUpdate.append(" OR `")
                    queryItemUpdate.append(self.arg.get(k))
                    queryItemUpdate.append("` = ?")
                queryItemUpdate.append(")")
                ps2 = con.prepareStatement(queryItemUpdate)
                try:
                    itemUpdate = item.getLeft()
                    mit = item.getRight()
                    try:
                        ps2.setInt(1, itemUpdate.getItemId())
                        ps2.setInt(2, mit.getType())
                        ps2.setInt(3, itemUpdate.getPosition())
                        ps2.setInt(4, itemUpdate.getQuantity())
                        ps2.setString(5, itemUpdate.getOwner())
                        ps2.setString(6, itemUpdate.getGMLog())
                        ps2.setInt(7, itemUpdate.getUniqueId())
                        ps2.setLong(8, itemUpdate.getExpiration())
                        ps2.setByte(9, itemUpdate.getFlag())
                        ps2.setByte(10, self.value)
                        ps2.setString(11, itemUpdate.getGiftFrom())
                        ps2.setInt(12, itemUpdate.getEquipOnlyId())
                        for k in range(lulz):
                        ps2.setInt(13 + k, (lulz.get(k)))
                        ps2.executeUpdate()
                        ps2.close()
                    except SQLException as ex:
                        print("GMLOG : " + itemUpdate.getGMLog() + "1 Table_equip : " + self.table + " " + ex)
                    if mit == (MapleInventoryType.EQUIP) || mit == (MapleInventoryType.EQUIPPED):
                        pse = con.prepareStatement("UPDATE `" + self.table_equip + "` SET `upgradeslots` = ?, `level` = ?, `str` = ?, `dex` = ?, `int` = ?, `luk` = ?, `hp` = ?, `mp` = ?, `watk` = ?, `matk` = ?, `wdef` = ?, `mdef` = ?, `acc` = ?, `avoid` = ?, `hands` = ?, `speed` = ?, `jump` = ?, `ViciousHammer` = ?, `itemEXP` = ?, `durability` = ?, `enhance` = ?, `potential1` = ?, `potential2` = ?, `potential3` = ?, `hpR` = ?, `mpR` = ?, `itemlevel` = ? WHERE `equipOnlyId` = ?")
                        equip = itemUpdate
                        pse.setInt(1, equip.getUpgradeSlots())
                        pse.setInt(2, equip.getLevel())
                        pse.setInt(3, equip.getStr())
                        pse.setInt(4, equip.getDex())
                        pse.setInt(5, equip.getInt())
                        pse.setInt(6, equip.getLuk())
                        pse.setInt(7, equip.getHp())
                        pse.setInt(8, equip.getMp())
                        pse.setInt(9, equip.getWatk())
                        pse.setInt(10, equip.getMatk())
                        pse.setInt(11, equip.getWdef())
                        pse.setInt(12, equip.getMdef())
                        pse.setInt(13, equip.getAcc())
                        pse.setInt(14, equip.getAvoid())
                        pse.setInt(15, equip.getHands())
                        pse.setInt(16, equip.getSpeed())
                        pse.setInt(17, equip.getJump())
                        pse.setInt(18, equip.getViciousHammer())
                        pse.setInt(19, equip.getItemEXP())
                        pse.setInt(20, equip.getDurability())
                        pse.setByte(21, equip.getEnhance())
                        pse.setInt(22, equip.getPotential1())
                        pse.setInt(23, equip.getPotential2())
                        pse.setInt(24, equip.getPotential3())
                        pse.setInt(25, equip.getHpR())
                        pse.setInt(26, equip.getMpR())
                        pse.setByte(27, equip.getEquipLevel())
                        pse.setInt(28, equip.getEquipOnlyId())
                        pse.executeUpdate()
                        pse.close()
                except Exception:
                    print("2 table_equip: " + self.table_equip + " " + ex)
            else:
                queryItemInsert = ""
                queryItemInsert.append(self.table)
                queryItemInsert.append("` (")
                for g in self.arg:
                    queryItemInsert.append(g)
                    queryItemInsert.append(", ")
                queryItemInsert.append("itemid, inventorytype, position, quantity, owner, GM_Log, uniqueid, expiredate, flag, `type`, sender, `equipOnlyId` ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ")
                for g in self.arg:
                queryItemInsert.append(", ?")
                queryItemInsert.append(")")
                ps3 = con.prepareStatement(queryItemInsert)
                itemTmp = item.getLeft()
                mit = item.getRight()
                try:
                    k = 1
                    = 0
                    while k < lulz:
                    ps3.setInt(k + 1, (lulz.get(k)))
                    ps3.setInt(k + 1, itemTmp.getItemId())
                    ps3.setInt(k + 2, mit.getType())
                    ps3.setInt(k + 3, itemTmp.getPosition())
                    ps3.setInt(k + 4, itemTmp.getQuantity())
                    ps3.setString(k + 5, itemTmp.getOwner())
                    ps3.setString(k + 6, itemTmp.getGMLog())
                    ps3.setInt(k + 7, itemTmp.getUniqueId())
                    ps3.setLong(k + 8, itemTmp.getExpiration())
                    ps3.setByte(k + 9, itemTmp.getFlag())
                    ps3.setByte(k + 10, self.value)
                    ps3.setString(k + 11, itemTmp.getGiftFrom())
                    ps3.setInt(k + 12, itemTmp.getEquipOnlyId())
                    ps3.executeUpdate()
                    ps3.close()
                    ps3 = con.prepareStatement("select @@identity as id")
                    rs2 = ps3.executeQuery()
                    newIndex = 0
                    if rs2.next():
                    newIndex = rs2.getInt(1)
                    rs2.close()
                    onlyID = 0
                    if itemTmp.getEquipOnlyId() == -1:
                        onlyID = newIndex
                        queryItemUpdateOnlyId = ""
                        queryItemUpdateOnlyId.append(self.table)
                        queryItemUpdateOnlyId.append("` set `equipOnlyId` = ? WHERE `inventoryitemid` = ?")
                        ps2 = con.prepareStatement(queryItemUpdateOnlyId)
                        ps2.setInt(1, onlyID)
                        ps2.setInt(2, onlyID)
                        ps2.executeUpdate()
                        ps2.close()
                        itemTmp.setEquipOnlyId(onlyID)
                    else:
                        onlyID = itemTmp.getEquipOnlyId()
                    ps3.close()
                    if mit == (MapleInventoryType.EQUIP) || mit == (MapleInventoryType.EQUIPPED):
                        if onlyID == 0:
                        raise RuntimeError("Inserting item failed.")
                        try:
                            pse = con.prepareStatement("INSERT INTO " + self.table_equip + " VALUES (DEFAULT, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
                            pse.setInt(1, newIndex)
                            equip = itemTmp
                            pse.setInt(2, equip.getUpgradeSlots())
                            pse.setInt(3, equip.getLevel())
                            pse.setInt(4, equip.getStr())
                            pse.setInt(5, equip.getDex())
                            pse.setInt(6, equip.getInt())
                            pse.setInt(7, equip.getLuk())
                            pse.setInt(8, equip.getHp())
                            pse.setInt(9, equip.getMp())
                            pse.setInt(10, equip.getWatk())
                            pse.setInt(11, equip.getMatk())
                            pse.setInt(12, equip.getWdef())
                            pse.setInt(13, equip.getMdef())
                            pse.setInt(14, equip.getAcc())
                            pse.setInt(15, equip.getAvoid())
                            pse.setInt(16, equip.getHands())
                            pse.setInt(17, equip.getSpeed())
                            pse.setInt(18, equip.getJump())
                            pse.setInt(19, equip.getViciousHammer())
                            pse.setInt(20, equip.getItemEXP())
                            pse.setInt(21, equip.getDurability())
                            pse.setByte(22, equip.getEnhance())
                            pse.setInt(23, equip.getPotential1())
                            pse.setInt(24, equip.getPotential2())
                            pse.setInt(25, equip.getPotential3())
                            pse.setInt(26, equip.getHpR())
                            pse.setInt(27, equip.getMpR())
                            pse.setByte(28, equip.getEquipLevel())
                            pse.setInt(29, onlyID)
                            pse.executeUpdate()
                            pse.close()
                        except SQLException as ex:
                            ex.printStackTrace()
                            print("INSERT NEW E ERROR : " + itemTmp.getItemId() + " EquipOnlyId : " + itemTmp.getEquipOnlyId() + " " + ex)
                except SQLException as ex:
                    ex.printStackTrace()
                    print("INSERT NEW ITEM ERROR : " + itemTmp.getItemId() + " EquipOnlyId : " + itemTmp.getEquipOnlyId() + " " + ex)
            rs.close()
        ps.close()

