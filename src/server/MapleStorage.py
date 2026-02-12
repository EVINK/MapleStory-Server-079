"""
MapleStorage - Converted from Java source
Original: server/MapleStorage.java
Package: server
"""

from enum import Enum
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Dict
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from database.DatabaseException import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MapleStorage:
    """
    Class MapleStorage
    Implements: Serializable
    """

    serialVersionUID = 9179541993413738569

    def __init__(self, id: int, slots: int, meso: int, accountId: int):
        self.id = None
        self.accountId = None
        self.items = None
        self.meso = 0
        self.slots = 0
        self.changed = False
        self.typeItems = None
        self.changed = False
        self.typeItems = new EnumMap<MapleInventoryType, List<IItem>>(MapleInventoryType.class)
        self.id = id
        self.slots = slots
        self.items = []
        self.meso = meso
        self.accountId = accountId


    def create(self, id: int) -> int:
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("INSERT INTO storages (accountid, slots, meso) VALUES (?, ?, ?)", 1)
        ps.setInt(1, id)
        ps.setInt(2, 4)
        ps.setInt(3, 0)
        ps.executeUpdate()
        rs = ps.getGeneratedKeys()
        if rs.next():
            storageid = rs.getInt(1)
            ps.close()
            rs.close()
            return storageid
        ps.close()
        rs.close()
        raise DatabaseException("Inserting char failed.")

    def loadStorage(self, id: int) -> Any:
        ret = None
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("SELECT * FROM storages WHERE accountid = ?")
            ps.setInt(1, id)
            rs = ps.executeQuery()
            if rs.next():
                storeId = rs.getInt("storageid")
                ret = MapleStorage(storeId, rs.getByte("slots"), rs.getInt("meso"), id)
                rs.close()
                ps.close()
                for mit in ItemLoader.STORAGE.loadItems(False, id).values():
                    ret.items.add(mit.getLeft())
            else:
                storeId = create(id)
                ret = MapleStorage(storeId, 4, 0, id)
                rs.close()
                ps.close()
        except Exception as ex:
            print("Error loading storage" + ex)
        return ret

    def saveToDB(self) -> None:
        if not self.changed:
            return
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("UPDATE storages SET slots = ?, meso = ? WHERE storageid = ?")
            ps.setInt(1, self.slots)
            ps.setInt(2, self.meso)
            ps.setInt(3, self.id)
            ps.executeUpdate()
            ps.close()
            listing = new ArrayList<Pair<IItem, MapleInventoryType>>()
            for item in self.items:
                listing.add(new Pair<IItem, MapleInventoryType>(item, GameConstants.getInventoryType(item.getItemId())))
            ItemLoader.STORAGE.saveItems(listing, self.accountId)
        except Exception as ex:
            print("Error saving storage" + ex)

    def takeOut(self, slot: int) -> Any:
        if slot >= self.items or slot < 0:
            return None
        self.changed = True
        ret = self.items.remove(slot)
        type = GameConstants.getInventoryType(ret.getItemId())
        self.typeItems.put(type, []))
        return ret

    def store(self, item: Any) -> None:
        self.changed = True
        self.items.add(item)
        type = GameConstants.getInventoryType(item.getItemId())
        self.typeItems.put(type, []))

    def getItems(self) -> list:
        return Collections.unmodifiableList((List<? extends IItem>)self.items)

    def filterItems(self, type: Any) -> list:
        ret = []
        for item in self.items:
            if GameConstants.getInventoryType(item.getItemId()) == type:
                ret.add(item)
        return ret

    def getSlot(self, type: Any, slot: int) -> int:
        ret = 0
        it = self.typeItems.get(type)
        if slot >= it or slot < 0:
            return -1
        for item in self.items:
            if item == it.get(slot):
                return ret
            ret += 1
        return -1

    def sendStorage(self, c: Any, npcId: int) -> None:
        Collections.sort(self.items, new Comparator<IItem>()
            public int compare(final IItem o1, final IItem o2)
                if GameConstants.getInventoryType(o1.getItemId()).getType() < GameConstants.getInventoryType(o2.getItemId()).getType():
                    return -1
                if GameConstants.getInventoryType(o1.getItemId()) == GameConstants.getInventoryType(o2.getItemId()):
                    return 0
                return 1
        for type in MapleInventoryType.values():
            self.typeItems.put(type, [])
        c.getSession().write(MaplePacketCreator.getStorage(npcId, self.slots, self.items, self.meso))

    def compare(self, o1: Any, o2: Any) -> int:
        if GameConstants.getInventoryType(o1.getItemId()).getType() < GameConstants.getInventoryType(o2.getItemId()).getType():
            return -1
        if GameConstants.getInventoryType(o1.getItemId()) == GameConstants.getInventoryType(o2.getItemId()):
            return 0
        return 1

    def sendStored(self, c: Any, type: Any) -> None:
        c.getSession().write(MaplePacketCreator.storeStorage(self.slots, type, self.typeItems.get(type)))

    def sendTakenOut(self, c: Any, type: Any) -> None:
        c.getSession().write(MaplePacketCreator.takeOutStorage(self.slots, type, self.typeItems.get(type)))

    def getMeso(self) -> int:
        return self.meso

    def findById(self, itemId: int) -> Any:
        for item in self.items:
            if item.getItemId() == itemId:
                return item
        return None

    def setMeso(self, meso: int) -> None:
        if meso < 0:
            return
        self.changed = True
        self.meso = meso

    def sendMeso(self, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.mesoStorage(self.slots, self.meso))

    def isFull(self) -> bool:
        return self.items >= self.slots

    def getSlots(self) -> int:
        return self.slots

    def increaseSlots(self, gain: int) -> None:
        self.changed = True
        self.slots += gain

    def setSlots(self, set: int) -> None:
        self.changed = True
        self.slots = set

    def close(self) -> None:
        self.typeItems.clear()

    def listByEquipOnlyId(self, equipOnlyId: int) -> list:
        ret = []
        for item in self.items:
            if item.getEquipOnlyId() > 0 and item.getEquipOnlyId() == equipOnlyId:
                ret.add(item)
        if ret > 1:
            Collections.sort(ret)
        return ret

