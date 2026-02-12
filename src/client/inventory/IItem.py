"""
IItem - Converted from Java source
Original: client/inventory/IItem.java
Package: client.inventory
"""

from typing import Optional, Any
import threading


from abc import ABC, abstractmethod

class IItem(ABC):
    """Interface IItem"""

    @abstractmethod
    def getType(self) -> int:
        pass

    @abstractmethod
    def getPosition(self) -> int:
        pass

    @abstractmethod
    def getFlag(self) -> int:
        pass

    @abstractmethod
    def getLocked(self) -> bool:
        pass

    @abstractmethod
    def getQuantity(self) -> int:
        pass

    @abstractmethod
    def getOwner(self) -> str:
        pass

    @abstractmethod
    def getGMLog(self) -> str:
        pass

    @abstractmethod
    def getItemId(self) -> int:
        pass

    @abstractmethod
    def getPet(self) -> Any:
        pass

    @abstractmethod
    def getUniqueId(self) -> int:
        pass

    @abstractmethod
    def copy(self) -> Any:
        pass

    @abstractmethod
    def getExpiration(self) -> int:
        pass

    @abstractmethod
    def setFlag(self, p0: int) -> None:
        pass

    @abstractmethod
    def setLocked(self, p0: int) -> None:
        pass

    @abstractmethod
    def setUniqueId(self, p0: int) -> None:
        pass

    @abstractmethod
    def setPosition(self, p0: int) -> None:
        pass

    @abstractmethod
    def setExpiration(self, p0: int) -> None:
        pass

    @abstractmethod
    def setOwner(self, p0: str) -> None:
        pass

    @abstractmethod
    def setGMLog(self, p0: str) -> None:
        pass

    @abstractmethod
    def setQuantity(self, p0: int) -> None:
        pass

    @abstractmethod
    def setGiftFrom(self, p0: str) -> None:
        pass

    @abstractmethod
    def setEquipLevel(self, p0: int) -> None:
        pass

    @abstractmethod
    def getEquipLevel(self) -> int:
        pass

    @abstractmethod
    def getGiftFrom(self) -> str:
        pass

    @abstractmethod
    def getRing(self) -> Any:
        pass

    @abstractmethod
    def getEquipOnlyId(self) -> int:
        pass

    @abstractmethod
    def hasSetOnlyId(self) -> bool:
        pass

    @abstractmethod
    def setEquipOnlyId(self, p0: int) -> None:
        pass

