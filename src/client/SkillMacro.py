"""
SkillMacro - Converted from Java source
Original: client/SkillMacro.java
Package: client
"""

from typing import Optional, Any


class SkillMacro:
    """
    Class SkillMacro
    Implements: Serializable
    """

    serialVersionUID = -63413738569

    def __init__(self, skill1: int, skill2: int, skill3: int, name: str, shout: int, position: int):
        self.macroId = 0
        self.skill1 = 0
        self.skill2 = 0
        self.skill3 = 0
        self.name = ""
        self.shout = 0
        self.position = 0
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
        self.name = name
        self.shout = shout
        self.position = position


    def getMacroId(self) -> int:
        return self.macroId

    def getSkill1(self) -> int:
        return self.skill1

    def getSkill2(self) -> int:
        return self.skill2

    def getSkill3(self) -> int:
        return self.skill3

    def getName(self) -> str:
        return self.name

    def getShout(self) -> int:
        return self.shout

    def getPosition(self) -> int:
        return self.position

    def setMacroId(self, macroId: int) -> None:
        self.macroId = macroId

    def setSkill1(self, skill1: int) -> None:
        self.skill1 = skill1

    def setSkill2(self, skill2: int) -> None:
        self.skill2 = skill2

    def setSkill3(self, skill3: int) -> None:
        self.skill3 = skill3

    def setName(self, name: str) -> None:
        self.name = name

    def setShout(self, shout: int) -> None:
        self.shout = shout

    def setPosition(self, position: int) -> None:
        self.position = position

