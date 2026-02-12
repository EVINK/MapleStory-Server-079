"""
MapleWeaponType - Converted from Java source
Original: client/inventory/MapleWeaponType.java
Package: client.inventory
"""

from enum import Enum, IntEnum
from typing import Optional, Any


class MapleWeaponType(Enum):
    """Enum MapleWeaponType"""

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
        self._maxDamageMultiplier = maxDamageMultiplier

    def getMaxDamageMultiplier(self) -> float:
        return self.damageMultiplier

