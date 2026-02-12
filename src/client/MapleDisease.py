"""
MapleDisease - 从Java源文件转换而来
对应Java源文件: client/MapleDisease.java
包路径: client
"""

from enum import Enum, IntEnum
from typing import Optional, Any

# 内部模块导入 (Internal module imports)
# from server.Randomizer import *  # TODO: 根据实际需要导入具体类


class MapleDisease(Enum):
    """枚举类 MapleDisease - 从Java枚举转换"""

    眩晕 = (562949953421312L)
    中毒 = (1125899906842624L)
    封印 = (2251799813685248L)
    黑暗 = (4503599627370496L)
    虚弱 = (4611686018427387904L)
    诅咒 = (Long.MIN_VALUE)
    缓慢 = (1L)
    变身 = (2L)
    诱惑 = (128L)
    ZOMBIFY = (16384L)
    REVERSE_DIRECTION = (524288L)
    冻结 = (2251799813685248L, true)
    POTION = (8796093022208L, true)
    SHADOW = (17592186044416L, true)
    BLIND = (35184372088832L, true)
    WEIRD_FLAME = (134217728L)

    def isFirst(self) -> bool:
        """方法 isFirst"""
        return False

    def getValue(self) -> int:
        """方法 getValue"""
        return 0

    def getRandom(self) -> Any:
        """方法 getRandom"""
        raise NotImplementedError("方法 getRandom 尚未实现")

    def getBySkill(self, skill: int) -> Any:
        """方法 getBySkill"""
        raise NotImplementedError("方法 getBySkill 尚未实现")

    def getByDisease(self, skill: Any) -> int:
        """方法 getByDisease"""
        return 0

