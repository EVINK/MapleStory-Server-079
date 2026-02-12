"""
MapleMist - Converted from Java source
Original: server/maps/MapleMist.java
Package: server.maps
"""

from typing import Optional, Any

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from handling.MaplePacket import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from server.life.MapleMonster import *  # TODO: import specific classes
# from server.life.MobSkill import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleMist(AbstractMapleMapObject):
    """
    Class MapleMist
    Extends: AbstractMapleMapObject
    """

    def __init__(self, mistPosition: Any, mob: Any, skill: Any):
        self.mistPosition = None
        self.source = None
        self.skill = None
        self.isMobMist = False
        self.skillDelay = 0
        self.skilllevel = 0
        self.isPoisonMist = 0
        self.ownerId = 0
        self.mistPosition = mistPosition
        self.ownerId = mob.getId()
        self.skill = skill
        self.skilllevel = skill.getSkillLevel()
        self.isMobMist = True
        self.isPoisonMist = 0
        self.skillDelay = 0


    def getType(self) -> Any:
        return MapleMapObjectType.MIST

    def getPosition(self) -> Any:
        return self.mistPosition.getLocation()

    def getSourceSkill(self) -> Any:
        return SkillFactory.getSkill(self.source.getSourceId())

    def isMobMist(self) -> bool:
        return self.isMobMist

    def isPoisonMist(self) -> int:
        return self.isPoisonMist

    def getSkillDelay(self) -> int:
        return self.skillDelay

    def getSkillLevel(self) -> int:
        return self.skilllevel

    def getOwnerId(self) -> int:
        return self.ownerId

    def getMobSkill(self) -> Any:
        return self.skill

    def getBox(self) -> Any:
        return self.mistPosition

    def getSource(self) -> Any:
        return self.source

    def setPosition(self, position: Any) -> None:
        pass

    def fakeSpawnData(self, level: int) -> Any:
        return MaplePacketCreator.spawnMist(this)

    def sendSpawnData(self, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.spawnMist(this))

    def sendDestroyData(self, c: Any) -> None:
        c.getSession().write(MaplePacketCreator.removeMist(self.getObjectId(), False))

    def makeChanceResult(self) -> bool:
        return self.source.makeChanceResult()

