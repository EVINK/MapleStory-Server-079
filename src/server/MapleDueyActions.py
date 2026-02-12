"""
MapleDueyActions - Converted from Java source
Original: server/MapleDueyActions.java
Package: server
"""

from typing import Optional, Any

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes


class MapleDueyActions:
    """
    Class MapleDueyActions
    """

    def __init__(self, pId: int, item: Any):
        self.sender = ""
        self.item = None
        self.mesos = 0
        self.quantity = 0
        self.sentTime = 0
        self.packageId = 0
        self.sender = None
        self.item = None
        self.mesos = 0
        self.quantity = 1
        self.packageId = 0
        self.item = item
        self.quantity = item.getQuantity()
        self.packageId = pId


    def getSender(self) -> str:
        return self.sender

    def setSender(self, name: str) -> None:
        self.sender = name

    def getItem(self) -> Any:
        return self.item

    def getMesos(self) -> int:
        return self.mesos

    def setMesos(self, set: int) -> None:
        self.mesos = set

    def getQuantity(self) -> int:
        return self.quantity

    def getPackageId(self) -> int:
        return self.packageId

    def setSentTime(self, sentTime: int) -> None:
        self.sentTime = sentTime

    def getSentTime(self) -> int:
        return self.sentTime

