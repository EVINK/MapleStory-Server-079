"""
MobAttackInfo - Converted from Java source
Original: server/life/MobAttackInfo.java
Package: server.life
"""

from typing import Optional, Any


class MobAttackInfo:
    """
    Class MobAttackInfo
    """

    def __init__(self):
        self.isDeadlyAttack = False
        self.mpBurn = 0
        self.mpCon = 0
        self.diseaseSkill = 0
        self.diseaseLevel = 0


    def setDeadlyAttack(self, isDeadlyAttack: bool) -> None:
        self.isDeadlyAttack = isDeadlyAttack

    def isDeadlyAttack(self) -> bool:
        return self.isDeadlyAttack

    def setMpBurn(self, mpBurn: int) -> None:
        self.mpBurn = mpBurn

    def getMpBurn(self) -> int:
        return self.mpBurn

    def setDiseaseSkill(self, diseaseSkill: int) -> None:
        self.diseaseSkill = diseaseSkill

    def getDiseaseSkill(self) -> int:
        return self.diseaseSkill

    def setDiseaseLevel(self, diseaseLevel: int) -> None:
        self.diseaseLevel = diseaseLevel

    def getDiseaseLevel(self) -> int:
        return self.diseaseLevel

    def setMpCon(self, mpCon: int) -> None:
        self.mpCon = mpCon

    def getMpCon(self) -> int:
        return self.mpCon

