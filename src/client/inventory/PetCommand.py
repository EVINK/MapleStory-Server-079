"""
PetCommand - Converted from Java source
Original: client/inventory/PetCommand.java
Package: client.inventory
"""

from typing import Optional, Any


class PetCommand:
    """
    Class PetCommand
    """

    def __init__(self, petId: int, skillId: int, prob: int, inc: int):
        self.petId = None
        self.skillId = None
        self.prob = None
        self.inc = None
        self.petId = petId
        self.skillId = skillId
        self.prob = prob
        self.inc = inc


    def getPetId(self) -> int:
        return self.petId

    def getSkillId(self) -> int:
        return self.skillId

    def getProbability(self) -> int:
        return self.prob

    def getIncrease(self) -> int:
        return self.inc

