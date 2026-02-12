"""
RandomAccessByteStream - Converted from Java source
Original: tools/data/input/RandomAccessByteStream.java
Package: tools.data.input
"""

from io import open
from typing import Optional, Any
import os


class RandomAccessByteStream(SeekableInputStreamBytestream):
    """
    Class RandomAccessByteStream
    Implements: SeekableInputStreamBytestream
    """

    def __init__(self, raf: Any):
        self.raf = None
        self.read = 0
        self.read = 0
        self.raf = raf


    def readByte(self) -> int:
        try:
            temp = self.raf.read()
            if temp == -1:
                raise RuntimeError("EOF")
            self.read += 1
            return temp
        except IOError as e:
            raise RuntimeError(e)

    def seek(self, offset: int) -> None:
        self.raf.seek(offset)

    def getPosition(self) -> int:
        return self.raf.getFilePointer()

    def getBytesRead(self) -> int:
        return self.read

    def available(self) -> int:
        try:
            return self.raf - self.raf.getFilePointer()
        except IOError as e:
            print("ERROR" + e)
            return 0

    def toString(self, b: bool) -> str:
        return self

