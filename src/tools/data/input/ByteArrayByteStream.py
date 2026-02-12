"""
ByteArrayByteStream - Converted from Java source
Original: tools/data/input/ByteArrayByteStream.java
Package: tools.data.input
"""

from typing import Optional, Any
import os

# Internal module imports
# from tools.HexTool import *  # TODO: import specific classes


class ByteArrayByteStream(SeekableInputStreamBytestream):
    """
    Class ByteArrayByteStream
    Implements: SeekableInputStreamBytestream
    """

    def __init__(self, arr: bytes):
        self.pos = 0
        self.bytesRead = 0
        self.pos = 0
        self.bytesRead = 0
        self.arr = arr


    def getPosition(self) -> int:
        return self.pos

    def seek(self, offset: int) -> None:
        self.pos = offset

    def getBytesRead(self) -> int:
        return self.bytesRead

    def readByte(self) -> int:
        self.bytesRead += 1
        return self.arr[self.pos++] & 0xFF

    def toString(self) -> str:
        return self.toString(False)

    def toString_b(self, b: bool) -> str:
        nows = ""
        if self.len(arr) - self.pos > 0:
            now = new byte[self.len(arr) - self.pos]
            System.arraycopy(self.arr, self.pos, now, 0, self.len(arr) - self.pos)
            nows = HexTool.toString(now)
        if b:
            return "All: " + HexTool.toString(self.arr) + "\nNow: " + nows
        return "Data: " + nows

    def available(self) -> int:
        return self.len(arr) - self.pos

