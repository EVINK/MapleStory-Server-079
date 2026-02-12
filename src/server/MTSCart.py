"""
MTSCart - Converted from Java source
Original: server/MTSCart.java
Package: server
"""

from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import Iterator
from typing import List
from typing import Optional, Any
import pymysql

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes
# from client.inventory.ItemLoader import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


class MTSCart:
    """
    Class MTSCart
    Implements: Serializable
    """

    serialVersionUID = 231541893513373578

    def __init__(self, characterId: int):
        self.characterId = None
        self.tab = 0
        self.type = 0
        self.page = 0
        self.transfer = None
        self.cart = None
        self.notYetSold = None
        self.owedNX = 0
        self.tab = 1
        self.type = 0
        self.page = 0
        self.transfer = []
        self.cart = []
        self.notYetSold = []
        self.owedNX = 0
        self.characterId = characterId
        for item in ItemLoader.MTS_TRANSFER.loadItems(False, characterId).values():
            self.transfer.add(item.getLeft())
        self.loadCart()
        self.loadNotYetSold()


    def getInventory(self) -> list:
        return self.transfer

    def addToInventory(self, item: Any) -> None:
        self.transfer.add(item)

    def removeFromInventory(self, item: Any) -> None:
        self.transfer.remove(item)

    def getCart(self) -> list:
        return self.cart

    def addToCart(self, car: int) -> bool:
        if !(car in self.cart):
            self.cart.add(car)
            return True
        return False

    def removeFromCart(self, car: int) -> None:
        for i in range(self.cart):
            if self.cart.get(i) == car:
                self.cart.remove(i)

    def getNotYetSold(self) -> list:
        return self.notYetSold

    def addToNotYetSold(self, car: int) -> None:
        self.notYetSold.add(car)

    def removeFromNotYetSold(self, car: int) -> None:
        for i in range(self.notYetSold):
            if self.notYetSold.get(i) == car:
                self.notYetSold.remove(i)

    def getSetOwedNX(self) -> int:
        on = self.owedNX
        self.owedNX = 0
        return on

    def increaseOwedNX(self, newNX: int) -> None:
        self.owedNX += newNX

    def save(self) -> None:
        itemsWithType = new ArrayList<Pair<IItem, MapleInventoryType>>()
        for item in self.getInventory():
            itemsWithType.add(new Pair<IItem, MapleInventoryType>(item, GameConstants.getInventoryType(item.getItemId())))
        ItemLoader.MTS_TRANSFER.saveItems(itemsWithType, self.characterId)
        con = DatabaseConnection.getConnection()
        ps = con.prepareStatement("DELETE FROM mts_cart WHERE characterid = ?")
        ps.setInt(1, self.characterId)
        ps.execute()
        ps.close()
        ps = con.prepareStatement("INSERT INTO mts_cart VALUES(DEFAULT, ?, ?)")
        ps.setInt(1, self.characterId)
        for i in self.cart:
            ps.setInt(2, i)
            ps.executeUpdate()
        if self.owedNX > 0:
            ps.setInt(2, -self.owedNX)
            ps.executeUpdate()
        ps.close()

    def loadCart(self) -> None:
        ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM mts_cart WHERE characterid = ?")
        ps.setInt(1, self.characterId)
        rs = ps.executeQuery()
        while rs.next():
            iId = rs.getInt("itemid")
            if iId < 0:
                self.owedNX -= iId
            else:
                if !MTSStorage.getInstance().check(iId):
                    continue
                self.cart.add(iId)
        rs.close()
        ps.close()

    def loadNotYetSold(self) -> None:
        ps = DatabaseConnection.getConnection().prepareStatement("SELECT * FROM mts_items WHERE characterid = ?")
        ps.setInt(1, self.characterId)
        rs = ps.executeQuery()
        while rs.next():
            pId = rs.getInt("id")
            if MTSStorage.getInstance().check(pId):
                self.notYetSold.add(pId)
        rs.close()
        ps.close()

    def changeInfo(self, tab: int, type: int, page: int) -> None:
        self.tab = tab
        self.type = type
        self.page = page

    def getTab(self) -> int:
        return self.tab

    def getType(self) -> int:
        return self.type

    def getPage(self) -> int:
        return self.page

