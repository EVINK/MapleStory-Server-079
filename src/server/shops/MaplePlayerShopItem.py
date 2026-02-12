"""
MaplePlayerShopItem - Converted from Java source
Original: server/shops/MaplePlayerShopItem.java
Package: server.shops
"""

from typing import Optional, Any

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes


class MaplePlayerShopItem:
    """
    Class MaplePlayerShopItem
    """

    def __init__(self, item: Any, bundles: int, price: int, flag: int):
        self.item = None
        self.bundles = 0
        self.price = 0
        self.flag = 0
        self.item = item
        self.bundles = bundles
        self.price = price
        self.flag = flag


