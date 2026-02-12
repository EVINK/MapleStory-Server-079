"""
MonsterDropEntry - Converted from Java source
Original: server/life/MonsterDropEntry.java
Package: server.life
"""

from typing import Optional, Any


class MonsterDropEntry:
    """
    Class MonsterDropEntry
    """

    def __init__(self, itemId: int, chance: int, Minimum: int, Maximum: int, questid: int):
        self.questid = 0
        self.itemId = 0
        self.chance = 0
        self.Minimum = 0
        self.Maximum = 0
        self.itemId = itemId
        self.chance = chance
        self.questid = questid
        self.Minimum = Minimum
        self.Maximum = Maximum


