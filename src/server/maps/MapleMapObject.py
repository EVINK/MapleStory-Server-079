"""
MapleMapObject - Converted from Java source
Original: server/maps/MapleMapObject.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class MapleMapObject(ABC):
    """Interface MapleMapObject"""

    @abstractmethod
    def getObjectId(self) -> int:
        pass

    @abstractmethod
    def setObjectId(self, p0: int) -> None:
        pass

    @abstractmethod
    def getType(self) -> Any:
        pass

    @abstractmethod
    def getPosition(self) -> Any:
        pass

    @abstractmethod
    def setPosition(self, p0: Any) -> None:
        pass

    @abstractmethod
    def sendSpawnData(self, p0: Any) -> None:
        pass

    @abstractmethod
    def sendDestroyData(self, p0: Any) -> None:
        pass

