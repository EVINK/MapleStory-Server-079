"""
GenericSeekableLittleEndianAccessor - Converted from Java source
Original: tools/data/input/GenericSeekableLittleEndianAccessor.java
Package: tools.data.input
"""

from typing import Optional, Any
import os


class GenericSeekableLittleEndianAccessor(GenericLittleEndianAccessor, SeekableLittleEndianAccessor):
    """
    Class GenericSeekableLittleEndianAccessor
    Extends: GenericLittleEndianAccessor
    Implements: SeekableLittleEndianAccessor
    """

    def __init__(self, bs: Any):
        self.bs = None
        super(bs)
        self.bs = bs


    def seek(self, offset: int) -> None:
        try:
            self.bs.seek(offset)
        except IOError as e:
            print("Seek failed" + e)

    def getPosition(self) -> int:
        try:
            return self.bs.getPosition()
        except IOError as e:
            print("getPosition failed" + e)
            return -1

    def skip(self, num: int) -> None:
        self.seek(self.getPosition() + num)

