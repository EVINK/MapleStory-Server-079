"""
MapleShopItem - 从Java源文件转换而来
对应Java源文件: server/MapleShopItem.java
包路径: server
"""


class MapleShopItem:
    """
    类 MapleShopItem - 从Java类转换
    """

    def __init__(self, buyable: int, itemId: int, price: int):
        """初始化 MapleShopItem"""
        self.buyable = None
        self.itemId = None
        self.price = None


    def getBuyable(self) -> int:
        """方法 getBuyable"""
        return getattr(self, 'buyable', 0)

    def getItemId(self) -> int:
        """方法 getItemId"""
        return getattr(self, 'item_id', 0)

    def getPrice(self) -> int:
        """方法 getPrice"""
        return getattr(self, 'price', 0)

