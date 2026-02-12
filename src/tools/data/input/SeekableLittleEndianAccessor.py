"""
SeekableLittleEndianAccessor - Converted from Java source
Original: tools/data/input/SeekableLittleEndianAccessor.java
Package: tools.data.input
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class SeekableLittleEndianAccessor(ABC):
    """Interface SeekableLittleEndianAccessor"""

    @abstractmethod
    def seek(self, p0: int) -> None:
        pass

    @abstractmethod
    def getPosition(self) -> int:
        pass

