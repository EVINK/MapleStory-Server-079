"""
LittleEndianAccessor - Converted from Java source
Original: tools/data/input/LittleEndianAccessor.java
Package: tools.data.input
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class LittleEndianAccessor(ABC):
    """Interface LittleEndianAccessor"""

    @abstractmethod
    def readByte(self) -> int:
        pass

    @abstractmethod
    def readByteAsInt(self) -> int:
        pass

    @abstractmethod
    def readChar(self) -> str:
        pass

    @abstractmethod
    def readShort(self) -> int:
        pass

    @abstractmethod
    def readInt(self) -> int:
        pass

    @abstractmethod
    def readLong(self) -> int:
        pass

    @abstractmethod
    def skip(self, p0: int) -> None:
        pass

    @abstractmethod
    def readFloat(self) -> float:
        pass

    @abstractmethod
    def readDouble(self) -> float:
        pass

    @abstractmethod
    def readAsciiString(self, p0: int) -> str:
        pass

    @abstractmethod
    def readMapleAsciiString(self) -> str:
        pass

    @abstractmethod
    def readPos(self) -> Any:
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

