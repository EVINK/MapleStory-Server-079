"""
ByteBufferOutputstream - Converted from Java source
Original: tools/data/output/ByteBufferOutputstream.java
Package: tools.data.output
"""

from io import BytesIO
from typing import Optional, Any
import asyncio
import struct


class ByteBufferOutputstream(ByteOutputStream):
    """
    Class ByteBufferOutputstream
    Implements: ByteOutputStream
    """

    def __init__(self, bb: Any):
        self.bb = None
        self.bb = bb


    def writeByte(self, b: int) -> None:
        self.bb.put(b)

