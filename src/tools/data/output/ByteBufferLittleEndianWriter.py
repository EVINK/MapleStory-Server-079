"""
ByteBufferLittleEndianWriter - Converted from Java source
Original: tools/data/output/ByteBufferLittleEndianWriter.java
Package: tools.data.output
"""

from io import BytesIO
from typing import Optional, Any
import asyncio
import struct


class ByteBufferLittleEndianWriter(GenericLittleEndianWriter):
    """
    Class ByteBufferLittleEndianWriter
    Extends: GenericLittleEndianWriter
    """

    def __init__(self):
        self.bb = None
        this(50, True)


    def getFlippedBB(self) -> Any:
        return self.bb.flip()

    def getByteBuffer(self) -> Any:
        return self.bb

