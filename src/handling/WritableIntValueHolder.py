"""
WritableIntValueHolder - Converted from Java source
Original: handling/WritableIntValueHolder.java
Package: handling
"""

from typing import Optional, Any


from abc import ABC, abstractmethod

class WritableIntValueHolder(ABC):
    """Interface WritableIntValueHolder"""

    @abstractmethod
    def getValue(self) -> int:
        pass

    @abstractmethod
    def setValue(self, p0: int) -> None:
        pass

