"""
BitTools - Converted from Java source
Original: tools/BitTools.java
Package: tools
"""

from typing import Optional, Any


class BitTools:
    """
    Class BitTools
    """


    def getShort(self, array: bytes, index: int) -> int:
        ret = array[index]
        ret &= 0xFF
        ret |= (array[index + 1] << 8 & 0xFF00)
        return ret

    def getString(self, array: bytes, index: int, length: int) -> str:
        cret = new char[length]
        for x in range(length):
            cret[x] = array[x + index]
        return str(cret)

    def getMapleString(self, array: bytes, index: int) -> str:
        length = (array[index] & 0xFF) | (array[index + 1] << 8 & 0xFF00)
        return getString(array, index + 2, length)

    def rollLeft(self, in: int, count: int) -> int:
        tmp = in & 0xFF
        tmp <<= count % 8
        return (byte)((tmp & 0xFF) | tmp >> 8)

    def rollRight(self, in: int, count: int) -> int:
        tmp = in & 0xFF
        tmp = tmp << 8 >>> count % 8
        return (byte)((tmp & 0xFF) | tmp >>> 8)

    def multiplyBytes(self, in: bytes, count: int, mul: int) -> bytes:
        ret = new byte[count * mul]
        for x in range(count * mul):
            ret[x] = in[x % count]
        return ret

    def doubleToShortBits(self, d: float) -> int:
        l = Double.doubleToLongBits(d)
        return (int)(l >> 48)

