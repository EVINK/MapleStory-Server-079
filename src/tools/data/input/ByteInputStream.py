"""
ByteInputStream - Converted from Java source
Original: tools/data/input/ByteInputStream.java
Package: tools.data.input
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class ByteInputStream(ABC):
    """Interface ByteInputStream"""

    @abstractmethod
    def readByte(self) -> int:
        pass

    @abstractmethod
    def getBytesRead(self) -> int:
        pass

    @abstractmethod
    def available(self) -> int:
        pass

    @abstractmethod
    def toString(self, p0: bool) -> str:
        pass

