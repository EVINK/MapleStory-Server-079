"""
MapleServerHandlerMBean - Converted from Java source
Original: handling/MapleServerHandlerMBean.java
Package: handling
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class MapleServerHandlerMBean(ABC):
    """Interface MapleServerHandlerMBean"""

    @abstractmethod
    def writeLog(self) -> None:
        pass

