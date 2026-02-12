"""
MapleCanvas - Converted from Java source
Original: provider/MapleCanvas.java
Package: provider
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleCanvas(ABC):
    """Interface MapleCanvas"""

    @abstractmethod
    def getHeight(self) -> int:
        pass

    @abstractmethod
    def getWidth(self) -> int:
        pass

    @abstractmethod
    def getImage(self) -> Any:
        pass

