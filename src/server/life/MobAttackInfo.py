"""
MobAttackInfo - 从Java源文件转换而来
对应Java源文件: server/life/MobAttackInfo.java
包路径: server.life
"""


class MobAttackInfo:
    """
    类 MobAttackInfo - 从Java类转换
    """

    def __init__(self):
        """初始化 MobAttackInfo"""
        self.isDeadlyAttack = False
        self.mpBurn = 0
        self.mpCon = 0
        self.diseaseSkill = 0
        self.diseaseLevel = 0


    def setDeadlyAttack(self, isDeadlyAttack: bool) -> None:
        """方法 setDeadlyAttack"""
        self.deadly_attack = isDeadlyAttack
        return None

    def isDeadlyAttack(self) -> bool:
        """方法 isDeadlyAttack"""
        return bool(getattr(self, 'deadly_attack', False))

    def setMpBurn(self, mpBurn: int) -> None:
        """方法 setMpBurn"""
        self.mp_burn = mpBurn
        return None

    def getMpBurn(self) -> int:
        """方法 getMpBurn"""
        return getattr(self, 'mp_burn', 0)

    def setDiseaseSkill(self, diseaseSkill: int) -> None:
        """方法 setDiseaseSkill"""
        self.disease_skill = diseaseSkill
        return None

    def getDiseaseSkill(self) -> int:
        """方法 getDiseaseSkill"""
        return getattr(self, 'disease_skill', 0)

    def setDiseaseLevel(self, diseaseLevel: int) -> None:
        """方法 setDiseaseLevel"""
        self.disease_level = diseaseLevel
        return None

    def getDiseaseLevel(self) -> int:
        """方法 getDiseaseLevel"""
        return getattr(self, 'disease_level', 0)

    def setMpCon(self, mpCon: int) -> None:
        """方法 setMpCon"""
        self.mp_con = mpCon
        return None

    def getMpCon(self) -> int:
        """方法 getMpCon"""
        return getattr(self, 'mp_con', 0)

