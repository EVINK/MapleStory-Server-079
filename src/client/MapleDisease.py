"""
MapleDisease - Converted from Java source
Original: client/MapleDisease.java
Package: client
"""

from enum import Enum, IntEnum
from typing import Optional, Any

# Internal module imports
# from server.Randomizer import *  # TODO: import specific classes


class MapleDisease(Enum):
    """Enum MapleDisease"""

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
        return self.first

    def getValue(self) -> int:
        return self.i

    def getRandom(self) -> Any:
        dis = None
        Block_1:
        while True:
            values = values()
            length = len(values), i = 0
            while i < length:
                dis = values[i]
                if Randomizer.nextInt(values().length) == 0:
                    Block_1 = None
        return dis

    def getBySkill(self, skill: int) -> Any:
        # switch (skill):
            # case 120:
                return MapleDisease.封印
            # case 121:
                return MapleDisease.黑暗
            # case 122:
                return MapleDisease.虚弱
            # case 123:
                return MapleDisease.眩晕
            # case 124:
                return MapleDisease.诅咒
            # case 125:
                return MapleDisease.中毒
            # case 126:
                return MapleDisease.缓慢
            # case 128:
                return MapleDisease.诱惑
            # case 132:
                return MapleDisease.REVERSE_DIRECTION
            # case 133:
                return MapleDisease.ZOMBIFY
            # case 134:
                return MapleDisease.POTION
            # case 135:
                return MapleDisease.SHADOW
            # case 136:
                return MapleDisease.BLIND
            # case 137:
                return MapleDisease.冻结
            # default:
                return None

    def getByDisease(self, skill: Any) -> int:
        # switch (skill):
            # case 封印:
                return 120
            # case 黑暗:
                return 121
            # case 虚弱:
                return 122
            # case 眩晕:
                return 123
            # case 诅咒:
                return 124
            # case 中毒:
                return 125
            # case 缓慢:
                return 126
            # case 诱惑:
                return 128
            # case REVERSE_DIRECTION:
                return 132
            # case ZOMBIFY:
                return 133
            # case POTION:
                return 134
            # case SHADOW:
                return 135
            # case BLIND:
                return 136
            # case 冻结:
                return 137
            # default:
                return 0

