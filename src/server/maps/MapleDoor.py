"""
MapleDoor - Converted from Java source
Original: server/maps/MapleDoor.java
Package: server.maps
"""

from typing import List
from typing import Optional, Any
from weakref import ref
import threading
import weakref

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from server.MaplePortal import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleDoor(AbstractMapleMapObject):
    """
    Class MapleDoor
    Extends: AbstractMapleMapObject
    """

    def __init__(self, owner: Any, targetPosition: Any, skillId: int):
        self.owner = None
        self.town = None
        self.townPortal = None
        self.target = None
        self.skillId = 0
        self.ownerId = 0
        self.targetPosition = None
        self.owner = new WeakReference<>(owner)
        self.ownerId = owner.getId()
        self.target = owner.getMap()
        self.setPosition(self.targetPosition = targetPosition)
        self.town = self.target.getReturnMap()
        self.townPortal = self.getFreePortal()
        self.skillId = skillId


    def getSkill(self) -> int:
        return self.skillId

    def getOwnerId(self) -> int:
        return self.ownerId

    def getFreePortal(self) -> Any:
        freePortals = []
        for port in self.town.getPortals():
            if port.getType() == 6:
                freePortals.add(port)
        Collections.sort(freePortals, new Comparator<MaplePortal>()
            public int compare(final MaplePortal o1, final MaplePortal o2)
                if o1.getId() < o2.getId():
                    return -1
                if o1.getId() == o2.getId():
                    return 0
                return 1
        for obj in self.town.getAllDoorsThreadsafe():
            door = obj
            if door.getOwner() is not None and door.getOwner().getParty() is not None and self.getOwner() is not None and self.getOwner().getParty() is not None and self.getOwner().getParty().getMemberById(door.getOwnerId()) is not None:
                freePortals.remove(door.getTownPortal())
        if freePortals <= 0:
            return None
        return freePortals.iterator().next()

    def compare(self, o1: Any, o2: Any) -> int:
        if o1.getId() < o2.getId():
            return -1
        if o1.getId() == o2.getId():
            return 0
        return 1

    def sendSpawnData(self, client: Any) -> None:
        if self.getOwner() is None:
            return
        if self.target.getId() == client.getPlayer().getMapId() or self.getOwnerId() == client.getPlayer().getId() or (self.getOwner() is not None and self.getOwner().getParty() is not None and self.getOwner().getParty().getMemberById(client.getPlayer().getId()) is not None):
            client.getSession().write(MaplePacketCreator.spawnDoor(self.getOwnerId(), (self.town.getId() == client.getPlayer().getMapId()) ? self.townPortal.getPosition() : self.targetPosition, True))
            if self.getOwner() is not None and self.getOwner().getParty() is not None and (self.getOwnerId() == client.getPlayer().getId() or self.getOwner().getParty().getMemberById(client.getPlayer().getId()) is not None):
                client.getSession().write(MaplePacketCreator.partyPortal(self.town.getId(), self.target.getId(), self.skillId, self.targetPosition))
            client.getSession().write(MaplePacketCreator.spawnPortal(self.town.getId(), self.target.getId(), self.skillId, self.targetPosition))

    def sendDestroyData(self, client: Any) -> None:
        if self.getOwner() is None:
            return
        if self.target.getId() == client.getPlayer().getMapId() or self.getOwnerId() == client.getPlayer().getId() or (self.getOwner() is not None and self.getOwner().getParty() is not None and self.getOwner().getParty().getMemberById(client.getPlayer().getId()) is not None):
            if self.getOwner().getParty() is not None and (self.getOwnerId() == client.getPlayer().getId() or self.getOwner().getParty().getMemberById(client.getPlayer().getId()) is not None):
                client.getSession().write(MaplePacketCreator.partyPortal(999999999, 999999999, 0, Point(-1, -1)))
            client.getSession().write(MaplePacketCreator.removeDoor(self.getOwnerId(), False))
            client.getSession().write(MaplePacketCreator.removeDoor(self.getOwnerId(), True))

    def warp(self, chr: Any, toTown: bool) -> None:
        if chr.getId() == self.getOwnerId() or (self.getOwner() is not None and self.getOwner().getParty() is not None and self.getOwner().getParty().getMemberById(chr.getId()) is not None):
            if not toTown:
                chr.changeMap(self.target, self.targetPosition)
            else:
                chr.changeMap(self.town, self.townPortal)
        else:
            chr.getClient().getSession().write(MaplePacketCreator.enableActions())

    def getOwner(self) -> Any:
        return self.owner.get()

    def getTown(self) -> Any:
        return self.town

    def getTownPortal(self) -> Any:
        return self.townPortal

    def getTarget(self) -> Any:
        return self.target

    def getTargetPosition(self) -> Any:
        return self.targetPosition

    def getType(self) -> Any:
        return MapleMapObjectType.DOOR

