"""
MapleShopItem - Converted from Java source
Original: server/MapleShopItem.java
Package: server
"""

from typing import Optional, Any


class MapleShopItem:
    """
    Class MapleShopItem
    """

    def __init__(self, buyable: int, itemId: int, price: int):
        self.buyable = None
        self.itemId = None
        self.price = None
        self.buyable = buyable
        self.itemId = itemId
        self.price = price


    def getBuyable(self) -> int:
        return self.buyable

    def getItemId(self) -> int:
        return self.itemId

    def getPrice(self) -> int:
        return self.price

