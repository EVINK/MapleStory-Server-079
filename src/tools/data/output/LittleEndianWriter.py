"""
LittleEndianWriter - Converted from Java source
Original: tools/data/output/LittleEndianWriter.java
Package: tools.data.output
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class LittleEndianWriter(ABC):
    """Interface LittleEndianWriter"""

    @abstractmethod
    def writeZeroBytes(self, p0: int) -> None:
        pass

    @abstractmethod
    def write(self, p0: bytes) -> None:
        pass

    @abstractmethod
    def write(self, p0: int) -> None:
        pass

    @abstractmethod
    def write(self, p0: int) -> None:
        pass

    @abstractmethod
    def writeInt(self, p0: int) -> None:
        pass

    @abstractmethod
    def writeShort(self, p0: int) -> None:
        pass

    @abstractmethod
    def writeShort(self, p0: int) -> None:
        pass

    @abstractmethod
    def writeLong(self, p0: int) -> None:
        pass

    @abstractmethod
    def writeAsciiString(self, p0: str) -> None:
        pass

    @abstractmethod
    def writeAsciiString(self, p0: str, p1: int) -> None:
        pass

    @abstractmethod
    def writePos(self, p0: Any) -> None:
        pass

    @abstractmethod
    def writeMapleAsciiString(self, p0: str) -> None:
        pass

