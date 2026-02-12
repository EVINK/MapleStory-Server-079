"""
MapleEventType - 从Java源文件转换而来
对应Java源文件: server/events/MapleEventType.java
包路径: server.events
"""

from enum import Enum, IntEnum


class MapleEventType(Enum):
    """枚举类 MapleEventType - 从Java枚举转换"""

    打椰子比赛 = ("椰子比赛", new int[])
    打瓶盖比赛 = ("打瓶盖", new int[])
    向高地 = ("向高地", new int[])
    上楼上楼 = ("上楼~上楼~", new int[])
    快速0X猜题 = ("快速OX猜题", new int[])
    雪球赛 = ("雪球赛", new int[])

    def getByString(self, splitted: str) -> Any:
        """方法 getByString"""
        raise NotImplementedError("方法 getByString 尚未实现")

