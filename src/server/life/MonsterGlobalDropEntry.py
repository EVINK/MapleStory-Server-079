"""
MonsterGlobalDropEntry - 从Java源文件转换而来
对应Java源文件: server/life/MonsterGlobalDropEntry.java
包路径: server.life
"""


class MonsterGlobalDropEntry:
    """
    类 MonsterGlobalDropEntry - 从Java类转换
    """

    def __init__(self, itemId: int, chance: int, continent: int, dropType: int, Minimum: int, Maximum: int, questid: int):
        """初始化 MonsterGlobalDropEntry"""
        self.dropType = 0
        self.questid = 0
        self.itemId = 0
        self.chance = 0
        self.Minimum = 0
        self.Maximum = 0
        self.continent = 0
        self.onlySelf = False


