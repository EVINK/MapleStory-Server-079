"""
MapleSummon - Converted from Java source
Original: server/maps/MapleSummon.java
Package: server.maps
"""

from typing import Optional, Any
import time

# Internal module imports
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.MapleClient import *  # TODO: import specific classes
# from client.anticheat.CheatingOffense import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class MapleSummon(AbstractAnimatedMapleMapObject):
    """
    Class MapleSummon
    Extends: AbstractAnimatedMapleMapObject
    """

    def __init__(self, owner: Any, skill: Any, pos: Any, movementType: Any):
        self.ownerid = 0
        self.skillLevel = 0
        self.ownerLevel = 0
        self.skill = 0
        self.fh = 0
        self.map = None
        self.hp = 0
        self.changedMap = False
        self.movementType = None
        self.lastSummonTickCount = 0
        self.Summon_tickResetCount = 0
        self.Server_ClientSummonTickDiff = 0
        self.changedMap = False
        self.ownerid = owner.getId()
        self.ownerLevel = owner.getLevel()
        self.skill = skill.getSourceId()
        self.map = owner.getMap()
        self.skillLevel = skill.getLevel()
        self.movementType = movementType
        self.setPosition(pos)
        try:
            self.fh = owner.getMap().getFootholds().findBelow(pos).getId()
        except TypeError as e:
            self.fh = 0
        if not self.is替身术():
            self.lastSummonTickCount = 0
            self.Summon_tickResetCount = 0
            self.Server_ClientSummonTickDiff = 0


    def sendSpawnData(self, client: Any) -> None:
        pass

    def sendDestroyData(self, client: Any) -> None:
        client.getSession().write(MaplePacketCreator.removeSummon(this, False))

    def updateMap(self, map: Any) -> None:
        self.map = map

    def getOwner(self) -> Any:
        return self.map.getCharacterById(self.ownerid)

    def getFh(self) -> int:
        return self.fh

    def setFh(self, fh: int) -> None:
        self.fh = fh

    def getOwnerId(self) -> int:
        return self.ownerid

    def getOwnerLevel(self) -> int:
        return self.ownerLevel

    def getSkill(self) -> int:
        return self.skill

    def getHP(self) -> int:
        return self.hp

    def addHP(self, delta: int) -> None:
        self.hp += delta

    def getMovementType(self) -> Any:
        return self.movementType

    def translated_is替身术(self) -> bool:
        # switch (self.skill):
            # case 3111002:
            # case 3211002:
            # case 4341006:
            # case 13111004:
            # case 33111003:
                return True
            # default:
                return False

    def isGaviota(self) -> bool:
        return self.skill == 5211002

    def isBeholder(self) -> bool:
        return self.skill == 1321007

    def isMultiSummon(self) -> bool:
        return self.skill == 5211002 or self.skill == 5211001 or self.skill == 5220002 or self.skill == 32111006

    def isSummon(self) -> bool:
        # switch (self.skill):
            # case 1321007:
            # case 2121005:
            # case 2221005:
            # case 2311006:
            # case 2321003:
            # case 5211001:
            # case 5211002:
            # case 5220002:
            # case 11001004:
            # case 12001004:
            # case 12111004:
            # case 13001004:
            # case 13111004:
            # case 14001005:
            # case 15001004:
                return True
            # default:
                return False

    def getSkillLevel(self) -> int:
        return self.skillLevel

    def getSummonType(self) -> int:
        if self.is替身术():
            return 0
        # switch (self.skill):
            # case 1321007:
                return 2
            # case 35111001:
            # case 35111009:
            # case 35111010:
                return 3
            # case 35121009:
                return 4
            # default:
                return 1

    def getType(self) -> Any:
        return MapleMapObjectType.SUMMON

    def CheckSummonAttackFrequency(self, chr: Any, tickcount: int) -> None:
        tickdifference = tickcount - self.lastSummonTickCount
        if tickdifference < GameConstants.getSummonAttackDelay(self.skill):
            chr.getCheatTracker().registerOffense(CheatingOffense.召唤兽快速攻击)
        STime_TC = int(time.time() * 1000) - tickcount
        S_C_Difference = self.Server_ClientSummonTickDiff - STime_TC
        if S_C_Difference > 200:
            chr.getCheatTracker().registerOffense(CheatingOffense.召唤兽快速攻击)
        self.Summon_tickResetCount += 1
        if self.Summon_tickResetCount > 4:
            self.Summon_tickResetCount = 0
            self.Server_ClientSummonTickDiff = STime_TC
        self.lastSummonTickCount = tickcount

    def isChangedMap(self) -> bool:
        return self.changedMap

    def setChangedMap(self, cm: bool) -> None:
        self.changedMap = cm

