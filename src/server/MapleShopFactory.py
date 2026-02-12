"""
MapleShopFactory - Converted from Java source
Original: server/MapleShopFactory.java
Package: server
"""

from typing import Dict
from typing import Optional, Any


class MapleShopFactory:
    """
    Class MapleShopFactory
    """

    def __init__(self):
        self.shops = None
        self.npcShops = None
        self.shops = {}
        self.npcShops = {}

    # Static initializer
    # instance = MapleShopFactory()


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def clear(self) -> None:
        self.shops.clear()
        self.npcShops.clear()

    def getShop(self, shopId: int) -> Any:
        if (shopId in self.shops):
            return self.shops.get(shopId)
        return self.loadShop(shopId, True)

    def getShopForNPC(self, npcId: int) -> Any:
        if (npcId in self.npcShops):
            return self.npcShops.get(npcId)
        return self.loadShop(npcId, False)

    def loadShop(self, id: int, isShopId: bool) -> Any:
        ret = MapleShop.createFromDB(id, isShopId)
        if ret is not None:
            self.shops.put(ret.getId(), ret)
            self.npcShops.put(ret.getNpcId(), ret)
        elif isShopId:
            self.shops.put(id, None)
        else:
            self.npcShops.put(id, None)
        return ret

