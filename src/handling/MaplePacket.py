"""
MaplePacket - Converted from Java source
Original: handling/MaplePacket.java
Package: handling
"""

from typing import Optional, Any
import threading


from abc import ABC, abstractmethod

class MaplePacket(ABC):
    """Interface MaplePacket"""

    @abstractmethod
    def getOnSend(self) -> Any:
        pass

    @abstractmethod
    def setOnSend(self, p0: Any) -> None:
        pass

