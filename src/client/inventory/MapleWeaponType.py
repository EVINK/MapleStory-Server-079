"""
MapleWeaponType - 从Java源文件转换而来
对应Java源文件: client/inventory/MapleWeaponType.java
包路径: client.inventory
"""

from enum import Enum, IntEnum


class MapleWeaponType(Enum):
    """枚举类 MapleWeaponType - 从Java枚举转换"""

    NOT_A_WEAPON = (4.0f)
    BOW = (3.4f)
    CLAW = (3.6f)
    DAGGER = (4.0f)
    CROSSBOW = (3.6f)
    AXE1H = (4.4f)
    SWORD1H = (4.0f)
    BLUNT1H = (4.4f)
    AXE2H = (4.8f)
    SWORD2H = (4.6f)
    BLUNT2H = (4.8f)
    POLE_ARM = (5.0f)
    SPEAR = (5.0f)
    STAFF = (3.6f)
    WAND = (3.6f)
    KNUCKLE = (4.8f)
    GUN = (3.6f)
    KATARA = (4.0f)

    def __init__(self, maxDamageMultiplier):
        """初始化枚举值"""
        self._maxDamageMultiplier = maxDamageMultiplier

    def getMaxDamageMultiplier(self) -> float:
        """方法 getMaxDamageMultiplier"""
        return 0

