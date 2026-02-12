"""
OverrideMonsterStats - 从Java源文件转换而来
对应Java源文件: server/life/OverrideMonsterStats.java
包路径: server.life
"""


class OverrideMonsterStats:
    """
    类 OverrideMonsterStats - 从Java类转换
    """

    def __init__(self):
        """初始化 OverrideMonsterStats"""
        self.hp = 0
        self.exp = 0
        self.mp = 0


    def getExp(self) -> int:
        """方法 getExp"""
        return getattr(self, 'exp', 0)

    def setOExp(self, exp: int) -> None:
        """方法 setOExp"""
        self.o_exp = exp
        return None

    def getHp(self) -> int:
        """方法 getHp"""
        return getattr(self, 'hp', 0)

    def setOHp(self, hp: int) -> None:
        """方法 setOHp"""
        self.o_hp = hp
        return None

    def getMp(self) -> int:
        """方法 getMp"""
        return getattr(self, 'mp', 0)

    def setOMp(self, mp: int) -> None:
        """方法 setOMp"""
        self.o_mp = mp
        return None

