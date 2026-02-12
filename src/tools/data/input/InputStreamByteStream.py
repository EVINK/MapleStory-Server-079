"""
InputStreamByteStream - Converted from Java source
Original: tools/data/input/InputStreamByteStream.java
Package: tools.data.input
"""

from io import IOBase
from typing import Optional, Any
import os


class InputStreamByteStream(ByteInputStream):
    """
    Class InputStreamByteStream
    Implements: ByteInputStream
    """

    def __init__(self, is: Any):
        self.is = None
        self.read = 0
        self.read = 0
        self.is = is


    def readByte(self) -> int:
        try:
            temp = self.is.read()
            if temp == -1:
                raise RuntimeError("EOF")
            self.read += 1
            return temp
        except IOError as e:
            raise RuntimeError(e)

    def getBytesRead(self) -> int:
        return self.read

    def available(self) -> int:
        try:
            return self.is.available()
        except IOError as e:
            print("ERROR" + e)
            return 0

    def toString(self, b: bool) -> str:
        return self

