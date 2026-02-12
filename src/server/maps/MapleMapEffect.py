"""
MapleMapEffect - Converted from Java source
Original: server/maps/MapleMapEffect.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleClient import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes
# from tools.packet.MTSCSPacket import *  # TODO: import specific classes


class MapleMapEffect:
    """
    Class MapleMapEffect
    """

    def __init__(self, msg: str, itemId: int):
        self.msg = ""
        self.itemId = 0
        self.active = False
        self.jukebox = False
        self.msg = ""
        self.itemId = 0
        self.active = True
        self.jukebox = False
        self.msg = msg
        self.itemId = itemId


    def setActive(self, active: bool) -> None:
        self.active = active

    def setJukebox(self, actie: bool) -> None:
        self.jukebox = actie

    def isJukebox(self) -> bool:
        return self.jukebox

    def makeDestroyData(self) -> Any:
        return self.jukebox ? MTSCSPacket.playCashSong(0, "") : MaplePacketCreator.removeMapEffect()

    def makeStartData(self) -> Any:
        return self.jukebox ? MTSCSPacket.playCashSong(self.itemId, self.msg) : MaplePacketCreator.startMapEffect(self.msg, self.itemId, self.active)

    def sendStartData(self, c: Any) -> None:
        c.getSession().write(self.makeStartData())

