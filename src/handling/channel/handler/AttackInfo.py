"""
AttackInfo - Converted from Java source
Original: handling/channel/handler/AttackInfo.java
Package: handling.channel.handler
"""

from typing import List
from typing import Optional, Any

# Internal module imports
# from client.ISkill import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.SkillFactory import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from server.MapleStatEffect import *  # TODO: import specific classes
# from tools.AttackPair import *  # TODO: import specific classes


class AttackInfo:
    """
    Class AttackInfo
    """

    def __init__(self):
        self.skill = 0
        self.charge = 0
        self.lastAttackTickCount = 0
        self.allDamage = []
        self.position = None
        self.hits = 0
        self.targets = 0
        self.tbyte = 0
        self.display = 0
        self.animation = 0
        self.speed = 0
        self.AOE = 0
        self.starSlot = 0
        self.cashSlot = 0
        self.unk = 0
        self.real = False
        self.isCloseRangeAttack = False
        self.real = True
        self.isCloseRangeAttack = False


    def getAttackEffect(self, chr: Any, skillLevel: int, skill_: Any) -> Any:
        if GameConstants.isMulungSkill(self.skill) || GameConstants.isPyramidSkill(self.skill):
            skillLevel = 1
        elif skillLevel <= 0:
            return None
        if GameConstants.isLinkedAranSkill(self.skill):
            skillLink = SkillFactory.getSkill(self.skill)
            if self.display > 80 && !skillLink.getAction():
                return None
            return skillLink.getEffect(skillLevel)
        else:
            if self.display > 80 && !skill_.getAction():
                return None
            return skill_.getEffect(skillLevel)

