"""
MerchItemPackage - Converted from Java source
Original: server/MerchItemPackage.java
Package: server
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.inventory.IItem import *  # TODO: import specific classes


class MerchItemPackage:
    """
    Class MerchItemPackage
    """

    def __init__(self):
        self.sentTime = 0
        self.mesos = 0
        self.packageid = 0
        self.items = []
        self.mesos = 0
        self.items = []


    def setItems(self, items: list) -> None:
        self.items = items

    def getItems(self) -> list:
        return self.items

    def setSentTime(self, sentTime: int) -> None:
        self.sentTime = sentTime

    def getSentTime(self) -> int:
        return self.sentTime

    def getMesos(self) -> int:
        return self.mesos

    def setMesos(self, set: int) -> None:
        self.mesos = set

    def getPackageid(self) -> int:
        return self.packageid

    def setPackageid(self, packageid: int) -> None:
        self.packageid = packageid

