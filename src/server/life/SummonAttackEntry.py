"""
SummonAttackEntry - 从Java源文件转换而来
对应Java源文件: server/life/SummonAttackEntry.java
包路径: server.life
"""

from typing import Optional, Any
from weakref import ref
import weakref


class SummonAttackEntry:
    """
    类 SummonAttackEntry - 从Java类转换
    """

    def __init__(self, mob: Any, damage: int):
        """初始化 SummonAttackEntry"""
        self.mob = None
        self.damage = None


    def getMonster(self) -> Any:
        """方法 getMonster"""
        return getattr(self, 'monster', None)

    def getDamage(self) -> int:
        """方法 getDamage"""
        return getattr(self, 'damage', 0)

