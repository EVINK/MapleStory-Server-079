"""
GenericLittleEndianWriter - Converted from Java source
Original: tools/data/output/GenericLittleEndianWriter.java
Package: tools.data.output
"""

from typing import Optional, Any


class GenericLittleEndianWriter(LittleEndianWriter):
    """
    Class GenericLittleEndianWriter
    Implements: LittleEndianWriter
    """

    def __init__(self):
        self.bos = None

    # Static initializer
    # GenericLittleEndianWriter.ASCII = Charset.forName("GBK")


    def setByteOutputStream(self, bos: Any) -> None:
        self.bos = bos

    def writeZeroBytes(self, i: int) -> None:
        for x in range(i):
            self.bos.writeByte(0)

    def write(self, b: bytes) -> None:
        for x in range(len(b)):
            self.bos.writeByte(b[x])

    def write_b(self, b: int) -> None:
        self.bos.writeByte(b)

    def writeShort(self, i: int) -> None:
        self.bos.writeByte((byte)(i & 0xFF))
        self.bos.writeByte((byte)(i >>> 8 & 0xFF))

    def writeShort_i(self, i: int) -> None:
        self.bos.writeByte((byte)(i & 0xFF))
        self.bos.writeByte((byte)(i >>> 8 & 0xFF))

    def writeInt(self, i: int) -> None:
        self.bos.writeByte((byte)(i & 0xFF))
        self.bos.writeByte((byte)(i >>> 8 & 0xFF))
        self.bos.writeByte((byte)(i >>> 16 & 0xFF))
        self.bos.writeByte((byte)(i >>> 24 & 0xFF))

    def writeAsciiString(self, s: str) -> None:
        self.write(s.encode("utf-8"))

    def writeAsciiString_s_max(self, s: str, max: int) -> None:
        if s.encode("utf-8").length > max:
            s = s[0:max]
        self.write(s.encode("utf-8"))
        i = s.encode("utf-8").length
        while i < max:
            self.write(0)

    def writeMapleAsciiString(self, s: str) -> None:
        self.writeShort(s.encode("utf-8").length)
        self.writeAsciiString(s)

    def writePos(self, s: Any) -> None:
        self.writeShort(s.x)
        self.writeShort(s.y)

    def writeLong(self, l: int) -> None:
        self.bos.writeByte((byte)(l & 0xFFL))
        self.bos.writeByte((byte)(l >>> 8 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 16 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 24 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 32 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 40 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 48 & 0xFFL))
        self.bos.writeByte((byte)(l >>> 56 & 0xFFL))

