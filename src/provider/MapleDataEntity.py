"""
MapleDataEntity - Converted from Java source
Original: provider/MapleDataEntity.java
Package: provider
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleDataEntity(ABC):
    """Interface MapleDataEntity"""

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getParent(self) -> Any:
        pass

