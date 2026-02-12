"""
ReactorDropEntry - Converted from Java source
Original: server/maps/ReactorDropEntry.java
Package: server.maps
"""

from typing import Optional, Any


class ReactorDropEntry:
    """
    Class ReactorDropEntry
    """

    def __init__(self, itemId: int, chance: int, questid: int):
        self.itemId = 0
        self.chance = 0
        self.questid = 0
        self.assignedRangeStart = 0
        self.assignedRangeLength = 0
        self.itemId = itemId
        self.chance = chance
        self.questid = questid


