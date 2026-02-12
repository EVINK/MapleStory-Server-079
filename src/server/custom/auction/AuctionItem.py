"""
AuctionItem - Converted from Java source
Original: server/custom/auction/AuctionItem.java
Package: server.custom.auction
"""

from typing import Optional, Any

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes


class AuctionItem:
    """
    Class AuctionItem
    """

    def __init__(self):
        self.id = 0
        self.characterid = 0
        self.characterName = ""
        self.auctionState = None
        self.buyer = 0
        self.buyerName = ""
        self.price = 0
        self.item = None
        self.quantity = 0


    def getId(self) -> int:
        return self.id

    def setId(self, id: int) -> None:
        self.id = id

    def getItem(self) -> Any:
        return self.item

    def setItem(self, item: Any) -> None:
        self.item = item

    def getPrice(self) -> int:
        return self.price

    def setPrice(self, price: int) -> None:
        self.price = price

    def getQuantity(self) -> int:
        return self.quantity

    def setQuantity(self, quantity: int) -> None:
        self.quantity = quantity

    def getAuctionState(self) -> Any:
        return self.auctionState

    def setAuctionState(self, auctionState: Any) -> None:
        self.auctionState = auctionState

    def getCharacterid(self) -> int:
        return self.characterid

    def setCharacterid(self, characterid: int) -> None:
        self.characterid = characterid

    def getBuyer(self) -> int:
        return self.buyer

    def setBuyer(self, buyer: int) -> None:
        self.buyer = buyer

    def getCharacterName(self) -> str:
        return self.characterName

    def setCharacterName(self, characterName: str) -> None:
        self.characterName = characterName

    def getBuyerName(self) -> str:
        return self.buyerName

    def setBuyerName(self, buyerName: str) -> None:
        self.buyerName = buyerName

