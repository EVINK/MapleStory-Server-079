"""
AuctionPoint - Converted from Java source
Original: server/custom/auction/AuctionPoint.java
Package: server.custom.auction
"""

from typing import Optional, Any


class AuctionPoint:
    """
    Class AuctionPoint
    """

    def __init__(self):
        self.characterid = 0
        self.point = 0
        self.point_sell = 0
        self.point_buy = 0


    def getCharacterid(self) -> int:
        return self.characterid

    def setCharacterid(self, characterid: int) -> None:
        self.characterid = characterid

    def getPoint(self) -> int:
        return self.point

    def setPoint(self, point: int) -> None:
        self.point = point

    def getPoint_sell(self) -> int:
        return self.point_sell

    def setPoint_sell(self, point_sell: int) -> None:
        self.point_sell = point_sell

    def getPoint_buy(self) -> int:
        return self.point_buy

    def setPoint_buy(self, point_buy: int) -> None:
        self.point_buy = point_buy

