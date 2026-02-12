"""
MapleMonsterStats - 从Java源文件转换而来
对应Java源文件: server/life/MapleMonsterStats.java
包路径: server.life
"""

from typing import Dict
from typing import List
from typing import Optional, List, Dict, Any, Set

# 内部模块导入 (Internal module imports)
# from tools.Pair import *  # TODO: 根据实际需要导入具体类


class MapleMonsterStats:
    """
    类 MapleMonsterStats - 从Java类转换
    """

    def __init__(self):
        """初始化 MapleMonsterStats"""
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


    def getExp(self) -> int:
        """方法 getExp"""
        return getattr(self, 'exp', 0)

    def setExp(self, exp: int) -> None:
        """方法 setExp"""
        self.exp = exp
        return None

    def getHp(self) -> int:
        """方法 getHp"""
        return getattr(self, 'hp', 0)

    def setHp(self, hp: int) -> None:
        """方法 setHp"""
        self.hp = hp
        return None

    def getMp(self) -> int:
        """方法 getMp"""
        return getattr(self, 'mp', 0)

    def setMp(self, mp: int) -> None:
        """方法 setMp"""
        self.mp = mp
        return None

    def getLevel(self) -> int:
        """方法 getLevel"""
        return getattr(self, 'level', 0)

    def setLevel(self, level: int) -> None:
        """方法 setLevel"""
        self.level = level
        return None

    def setSelfD(self, selfDestruction_action: int) -> None:
        """方法 setSelfD"""
        self.self_d = selfDestruction_action
        return None

    def getSelfD(self) -> int:
        """方法 getSelfD"""
        return getattr(self, 'self_d', 0)

    def setSelfDHP(self, selfDestruction_hp: int) -> None:
        """方法 setSelfDHP"""
        self.self_dhp = selfDestruction_hp
        return None

    def getSelfDHp(self) -> int:
        """方法 getSelfDHp"""
        return getattr(self, 'self_d_hp', 0)

    def setFixedDamage(self, damage: int) -> None:
        """方法 setFixedDamage"""
        self.fixed_damage = damage
        return None

    def getFixedDamage(self) -> int:
        """方法 getFixedDamage"""
        return getattr(self, 'fixed_damage', 0)

    def setPhysicalDefense(self, PhysicalDefense: int) -> None:
        """方法 setPhysicalDefense"""
        self.physical_defense = PhysicalDefense
        return None

    def getPhysicalDefense(self) -> int:
        """方法 getPhysicalDefense"""
        return getattr(self, 'physical_defense', 0)

    def setMagicDefense(self, MagicDefense: int) -> None:
        """方法 setMagicDefense"""
        self.magic_defense = MagicDefense
        return None

    def getMagicDefense(self) -> int:
        """方法 getMagicDefense"""
        return getattr(self, 'magic_defense', 0)

    def setEva(self, eva: int) -> None:
        """方法 setEva"""
        self.eva = eva
        return None

    def getEva(self) -> int:
        """方法 getEva"""
        return getattr(self, 'eva', 0)

    def setOnlyNormalAttack(self, onlyNormalAttack: bool) -> None:
        """方法 setOnlyNormalAttack"""
        self.only_normal_attack = onlyNormalAttack
        return None

    def getOnlyNoramlAttack(self) -> bool:
        """方法 getOnlyNoramlAttack"""
        return getattr(self, 'only_noraml_attack', False)

    def getBanishInfo(self) -> Any:
        """方法 getBanishInfo"""
        return getattr(self, 'banish_info', None)

    def setBanishInfo(self, banish: Any) -> None:
        """方法 setBanishInfo"""
        self.banish_info = banish
        return None

    def getRemoveAfter(self) -> int:
        """方法 getRemoveAfter"""
        return getattr(self, 'remove_after', 0)

    def setRemoveAfter(self, removeAfter: int) -> None:
        """方法 setRemoveAfter"""
        self.remove_after = removeAfter
        return None

    def getrareItemDropLevel(self) -> int:
        """方法 getrareItemDropLevel"""
        return getattr(self, 'rare_item_drop_level', 0)

    def setrareItemDropLevel(self, rareItemDropLevel: int) -> None:
        """方法 setrareItemDropLevel"""
        self.rare_item_drop_level = rareItemDropLevel
        return None

    def setBoss(self, boss: bool) -> None:
        """方法 setBoss"""
        self.boss = boss
        return None

    def isBoss(self) -> bool:
        """方法 isBoss"""
        return bool(getattr(self, 'boss', False))

    def setFfaLoot(self, ffaLoot: bool) -> None:
        """方法 setFfaLoot"""
        self.ffa_loot = ffaLoot
        return None

    def isFfaLoot(self) -> bool:
        """方法 isFfaLoot"""
        return bool(getattr(self, 'ffa_loot', False))

    def setExplosiveReward(self, isExplosiveReward: bool) -> None:
        """方法 setExplosiveReward"""
        self.explosive_reward = isExplosiveReward
        return None

    def isExplosiveReward(self) -> bool:
        """方法 isExplosiveReward"""
        return bool(getattr(self, 'explosive_reward', False))

    def setMobile(self, mobile: bool) -> None:
        """方法 setMobile"""
        self.mobile = mobile
        return None

    def getMobile(self) -> bool:
        """方法 getMobile"""
        return getattr(self, 'mobile', False)

    def setFly(self, fly: bool) -> None:
        """方法 setFly"""
        self.fly = fly
        return None

    def getFly(self) -> bool:
        """方法 getFly"""
        return getattr(self, 'fly', False)

    def getRevives(self) -> list:
        """方法 getRevives"""
        return getattr(self, 'revives', [])

    def setRevives(self, revives: list) -> None:
        """方法 setRevives"""
        self.revives = revives
        return None

    def setUndead(self, undead: bool) -> None:
        """方法 setUndead"""
        self.undead = undead
        return None

    def getUndead(self) -> bool:
        """方法 getUndead"""
        return getattr(self, 'undead', False)

    def setEffectiveness(self, e: Any, ee: Any) -> None:
        """方法 setEffectiveness"""
        self.effectiveness = e
        return None

    def removeEffectiveness(self, e: Any) -> None:
        """方法 removeEffectiveness"""
        pass

    def getEffectiveness(self, e: Any) -> Any:
        """方法 getEffectiveness"""
        raise NotImplementedError("方法 getEffectiveness 尚未实现")

    def getName(self) -> str:
        """方法 getName"""
        return getattr(self, 'name', "")

    def setName(self, name: str) -> None:
        """方法 setName"""
        self.name = name
        return None

    def getTagColor(self) -> int:
        """方法 getTagColor"""
        return getattr(self, 'tag_color', 0)

    def setTagColor(self, tagColor: int) -> None:
        """方法 setTagColor"""
        self.tag_color = tagColor
        return None

    def getTagBgColor(self) -> int:
        """方法 getTagBgColor"""
        return getattr(self, 'tag_bg_color', 0)

