"""
MaplePartyCharacter - Converted from Java source
Original: handling/world/MaplePartyCharacter.java
Package: handling.world
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from server.maps.MapleDoor import *  # TODO: import specific classes


class MaplePartyCharacter:
    """
    Class MaplePartyCharacter
    Implements: Serializable
    """

    def __init__(self, maplechar: Any):
        self.name = ""
        self.id = 0
        self.level = 0
        self.channel = 0
        self.jobid = 0
        self.mapid = 0
        self.doorTown = 0
        self.doorTarget = 0
        self.doorSkill = 0
        self.doorPosition = None
        self.online = False
        self.doorTown = 999999999
        self.doorTarget = 999999999
        self.doorSkill = 0
        self.doorPosition = Point(0, 0)
        self.name = maplechar.getName()
        self.level = maplechar.getLevel()
        self.channel = maplechar.getClient().getChannel()
        self.id = maplechar.getId()
        self.jobid = maplechar.getJob()
        self.mapid = maplechar.getMapId()
        self.online = True
        doors = maplechar.getDoors()
        if doors > 0:
            door = doors.get(0)
            self.doorTown = door.getTown().getId()
            self.doorTarget = door.getTarget().getId()
            self.doorSkill = door.getSkill()
            self.doorPosition = door.getTargetPosition()
        else:
            self.doorPosition = Point(maplechar.getPosition())

    # Static initializer
    # MaplePartyCharacter.serialVersionUID = 6215463252132450750


    def getLevel(self) -> int:
        return self.level

    def getChannel(self) -> int:
        return self.channel

    def isOnline(self) -> bool:
        return self.online

    def setOnline(self, online: bool) -> None:
        self.online = online

    def getMapid(self) -> int:
        return self.mapid

    def getName(self) -> str:
        return self.name

    def getId(self) -> int:
        return self.id

    def getJobId(self) -> int:
        return self.jobid

    def getDoorTown(self) -> int:
        return self.doorTown

    def getDoorTarget(self) -> int:
        return self.doorTarget

    def getDoorSkill(self) -> int:
        return self.doorSkill

    def getDoorPosition(self) -> Any:
        return self.doorPosition

    def hashCode(self) -> int:
        prime = 31
        result = 1
        result = prime * result + ((self.name is None) ? 0 : self.name.hashCode())
        return result

    def equals(self, obj: Any) -> bool:
        if this == obj:
            return True
        if obj is None:
            return False
        if self.getClass() != obj.getClass():
            return False
        other = obj
        if self.name is None:
            if other.name is not None:
                return False
        elif not self.name == (other.name):
            return False
        return True

