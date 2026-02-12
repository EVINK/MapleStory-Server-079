"""
MapleData - Converted from Java source
Original: provider/MapleData.java
Package: provider
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from provider.WzXML.MapleDataType import *  # TODO: import specific classes


from abc import ABC, abstractmethod

class MapleData(ABC):
    """Interface MapleData"""

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getType(self) -> Any:
        pass

    @abstractmethod
    def getChildren(self) -> list:
        pass

    @abstractmethod
    def getChildByPath(self, p0: str) -> Any:
        pass

    @abstractmethod
    def getData(self) -> Any:
        pass

