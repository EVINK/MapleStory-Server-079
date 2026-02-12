"""
PlayerRandomStream - Converted from Java source
Original: client/PlayerRandomStream.java
Package: client
"""

from typing import Optional, Any

# Internal module imports
# from server.Randomizer import *  # TODO: import specific classes
# from tools.data.output.MaplePacketLittleEndianWriter import *  # TODO: import specific classes


class PlayerRandomStream:
    """
    Class PlayerRandomStream
    """

    def __init__(self):
        self.seed1 = None
        self.seed2 = None
        self.seed3 = None
        self.seed1_ = None
        self.seed2_ = None
        self.seed3_ = None
        self.seed1__ = None
        self.seed2__ = None
        self.seed3__ = None
        self.seed1___ = None
        self.seed2___ = None
        self.seed3___ = None
        v4 = 5
        self.CRand32__Seed(Randomizer.nextLong(), 1170746341 * v4 - 755606699, 1170746341 * v4 - 755606699)


    def CRand32__Seed(self, s1: int, s2: int, s3: int) -> None:
        self.seed1 = (s1 | 0x100000)
        self.seed2 = (s2 | 0x1000)
        self.seed3 = (s3 | 0x10)
        self.seed1_ = (s1 | 0x100000)
        self.seed2_ = (s2 | 0x1000)
        self.seed3_ = (s3 | 0x10)
        self.seed1__ = (s1 | 0x100000)
        self.seed2__ = (s2 | 0x1000)
        self.seed3__ = (s3 | 0x10)

    def CRand32__Random(self) -> int:
        v4 = self.seed1
        v5 = self.seed2
        v6 = self.seed3
        v7 = self.seed1
        v8 = (v4 & 0xFFFFFFFFFFFFFFFEL) << 12 ^ ((v7 & 0x7FFC0) ^ v4 >> 13) >> 6
        v9 = 16 * (v5 & 0xFFFFFFFFFFFFFFF8) ^ (v5 >> 2 ^ (v5 & 0x3F800000)) >> 23
        v10 = (v6 & 0xFFFFFFFFFFFFFFF0) << 17 ^ (v6 >> 3 ^ (v6 & 0x1FFFFF00)) >> 8
        self.seed3_ = (v10 & 0xFFFFFFFFL)
        self.seed1_ = (v8 & 0xFFFFFFFFL)
        self.seed2_ = (v9 & 0xFFFFFFFFL)
        return (v8 ^ v9 ^ v10) & 0xFFFFFFFFL

    def CRand32__Random_Character(self) -> int:
        v4 = self.seed1_
        v5 = self.seed2_
        v6 = self.seed3_
        v7 = self.seed1_
        v8 = (v4 & 0xFFFFFFFFFFFFFFFEL) << 12 ^ ((v7 & 0x7FFC0) ^ v4 >> 13) >> 6
        v9 = 16 * (v5 & 0xFFFFFFFFFFFFFFF8) ^ (v5 >> 2 ^ (v5 & 0x3F800000)) >> 23
        v10 = (v6 & 0xFFFFFFFFFFFFFFF0) << 17 ^ (v6 >> 3 ^ (v6 & 0x1FFFFF00)) >> 8
        self.seed3_ = (v10 & 0xFFFFFFFFL)
        self.seed1_ = (v8 & 0xFFFFFFFFL)
        self.seed2_ = (v9 & 0xFFFFFFFFL)
        return (v8 ^ v9 ^ v10) & 0xFFFFFFFFL

    def CRand32__Random_CheckDamageMiss(self) -> int:
        v4 = self.seed1__
        v5 = self.seed2__
        v6 = self.seed3__
        v7 = self.seed1__
        v8 = (v4 & 0xFFFFFFFFFFFFFFFEL) << 12 ^ ((v7 & 0x7FFC0) ^ v4 >> 13) >> 6
        v9 = 16 * (v5 & 0xFFFFFFFFFFFFFFF8) ^ (v5 >> 2 ^ (v5 & 0x3F800000)) >> 23
        v10 = (v6 & 0xFFFFFFFFFFFFFFF0) << 17 ^ (v6 >> 3 ^ (v6 & 0x1FFFFF00)) >> 8
        self.seed3_ = (v10 & 0xFFFFFFFFL)
        self.seed1_ = (v8 & 0xFFFFFFFFL)
        self.seed2_ = (v9 & 0xFFFFFFFFL)
        return (v8 ^ v9 ^ v10) & 0xFFFFFFFFL

    def CRand32__Random_ForMonster(self) -> int:
        v4 = self.seed1___
        v5 = self.seed2___
        v6 = self.seed3___
        v7 = self.seed1___
        v8 = (v4 & 0xFFFFFFFFFFFFFFFEL) << 12 ^ ((v7 & 0x7FFC0) ^ v4 >> 13) >> 6
        v9 = 16 * (v5 & 0xFFFFFFFFFFFFFFF8) ^ (v5 >> 2 ^ (v5 & 0x3F800000)) >> 23
        v10 = (v6 & 0xFFFFFFFFFFFFFFF0) << 17 ^ (v6 >> 3 ^ (v6 & 0x1FFFFF00)) >> 8
        self.seed3_ = (v10 & 0xFFFFFFFFL)
        self.seed1_ = (v8 & 0xFFFFFFFFL)
        self.seed2_ = (v9 & 0xFFFFFFFFL)
        return (v8 ^ v9 ^ v10) & 0xFFFFFFFFL

    def connectData(self, mplew: Any) -> None:
        v5 = self.CRand32__Random()
        s2 = self.CRand32__Random()
        v6 = self.CRand32__Random()
        self.CRand32__Seed(v5, s2, v6)
        mplew.writeInt(v5)
        mplew.writeInt(s2)
        mplew.writeInt(v6)

