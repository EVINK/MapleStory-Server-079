"""
ByteOutputStream - Converted from Java source
Original: tools/data/output/ByteOutputStream.java
Package: tools.data.output
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class ByteOutputStream(ABC):
    """Interface ByteOutputStream"""

    @abstractmethod
    def writeByte(self, p0: int) -> None:
        pass

