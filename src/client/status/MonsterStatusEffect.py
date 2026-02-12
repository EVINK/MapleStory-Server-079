"""
MonsterStatusEffect - Converted from Java source
Original: client/status/MonsterStatusEffect.java
Package: client.status
"""

from concurrent.futures import Future
from typing import List
from typing import Optional, Any
import sched

# Internal module imports
# from server.life import *  # TODO: import specific classes


class MonsterStatusEffect:
    """
    Class MonsterStatusEffect
    """

    def __init__(self, stat: Any, x: int, skillId: int, mobskill: Any, monsterSkill: bool):
        self.stati = None
        self.skill = 0
        self.mobskill = None
        self.monsterSkill = False
        self.x = None
        self.reflect = False
        self.reflect = False
        self.stati = stat
        self.skill = skillId
        self.monsterSkill = monsterSkill
        self.mobskill = mobskill
        self.x = x


    def getStati(self) -> Any:
        return self.stati

    def getX(self) -> int:
        return self.x

    def setValue(self, status: Any, newVal: int) -> None:
        self.stati = status
        self.x = newVal

    def getSkill(self) -> int:
        return self.skill

    def getMobSkill(self) -> Any:
        return self.mobskill

    def isMonsterSkill(self) -> bool:
        return self.monsterSkill

    def setCancelTask(self, cancelTask: Any) -> None:
        self.cancelTask = cancelTask

    def setPoisonSchedule(self, poisonSchedule: Any) -> None:
        self.poisonSchedule = poisonSchedule

    def cancelTask(self) -> None:
        if self.cancelTask is not None:
            self.cancelTask.cancel(False)
        self.cancelTask = None

    def cancelPoisonSchedule(self) -> None:
        if self.poisonSchedule is not None:
            self.poisonSchedule.cancel(False)
            self.poisonSchedule = None

    def isReflect(self) -> bool:
        return self.reflect

