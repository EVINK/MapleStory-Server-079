"""
MapleDragon - Converted from Java source
Original: server/maps/MapleDragon.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes


class MapleDragon(AbstractAnimatedMapleMapObject):
    """
    Class MapleDragon
    Extends: AbstractAnimatedMapleMapObject
    """

    def __init__(self, owner: Any):
        self.owner = None
        self.jobid = None
        self.owner = owner.getId()
        self.jobid = owner.getJob()
        if self.jobid < 2200 || self.jobid > 2218:
            raise RuntimeError("Trying to create a dragon for a non-Evan")
        self.setPosition(owner.getPosition())
        self.setStance(4)


    def sendSpawnData(self, client: Any) -> None:
        pass

    def sendDestroyData(self, client: Any) -> None:
        pass

    def getOwner(self) -> int:
        return self.owner

    def getJobId(self) -> int:
        return self.jobid

    def getType(self) -> Any:
        return MapleMapObjectType.SUMMON

