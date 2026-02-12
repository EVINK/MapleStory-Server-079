"""
MapleQuestRequirementType - 从Java源文件转换而来
对应Java源文件: server/quest/MapleQuestRequirementType.java
包路径: server.quest
"""

from enum import Enum, IntEnum


class MapleQuestRequirementType(Enum):
    """枚举类 MapleQuestRequirementType - 从Java枚举转换"""

    UNDEFINED = (-1)
    job = (0)
    item = (1)
    quest = (2)
    lvmin = (3)
    lvmax = (4)
    end = (5)
    mob = (6)
    npc = (7)
    fieldEnter = (8)
    interval = (9)
    startscript = (10)
    endscript = (10)
    pet = (11)
    pettamenessmin = (12)
    mbmin = (13)
    questComplete = (14)
    pop = (15)
    skill = (16)
    mbcard = (17)

    def getITEM(self) -> Any:
        """方法 getITEM"""
        raise NotImplementedError("方法 getITEM 尚未实现")

    def getType(self) -> int:
        """方法 getType"""
        return 0

    def getByType(self, type: int) -> Any:
        """方法 getByType"""
        raise NotImplementedError("方法 getByType 尚未实现")

    def getByWZName(self, name: str) -> Any:
        """方法 getByWZName"""
        raise NotImplementedError("方法 getByWZName 尚未实现")

