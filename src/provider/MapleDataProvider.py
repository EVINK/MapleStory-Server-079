"""
MapleDataProvider - Converted from Java source
Original: provider/MapleDataProvider.java
Package: provider
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleDataProvider(ABC):
    """Interface MapleDataProvider"""

    @abstractmethod
    def getData(self, p0: str) -> Any:
        pass

    @abstractmethod
    def getRoot(self) -> Any:
        pass

