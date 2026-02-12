"""
LifeMovement - Converted from Java source
Original: server/movement/LifeMovement.java
Package: server.movement
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class LifeMovement(ABC):
    """Interface LifeMovement"""

    @abstractmethod
    def getPosition(self) -> Any:
        pass

    @abstractmethod
    def getNewstate(self) -> int:
        pass

    @abstractmethod
    def getDuration(self) -> int:
        pass

    @abstractmethod
    def getType(self) -> int:
        pass

