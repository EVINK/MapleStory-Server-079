"""
ByteArrayMaplePacket - Converted from Java source
Original: handling/ByteArrayMaplePacket.java
Package: handling
"""

from typing import Optional, Any
import threading

# Internal module imports
# from tools.HexTool import *  # TODO: import specific classes


class ByteArrayMaplePacket(MaplePacket):
    """
    Class ByteArrayMaplePacket
    Implements: MaplePacket
    """

    def __init__(self, data: bytes):
        self.onSend = None
        self.data = data

    # Static initializer
    # ByteArrayMaplePacket.serialVersionUID = -7997681658570958848


    def getBytes(self) -> bytes:
        return self.data

    def getOnSend(self) -> Any:
        return self.onSend

    def setOnSend(self, onSend: Any) -> None:
        self.onSend = onSend

    def toString(self) -> str:
        return HexTool.toString(self.data)

