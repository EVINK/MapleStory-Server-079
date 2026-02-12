"""
MapleMapItem - Converted from Java source
Original: server/maps/MapleMapItem.java
Package: server.maps
"""

from threading import Lock
from threading import RLock
from typing import Optional, Any
import threading
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.inventory.IItem import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleMapItem(AbstractMapleMapObject):
    """
    Class MapleMapItem
    Extends: AbstractMapleMapObject
    """

    def __init__(self, item: Any, position: Any, dropper: Any, owner: Any, type: int, playerDrop: bool):
        self.item = None
        self.dropper = None
        self.character_ownerid = 0
        self.meso = 0
        self.questid = 0
        self.type = 0
        self.pickedUp = False
        self.playerDrop = False
        self.randDrop = False
        self.nextExpiry = 0
        self.nextFFA = 0
        self.lock = None
        self.meso = 0
        self.questid = -1
        self.pickedUp = False
        self.randDrop = False
        self.nextExpiry = 0
        self.nextFFA = 0
        self.lock = ReentrantLock()
        self.setPosition(position)
        self.item = item
        self.dropper = dropper
        self.character_ownerid = owner.getId()
        self.type = type
        self.playerDrop = playerDrop


    def getItem(self) -> Any:
        return self.item

    def setItem(self, z: Any) -> None:
        self.item = z

    def getQuest(self) -> int:
        return self.questid

    def getItemId(self) -> int:
        if self.getMeso() > 0:
            return self.meso
        return self.item.getItemId()

    def getDropper(self) -> Any:
        return self.dropper

    def getOwner(self) -> int:
        return self.character_ownerid

    def getMeso(self) -> int:
        return self.meso

    def isPlayerDrop(self) -> bool:
        return self.playerDrop

    def isPickedUp(self) -> bool:
        return self.pickedUp

    def setPickedUp(self, pickedUp: bool) -> None:
        self.pickedUp = pickedUp

    def getDropType(self) -> int:
        return self.type

    def setDropType(self, z: int) -> None:
        self.type = z

    def isRandDrop(self) -> bool:
        return self.randDrop

    def getType(self) -> Any:
        return MapleMapObjectType.ITEM

    def sendSpawnData(self, client: Any) -> None:
        if self.questid <= 0 || client.getPlayer().getQuestStatus(self.questid) == 1:
            client.getSession().write(MaplePacketCreator.dropItemFromMapObject(this, None, self.getPosition(), 2))

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.removeItemFromMap(self.getObjectId(), 1, 0))

    def getLock(self) -> Any:
        return self.lock

    def registerExpire(self, time: int) -> None:
        self.nextExpiry = int(time.time() * 1000) + time

    def registerFFA(self, time: int) -> None:
        self.nextFFA = int(time.time() * 1000) + time

    def shouldExpire(self) -> bool:
        return !self.pickedUp && self.nextExpiry > 0 && self.nextExpiry < int(time.time() * 1000)

    def shouldFFA(self) -> bool:
        return !self.pickedUp && self.type < 2 && self.nextFFA > 0 && self.nextFFA < int(time.time() * 1000)

    def expire(self, map: Any) -> None:
        self.pickedUp = True
        map.broadcastMessage(MaplePacketCreator.removeItemFromMap(self.getObjectId(), 0, 0))
        map.removeMapObject(this)

    def hasFFA(self) -> bool:
        return self.nextFFA > 0

