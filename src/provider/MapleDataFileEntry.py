"""
MapleDataFileEntry - Converted from Java source
Original: provider/MapleDataFileEntry.java
Package: provider
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleDataFileEntry(ABC):
    """Interface MapleDataFileEntry"""

    @abstractmethod
    def setOffset(self, p0: int) -> None:
        pass

