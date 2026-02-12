"""
AuctionPoint1 - Converted from Java source
Original: server/custom/auction1/AuctionPoint1.java
Package: server.custom.auction1
"""

from typing import Optional, Any


class AuctionPoint1:
    """
    Class AuctionPoint1
    """

    def __init__(self):
        self.characterid = 0
        self.point1 = 0
        self.point1_sell = 0
        self.point1_buy = 0


    def getCharacterid(self) -> int:
        return self.characterid

    def setCharacterid(self, characterid: int) -> None:
        self.characterid = characterid

    def getPoint1(self) -> int:
        return self.point1

    def setPoint(self, point: int) -> None:
        self.point1 = self.point1

    def getPoint1_sell(self) -> int:
        return self.point1_sell

    def setPoint1_sell(self, point1_sell: int) -> None:
        self.point1_sell = point1_sell

    def getPoint1_buy(self) -> int:
        return self.point1_buy

    def setPoint1_buy(self, point1_buy: int) -> None:
        self.point1_buy = point1_buy

