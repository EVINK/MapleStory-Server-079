"""
MapleStat - Converted from Java source
Original: client/MapleStat.java
Package: client
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleStat(Enum):
    """Enum MapleStat"""

    SKIN = (1)
    FACE = (2)
    HAIR = (4)
    LEVEL = (64)
    JOB = (128)
    STR = (256)
    DEX = (512)
    INT = (1024)
    LUK = (2048)
    HP = (4096)
    MAXHP = (8192)
    MP = (16384)
    MAXMP = (32768)
    AVAILABLEAP = (65536)
    AVAILABLESP = (131072)
    EXP = (262144)
    FAME = (524288)
    MESO = (1048576)
    PET = (2097160)

    def getValue(self) -> int:
        return self.i

    def getByValue(self, value: int) -> Any:
        for stat in values():
            if stat.i == value:
                return stat
        return None

    def getValue(self) -> int:
        return self.i


# Inner class from Java (originally nested)
class Temp(Enum):
    """Enum Temp"""

    STR = (1)
    DEX = (2)
    INT = (4)
    LUK = (8)
    WATK = (16)
    WDEF = (32)
    MATK = (64)
    MDEF = (128)
    ACC = (256)
    AVOID = (512)
    SPEED = (1024)
    JUMP = (2048)

    def __init__(self, i):
        self._i = i

    def getValue(self) -> int:
        return self.i

