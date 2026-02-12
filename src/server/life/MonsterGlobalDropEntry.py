"""
MonsterGlobalDropEntry - Converted from Java source
Original: server/life/MonsterGlobalDropEntry.java
Package: server.life
"""

from typing import Optional, Any


class MonsterGlobalDropEntry:
    """
    Class MonsterGlobalDropEntry
    """

    def __init__(self, itemId: int, chance: int, continent: int, dropType: int, Minimum: int, Maximum: int, questid: int):
        self.dropType = 0
        self.questid = 0
        self.itemId = 0
        self.chance = 0
        self.Minimum = 0
        self.Maximum = 0
        self.continent = 0
        self.onlySelf = False
        self.onlySelf = False
        self.itemId = itemId
        self.chance = chance
        self.dropType = dropType
        self.continent = continent
        self.questid = questid
        self.Minimum = Minimum
        self.Maximum = Maximum


