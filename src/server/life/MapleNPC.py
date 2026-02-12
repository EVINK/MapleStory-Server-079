"""
MapleNPC - Converted from Java source
Original: server/life/MapleNPC.java
Package: server.life
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from server.MapleShopFactory import *  # TODO: import specific classes
# from server.maps.MapleMapObjectType import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleNPC(AbstractLoadedMapleLife):
    """
    Class MapleNPC
    Extends: AbstractLoadedMapleLife
    """

    def __init__(self, id: int, name: str):
        self.name = ""
        self.custom = False
        super(id)
        self.name = "MISSINGNO"
        self.custom = False
        self.name = name


    def hasShop(self) -> bool:
        return MapleShopFactory.getInstance().getShopForNPC(self.getId()) is not None

    def sendShop(self, c: Any) -> None:
        if c.getPlayer().isGM():
            c.getPlayer().dropMessage("您已经建立与商店npc[" + self.getId() + "]的连接")
        MapleShopFactory.getInstance().getShopForNPC(self.getId()).sendShop(c)

    def sendSpawnData(self, client: Any) -> None:
        if self.getId() < 9901000:
            client.getSession().write(MaplePacketCreator.spawnNPC(this, True))
            client.getSession().write(MaplePacketCreator.spawnNPCRequestController(this, True))

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.removeNPC(self.getObjectId()))

    def getType(self) -> Any:
        return MapleMapObjectType.NPC

    def getName(self) -> str:
        return self.name

    def setName(self, n: str) -> None:
        self.name = n

    def isCustom(self) -> bool:
        return self.custom

    def setCustom(self, custom: bool) -> None:
        self.custom = custom

