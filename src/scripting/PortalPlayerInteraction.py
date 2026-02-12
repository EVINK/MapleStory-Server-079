"""
PortalPlayerInteraction - Converted from Java source
Original: scripting/PortalPlayerInteraction.java
Package: scripting
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes


class PortalPlayerInteraction(AbstractPlayerInteraction):
    """
    Class PortalPlayerInteraction
    Extends: AbstractPlayerInteraction
    """

    def __init__(self, c: Any, portal: Any):
        self.portal = None
        super(c)
        self.portal = portal


    def getPortal(self) -> Any:
        return self.portal

    def inFreeMarket(self) -> None:
        if self.getPlayer().getLevel() >= 10:
            self.saveLocation("FREE_MARKET")
            self.playPortalSE()
            self.warp(910000000, "st00")
        else:
            self.playerMessage(5, "你需要10级才可以进入自由市场")

    def spawnMonster(self, id: int) -> None:
        self.spawnMonster(id, 1, self.portal.getPosition())

    def spawnMonster_id_qty(self, id: int, qty: int) -> None:
        self.spawnMonster(id, qty, self.portal.getPosition())

