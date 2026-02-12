"""
MapleLove - Converted from Java source
Original: server/maps/MapleLove.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleLove(AbstractMapleMapObject):
    """
    Class MapleLove
    Extends: AbstractMapleMapObject
    """

    def __init__(self, owner: Any, pos: Any, ft: int, text: str, itemid: int):
        self.pos = None
        self.owner = None
        self.text = None
        self.ft = None
        self.itemid = None
        self.owner = owner
        self.pos = pos
        self.text = text
        self.ft = ft
        self.itemid = itemid


    def getType(self) -> Any:
        return MapleMapObjectType.LOVE

    def getPosition(self) -> Any:
        return self.pos.getLocation()

    def getOwner(self) -> Any:
        return self.owner

    def setPosition(self, position: Any) -> None:
        raise NotImplementedError()

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(self.makeDestroyData())

    def sendSpawnData(self, client: Any) -> None:
        client.getSession().write(self.makeSpawnData())

    def makeSpawnData(self) -> Any:
        return MaplePacketCreator.spawnLove(self.getObjectId(), self.itemid, self.owner.getName(), self.text, self.pos, self.ft)

    def makeDestroyData(self) -> Any:
        return MaplePacketCreator.removeLove(self.getObjectId())

