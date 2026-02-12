"""
CherryMSLottery - Converted from Java source
Original: KinMS/db/CherryMSLottery.java
Package: KinMS.db
"""

from typing import Collection
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from server.maps.MapleMapFactory import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class CherryMSLottery(ABC):
    """Interface CherryMSLottery"""

    @abstractmethod
    def addChar(self, p0: Any) -> None:
        pass

    @abstractmethod
    def doLottery(self) -> None:
        pass

    @abstractmethod
    def drawalottery(self) -> None:
        pass

    @abstractmethod
    def getAllpeichu(self) -> int:
        pass

    @abstractmethod
    def getAlltouzhu(self) -> int:
        pass

    @abstractmethod
    def getChannelServer(self) -> Any:
        pass

    @abstractmethod
    def getCharacters(self) -> list:
        pass

    @abstractmethod
    def getMapleMapFactory(self) -> Any:
        pass

    @abstractmethod
    def getTouNumbyType(self, p0: int) -> int:
        pass

    @abstractmethod
    def getZjNum(self) -> int:
        pass

    @abstractmethod
    def setAllpeichu(self, p0: int) -> None:
        pass

    @abstractmethod
    def setAlltouzhu(self, p0: int) -> None:
        pass

    @abstractmethod
    def setCharacters(self, p0: list) -> None:
        pass

    @abstractmethod
    def setZjNum(self, p0: int) -> None:
        pass

    @abstractmethod
    def warp(self, p0: int, p1: Any) -> None:
        pass

