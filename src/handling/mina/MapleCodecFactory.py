"""
MapleCodecFactory - Converted from Java source
Original: handling/mina/MapleCodecFactory.java
Package: handling.mina
"""

from typing import Optional, Any
import asyncio


class MapleCodecFactory(ProtocolCodecFactory):
    """
    Class MapleCodecFactory
    Implements: ProtocolCodecFactory
    """

    def __init__(self):
        self.encoder = None
        self.decoder = None
        self.encoder = MaplePacketEncoder()
        self.decoder = MaplePacketDecoder()


    def getEncoder(self) -> Any:
        return self.encoder

    def getDecoder(self) -> Any:
        return self.decoder

    def getEncoder_session(self, session: Any) -> Any:
        return self.encoder

    def getDecoder_session(self, session: Any) -> Any:
        return self.decoder

