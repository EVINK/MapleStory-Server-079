"""
GenericLittleEndianAccessor - Converted from Java source
Original: tools/data/input/GenericLittleEndianAccessor.java
Package: tools.data.input
"""

from typing import Optional, Any


class GenericLittleEndianAccessor(LittleEndianAccessor):
    """
    Class GenericLittleEndianAccessor
    Implements: LittleEndianAccessor
    """

    def __init__(self, bs: Any):
        self.bs = None
        self.bs = bs


    def readByteAsInt(self) -> int:
        return self.bs.readByte()

    def readByte(self) -> int:
        return self.bs.readByte()

    def readInt(self) -> int:
        byte1 = self.bs.readByte()
        byte2 = self.bs.readByte()
        byte3 = self.bs.readByte()
        byte4 = self.bs.readByte()
        return (byte4 << 24) + (byte3 << 16) + (byte2 << 8) + byte1

    def readShort(self) -> int:
        byte1 = self.bs.readByte()
        byte2 = self.bs.readByte()
        return (short)((byte2 << 8) + byte1)

    def readChar(self) -> str:
        return self.readShort()

    def readLong(self) -> int:
        byte1 = self.bs.readByte()
        byte2 = self.bs.readByte()
        byte3 = self.bs.readByte()
        byte4 = self.bs.readByte()
        byte5 = self.bs.readByte()
        byte6 = self.bs.readByte()
        byte7 = self.bs.readByte()
        byte8 = self.bs.readByte()
        return (byte8 << 56) + (byte7 << 48) + (byte6 << 40) + (byte5 << 32) + (byte4 << 24) + (byte3 << 16) + (byte2 << 8) + byte1

    def readFloat(self) -> float:
        return Float.intBitsToFloat(self.readInt())

    def readDouble(self) -> float:
        return Double.longBitsToDouble(self.readLong())

    def readAsciiString(self, n: int) -> str:
        ret = new byte[n]
        for x in range(n):
            ret[x] = self.readByte()
        try:
            str = String(ret, "gbk")
            return str
        except UnsupportedEncodingException as e:
            print(e)
            return None

    def getBytesRead(self) -> int:
        return self.bs.getBytesRead()

    def readMapleAsciiString(self) -> str:
        return self.readAsciiString(self.readShort())

    def readPos(self) -> Any:
        x = self.readShort()
        y = self.readShort()
        return Point(x, y)

    def read(self, num: int) -> bytes:
        ret = new byte[num]
        for x in range(num):
            ret[x] = self.readByte()
        return ret

    def skip(self, num: int) -> None:
        for x in range(num):
            self.readByte()

    def available(self) -> int:
        return self.bs.available()

    def toString(self) -> str:
        return self.bs

    def toString_b(self, b: bool) -> str:
        return self.bs.toString(b)

