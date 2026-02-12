"""
MapleStat - 从Java源文件转换而来
对应Java源文件: client/MapleStat.java
包路径: client
"""

from enum import Enum, IntEnum


class MapleStat(Enum):
    """枚举类 MapleStat - 从Java枚举转换"""

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
        """方法 getValue"""
        return getattr(self, 'value', 0)

    def getByValue(self, value: int) -> Any:
        """方法 getByValue"""
        raise NotImplementedError("方法 getByValue 尚未实现")

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)


class Temp(Enum):
    """枚举类 Temp - 从Java枚举转换"""

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
        """初始化枚举值"""
        self._i = i

    def getValue(self) -> int:
        """方法 getValue"""
        return getattr(self, 'value', 0)

