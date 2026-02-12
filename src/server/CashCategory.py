"""
CashCategory - Converted from Java source
Original: server/CashCategory.java
Package: server
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class CashCategory:
    """
    Class CashCategory
    """

    def __init__(self, id: int, name: str, parent: int, flag: int, sold: int):
        self.id = None
        self.parent = None
        self.flag = None
        self.sold = None
        self.name = None
        self.value = None
        self.id = id
        self.name = name
        self.parent = parent
        self.flag = flag
        self.sold = sold


    def getId(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name

    def getParentDirectory(self) -> int:
        return self.parent

    def getFlag(self) -> int:
        return self.flag

    def getSold(self) -> int:
        return self.sold

    def getValue(self) -> int:
        return self.value


# Inner class from Java (originally nested)
class CSFlag(Enum):
    """Enum CSFlag"""

    NORMAL = (0)
    NEW = (1)
    HOT = (2)

    def __init__(self, value):
        self._value = value

    def getValue(self) -> int:
        return self.value

