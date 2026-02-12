"""
ChangeableStats - Converted from Java source
Original: server/life/ChangeableStats.java
Package: server.life
"""

from typing import Optional, Any
import math

# Internal module imports
# from constants.GameConstants import *  # TODO: import specific classes


class ChangeableStats(OverrideMonsterStats):
    """
    Class ChangeableStats
    Extends: OverrideMonsterStats
    """

    def __init__(self, stats: Any, ostats: Any):
        self.watk = 0
        self.matk = 0
        self.acc = 0
        self.eva = 0
        self.PDRate = 0
        self.MDRate = 0
        self.pushed = 0
        self.level = 0
        self.hp = ostats.getHp()
        self.exp = ostats.getExp()
        self.mp = ostats.getMp()
        self.acc = stats.getAcc()
        self.eva = stats.getEva()
        self.level = stats.getLevel()


