"""
MapleDataEntry - Converted from Java source
Original: provider/MapleDataEntry.java
Package: provider
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleDataEntry(ABC):
    """Interface MapleDataEntry"""

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getSize(self) -> int:
        pass

    @abstractmethod
    def getChecksum(self) -> int:
        pass

    @abstractmethod
    def getOffset(self) -> int:
        pass

