"""
SeekableInputStreamBytestream - Converted from Java source
Original: tools/data/input/SeekableInputStreamBytestream.java
Package: tools.data.input
"""

from typing import Optional, Any
import os


from abc import ABC, abstractmethod

class SeekableInputStreamBytestream(ABC):
    """Interface SeekableInputStreamBytestream"""

    @abstractmethod
    def seek(self, p0: int) -> None:
        pass

    @abstractmethod
    def getPosition(self) -> int:
        pass

    @abstractmethod
    def toString(self, p0: bool) -> str:
        pass

