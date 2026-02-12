"""
AnimatedMapleMapObject - Converted from Java source
Original: server/maps/AnimatedMapleMapObject.java
Package: server.maps
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class AnimatedMapleMapObject(ABC):
    """Interface AnimatedMapleMapObject"""

    @abstractmethod
    def getStance(self) -> int:
        pass

    @abstractmethod
    def setStance(self, p0: int) -> None:
        pass

    @abstractmethod
    def isFacingLeft(self) -> bool:
        pass

