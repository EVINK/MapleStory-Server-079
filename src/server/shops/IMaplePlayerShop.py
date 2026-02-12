"""
IMaplePlayerShop - Converted from Java source
Original: server/shops/IMaplePlayerShop.java
Package: server.shops
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from tools.Pair import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class IMaplePlayerShop(ABC):
    """Interface IMaplePlayerShop"""

    @abstractmethod
    def getOwnerName(self) -> str:
        pass

    @abstractmethod
    def getDescription(self) -> str:
        pass

    @abstractmethod
    def getVisitors(self) -> list:
        pass

    @abstractmethod
    def getItems(self) -> list:
        pass

    @abstractmethod
    def isOpen(self) -> bool:
        pass

    @abstractmethod
    def removeItem(self, p0: int) -> bool:
        pass

    @abstractmethod
    def isOwner(self, p0: Any) -> bool:
        pass

    @abstractmethod
    def getShopType(self) -> int:
        pass

    @abstractmethod
    def getVisitorSlot(self, p0: Any) -> int:
        pass

    @abstractmethod
    def getFreeSlot(self) -> int:
        pass

    @abstractmethod
    def getItemId(self) -> int:
        pass

    @abstractmethod
    def getMeso(self) -> int:
        pass

    @abstractmethod
    def getOwnerId(self) -> int:
        pass

    @abstractmethod
    def getOwnerAccId(self) -> int:
        pass

    @abstractmethod
    def setOpen(self, p0: bool) -> None:
        pass

    @abstractmethod
    def setMeso(self, p0: int) -> None:
        pass

    @abstractmethod
    def addItem(self, p0: Any) -> None:
        pass

    @abstractmethod
    def removeFromSlot(self, p0: int) -> None:
        pass

    @abstractmethod
    def broadcastToVisitors(self, p0: Any) -> None:
        pass

    @abstractmethod
    def addVisitor(self, p0: Any) -> None:
        pass

    @abstractmethod
    def removeVisitor(self, p0: Any) -> None:
        pass

    @abstractmethod
    def removeAllVisitors(self, p0: int, p1: int) -> None:
        pass

    @abstractmethod
    def buy(self, p0: Any, p1: int, p2: int) -> None:
        pass

    @abstractmethod
    def closeShop(self, p0: bool, p1: bool) -> None:
        pass

    @abstractmethod
    def getPassword(self) -> str:
        pass

    @abstractmethod
    def getMapId(self) -> int:
        pass

    @abstractmethod
    def getChannel(self) -> int:
        pass

    @abstractmethod
    def getMaxSize(self) -> int:
        pass

    @abstractmethod
    def getSize(self) -> int:
        pass

    @abstractmethod
    def getGameType(self) -> int:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def setAvailable(self, p0: bool) -> None:
        pass

    @abstractmethod
    def isAvailable(self) -> bool:
        pass

    @abstractmethod
    def getBoughtItems(self) -> Any:
        pass

