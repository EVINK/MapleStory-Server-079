"""
MapleMonsterStats - Converted from Java source
Original: server/life/MapleMonsterStats.java
Package: server.life
"""

from typing import Dict
from typing import List
from typing import Optional, Any

# Internal module imports
# from tools.Pair import *  # TODO: import specific classes


class MapleMonsterStats:
    """
    Class MapleMonsterStats
    """

    def __init__(self):
        self.cp = 0
        self.selfDestruction_action = 0
        self.tagColor = 0
        self.tagBgColor = 0
        self.rareItemDropLevel = 0
        self.HPDisplayType = 0
        self.level = 0
        self.PhysicalDefense = 0
        self.MagicDefense = 0
        self.eva = 0
        self.hp = 0
        self.exp = 0
        self.mp = 0
        self.removeAfter = 0
        self.buffToGive = 0
        self.fixedDamage = 0
        self.selfDestruction_hp = 0
        self.dropItemPeriod = 0
        self.point = 0
        self.boss = False
        self.undead = False
        self.ffaLoot = False
        self.firstAttack = False
        self.isExplosiveReward = False
        self.mobile = False
        self.fly = False
        self.onlyNormalAttack = False
        self.friendly = False
        self.noDoom = False
        self.name = ""
        self.resistance = None
        self.revives = []
        self.skills = None
        self.banish = None
        self.changeable = False
        self.acc = 0
        self.resistance = {}
        self.revives = []
        self.skills = new ArrayList<Pair<Integer, Integer>>()


    def getExp(self) -> int:
        return self.exp

    def setExp(self, exp: int) -> None:
        self.exp = exp

    def getHp(self) -> int:
        return self.hp

    def setHp(self, hp: int) -> None:
        self.hp = hp

    def getMp(self) -> int:
        return self.mp

    def setMp(self, mp: int) -> None:
        self.mp = mp

    def getLevel(self) -> int:
        return self.level

    def setLevel(self, level: int) -> None:
        self.level = level

    def setSelfD(self, selfDestruction_action: int) -> None:
        self.selfDestruction_action = selfDestruction_action

    def getSelfD(self) -> int:
        return self.selfDestruction_action

    def setSelfDHP(self, selfDestruction_hp: int) -> None:
        self.selfDestruction_hp = selfDestruction_hp

    def getSelfDHp(self) -> int:
        return self.selfDestruction_hp

    def setFixedDamage(self, damage: int) -> None:
        self.fixedDamage = damage

    def getFixedDamage(self) -> int:
        return self.fixedDamage

    def setPhysicalDefense(self, PhysicalDefense: int) -> None:
        self.PhysicalDefense = PhysicalDefense

    def getPhysicalDefense(self) -> int:
        return self.PhysicalDefense

    def setMagicDefense(self, MagicDefense: int) -> None:
        self.MagicDefense = MagicDefense

    def getMagicDefense(self) -> int:
        return self.MagicDefense

    def setEva(self, eva: int) -> None:
        self.eva = eva

    def getEva(self) -> int:
        return self.eva

    def setOnlyNormalAttack(self, onlyNormalAttack: bool) -> None:
        self.onlyNormalAttack = onlyNormalAttack

    def getOnlyNoramlAttack(self) -> bool:
        return self.onlyNormalAttack

    def getBanishInfo(self) -> Any:
        return self.banish

    def setBanishInfo(self, banish: Any) -> None:
        self.banish = banish

    def getRemoveAfter(self) -> int:
        return self.removeAfter

    def setRemoveAfter(self, removeAfter: int) -> None:
        self.removeAfter = removeAfter

    def getrareItemDropLevel(self) -> int:
        return self.rareItemDropLevel

    def setrareItemDropLevel(self, rareItemDropLevel: int) -> None:
        self.rareItemDropLevel = rareItemDropLevel

    def setBoss(self, boss: bool) -> None:
        self.boss = boss

    def isBoss(self) -> bool:
        return self.boss

    def setFfaLoot(self, ffaLoot: bool) -> None:
        self.ffaLoot = ffaLoot

    def isFfaLoot(self) -> bool:
        return self.ffaLoot

    def setExplosiveReward(self, isExplosiveReward: bool) -> None:
        self.isExplosiveReward = isExplosiveReward

    def isExplosiveReward(self) -> bool:
        return self.isExplosiveReward

    def setMobile(self, mobile: bool) -> None:
        self.mobile = mobile

    def getMobile(self) -> bool:
        return self.mobile

    def setFly(self, fly: bool) -> None:
        self.fly = fly

    def getFly(self) -> bool:
        return self.fly

    def getRevives(self) -> list:
        return self.revives

    def setRevives(self, revives: list) -> None:
        self.revives = revives

    def setUndead(self, undead: bool) -> None:
        self.undead = undead

    def getUndead(self) -> bool:
        return self.undead

    def setEffectiveness(self, e: Any, ee: Any) -> None:
        self.resistance.put(e, ee)

    def removeEffectiveness(self, e: Any) -> None:
        self.resistance.remove(e)

    def getEffectiveness(self, e: Any) -> Any:
        elementalEffectiveness = self.resistance.get(e)
        if elementalEffectiveness is None:
            return ElementalEffectiveness.正常
        return elementalEffectiveness

    def getName(self) -> str:
        return self.name

    def setName(self, name: str) -> None:
        self.name = name

    def getTagColor(self) -> int:
        return self.tagColor

    def setTagColor(self, tagColor: int) -> None:
        self.tagColor = tagColor

    def getTagBgColor(self) -> int:
        return self.tagBgColor

    def setTagBgColor(self, tagBgColor: int) -> None:
        self.tagBgColor = tagBgColor

    def setSkills(self, skill_: list) -> None:
        for skill in skill_:
            self.skills.add(skill)

    def getSkills(self) -> list:
        return Collections.unmodifiableList(self.skills)

    def getNoSkills(self) -> int:
        return self.skills

    def hasSkill(self, skillId: int, level: int) -> bool:
        for skill in self.skills:
            if skill.getLeft() == skillId && skill.getRight() == level:
                return True
        return False

    def setFirstAttack(self, firstAttack: bool) -> None:
        self.firstAttack = firstAttack

    def isFirstAttack(self) -> bool:
        return self.firstAttack

    def setCP(self, cp: int) -> None:
        self.cp = cp

    def getCP(self) -> int:
        return self.cp

    def setPoint(self, cp: int) -> None:
        self.point = cp

    def getPoint(self) -> int:
        return self.point

    def setFriendly(self, friendly: bool) -> None:
        self.friendly = friendly

    def isFriendly(self) -> bool:
        return self.friendly

    def setNoDoom(self, doom: bool) -> None:
        self.noDoom = doom

    def isNoDoom(self) -> bool:
        return self.noDoom

    def setBuffToGive(self, buff: int) -> None:
        self.buffToGive = buff

    def getBuffToGive(self) -> int:
        return self.buffToGive

    def getHPDisplayType(self) -> int:
        return self.HPDisplayType

    def setHPDisplayType(self, HPDisplayType: int) -> None:
        self.HPDisplayType = HPDisplayType

    def getDropItemPeriod(self) -> int:
        return self.dropItemPeriod

    def setDropItemPeriod(self, d: int) -> None:
        self.dropItemPeriod = d

    def setChange(self, invin: bool) -> None:
        self.changeable = invin

    def isChangeable(self) -> bool:
        return self.changeable

    def getAcc(self) -> int:
        return self.acc

    def setAcc(self, acc: int) -> None:
        self.acc = acc

