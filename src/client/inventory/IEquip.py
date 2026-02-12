"""
IEquip - Converted from Java source
Original: client/inventory/IEquip.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from typing import Optional, Any


from abc import ABC, abstractmethod

class IEquip(ABC):
    """Interface IEquip"""

    @abstractmethod
    def getUpgradeSlots(self) -> int:
        pass

    @abstractmethod
    def getLevel(self) -> int:
        pass

    @abstractmethod
    def getViciousHammer(self) -> int:
        pass

    @abstractmethod
    def getItemEXP(self) -> int:
        pass

    @abstractmethod
    def getExpPercentage(self) -> int:
        pass

    @abstractmethod
    def getEquipLevel(self) -> int:
        pass

    @abstractmethod
    def getEquipLevels(self) -> int:
        pass

    @abstractmethod
    def getEquipExp(self) -> int:
        pass

    @abstractmethod
    def getEquipExpForLevel(self) -> int:
        pass

    @abstractmethod
    def getBaseLevel(self) -> int:
        pass

    @abstractmethod
    def getStr(self) -> int:
        pass

    @abstractmethod
    def getDex(self) -> int:
        pass

    @abstractmethod
    def getInt(self) -> int:
        pass

    @abstractmethod
    def getLuk(self) -> int:
        pass

    @abstractmethod
    def getHp(self) -> int:
        pass

    @abstractmethod
    def getMp(self) -> int:
        pass

    @abstractmethod
    def getWatk(self) -> int:
        pass

    @abstractmethod
    def getMatk(self) -> int:
        pass

    @abstractmethod
    def getWdef(self) -> int:
        pass

    @abstractmethod
    def getMdef(self) -> int:
        pass

    @abstractmethod
    def getAcc(self) -> int:
        pass

    @abstractmethod
    def getAvoid(self) -> int:
        pass

    @abstractmethod
    def getHands(self) -> int:
        pass

    @abstractmethod
    def getSpeed(self) -> int:
        pass

    @abstractmethod
    def getJump(self) -> int:
        pass

    @abstractmethod
    def getDurability(self) -> int:
        pass

    @abstractmethod
    def getEnhance(self) -> int:
        pass

    @abstractmethod
    def getState(self) -> int:
        pass

    @abstractmethod
    def getPotential1(self) -> int:
        pass

    @abstractmethod
    def getPotential2(self) -> int:
        pass

    @abstractmethod
    def getPotential3(self) -> int:
        pass

    @abstractmethod
    def getHpR(self) -> int:
        pass

    @abstractmethod
    def getMpR(self) -> int:
        pass


# Inner class from Java (originally nested)
class ScrollResult(Enum):
    """Enum ScrollResult"""

    SUCCESS = 0
    FAIL = 1
    CURSE = 2

