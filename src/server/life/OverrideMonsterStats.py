"""
OverrideMonsterStats - Converted from Java source
Original: server/life/OverrideMonsterStats.java
Package: server.life
"""

from typing import Optional, Any


class OverrideMonsterStats:
    """
    Class OverrideMonsterStats
    """

    def __init__(self):
        self.hp = 0
        self.exp = 0
        self.mp = 0
        self.hp = 0
        self.exp = 0
        self.mp = 0


    def getExp(self) -> int:
        return self.exp

    def setOExp(self, exp: int) -> None:
        self.exp = exp

    def getHp(self) -> int:
        return self.hp

    def setOHp(self, hp: int) -> None:
        self.hp = hp

    def getMp(self) -> int:
        return self.mp

    def setOMp(self, mp: int) -> None:
        self.mp = mp

