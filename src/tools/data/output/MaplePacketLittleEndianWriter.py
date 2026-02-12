"""
MaplePacketLittleEndianWriter - Converted from Java source
Original: tools/data/output/MaplePacketLittleEndianWriter.java
Package: tools.data.output
"""

from io import BytesIO
from typing import Optional, Any
import struct

# Internal module imports
# from handling.ByteArrayMaplePacket import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from server.ServerProperties import *  # TODO: import specific classes
# from tools.HexTool import *  # TODO: import specific classes


class MaplePacketLittleEndianWriter(GenericLittleEndianWriter):
    """
    Class MaplePacketLittleEndianWriter
    Extends: GenericLittleEndianWriter
    """

    def __init__(self):
        self.baos = None
        this(32)

    # Static initializer
    # MaplePacketLittleEndianWriter.debugMode = bool(ServerProperties.getProperty("RoyMS.Debug", "False"))


    def getPacket(self) -> Any:
        if MaplePacketLittleEndianWriter.debugMode:
            packet = ByteArrayMaplePacket(self.baos.toByteArray())
            print("Packet to be sent:\n" + packet)
        return ByteArrayMaplePacket(self.baos.toByteArray())

    def toString(self) -> str:
        return HexTool.toString(self.baos.toByteArray())

