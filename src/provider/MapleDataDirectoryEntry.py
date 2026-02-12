"""
MapleDataDirectoryEntry - Converted from Java source
Original: provider/MapleDataDirectoryEntry.java
Package: provider
"""

from typing import List
from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleDataDirectoryEntry(ABC):
    """Interface MapleDataDirectoryEntry"""

    @abstractmethod
    def getSubdirectories(self) -> list:
        pass

    @abstractmethod
    def getFiles(self) -> list:
        pass

    @abstractmethod
    def getEntry(self, p0: str) -> Any:
        pass

