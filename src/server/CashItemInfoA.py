"""
CashItemInfoA - Converted from Java source
Original: server/CashItemInfoA.java
Package: server
"""

from typing import Optional, Any

# Internal module imports
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes


class CashItemInfoA:
    """
    Class CashItemInfoA
    """

    def __init__(self, SN: int, itemId: int, count: int, price: int, period: int, gender: int, onSale: bool):
        self.SN = None
        self.itemId = None
        self.count = None
        self.price = None
        self.period = None
        self.gender = None
        self.onSale = None
        self.SN = SN
        self.itemId = itemId
        self.count = count
        self.price = price
        self.period = period
        self.gender = gender
        self.onSale = onSale


    def getInventoryType(self, itemId: int) -> Any:
        type = (byte)(itemId / 1000000)
        if type < 1 || type > 5:
            return MapleInventoryType.UNDEFINED
        return MapleInventoryType.getByType(type)

    def getSN(self) -> int:
        return self.SN

    def getId(self) -> int:
        return self.itemId

    def genderEquals(self, g: int) -> bool:
        return g == self.gender || self.gender == 2

    def getItemId(self) -> int:
        return self.itemId

    def getCount(self) -> int:
        return self.count

    def getPrice(self) -> int:
        return self.price

    def getPeriod(self) -> int:
        return self.period

    def getGender(self) -> int:
        return self.gender

    def onSale(self) -> bool:
        return self.onSale

    def getItemId_i(self, i: int) -> int:
        return self.itemId

