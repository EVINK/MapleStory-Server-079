"""
ISkill - Converted from Java source
Original: client/ISkill.java
Package: client
"""

from typing import Optional, Any

# Internal module imports
# from server import *  # TODO: import specific classes
# from server.life import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class ISkill(ABC):
    """Interface ISkill"""

    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def getEffect(self, p0: int) -> Any:
        pass

    @abstractmethod
    def getMaxLevel(self) -> int:
        pass

    @abstractmethod
    def getAnimationTime(self) -> int:
        pass

    @abstractmethod
    def canBeLearnedBy(self, p0: int) -> bool:
        pass

    @abstractmethod
    def isFourthJob(self) -> bool:
        pass

    @abstractmethod
    def getAction(self) -> bool:
        pass

    @abstractmethod
    def isTimeLimited(self) -> bool:
        pass

    @abstractmethod
    def getMasterLevel(self) -> int:
        pass

    @abstractmethod
    def getElement(self) -> Any:
        pass

    @abstractmethod
    def isBeginnerSkill(self) -> bool:
        pass

    @abstractmethod
    def hasRequiredSkill(self) -> bool:
        pass

    @abstractmethod
    def isInvisible(self) -> bool:
        pass

    @abstractmethod
    def isChargeSkill(self) -> bool:
        pass

    @abstractmethod
    def getRequiredSkillLevel(self) -> int:
        pass

    @abstractmethod
    def getRequiredSkillId(self) -> int:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

