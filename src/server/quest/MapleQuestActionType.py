"""
MapleQuestActionType - 从Java源文件转换而来
对应Java源文件: server/quest/MapleQuestActionType.java
包路径: server.quest
"""

from enum import Enum, IntEnum


class MapleQuestActionType(Enum):
    """枚举类 MapleQuestActionType - 从Java枚举转换"""

    UNDEFINED = (-1)
    exp = (0)
    item = (1)
    nextQuest = (2)
    money = (3)
    quest = (4)
    skill = (5)
    pop = (6)
    buffItemID = (7)
    infoNumber = (8)
    yes = (9)
    no = (10)
    sp = (11)

    def __init__(self, type):
        """初始化枚举值"""
        self._type = type

    def getType(self) -> int:
        """方法 getType"""
        return getattr(self, 'type', 0)

    def getByType(self, type: int) -> Any:
        """方法 getByType"""
        raise NotImplementedError("方法 getByType 尚未实现")

    def getByWZName(self, name: str) -> Any:
        """方法 getByWZName"""
        raise NotImplementedError("方法 getByWZName 尚未实现")

