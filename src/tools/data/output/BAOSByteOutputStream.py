"""
BAOSByteOutputStream - Converted from Java source
Original: tools/data/output/BAOSByteOutputStream.java
Package: tools.data.output
"""

from io import BytesIO
from typing import Optional, Any
import struct


class BAOSByteOutputStream(ByteOutputStream):
    """
    Class BAOSByteOutputStream
    Implements: ByteOutputStream
    """

    def __init__(self, baos: Any):
        self.baos = None
        self.baos = baos


    def writeByte(self, b: int) -> None:
        self.baos.write(b)

