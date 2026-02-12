"""
SummonAttackEntry - Converted from Java source
Original: server/life/SummonAttackEntry.java
Package: server.life
"""

from typing import Optional, Any
from weakref import ref
import weakref


class SummonAttackEntry:
    """
    Class SummonAttackEntry
    """

    def __init__(self, mob: Any, damage: int):
        self.mob = None
        self.damage = None
        self.mob = new WeakReference<MapleMonster>(mob)
        self.damage = damage


    def getMonster(self) -> Any:
        return self.mob.get()

    def getDamage(self) -> int:
        return self.damage

