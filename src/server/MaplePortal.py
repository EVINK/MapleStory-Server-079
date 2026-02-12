"""
MaplePortal - Converted from Java source
Original: server/MaplePortal.java
Package: server
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class MaplePortal(ABC):
    """Interface MaplePortal"""

    @abstractmethod
    def getType(self) -> int:
        pass

    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def getPosition(self) -> Any:
        pass

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getTarget(self) -> str:
        pass

    @abstractmethod
    def getScriptName(self) -> str:
        pass

    @abstractmethod
    def setScriptName(self, p0: str) -> None:
        pass

    @abstractmethod
    def getTargetMapId(self) -> int:
        pass

    @abstractmethod
    def enterPortal(self, p0: Any) -> None:
        pass

    @abstractmethod
    def setPortalState(self, p0: bool) -> None:
        pass

    @abstractmethod
    def getPortalState(self) -> bool:
        pass

